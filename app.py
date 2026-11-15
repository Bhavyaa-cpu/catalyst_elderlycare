"""
Catalyst Care - Main Web Application Server
Built using Python 3.14, Tornado 6.5, Pandas 3.0, and SQLite3.
Provides high-performance REST APIs, responsive Jinja2 rendering, and Web Speech API orchestration.
"""
import os
import json
import asyncio
from datetime import datetime, date
from pathlib import Path
import tornado.web
import tornado.ioloop
from jinja2 import Environment, FileSystemLoader

# Import configurations & core feature modules
from config import (
    BASE_DIR, DB_PATH, UPLOAD_DIR, STATIC_DIR,
    SERVER_HOST, SERVER_PORT, APP_NAME, APP_SUBTITLE, APP_VERSION,
    MEDICAL_DISCLAIMER
)
import database
import modules.appointments as appts_mod
import modules.medications as meds_mod
import modules.documents as docs_mod
import modules.travel as travel_mod
import modules.doctors as docs_dir_mod
import modules.coordination as coord_mod
import modules.emergency as emerg_mod
import modules.timeline as time_mod
import modules.analytics as anal_mod
import modules.voice_assistant as voice_mod

# Configure Jinja2 Template Engine
templates_dir = BASE_DIR / "templates"
jinja_env = Environment(loader=FileSystemLoader(str(templates_dir)))

class BaseHandler(tornado.web.RequestHandler):
    """Base request handler providing JSON serialization and CORS headers."""
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def write_json(self, data: dict, status: int = 200):
        self.set_status(status)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(data, default=str))

class IndexHandler(BaseHandler):
    """Renders the primary single-page healthcare dashboard."""
    def get(self):
        template = jinja_env.get_template("index.html")
        rendered = template.render(
            app_name=APP_NAME,
            app_subtitle=APP_SUBTITLE,
            app_version=APP_VERSION,
            medical_disclaimer=MEDICAL_DISCLAIMER,
            today_date=date.today().strftime('%Y-%m-%d')
        )
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.write(rendered)

class StateHandler(BaseHandler):
    """Returns complete aggregated state for an elderly user."""
    def get(self):
        elderly_id = int(self.get_argument("elderly_id", 1))
        role = self.get_argument("role", "elderly")

        # Aggregate data from modules
        appointments = appts_mod.get_elderly_appointments(elderly_id)
        medications = meds_mod.get_elderly_medications(elderly_id)
        today_reminders = meds_mod.get_today_medication_reminders(elderly_id)
        documents = docs_mod.get_elderly_documents(elderly_id)
        doctors = docs_dir_mod.get_all_doctors()
        caretakers = coord_mod.get_authorized_caretakers(elderly_id)
        tasks = coord_mod.get_caregiver_tasks(elderly_id)
        journal = coord_mod.get_care_journal_entries(elderly_id)
        notifications = coord_mod.get_notification_center(elderly_id, role_filter=role)
        timeline = time_mod.get_health_timeline(elderly_id)
        refill_forecast = anal_mod.get_refill_forecasting(elderly_id)
        health_trend = anal_mod.get_overall_health_trend_analytics(elderly_id)
        daily_briefing = appts_mod.generate_daily_voice_briefing(elderly_id)
        weekly_summary = appts_mod.generate_weekly_caretaker_summary(elderly_id)

        self.write_json({
            "elderly_id": elderly_id,
            "role": role,
            "appointments": appointments,
            "medications": medications,
            "today_reminders": today_reminders,
            "documents": documents,
            "doctors": doctors,
            "caretakers": caretakers,
            "tasks": tasks,
            "journal": journal,
            "notifications": notifications,
            "timeline": timeline,
            "refill_forecast": refill_forecast,
            "health_trend": health_trend,
            "daily_briefing": daily_briefing,
            "weekly_summary": weekly_summary
        })

