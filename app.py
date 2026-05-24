import os
import sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from core.rewrite_engine import process_tool, metrics, normalize_text
from core.ai_clients import rewrite_with_ai

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Originality Studio Pro")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "app.db")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key-before-production")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS api_settings (
                user_id INTEGER PRIMARY KEY,
                provider TEXT DEFAULT 'gemini',
                model TEXT DEFAULT 'gemini-1.5-flash',
                api_key TEXT DEFAULT '',
                updated_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tool TEXT NOT NULL,
                tone TEXT,
                strength TEXT,
                input_text TEXT NOT NULL,
                output_text TEXT NOT NULL,
                score_similarity REAL,
                score_lift REAL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )


init_db()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    with db() as conn:
        return conn.execute("SELECT id, name, email, role FROM users WHERE id = ?", (uid,)).fetchone()


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            return jsonify({"ok": False, "error": "Please sign in first."}), 401
        return fn(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    return render_template("index.html", app_name=APP_NAME, user=current_user())


@app.post("/api/signup")
def signup():
    data = request.get_json(force=True)
    name = normalize_text(data.get("name", ""))
    email = normalize_text(data.get("email", "")).lower()
    password = data.get("password", "")
    if len(name) < 2 or "@" not in email or len(password) < 6:
        return jsonify({"ok": False, "error": "Use a valid name, email, and a password of at least 6 characters."}), 400
    try:
        with db() as conn:
            existing_count = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
            role = "admin" if existing_count == 0 else "user"
            cur = conn.execute(
                "INSERT INTO users (name, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
                (name, email, generate_password_hash(password), role, datetime.utcnow().isoformat()),
            )
            uid = cur.lastrowid
            conn.execute(
                "INSERT INTO api_settings (user_id, provider, model, api_key, updated_at) VALUES (?, ?, ?, ?, ?)",
                (uid, os.getenv("DEFAULT_AI_PROVIDER", "gemini"), os.getenv("GEMINI_MODEL", "gemini-1.5-flash"), "", datetime.utcnow().isoformat()),
            )
            session["user_id"] = uid
        return jsonify({"ok": True})
    except sqlite3.IntegrityError:
        return jsonify({"ok": False, "error": "This email is already registered."}), 409


@app.post("/api/login")
def login():
    data = request.get_json(force=True)
    email = normalize_text(data.get("email", "")).lower()
    password = data.get("password", "")
    with db() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"ok": False, "error": "Incorrect email or password."}), 401
    session["user_id"] = user["id"]
    return jsonify({"ok": True})


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/me")
def me():
    user = current_user()
    if not user:
        return jsonify({"ok": True, "user": None})
    return jsonify({"ok": True, "user": dict(user)})


@app.get("/api/settings")
@login_required
def get_settings():
    user = current_user()
    with db() as conn:
        row = conn.execute("SELECT provider, model, api_key FROM api_settings WHERE user_id = ?", (user["id"],)).fetchone()
    if not row:
        return jsonify({"ok": True, "settings": {"provider": "gemini", "model": "gemini-1.5-flash", "has_key": False}})
    return jsonify({
        "ok": True,
        "settings": {
            "provider": row["provider"],
            "model": row["model"],
            "has_key": bool(row["api_key"]),
            "masked_key": (row["api_key"][:6] + "..." + row["api_key"][-4:]) if row["api_key"] else "",
        },
    })


@app.post("/api/settings")
@login_required
def save_settings():
    user = current_user()
    data = request.get_json(force=True)
    provider = (data.get("provider") or "gemini").lower()
    if provider not in {"gemini", "openai"}:
        provider = "gemini"
    model = normalize_text(data.get("model") or ("gemini-1.5-flash" if provider == "gemini" else "gpt-4o-mini"))
    api_key = (data.get("api_key") or "").strip()
    with db() as conn:
        old = conn.execute("SELECT api_key FROM api_settings WHERE user_id = ?", (user["id"],)).fetchone()
        if not api_key and old:
            api_key = old["api_key"]
        conn.execute(
            "INSERT INTO api_settings (user_id, provider, model, api_key, updated_at) VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET provider=excluded.provider, model=excluded.model, api_key=excluded.api_key, updated_at=excluded.updated_at",
            (user["id"], provider, model, api_key, datetime.utcnow().isoformat()),
        )
    return jsonify({"ok": True, "message": "Settings saved."})


@app.post("/api/tool")
@login_required
def run_tool():
    user = current_user()
    data = request.get_json(force=True)
    text = normalize_text(data.get("text", ""))
    tool = data.get("tool", "algorithm_rewriter")
    tone = data.get("tone", "professional")
    strength = data.get("strength", "maximum")

    if len(text) < 2:
        return jsonify({"ok": False, "error": "Please enter text first."}), 400
    if len(text) > 12000:
        return jsonify({"ok": False, "error": "Please keep text under 12,000 characters per request."}), 400

    note = "Processed successfully."
    if tool == "ai_rewriter":
        with db() as conn:
            row = conn.execute("SELECT provider, model, api_key FROM api_settings WHERE user_id = ?", (user["id"],)).fetchone()
        settings = dict(row) if row else {}
        output, note = rewrite_with_ai(text, tone=tone, strength=strength, user_settings=settings)
    else:
        output = process_tool(tool, text, tone=tone, strength=strength)

    # Never return identical output for rewriting tools.
    if tool in {"algorithm_rewriter", "ai_rewriter", "ai_style_cleaner", "product_rewriter"} and output.strip().lower() == text.strip().lower():
        output = process_tool("algorithm_rewriter", text, tone=tone, strength="maximum")
        note = "The first output was too similar, so a stronger rewrite was applied."

    score = metrics(text, output)
    with db() as conn:
        conn.execute(
            "INSERT INTO history (user_id, tool, tone, strength, input_text, output_text, score_similarity, score_lift, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user["id"], tool, tone, strength, text, output, score["similarity"], score["originality_lift"], datetime.utcnow().isoformat()),
        )
    return jsonify({"ok": True, "output": output, "metrics": score, "note": note})


@app.get("/api/history")
@login_required
def history():
    user = current_user()
    with db() as conn:
        rows = conn.execute(
            "SELECT id, tool, tone, strength, substr(input_text, 1, 160) AS input_preview, substr(output_text, 1, 160) AS output_preview, score_similarity, score_lift, created_at "
            "FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 30",
            (user["id"],),
        ).fetchall()
    return jsonify({"ok": True, "history": [dict(r) for r in rows]})


@app.post("/api/history/clear")
@login_required
def clear_history():
    user = current_user()
    with db() as conn:
        conn.execute("DELETE FROM history WHERE user_id = ?", (user["id"],))
    return jsonify({"ok": True})


@app.get("/health")
def health():
    return jsonify({"ok": True, "app": APP_NAME})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
