# 🌿 Catalyst Care
### Intelligent Healthcare Management, Smart Appointment Coordination & AI Voice Companion for Elderly & Caregivers

A complete, accessible, modern web application engineered for hackathons and geriatric healthcare management. Catalyst Care bridges the gap between elderly parents, busy family caregivers, and doctors through voice-first interactions, proactive appointment preparation, medication refill forecasting, and Pandas-powered clinical analytics.

---

## 🏆 Project Highlights

- **Zero Uninstalled Dependencies**: Runs directly on your existing environment using Python standard library + Tornado, Pandas, Jinja2, and SQLite. No Streamlit or Plotly installations required.
- **Voice-First Multi-Lingual Assistant**: Web Speech API Speech-to-Text (STT) and Text-to-Speech (TTS) supporting **English**, **తెలుగు (Telugu)**, and **हिन्दी (Hindi)** with sensitive action confirmation safeguards.
- **Overall Health Score Graph (User Request)**: Plots a responsive interactive trajectory of the elder's overall health index over time calculated from submitted blood pressure, glucose, SpO2, and cholesterol reports.
- **Smart 2-Day Pre-Appointment Assistant**: Scans upcoming visits, auto-generates specialty checklists (Cardiology, Neurology, Orthopedics), audits uploaded reports, and alerts caregivers about missing tests.
- **Safe Medication Tracking**: 1-tap elderly confirmation cards, automatic stock deduction, depletion timeline prediction, and low-stock refill alerts.
- **Simulated Travel & Departure Intelligence**: Computes stress-free departure times factoring hospital distances, traffic, and a 25-minute senior transit buffer.
- **Emergency SOS Hub**: Accessible large-button emergency trigger with accidental activation safeguards, simulated GPS broadcasting, and family notification dispatch.
- **Multi-Role Prototype Switcher**: Instantly switch between **Elderly User** (*Smt. Lakshmi Devi*), **Caretaker** (*Priya Sharma*), and **Doctor** (*Dr. Ramesh Sharma*).

---

## 🚀 How to Launch on Windows 11

### Step 1: Open Terminal in Project Directory
Open **PowerShell** or **Command Prompt** and navigate to your project folder:
```powershell
cd c:\Users\bhavs\Downloads\Catalyst
```

### Step 2: Initialize Database (Pre-seeded with Sample Data)
Run the database initialization script to create tables and load realistic demonstration data:
```powershell
python init_db.py
```
*Output: `Database initialization and seed complete!`*

### Step 3: Start the Web Application
```powershell
python app.py
```

