import os
from datetime import timedelta

# database_url = "sqlite:///huinno_memo.db"
# basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'FEAROFGOD'
    GOOGLE_OAUTH_FILE = 'client_secret.json'
    GOOGLE_CLIENT_ID = "19469239236-2o3iabr5hhqos49luk25lpbqit2ns4js.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)
    SESSION_TYPE = 'filesystem'
    # SQLALCHEMY_DATABASE_URI = database_url
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
