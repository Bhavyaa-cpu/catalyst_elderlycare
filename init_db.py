"""
Catalyst Care - Database Initializer & Synthetic Seed Script
Generates a complete, realistic dataset for elderly healthcare management.
"""
from datetime import datetime, date, timedelta
from database import init_database, get_connection, execute_query
from config import DB_PATH

def seed_database():
    """Initializes tables and seeds synthetic healthcare data."""
    print("Initializing Catalyst Care Database schema...")
    init_database()

    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data safely
    tables = [
        "health_reports", "care_journal", "followup_appointments", "timeline_events",
        "emergency_events", "emergency_contacts", "caregiver_tasks", "notifications",
        "preparation_checklists", "medical_documents", "medication_reminders", "medications",
        "appointments", "doctor_availability", "doctors", "caretakers", "elderly_profiles", "users"
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

    conn.commit()
    print("Database cleared. Seeding realistic sample data...")

    # 1. Users
    cursor.execute("""
    INSERT INTO users (name, email, phone, role, language) VALUES
    ('Smt. Lakshmi Devi', 'lakshmi.devi@catalystdemo.in', '+91 98450 11223', 'elderly', 'en-IN'),
    ('Priya Sharma', 'priya.sharma@catalystdemo.in', '+91 98450 44556', 'caretaker', 'en-IN'),
    ('Rahul Sharma', 'rahul.sharma@catalystdemo.in', '+91 98450 77889', 'caretaker', 'en-IN'),
    ('Dr. Ramesh Sharma', 'dr.ramesh@apollohealth.in', '+91 98450 99001', 'doctor_admin', 'en-IN'),
    ('Dr. Ananya Iyer', 'dr.ananya@manipalhealth.in', '+91 98450 99002', 'doctor_admin', 'en-IN'),
    ('Dr. Vikram Reddy', 'dr.vikram@fortiscare.in', '+91 98450 99003', 'doctor_admin', 'en-IN');
    """)

    # 2. Elderly Profile
    cursor.execute("""
    INSERT INTO elderly_profiles (
        user_id, full_name, age, gender, blood_group, primary_address, city,
        primary_hospital, emergency_notes, travel_buffer_mins, auto_confirm_booking
    ) VALUES (
        1, 'Smt. Lakshmi Devi', 72, 'Female', 'O+',
        'Flat 302, Green Glen Gardens, Bellandur, Bangalore', 'Bangalore',
        'Apollo Hospitals, Bannerghatta Road',
        'Hypertension (5 yrs), Type 2 Diabetes, Mild Osteoarthritis in right knee. Penicillin allergy.',
        25, 1
    );
    """)

    # 3. Caretakers
    cursor.execute("""
    INSERT INTO caretakers (
        user_id, elderly_id, relationship, priority_order, phone, email, is_primary,
        can_manage_appointments, can_manage_medications, escalation_delay_mins, notification_channel
    ) VALUES
    (2, 1, 'Daughter', 1, '+91 98450 44556', 'priya.sharma@catalystdemo.in', 1, 1, 1, 30, 'IN_APP'),
    (3, 1, 'Son', 2, '+91 98450 77889', 'rahul.sharma@catalystdemo.in', 0, 1, 1, 45, 'IN_APP');
    """)

    # 4. Doctors
    cursor.execute("""
    INSERT INTO doctors (
        user_id, name, specialty, hospital_clinic, location, consultation_fee, contact_phone, bio, rating
    ) VALUES
    (4, 'Dr. Ramesh Sharma', 'Cardiologist', 'Apollo Hospitals', 'Bannerghatta Road, Bangalore', 1000.0, '+91 98450 99001', 'Senior Consultant Interventional Cardiologist with 24 years experience.', 4.9),
    (5, 'Dr. Ananya Iyer', 'Neurologist & Geriatrician', 'Manipal Hospital', 'Old Airport Road, Bangalore', 900.0, '+91 98450 99002', 'Specialist in geriatric memory care, neurological balance and wellness.', 4.8),
    (6, 'Dr. Vikram Reddy', 'Orthopedic Surgeon', 'Fortis Hospital', 'Cunningham Road, Bangalore', 850.0, '+91 98450 99003', 'Chief Orthopedic Surgeon specializing in joint replacement and geriatric mobility.', 4.7);
    """)

    # 5. Doctor Availability Slots
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for doc_id in [1, 2, 3]:
        for day in days:
            cursor.execute("""
            INSERT INTO doctor_availability (doctor_id, day_of_week, start_time, end_time, slot_duration_mins, is_active)
            VALUES (?, ?, '09:00', '13:00', 30, 1),
                   (?, ?, '14:30', '17:30', 30, 1)
            """, (doc_id, day, doc_id, day))

    today_str = date.today().strftime('%Y-%m-%d')
    tomorrow_str = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    three_days_str = (date.today() + timedelta(days=3)).strftime('%Y-%m-%d')
    next_week_str = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
    past_10d_str = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')

    # 6. Appointments
    cursor.execute("""
    INSERT INTO appointments (
        elderly_id, doctor_id, appointment_date, appointment_time, duration_mins,
        purpose, status, accompanied_by_caretaker_id, location, estimated_travel_mins,
        simulated_traffic_status, suggested_departure_time, departure_alert_sent, auto_booked, notes
    ) VALUES
    (1, 1, ?, '10:00', 30, 'Quarterly Cardiac Evaluation & BP Review', 'scheduled', 1,
     'Apollo Hospitals, Bannerghatta Road', 25, 'Moderate Traffic (Simulated)', '09:05', 0, 0,
     'Bring recent ECG report and blood pressure logs.'),
    (1, 2, ?, '11:30', 30, 'Geriatric Memory & Mobility Routine Review', 'scheduled', 1,
     'Manipal Hospital, Old Airport Road', 35, 'Heavy Traffic (Simulated)', '10:30', 0, 1,
     'Discuss mild morning dizziness and sleep quality.'),
    (1, 3, ?, '15:00', 30, 'Right Knee Osteoarthritis Follow-up', 'scheduled', 2,
     'Fortis Hospital, Cunningham Road', 30, 'Normal Traffic (Simulated)', '14:05', 0, 0,
     'Review physical therapy exercise progress.'),
    (1, 1, ?, '10:00', 30, 'Routine Medication Adjustment & ECG', 'completed', 1,
     'Apollo Hospitals, Bannerghatta Road', 25, 'Normal Traffic', '09:10', 1, 0,
     'Blood pressure stable on Telmisartan. Continue current dosage.');
    """, (today_str, three_days_str, next_week_str, past_10d_str))

    # 7. Medications
    cursor.execute("""
    INSERT INTO medications (
        elderly_id, name, dosage, form, frequency, timing_slots, food_relation,
        current_stock, unit, daily_consumption, refill_threshold, prescribed_by_doctor_id, instructions, is_active
    ) VALUES
    (1, 'Telmisartan', '40 mg', 'Tablet', 'Once daily', '08:00', 'After Food', 24, 'tablets', 1, 7, 1, 'Take with warm water every morning for blood pressure.', 1),
    (1, 'Metformin', '500 mg', 'Tablet', 'Twice daily', '08:30,20:30', 'After Food', 18, 'tablets', 2, 7, 1, 'Take after breakfast and dinner for blood sugar regulation.', 1),
    (1, 'Atorvastatin', '10 mg', 'Tablet', 'Once daily', '21:00', 'After Food', 4, 'tablets', 1, 7, 1, 'Take at bedtime for cholesterol control. Low stock alert!', 1),
    (1, 'Calcium + Vitamin D3', '500 mg + 250 IU', 'Tablet', 'Once daily', '13:00', 'With Food', 15, 'tablets', 1, 5, 3, 'Take after lunch for bone density support.', 1);
    """)

    # 8. Medication Reminders (Today & Yesterday)
    yesterday_str = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    cursor.execute("""
    INSERT INTO medication_reminders (
        medication_id, elderly_id, reminder_date, reminder_time, status, acknowledged_at, acknowledged_by_role, escalation_sent
    ) VALUES
    (1, 1, ?, '08:00', 'acknowledged', datetime('now', '-3 hours'), 'elderly', 0),
    (2, 1, ?, '08:30', 'acknowledged', datetime('now', '-2.5 hours'), 'elderly', 0),
    (4, 1, ?, '13:00', 'pending', NULL, NULL, 0),
    (2, 1, ?, '20:30', 'pending', NULL, NULL, 0),
    (3, 1, ?, '21:00', 'pending', NULL, NULL, 0),
    (2, 1, ?, '20:30', 'unacknowledged', NULL, NULL, 1);
    """, (today_str, today_str, today_str, today_str, today_str, yesterday_str))

    # 9. Medical Documents
    cursor.execute("""
    INSERT INTO medical_documents (
        elderly_id, appointment_id, title, doc_type, file_path, extracted_text, verified_by_caretaker
    ) VALUES
    (1, 1, '12-Lead Resting ECG Report', 'ecg', 'uploads/sample_ecg.pdf',
     'Normal sinus rhythm. Heart rate 72 bpm. PR interval 160ms. QRS duration 92ms. No acute ST-T changes or ischemia noted.', 1),
    (1, 1, 'HbA1c & Fasting Glucose Profile', 'blood_test', 'uploads/sample_blood_test.pdf',
     'HbA1c: 6.8% (Good control). Fasting Blood Glucose: 110 mg/dL. Postprandial: 142 mg/dL. Serum Creatinine: 0.9 mg/dL.', 1),
    (1, 3, 'Bilateral Knee Standing X-Ray', 'radiology', 'uploads/sample_knee_xray.pdf',
     'Mild-to-moderate medial compartment joint space narrowing in right knee. Marginal osteophytes present. Grade II Kellgren-Lawrence.', 1),
    (1, 4, 'Apollo Cardiology Prescription Summary', 'prescription', 'uploads/sample_prescription.pdf',
     'Rx: Tab Telmisartan 40mg (1-0-0), Tab Metformin 500mg (1-0-1), Tab Atorvastatin 10mg (0-0-1). Regular 30 min gentle walk.', 1);
    """)

    # 10. Preparation Checklists
    cursor.execute("""
    INSERT INTO preparation_checklists (
        appointment_id, item_title, is_mandatory, is_completed, document_id, notes
    ) VALUES
    (1, 'Previous ECG Report (within 3 months)', 1, 1, 1, 'Verified by Priya on 12th Nov'),
    (1, 'Fasting Lipid & Glucose Report', 1, 1, 2, 'HbA1c 6.8% attached'),
    (1, 'Active Prescriptions List', 1, 1, 4, 'Carried digitally in app'),
    (1, 'Home Blood Pressure Log Sheet', 0, 0, NULL, 'Elderly advised to record last 3 morning readings'),
    (2, 'Daily Routine & Sleep Quality Notes', 1, 0, NULL, 'Caretaker to prepare 1-page summary'),
    (2, 'Neurology History & Previous Scans', 1, 0, NULL, 'Locate 2024 MRI scan CD');
    """)

    # 11. Notifications
    cursor.execute("""
    INSERT INTO notifications (
        elderly_id, recipient_role, category, title, message, priority, is_read, is_acknowledged, simulated_channel
    ) VALUES
    (1, 'elderly', 'appointment', 'Cardiologist Visit Today at 10:00 AM',
     'Good morning Lakshmi ji! You have an appointment with Dr. Ramesh Sharma at Apollo Hospitals today at 10:00 AM. Priya is accompanying you.', 'urgent', 0, 0, 'IN_APP'),
    (1, 'caretaker', 'medication', 'Refill Required: Atorvastatin 10 mg',
     'Notice: Atorvastatin has only 4 tablets remaining (~4 days of supply). Please re-order soon.', 'high', 0, 0, 'IN_APP'),
    (1, 'caretaker', 'escalation', 'Unacknowledged Reminder Alert',
     'Yesterday evening Metformin (20:30) was not confirmed in app. Friendly check-in recommended.', 'high', 0, 1, 'SMS_SIMULATED'),
    (1, 'elderly', 'travel', 'Suggested Departure Alert',
     'Leave by 09:05 AM to arrive at Apollo Hospitals comfortably by 09:50 AM (estimated travel 25 mins).', 'normal', 0, 0, 'IN_APP');
    """)

    # 12. Caregiver Tasks
    cursor.execute("""
    INSERT INTO caregiver_tasks (
        elderly_id, assigned_to_caretaker_id, title, due_date, priority, status, notes
    ) VALUES
    (1, 1, 'Accompany Mother to Apollo Cardiology Consultation', ?, 'High', 'in_progress', 'Car ready, documents packed in blue folder.'),
    (1, 1, 'Order 30-day Refill for Atorvastatin 10mg', ?, 'Urgent', 'pending', 'Use Apollo 24/7 or Netmeds with Dr. Sharma prescription.'),
    (1, 2, 'Pick up Knee Brace & Physiotherapy Gel', ?, 'Medium', 'pending', 'From MedPlus Pharmacy near Bellandur junction.');
    """, (today_str, tomorrow_str, three_days_str))

    # 13. Emergency Contacts
    cursor.execute("""
    INSERT INTO emergency_contacts (
        elderly_id, name, relationship, phone, priority, is_active
    ) VALUES
    (1, 'Priya Sharma (Daughter)', 'Primary Caretaker', '+91 98450 44556', 1, 1),
    (1, 'Rahul Sharma (Son)', 'Secondary Caretaker', '+91 98450 77889', 2, 1),
    (1, 'Dr. Ramesh Sharma', 'Consultant Cardiologist', '+91 98450 99001', 3, 1),
    (1, 'Apollo Emergency Response Line', 'Hospital Hotline', '1066', 4, 1);
    """)

    # 14. Emergency Events Log (Historical test event)
    cursor.execute("""
    INSERT INTO emergency_events (
        elderly_id, triggered_at, triggered_by, status, location_lat, location_lng,
        location_address, contacts_alerted_summary, resolution_notes
    ) VALUES
    (1, datetime('now', '-25 days'), 'Priya Sharma (Test)', 'resolved', 12.9345, 77.6892,
     'Flat 302, Green Glen Gardens, Bellandur, Bangalore',
     'SMS & In-App broadcast sent to Priya Sharma, Rahul Sharma and Apollo Hotline.',
     'Drill test completed successfully. Response simulated in 2 minutes.');
    """)

    # 15. Timeline Events
    cursor.execute("""
    INSERT INTO timeline_events (
        elderly_id, event_type, title, description, event_date, author_or_doctor, report_score
    ) VALUES
    (1, 'visit', 'Quarterly Cardiology Consultation', 'Regular checkup with Dr. Ramesh Sharma. Blood pressure was well-controlled at 122/78 mmHg. Heart sound normal S1/S2.', ?, 'Dr. Ramesh Sharma', 92.0),
    (1, 'lab_report', 'Comprehensive Metabolic & Lipid Panel', 'Metropolis Labs: Fasting blood sugar 110 mg/dL, HbA1c 6.8%, Total Cholesterol 180 mg/dL.', ?, 'Metropolis Pathology', 89.0),
    (1, 'medication', 'Atorvastatin Stock Monitored', 'Stock dropped to 4 units. System flagged automated reminder for caretaker.', ?, 'Catalyst Care Engine', NULL),
    (1, 'observation', 'Caretaker Morning Wellness Note', 'Lakshmi ji slept 7 hours peacefully. Completed 20-minute morning garden walk without knee pain.', ?, 'Priya Sharma', 95.0),
    (1, 'visit', 'Orthopedic Review & Knee Assessment', 'Dr. Vikram Reddy evaluated right knee osteo-joint. Advised hot fomentation and gentle quad strengthening.', ?, 'Dr. Vikram Reddy', 84.0);
    """, (today_str, yesterday_str, today_str, today_str, past_10d_str))

    # 16. Care Journal
    cursor.execute("""
    INSERT INTO care_journal (
        elderly_id, author_name, author_role, entry_date, entry_text, vitals_summary, mood
    ) VALUES
    (1, 'Priya Sharma', 'Caretaker', ?, 'Mother was in cheerful spirits today. Enjoyed idli and coconut chutney for breakfast. Reminded her about water intake throughout the day.', 'BP: 122/78, Sugar: 110', 'Cheerful'),
    (1, 'Rahul Sharma', 'Caretaker', ?, 'Visited mother in the evening. We walked around the apartment clubhouse. Her gait is steady, no complaints of dizziness.', 'BP: 124/80, SpO2: 98%', 'Relaxed'),
    (1, 'Smt. Lakshmi Devi', 'Elderly', ?, 'I felt energetic today. Listened to morning devotional songs and took all my morning tablets on time.', 'Self check: Feeling well', 'Happy');
    """, (today_str, yesterday_str, (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')))

    # 17. Follow-up Appointments
    cursor.execute("""
    INSERT INTO followup_appointments (
        elderly_id, previous_appointment_id, recommended_date, specialty, doctor_name, notes, is_booked
    ) VALUES
    (1, 4, ?, 'Cardiology', 'Dr. Ramesh Sharma', 'Repeat serum creatinine and lipid profile prior to visit.', 1),
    (1, 3, ?, 'Orthopedics', 'Dr. Vikram Reddy', 'Review quad strength after 4 weeks of physical therapy.', 0);
    """, ((date.today() + timedelta(days=60)).strftime('%Y-%m-%d'), (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')))

    # 18. Health Reports & Vitals (Historical sequence for the requested overall health graph!)
    # Computes composite health score: weighted evaluation of BP, Glucose, SpO2, Heart Rate, Cholesterol
    vitals_data = [
        (1, (date.today() - timedelta(days=150)).strftime('%Y-%m-%d'), 'Post-Diwali Health Checkup', 142, 92, 148, 96, 78, 220, 68.5, 'Slightly elevated BP and fasting glucose. Commenced Telmisartan.', 'Mild hypertension and borderline sugar.'),
        (1, (date.today() - timedelta(days=120)).strftime('%Y-%m-%d'), 'Monthly Metabolic Routine', 138, 88, 136, 97, 76, 210, 73.0, 'Gradual improvement after dosage initiation. Diet modification helping.', 'Progressing well, continue medication.'),
        (1, (date.today() - timedelta(days=90)).strftime('%Y-%m-%d'), 'Quarterly Cardiology Panel', 132, 85, 128, 97, 74, 198, 79.2, 'BP significantly stabilized. Cholesterol within borderline target.', 'Cholesterol < 200 achieved. Heart sounds clear.'),
        (1, (date.today() - timedelta(days=60)).strftime('%Y-%m-%d'), 'Mid-Quarter Vitals Screening', 128, 82, 120, 98, 72, 190, 85.0, 'Excellent adherence to morning medication schedule.', 'Vitals approaching ideal target range.'),
        (1, (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'), 'Comprehensive Geriatric Review', 124, 80, 115, 98, 70, 185, 89.4, 'Both systolic and diastolic readings within normal range.', 'Steady rhythm, optimal oxygen saturation.'),
        (1, today_str, 'Latest Pre-Consultation Vitals', 122, 78, 110, 99, 72, 180, 92.5, 'Optimal blood pressure, fasting glucose 110 mg/dL, 99% SpO2.', 'Superb health trajectory. Routine maintained seamlessly.')
    ]

    for record in vitals_data:
        cursor.execute("""
        INSERT INTO health_reports (
            elderly_id, report_date, report_name, systolic_bp, diastolic_bp, blood_glucose_mg_dl,
            spo2_percent, heart_rate_bpm, cholesterol_mg_dl, composite_health_score, doctor_notes, extracted_summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, record)

    conn.commit()
    conn.close()
    print("Database initialization and seed complete!")

if __name__ == "__main__":
    seed_database()
