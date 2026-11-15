"""
Catalyst Care - Database Manager
Handles SQLite database connection, table creation, migrations, and CRUD operations.
"""
import sqlite3
import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
from config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Creates a database connection with row factory configured."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_database() -> None:
    """Initializes all SQLite database tables with strict relational schemas."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        role TEXT NOT NULL CHECK(role IN ('elderly', 'caretaker', 'doctor_admin')),
        language TEXT DEFAULT 'en-IN',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Elderly Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS elderly_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT,
        blood_group TEXT,
        primary_address TEXT,
        city TEXT DEFAULT 'Bangalore',
        primary_hospital TEXT,
        emergency_notes TEXT,
        travel_buffer_mins INTEGER DEFAULT 25,
        auto_confirm_booking INTEGER DEFAULT 0,
        high_contrast_pref INTEGER DEFAULT 0,
        large_font_pref INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 3. Caretakers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS caretakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        elderly_id INTEGER NOT NULL,
        relationship TEXT NOT NULL,
        priority_order INTEGER DEFAULT 1,
        phone TEXT NOT NULL,
        email TEXT,
        is_primary INTEGER DEFAULT 0,
        can_manage_appointments INTEGER DEFAULT 1,
        can_manage_medications INTEGER DEFAULT 1,
        escalation_delay_mins INTEGER DEFAULT 30,
        notification_channel TEXT DEFAULT 'IN_APP',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    # 4. Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        hospital_clinic TEXT NOT NULL,
        location TEXT NOT NULL,
        consultation_fee REAL DEFAULT 800.0,
        contact_phone TEXT,
        contact_email TEXT,
        bio TEXT,
        rating REAL DEFAULT 4.8,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # 5. Doctor Availability Slots Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctor_availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        day_of_week TEXT NOT NULL, -- Monday, Tuesday, etc.
        start_time TEXT NOT NULL,   -- e.g. '09:00'
        end_time TEXT NOT NULL,     -- e.g. '13:00'
        slot_duration_mins INTEGER DEFAULT 30,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
    );
    """)

    # 6. Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL, -- YYYY-MM-DD
        appointment_time TEXT NOT NULL, -- HH:MM
        duration_mins INTEGER DEFAULT 30,
        purpose TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled', 'rescheduled')),
        accompanied_by_caretaker_id INTEGER,
        location TEXT NOT NULL,
        estimated_travel_mins INTEGER DEFAULT 25,
        simulated_traffic_status TEXT DEFAULT 'Normal (Simulated)',
        suggested_departure_time TEXT,
        departure_alert_sent INTEGER DEFAULT 0,
        auto_booked INTEGER DEFAULT 0,
        cancellation_reason TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
        FOREIGN KEY (accompanied_by_caretaker_id) REFERENCES caretakers(id) ON DELETE SET NULL
    );
    """)

    # 7. Medications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        dosage TEXT NOT NULL,        -- e.g. '500 mg'
        form TEXT DEFAULT 'Tablet',   -- Tablet, Capsule, Syrup, Injection
        frequency TEXT NOT NULL,     -- e.g. 'Twice daily'
        timing_slots TEXT NOT NULL,  -- JSON or comma-separated e.g. '08:00,20:00'
        food_relation TEXT DEFAULT 'After Food', -- Before Food, After Food, With Food
        current_stock INTEGER NOT NULL DEFAULT 30,
        unit TEXT DEFAULT 'tablets',
        daily_consumption INTEGER DEFAULT 1,
        refill_threshold INTEGER DEFAULT 7, -- Days of supply remaining to trigger alert
        prescribed_by_doctor_id INTEGER,
        instructions TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE,
        FOREIGN KEY (prescribed_by_doctor_id) REFERENCES doctors(id) ON DELETE SET NULL
    );
    """)

    # 8. Medication Reminders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medication_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication_id INTEGER NOT NULL,
        elderly_id INTEGER NOT NULL,
        reminder_date TEXT NOT NULL, -- YYYY-MM-DD
        reminder_time TEXT NOT NULL, -- HH:MM
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'acknowledged', 'unacknowledged', 'escalated')),
        acknowledged_at TIMESTAMP,
        acknowledged_by_role TEXT,
        escalation_sent INTEGER DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (medication_id) REFERENCES medications(id) ON DELETE CASCADE,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    # 9. Medical Documents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        appointment_id INTEGER,
        title TEXT NOT NULL,
        doc_type TEXT NOT NULL, -- prescription, ecg, blood_test, radiology, discharge_summary, general
        file_path TEXT,
        extracted_text TEXT,
        verified_by_caretaker INTEGER DEFAULT 0,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE,
        FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL
    );
    """)

    # 10. Preparation Checklists Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS preparation_checklists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER NOT NULL,
        item_title TEXT NOT NULL,
        is_mandatory INTEGER DEFAULT 1,
        is_completed INTEGER DEFAULT 0,
        document_id INTEGER,
        notes TEXT,
        FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
        FOREIGN KEY (document_id) REFERENCES medical_documents(id) ON DELETE SET NULL
    );
    """)

    # 11. Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        recipient_role TEXT NOT NULL, -- elderly, caretaker, doctor_admin, all
        recipient_id INTEGER,
        category TEXT NOT NULL,       -- appointment, medication, travel, document, sos, escalation, booking
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        priority TEXT DEFAULT 'normal' CHECK(priority IN ('normal', 'high', 'urgent')),
        is_read INTEGER DEFAULT 0,
        is_acknowledged INTEGER DEFAULT 0,
        acknowledged_at TIMESTAMP,
        simulated_channel TEXT DEFAULT 'IN_APP', -- IN_APP, SMS_SIMULATED, WHATSAPP_SIMULATED
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    # 12. Caregiver Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS caregiver_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        assigned_to_caretaker_id INTEGER,
        title TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority TEXT DEFAULT 'Medium' CHECK(priority IN ('Low', 'Medium', 'High', 'Urgent')),
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed')),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE,
        FOREIGN KEY (assigned_to_caretaker_id) REFERENCES caretakers(id) ON DELETE SET NULL
    );
    """)

    # 13. Emergency Contacts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        relationship TEXT NOT NULL,
        phone TEXT NOT NULL,
        priority INTEGER DEFAULT 1,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    # 14. Emergency Events Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        triggered_by TEXT NOT NULL,
        status TEXT DEFAULT 'simulated_active' CHECK(status IN ('simulated_active', 'resolved')),
        location_lat REAL DEFAULT 12.9716,
        location_lng REAL DEFAULT 77.5946,
        location_address TEXT DEFAULT 'Bangalore Central, Karnataka (Simulated GPS)',
        contacts_alerted_summary TEXT,
        resolution_notes TEXT,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    # 15. Timeline Events Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        event_type TEXT NOT NULL, -- visit, medication, lab_report, followup, observation, sos
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        event_date TEXT NOT NULL,
        author_or_doctor TEXT,
        report_score REAL,
        metadata_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    # 16. Follow-up Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followup_appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        previous_appointment_id INTEGER,
        recommended_date TEXT NOT NULL,
        specialty TEXT NOT NULL,
        doctor_name TEXT,
        notes TEXT,
        is_booked INTEGER DEFAULT 0,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE,
        FOREIGN KEY (previous_appointment_id) REFERENCES appointments(id) ON DELETE SET NULL
    );
    """)

    # 17. Care Journal Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS care_journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        author_name TEXT NOT NULL,
        author_role TEXT NOT NULL,
        entry_date TEXT NOT NULL,
        entry_text TEXT NOT NULL,
        vitals_summary TEXT,
        mood TEXT DEFAULT 'Normal',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    # 18. Health Reports & Vitals Table (Supports User's specific health trend graph request!)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elderly_id INTEGER NOT NULL,
        report_date TEXT NOT NULL,
        report_name TEXT NOT NULL,
        systolic_bp INTEGER,          -- mmHg (Normal 110-125)
        diastolic_bp INTEGER,         -- mmHg (Normal 70-85)
        blood_glucose_mg_dl INTEGER,  -- mg/dL Fasting (Normal 70-110)
        spo2_percent INTEGER,         -- % (Normal 95-100)
        heart_rate_bpm INTEGER,       -- bpm (Normal 60-90)
        cholesterol_mg_dl INTEGER,    -- mg/dL (Normal < 200)
        composite_health_score REAL,  -- Computed score (0-100)
        doctor_notes TEXT,
        extracted_summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (elderly_id) REFERENCES elderly_profiles(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

# Helper Query Execution Functions

def execute_query(query: str, params: Tuple = ()) -> int:
    """Executes an INSERT, UPDATE, or DELETE query and returns the lastrowid or affected rows."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def fetch_all(query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    """Fetches all rows matching query as list of dictionaries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result

def fetch_one(query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
    """Fetches single row matching query as dictionary."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
