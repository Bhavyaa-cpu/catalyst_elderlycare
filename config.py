"""
Catalyst Care - Intelligent Healthcare Management System for Elderly & Caretakers
Configuration and Application Settings
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "catalyst_care.db"
UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = BASE_DIR / "static"

# Ensure runtime directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Server Configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8501

# Application Identity
APP_NAME = "Catalyst Care"
APP_SUBTITLE = "Smart Elderly Health, Appointment & Caregiver Coordination Platform"
APP_VERSION = "2.0.0"

# Design Theme Palette
THEME = {
    "teal_primary": "#0d9488",      # Teal Blue
    "teal_dark": "#0f766e",
    "teal_light": "#ccfbf1",
    "green_royal": "#15803d",      # Royal Green
    "green_emerald": "#059669",
    "green_light": "#dcfce7",
    "navy_dark": "#0f172a",
    "bg_slate": "#f8fafc",
    "card_bg": "#ffffff",
    "alert_red": "#dc2626",
    "alert_light": "#fee2e2",
    "warning_amber": "#d97706",
}

# User Roles
ROLE_ELDERLY = "elderly"
ROLE_CARETAKER = "caretaker"
ROLE_DOCTOR_ADMIN = "doctor_admin"

AVAILABLE_ROLES = [
    {"id": ROLE_ELDERLY, "label": "Elderly User (Smt. Lakshmi Devi)", "icon": "👵"},
    {"id": ROLE_CARETAKER, "label": "Caretaker / Daughter (Priya Sharma)", "icon": "👩‍⚕️"},
    {"id": ROLE_DOCTOR_ADMIN, "label": "Doctor / Admin (Dr. Ramesh Sharma)", "icon": "🩺"},
]

# Supported Languages for Voice & Interface
LANGUAGES = {
    "en-IN": {"code": "en", "name": "English (India)", "voice_lang": "en-IN"},
    "te-IN": {"code": "te", "name": "తెలుగు (Telugu)", "voice_lang": "te-IN"},
    "hi-IN": {"code": "hi", "name": "हिन्दी (Hindi)", "voice_lang": "hi-IN"},
}

# Medical & Travel Simulation Settings
SIMULATION_MODE = True
TRAVEL_BUFFER_MINUTES = 25
ALERT_HOURS_BEFORE_APPOINTMENT = 2

# Safety Disclaimers
MEDICAL_DISCLAIMER = (
    "NOTICE: Catalyst Care provides schedule, reminder, and document assistance. "
    "It never independently diagnoses, prescribes, or modifies medication dosages. "
    "An unacknowledged reminder does not prove a dose was missed. In emergencies, call 112 or local emergency services."
)
