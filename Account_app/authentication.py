import jwt
from .models import User
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os

load_dotenv()


def create_access_token(id):
    algorithm = "HS256"

    payload = {
        'user_id' : id,
        'iat' : datetime.now(timezone.utc),
        'exp' : datetime.now(timezone.utc) + timedelta(minutes=15)
    }

    secret_key = os.getenv("access_token_key")
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, os.getenv("access_token_key"), algorithms="HS256")
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return {"error" : "token Expierd"}
    except jwt.InvalidTokenError:
        return {"error" : "token Invalid"}


def create_refresh_token(id):
    algorithm = "HS256"

    payload = {
        'user_id' : id,
        'iat' : datetime.now(timezone.utc),
        'exp' : datetime.now(timezone.utc) + timedelta(days=7)
    }

    secret_key = os.getenv("refresh_token_key")
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, os.getenv("refresh_token_key"), algorithms="HS256")
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return {"error" : "token Expierd"}
    except jwt.InvalidTokenError:
        return {"error" : "token Invalid"}

