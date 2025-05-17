import sqlite3

conn = sqlite3.connect("doctors.db")
cursor = conn.cursor()

# Create doctors table
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    clinic TEXT NOT NULL,
    fee TEXT NOT NULL,
    slots TEXT NOT NULL,
    specialization TEXT NOT NULL,
    location TEXT NOT NULL
)
""")

# Insert sample data (run once)
doctors_data = [
    ("Dr. Ravi", "City Clinic", "₹500", "10:00 AM,2:00 PM", "General Physician", "Chennai"),
    ("Dr. Anjali", "Health Plus", "₹600", "11:30 AM,4:00 PM", "General Physician", "Chennai"),
    ("Dr. Kumar", "Neuro Center", "₹1200", "9:00 AM,3:00 PM", "Neurologist", "Chennai"),
    ("Dr. Priya", "Brain Care", "₹1500", "1:00 PM,5:30 PM", "Neurologist", "Chennai"),
    ("Dr. Meena", "ENT Clinic", "₹800", "10:30 AM,3:30 PM", "Ent Specialist", "Chennai"),
]

cursor.executemany("""
INSERT INTO doctors (name, clinic, fee, slots, specialization, location)
VALUES (?, ?, ?, ?, ?, ?)
""", doctors_data)

conn.commit()
conn.close()
print("Database setup complete!")
