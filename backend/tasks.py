import csv
import os
import smtplib
from email.message import EmailMessage

from flask import current_app, render_template_string

from celery_app import celery
from model.booking import Booking
from model.user import User

REPORT_TEMPLATE = """
<h1>Monthly Trekking Report</h1>
<ul>
  <li>Total treks: {{ treks }}</li>
  <li>Total staff: {{ staff }}</li>
  <li>Total trekkers: {{ trekkers }}</li>
  <li>Total bookings: {{ bookings }}</li>
</ul>
"""


def send_email(to, subject, body):
    server = current_app.config["MAIL_SERVER"]
    if not server:
        print(f"[email suppressed] to={to} subject={subject}\n{body}")
        return

    msg = EmailMessage()
    msg["From"] = current_app.config["MAIL_FROM"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body, subtype="html")
    with smtplib.SMTP(server, current_app.config["MAIL_PORT"]) as smtp:
        smtp.starttls()
        smtp.login(current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"])
        smtp.send_message(msg)


@celery.task(name="tasks.send_daily_reminders")
def send_daily_reminders():
    bookings = Booking.query.filter_by(status="Booked").all()
    for b in bookings:
        if b.trek.status != "Open":
            continue
        send_email(
            b.user.email,
            f"Reminder: your trek '{b.trek.name}' is coming up",
            f"<p>Hi {b.user.name}, this is a reminder about your upcoming trek "
            f"<strong>{b.trek.name}</strong> in {b.trek.location}.</p>",
        )
    return len(bookings)


@celery.task(name="tasks.generate_monthly_report")
def generate_monthly_report():
    from model.trek import Trek

    stats = {
        "treks": Trek.query.count(),
        "staff": User.query.filter_by(role="staff").count(),
        "trekkers": User.query.filter_by(role="trekker").count(),
        "bookings": Booking.query.count(),
    }
    html = render_template_string(REPORT_TEMPLATE, **stats)
    send_email(current_app.config["ADMIN_EMAIL"], "Monthly Trekking Report", html)
    return stats


@celery.task(name="tasks.export_booking_history_csv", bind=True)
def export_booking_history_csv(self, user_id):
    os.makedirs(current_app.config["EXPORT_DIR"], exist_ok=True)
    path = os.path.join(current_app.config["EXPORT_DIR"], f"booking_history_{user_id}_{self.request.id}.csv")

    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booked_at.desc()).all()
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["trek", "location", "status", "booked_at"])
        for b in bookings:
            writer.writerow([b.trek.name, b.trek.location, b.status, b.booked_at.isoformat()])

    return path
