from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from cache import cache_invalidate
from decorators import role_required
from extensions import db
from model.booking import Booking
from model.trek import Trek

staff_bp = Blueprint("staff", __name__, url_prefix="/api/staff")


def trek_dict(t, participant_count=None):
    d = {
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration_days": t.duration_days,
        "price": t.price,
        "slots": t.slots,
        "status": t.status,
    }
    if participant_count is not None:
        d["participant_count"] = participant_count
    return d


@staff_bp.get("/treks")
@role_required("staff")
def list_my_treks():
    staff_id = get_jwt_identity()
    treks = Trek.query.filter_by(staff_id=staff_id).all()
    return jsonify(
        [trek_dict(t, Booking.query.filter_by(trek_id=t.id, status="Booked").count()) for t in treks]
    )


@staff_bp.put("/treks/<int:trek_id>")
@role_required("staff")
def update_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    for field in ["slots", "status"]:
        if field in data:
            setattr(trek, field, data[field])
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(trek_dict(trek))


@staff_bp.patch("/treks/<int:trek_id>/status")
@role_required("staff")
def set_status(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    status = (request.get_json() or {}).get("status")
    valid_transitions = {"Open": ("Started", "Closed"), "Started": ("Completed", "Closed")}
    if status not in valid_transitions.get(trek.status, ()):
        return jsonify({"error": f"cannot move from {trek.status} to {status}"}), 400

    trek.status = status
    db.session.commit()
    cache_invalidate("treks:")
    return jsonify(trek_dict(trek))


@staff_bp.get("/treks/<int:trek_id>/participants")
@role_required("staff")
def participants(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    bookings = Booking.query.filter_by(trek_id=trek_id, status="Booked").all()
    return jsonify([{"id": b.user.id, "name": b.user.name, "email": b.user.email} for b in bookings])