class VoiceQueryHandler(BaseHandler):
    """Processes natural language voice/text queries in English, Telugu, or Hindi."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            body = {}

        query = body.get("query", "")
        elderly_id = int(body.get("elderly_id", 1))

        res = voice_mod.process_voice_query(elderly_id, query)
        self.write_json(res)

class BookAppointmentHandler(BaseHandler):
    """Schedules an appointment with conflict checking and pre-approved auto-rules."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid request body"}, 400)
            return

        elderly_id = int(body.get("elderly_id", 1))
        doctor_id = int(body.get("doctor_id", 1))
        target_date = body.get("appointment_date")
        target_time = body.get("appointment_time")
        purpose = body.get("purpose", "Consultation")
        accompanied = body.get("accompanied_by_caretaker_id")

        success, msg, appt_id = docs_dir_mod.book_appointment_with_auto_rules(
            elderly_id=elderly_id,
            doctor_id=doctor_id,
            target_date=target_date,
            requested_time=target_time,
            purpose=purpose,
            accompanied_by_caretaker_id=accompanied
        )

        self.write_json({"success": success, "message": msg, "appointment_id": appt_id})

class CancelAppointmentHandler(BaseHandler):
    """Cancels an appointment."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid request body"}, 400)
            return

        appt_id = int(body.get("appointment_id", 0))
        reason = body.get("reason", "Cancelled by patient/caretaker")
        success, msg = appts_mod.cancel_appointment(appt_id, reason)
        self.write_json({"success": success, "message": msg})

class AcknowledgeMedicationHandler(BaseHandler):
    """Records 1-tap confirmation that a dose was taken and updates stock."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid request body"}, 400)
            return

        reminder_id = int(body.get("reminder_id", 0))
        role = body.get("role", "elderly")

        success, msg = meds_mod.acknowledge_medication_reminder(reminder_id, role)
        self.write_json({"success": success, "message": msg})

class UpdateMedicationStockHandler(BaseHandler):
    """Updates medicine stock count when refilled."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid request body"}, 400)
            return

        med_id = int(body.get("medication_id", 0))
        new_stock = int(body.get("new_stock", 30))

        success, msg = meds_mod.update_medication_stock(med_id, new_stock)
        self.write_json({"success": success, "message": msg})

class UploadDocumentHandler(BaseHandler):
    """Handles medical document upload and basic text extraction."""
    def post(self):
        elderly_id = int(self.get_argument("elderly_id", 1))
        title = self.get_argument("title", "Clinical Record")
        doc_type = self.get_argument("doc_type", "general")

        files = self.request.files.get("file")
        if not files:
            self.write_json({"success": False, "message": "No file uploaded"}, 400)
            return

        file_obj = files[0]
        filename = file_obj['filename']
        file_bytes = file_obj['body']

        success, msg, doc_id = docs_mod.upload_medical_document(
            elderly_id=elderly_id,
            title=title,
            doc_type=doc_type,
            file_bytes=file_bytes,
            filename=filename
        )
        self.write_json({"success": success, "message": msg, "document_id": doc_id})

class ToggleTaskHandler(BaseHandler):
    """Updates caregiver task status."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid body"}, 400)
            return

        task_id = int(body.get("task_id", 0))
        status = body.get("status", "completed")
        success, msg = coord_mod.update_caregiver_task_status(task_id, status)
        self.write_json({"success": success, "message": msg})

class EmergencySOSHandler(BaseHandler):
    """Triggers simulated emergency SOS broadcast with GPS coordinates."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            body = {}

        elderly_id = int(body.get("elderly_id", 1))
        triggered_by = body.get("triggered_by", "Smt. Lakshmi Devi")

        result = emerg_mod.trigger_emergency_sos(elderly_id=elderly_id, triggered_by=triggered_by)
        self.write_json(result)

class AddMedicationHandler(BaseHandler):
    """Adds a new prescribed medication record."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid request body"}, 400)
            return

        success, msg, med_id = meds_mod.add_medication(
            elderly_id=int(body.get("elderly_id", 1)),
            name=body.get("name", ""),
            dosage=body.get("dosage", ""),
            form=body.get("form", "Tablet"),
            frequency=body.get("frequency", "Once daily"),
            timing_slots=body.get("timing_slots", "08:00"),
            food_relation=body.get("food_relation", "After Food"),
            current_stock=int(body.get("current_stock", 30)),
            daily_consumption=int(body.get("daily_consumption", 1)),
            instructions=body.get("instructions", "")
        )
        self.write_json({"success": success, "message": msg, "medication_id": med_id})

