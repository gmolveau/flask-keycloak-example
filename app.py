import secrets

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "OAG581bggitAfmL6Aa5kbBjTN9li-OK6A1ROaBGHSzM"

# OAuth configuration
oauth = OAuth(app)
oauth.register(
    name="keycloak",
    client_id="flask-app",
    client_secret="L0nrBUABwIm3ghXrrXmoX76BJ6xjzDvy_wzDff6rKQ0",
    server_metadata_url="http://localhost:8080/realms/myrealm/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
    },
)


@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
        username = user.get("preferred_username", "N/A")
        sub = user.get("sub", "N/A")
        roles = user.get("realm_access", {}).get("roles", [])
        groups = user.get("groups", [])
        return f"Username: {username}<br>Sub: {sub}<br>Roles: {roles}<br>Groups: {groups}<br><a href='/logout'>Logout</a>"
    return "Not logged in. <a href='/login'>Login</a>"


@app.route("/login")
def login():
    nonce = secrets.token_urlsafe(16)
    session["nonce"] = nonce
    print(nonce)
    redirect_uri = url_for("callback", _external=True)
    print(redirect_uri)
    return oauth.keycloak.authorize_redirect(redirect_uri, nonce=nonce)


@app.route("/callback")
def callback():
    nonce = session.pop("nonce", None)
    if not nonce:
        return "Error: Missing nonce in session", 400
    token = oauth.keycloak.authorize_access_token()
    user = oauth.keycloak.parse_id_token(token, nonce)
    session["user"] = user
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
