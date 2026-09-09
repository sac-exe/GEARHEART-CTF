from flask import Flask, request, session, redirect, render_template, render_template_string, make_response
import os
import uuid
import subprocess 


# Blacklist v2 - developer got more paranoid after a red team report.
# Blocks not just the obvious payload words, but the introspection/bypass
# primitives themselves, AND the concatenation operators (~ and +).
BLACKLIST = [
    "os", "popen", "system", "import", "eval", "exec", "open(", "read_flag",
    "class", "mro", "base", "subclasses", "globals", "builtins",
    "config", "request", "self", "subprocess", "cat ", "type ", "cmd",
    "~", "+", "format", "attr"
]

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory "database" of users
USERS = {
    "guest": "guest123",
}

# In-memory session store: session_id -> username
# This is intentionally simple so we can leak it later (that's the vuln)
ACTIVE_SESSIONS = {}

# Pre-seed an "admin" session that has been active for a long time
# (simulates the "old session that never expired" scenario)
ADMIN_SESSION_ID = str(uuid.uuid4())
ACTIVE_SESSIONS[ADMIN_SESSION_ID] = "admin"


@app.route("/", methods=["GET"])
def home():
    sid = request.cookies.get("session_id")
    username = ACTIVE_SESSIONS.get(sid)

    if not username:
        return redirect("/login")

    return render_template("index.html", username=username, announcement="Welcome to the portal.")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        if USERS.get(u) == p:
            sid = str(uuid.uuid4())
            ACTIVE_SESSIONS[sid] = u
            resp = make_response(redirect("/"))
            resp.set_cookie("session_id", sid)
            return resp
        else:
            return "Invalid credentials", 401

    return '''
        <link rel="stylesheet" href="/static/style.css">
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
        <p>Hint: try registering as guest / guest123</p>
    '''


@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.delete_cookie("session_id")
    return resp


@app.route("/broadcast", methods=["GET", "POST"])
def broadcast():
    sid = request.cookies.get("session_id")
    username = ACTIVE_SESSIONS.get(sid)

    # Broken access control check: only admin should see this
    if username != "admin":
        return "Forbidden: admin only", 403

    result = ""
    if request.method == "POST":
        msg = request.form.get("message", "")

        # The "fix" the developer added after a past incident - a naive blacklist
        lowered = msg.lower()
        blocked = any(word in lowered for word in BLACKLIST)

        if blocked:
            result = "Blocked: message contains forbidden content."
        else:
            # Still rendered via Jinja2 template - still vulnerable if you bypass the filter
            try:
                result = render_template_string(msg)
            except Exception as e:
                result = f"Error: {e}"

    return f'''
        <link rel="stylesheet" href="/static/style.css">
        <h1>Admin Broadcast Panel</h1>
        <form method="POST">
            <textarea name="message" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Send Broadcast">
        </form>
        <p>Result:</p>
        <div id="broadcast-result">{result}</div>
        
        <!-- 70726976617465206b6579206261636b757020617661696c61626c65206174202f5f5f6b65795f7265636f766572795f706f7274616c -->
    '''


# --- VULNERABLE ENDPOINT (Stage 4) ---
# The private key that decrypts the flag - developer left a "backup" exposed
@app.route("/__key_recovery_portal")
def key_recovery():
    with open("private.pem") as f:
        return f"<pre>{f.read()}</pre>"


# --- VULNERABLE ENDPOINT (Stage 2) ---
# This mirrors "Old Sessions" - it leaks ALL active session IDs, including admin's
@app.route("/__debug_status")
def debug_status():
    output = "<link rel=\"stylesheet\" href=\"/static/style.css\">"
    for sid, uname in ACTIVE_SESSIONS.items():
        output += f"session:{sid} -> user:{uname}<br>"
    return output


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