class AddTaskHandler(BaseHandler):
    """Assigns a caregiver action task."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid request body"}, 400)
            return

        success, msg, task_id = coord_mod.add_caregiver_task(
            elderly_id=int(body.get("elderly_id", 1)),
            title=body.get("title", ""),
            due_date=body.get("due_date", date.today().strftime('%Y-%m-%d')),
            assigned_to_caretaker_id=body.get("assigned_to_caretaker_id"),
            priority=body.get("priority", "Medium")
        )
        self.write_json({"success": success, "message": msg, "task_id": task_id})

class AddJournalHandler(BaseHandler):
    """Records an entry in the family care journal."""
    def post(self):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            self.write_json({"success": False, "message": "Invalid request body"}, 400)
            return

        success, msg, j_id = coord_mod.add_care_journal_entry(
            elderly_id=int(body.get("elderly_id", 1)),
            author_name=body.get("author_name", "Family"),
            author_role=body.get("author_role", "Caretaker"),
            entry_text=body.get("entry_text", ""),
            vitals_summary=body.get("vitals_summary", ""),
            mood=body.get("mood", "Normal")
        )
        self.write_json({"success": success, "message": msg, "journal_id": j_id})

class AnalyticsHandler(BaseHandler):
    """Returns Pandas-powered analytics including overall health trend graph data."""
    def get(self):
        elderly_id = int(self.get_argument("elderly_id", 1))

        appts_anal = anal_mod.get_appointment_analytics(elderly_id)
        meds_anal = anal_mod.get_medication_adherence_analytics(elderly_id)
        tasks_anal = anal_mod.get_caregiver_task_analytics(elderly_id)
        refills = anal_mod.get_refill_forecasting(elderly_id)
        overall_health = anal_mod.get_overall_health_trend_analytics(elderly_id)

        self.write_json({
            "elderly_id": elderly_id,
            "appointments": appts_anal,
            "medication_adherence": meds_anal,
            "caregiver_tasks": tasks_anal,
            "refill_forecast": refills,
            "overall_health": overall_health
        })

def make_app():
    """Constructs the Tornado web application routing table."""
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/api/state", StateHandler),
        (r"/api/voice-query", VoiceQueryHandler),
        (r"/api/appointments/book", BookAppointmentHandler),
        (r"/api/appointments/cancel", CancelAppointmentHandler),
        (r"/api/medications/acknowledge", AcknowledgeMedicationHandler),
        (r"/api/medications/add", AddMedicationHandler),
        (r"/api/medications/update-stock", UpdateMedicationStockHandler),
        (r"/api/documents/upload", UploadDocumentHandler),
        (r"/api/tasks/add", AddTaskHandler),
        (r"/api/tasks/toggle", ToggleTaskHandler),
        (r"/api/journal/add", AddJournalHandler),
        (r"/api/emergency/sos", EmergencySOSHandler),
        (r"/api/analytics", AnalyticsHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": str(STATIC_DIR)}),
        (r"/uploads/(.*)", tornado.web.StaticFileHandler, {"path": str(UPLOAD_DIR)}),
    ], debug=False)

def main():
    """Initializes database if missing and starts the Tornado event loop."""
    import threading
    import webbrowser
    import time

    if not DB_PATH.exists():
        print("Database not detected. Initializing and seeding sample data...")
        from init_db import seed_database
        seed_database()

    app = make_app()
    app.listen(SERVER_PORT, address=SERVER_HOST)
    print("=" * 70)
    print(f"🌿 {APP_NAME} v{APP_VERSION} is LIVE and RUNNING!")
    print(f"👉 Open in your web browser: http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"👉 Localhost alternative:   http://localhost:{SERVER_PORT}")
    print("=" * 70)
    print("Opening web application in your default browser automatically...")
    print("Press Ctrl+C to stop the server.")

    # Automatically launch default browser
    def auto_open_browser():
        time.sleep(1.2)
        try:
            webbrowser.open(f"http://localhost:{SERVER_PORT}")
        except Exception:
            pass

    threading.Thread(target=auto_open_browser, daemon=True).start()
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
