import os

def _get_env():
    return os.environ.get("ENV")

def env_sqlite():
    return _get_env() == "SQLITE"

def env_production():
    return _get_env() == "HEROKU"

def env_db_url():
    if env_production():
        return os.environ.get("DATABASE_URL")
    elif env_sqlite():
        return "sqlite:///database.db"
    else:
        return "postgres://postgres@localhost:5432/webi_shoppi"

def get_required_msg():
    return "Kenttä on pakollinen"
