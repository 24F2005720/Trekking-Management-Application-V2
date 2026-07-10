from flask import Flask

from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from model import booking, staff_profile, trek, user  # noqa: F401  registers tables

    @app.route("/")
    def home():
        return {"message": "Trekking Management Application API"}

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