### Step 4: Open in Web Browser
Open your favorite browser (Google Chrome, Microsoft Edge, or Brave) and visit:
👉 **[http://localhost:8501](http://localhost:8501)** or **[http://127.0.0.1:8501](http://127.0.0.1:8501)**

### Step 5: Run Automated Unit Tests
To verify all 17 automated tests for appointments, conflict detection, medication stock, Pandas analytics, and voice queries:
```powershell
python -m unittest discover tests
```
*Output: `Ran 17 tests in 0.112s ... OK`*

---

## 🧭 Application Navigation (14 Views)

1. **Home Dashboard**: Daily voice morning briefing, stat counters, quick role portals.
2. **Elderly User Dashboard**: Extra-large typography, big voice microphone, 1-tap "I Took This Medicine" cards, and 1-touch Emergency SOS.
3. **Caretaker Dashboard**: Weekly clinical summary, family task delegation board, low-stock refill warnings, and unacknowledged alerts.
4. **Smart Appointment Calendar**: Master schedule, conflict detection badges, status filters, and rescheduling tools.
5. **AI Voice Assistant**: Web Speech STT & TTS, language selector (EN, TE, HI), speech feedback, text fallback input, and safety confirmation gates.
6. **Medication Manager**: Active prescriptions, dosage timings, food relations, stock level meters, and refill restock buttons.
7. **Document Preparation**: Pre-appointment 2-day checklist, document vault with uploaded PDF/images, and text extraction summaries.
8. **Travel Intelligence**: Clinic locations, departure time calculator (`Departure = Appt - Travel - Buffer`), 2-hour departure alerts.
9. **Doctor Availability & Booking**: Verified doctor profiles, clinical slots, slot conflict detection, and pre-approved auto-booking rules.
10. **Family Coordination**: Caretaker hierarchy (Primary vs Secondary), caregiver task board, shared care journal, and one-touch family calling simulation.
11. **Emergency SOS**: Large high-contrast SOS trigger, accidental activation modal, contact broadcast list, simulated GPS coordinates, and resolution history.
12. **Health Timeline**: Chronological clinical history merging doctor visits, medication acknowledgements, lab reports, and family notes.
13. **Health Analytics Dashboard**: Pandas-powered metrics:
    - **Overall Health Score Trend Graph** based on submitted reports.
    - Medication Adherence Rate.
    - Appointment Attendance Rate.
    - Medicine stock depletion curve.
14. **Settings & Accessibility**: High-contrast mode toggle, large-font toggle, role switcher, and compliance disclaimers.

---

## ⚙️ Feature Implementation Status Matrix

| Feature | Status | Implementation Details |
|---|---|---|
| **SQL Database Storage** | 🟢 **Fully Working** | SQLite (`catalyst_care.db`) with 18 relational tables, foreign keys, and indexes. |
| **Appointment Scheduling** | 🟢 **Fully Working** | Add, edit, cancel with overlap conflict detection preventing double booking. |
| **Medication Management** | 🟢 **Fully Working** | 1-tap confirmation, stock deduction, days of supply math, refill alerts. |
| **Document Preparation** | 🟢 **Fully Working** | 2-day pre-appointment audit, specialty checklist templates, text extraction. |
| **Voice Assistant** | 🟢 **Fully Working** | Browser Web Speech API (STT + TTS) in English, Telugu, Hindi + text fallback. |
| **Overall Health Graph** | 🟢 **Fully Working** | Native responsive HTML5 Canvas chart computed via Pandas from submitted reports. |
| **Pandas Analytics** | 🟢 **Fully Working** | Adherence rates, attendance stats, and refill forecasting using Pandas Series/DataFrames. |
| **Accessibility Modes** | 🟢 **Fully Working** | Toggleable High-Contrast CSS and Large-Font scaling for elderly users. |
| **Multi-Caretaker Escalation** | 🟢 **Fully Working** | Escalates unacknowledged urgent notifications from Primary to Secondary caregiver. |
| **Live Traffic API** | 🟡 **Simulated Adapter** | Computes departure with 25-minute senior buffer; adapter ready for Google Maps API. |
| **SMS / WhatsApp Alerts** | 🟡 **Simulated Adapter** | Dispatches to in-app notification center; ready for Twilio / Meta WhatsApp API. |
| **Emergency 112 Dialing** | 🟡 **Simulated Adapter** | Dispatches emergency alerts & GPS coordinates; does not place live telecom 112 calls. |

---

## 📂 Project Architecture

```
Catalyst/
│
├── app.py                      # Main Tornado web server & REST API router
├── config.py                   # Central settings, color palette, roles, and paths
├── database.py                 # SQLite relational schema & execution helpers
├── init_db.py                  # Database initialization and sample data seeder
├── requirements.txt            # Documented dependencies
├── README.md                   # Complete guide & documentation
├── .gitignore                  # Excludes private databases, keys, uploads, and caches
│
├── modules/                    # Clean modular backend feature packages
│   ├── __init__.py
│   ├── appointments.py         # Scheduling, conflict detection & briefings
│   ├── medications.py          # Stock tracking, reminders & refill forecasting
│   ├── documents.py            # Uploads, text extraction & 2-day checklist audit
│   ├── travel.py               # Departure calculations & traffic adapter
│   ├── doctors.py              # Availability slots & pre-approved booking rules
│   ├── coordination.py         # Multi-caretaker escalation, task board & care journal
│   ├── emergency.py            # Accessible SOS trigger, accidental protection & GPS
│   ├── timeline.py             # Chronological clinical history aggregator
│   ├── analytics.py            # Pandas healthcare schedule & overall health graph
│   └── voice_assistant.py      # Multi-lingual NLP (English, Telugu, Hindi)
│
├── templates/
│   └── index.html              # Modern, responsive Jinja2 single-page layout
│
├── static/
│   ├── css/
│   │   └── style.css           # Teal blue (#0d9488) & royal green (#15803d) theme
│   └── js/
│       └── app.js              # Controller for STT/TTS, Canvas graphs & UI router
│
├── uploads/                    # Secure local vault for PDF & image medical reports
│   ├── sample_ecg.pdf
│   ├── sample_blood_test.pdf
│   ├── sample_knee_xray.pdf
│   └── sample_prescription.pdf
│
└── tests/                      # Automated unit test suite (17 tests)
    ├── test_database.py
    ├── test_appointments.py
    ├── test_medications.py
    ├── test_analytics.py
    ├── test_voice_assistant.py
    └── test_features.py
```

---

## 🔒 Privacy, Security & Clinical Safety

1. **Synthetic Data Only**: All patient names, phone numbers, and addresses (*e.g., Smt. Lakshmi Devi, Bangalore*) are completely synthetic demonstration profiles.
2. **Local Data Isolation**: All medical records and database files reside strictly within your local machine. No external cloud uploads occur.
3. **Clinical Safety Safeguards**:
   - Catalyst Care **never** independently modifies medication dosages or diagnoses conditions.
   - Unacknowledged reminders are **never** treated as proof that a dose was missed.
   - Cancelling appointments and sharing clinical files requires mandatory user confirmation.
   - Simulated emergency alerts are clearly labeled to prevent confusion during hackathon demonstrations.

---

## 💡 Beginner Developer Tips for Hackathon Presentation

When presenting this project to judges:
1. **Highlight the Problem**: Elderly people struggle with complicated medical apps, remembering multi-dose schedules, and organizing reports before doctor visits.
2. **Show the Voice Assistant**: Switch language to **Telugu** or **Hindi**, ask *"What appointments do I have today?"*, and demonstrate the text-to-speech voice response.
3. **Show the Overall Health Graph**: Navigate to the **Health Analytics** tab and explain how Pandas calculates the composite score (BP, glucose, SpO2) across 6 months of submitted reports to prove positive health recovery!
4. **Show Conflict Detection**: Try booking an appointment at the same time as an existing one to prove the intelligent scheduling engine blocks overlaps.
5. **Demonstrate 1-Tap Confirmation**: Open the Elderly User Dashboard and click *"✅ I Took This Medicine"* to show immediate real-time stock deduction and timeline recording.
