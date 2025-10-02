import psycopg2
import os

# Load DB URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    name TEXT PRIMARY KEY,
    phone TEXT,
    email TEXT
);
""")
conn.commit()


# --- Functions ---
def add_contact(name, phone, email):
    try:
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)", 
                       (name, phone, email))
        conn.commit()
        print("✅ Contact added successfully!")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("⚠️ Contact already exists!")

def search_contact(name):
    cursor.execute("SELECT * FROM contacts WHERE name=%s", (name,))
    result = cursor.fetchone()
    if result:
        print(f"Found: Name={result[0]}, Phone={result[1]}, Email={result[2]}")
    else:
        print("❌ Contact not found.")

def update_contact(name, phone, email):
    cursor.execute("UPDATE contacts SET phone=%s, email=%s WHERE name=%s", (phone, email, name))
    conn.commit()

def search_contacts(query):
    cursor.execute(
        "SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s OR email ILIKE %s ORDER BY name",
        (f"%{query}%", f"%{query}%", f"%{query}%")
    )
    return cursor.fetchall()

def delete_contact(name):
    cursor.execute("DELETE FROM contacts WHERE name=%s", (name,))
    conn.commit()
    print("🗑️ Contact deleted (if it existed).")

def display_contacts():
    cursor.execute("SELECT * FROM contacts ORDER BY name")
    results = cursor.fetchall()
    for row in results:
        print(f"Name: {row[0]}, Phone: {row[1]}, Email: {row[2]}")

def get_all_contacts():
    cursor.execute("SELECT * FROM contacts ORDER BY name")
    return cursor.fetchall()
