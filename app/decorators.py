# app/decorators.py

import time
from functools import wraps
from flask import request, Response
from werkzeug.security import check_password_hash
from .config import Config
from .exceptions import InvalidUsage  # Import our custom exception

# In-memory login attempt tracker (for demonstration purposes)
login_attempts = {}


def check_auth(username, password):
    """Validate credentials against the configuration."""
    return username == Config.USERNAME and check_password_hash(
        Config.UPLOAD_PASSWORD_HASH, password
    )


def authenticate():
    """Return a 401 response that prompts for authentication."""
    html_response = """
    <html>
        <body>
            <h2>Authentication Required</h2>
            <p>Please enter the correct username and password.</p>
            <button onclick="window.location.href='/'">Go to Home</button>
        </body>
    </html>
    """
    return Response(
        html_response, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )


def is_ip_blocked(ip):
    """Determine if an IP address should be blocked based on failed attempts."""
    if ip in login_attempts:
        attempts, last_attempt = login_attempts[ip]
        if (
            attempts >= Config.MAX_ATTEMPTS
            and time.time() - last_attempt < Config.BLOCK_TIME
        ):
            return True
    return False


def register_failed_attempt(ip):
    """Record a failed login attempt and return the number of remaining attempts."""
    if ip in login_attempts:
        attempts, _ = login_attempts[ip]
        login_attempts[ip] = (attempts + 1, time.time())
    else:
        login_attempts[ip] = (1, time.time())
    remaining_attempts = Config.MAX_ATTEMPTS - login_attempts[ip][0]
    return remaining_attempts


def requires_auth(force_reauth=False):
    """Decorator to enforce basic authentication."""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = request.remote_addr
            if is_ip_blocked(ip):
                # Instead of using abort(), raise our custom exception
                raise InvalidUsage(
                    "Your IP is blocked due to too many failed login attempts.",
                    status_code=403,
                )
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password) or force_reauth:
                register_failed_attempt(ip)
                return authenticate()
            return f(*args, **kwargs)

        return decorated

    return decorator
