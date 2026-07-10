from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from decorators import role_required
from extensions import db
from model.booking import Booking
from model.trek import Trek
from model.user import User

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


def trek_dict(t):
    return {
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration_days": t.duration_days,
        "price": t.price,
        "slots": t.slots,
        "status": t.status,
    }


@user_bp.get("/treks")
@role_required("trekker")
def list_open_treks():
    query = Trek.query.filter_by(status="Open")
    if difficulty := request.args.get("difficulty"):
        query = query.filter_by(difficulty=difficulty)
    if location := request.args.get("location"):
        query = query.filter(Trek.location.ilike(f"%{location}%"))
    if duration := request.args.get("duration"):
        query = query.filter_by(duration_days=duration)
    return jsonify([trek_dict(t) for t in query.all()])


@user_bp.post("/treks/<int:trek_id>/book")
@role_required("trekker")
def book_trek(trek_id):
    user_id = get_jwt_identity()

    trek = Trek.query.with_for_update().get_or_404(trek_id)
    if trek.status != "Open" or trek.slots <= 0:
        return jsonify({"error": "trek is not open for booking"}), 400
    if Booking.query.filter_by(user_id=user_id, trek_id=trek_id).first():
        return jsonify({"error": "already booked"}), 409

    trek.slots -= 1
    db.session.add(Booking(user_id=user_id, trek_id=trek_id))
    db.session.commit()
    return jsonify({"message": "booked"}), 201


@user_bp.get("/profile")
@role_required("trekker")
def get_profile():
    user = User.query.get_or_404(get_jwt_identity())
    return jsonify({"id": user.id, "name": user.name, "email": user.email})


@user_bp.put("/profile")
@role_required("trekker")
def update_profile():
    user = User.query.get_or_404(get_jwt_identity())
    data = request.get_json() or {}
    if name := data.get("name"):
        user.name = name
    if password := data.get("password"):
        user.set_password(password)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email})
