from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from key_public import public_key
from models import db, Users

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        TOKEN = None
        if "Authorization" in request.headers:
            TOKEN = request.headers["Authorization"].split(" ")[1]
        if not TOKEN:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            PUBLIC_KEY=public_key()
            DATA = jwt.decode(TOKEN, PUBLIC_KEY, audience="account",algorithms=["RS256"])
            CURRENT_USER=db.session.query(Users).filter_by(login=(DATA["preferred_username"])).first()
            if CURRENT_USER is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if CURRENT_USER.__dict__["active"] is False:
                abort(403)
        except jwt.ExpiredSignatureError:
            print("Token expired. Get new one")
        except jwt.InvalidTokenError:
            print("Invalid Token")
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(CURRENT_USER, *args, **kwargs)

    return decorated
