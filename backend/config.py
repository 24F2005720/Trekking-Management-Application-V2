class Config:
    SECRET_KEY = "it-is-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "it-is-secret"

    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

   
    MAIL_SERVER = None
    MAIL_FROM = "noreply@trekking.local"
    ADMIN_EMAIL = "admin@trekking.com"
    EXPORT_DIR = "exports"
