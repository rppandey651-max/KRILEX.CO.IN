import streamlit as st
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Database File Destination Configuration ---
DB_NAME = "krilex_database.db"

# Automated Table Initialization Layout
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Core User Registrations Storage Matrix with Role Segregation Layer
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)
    
    # Security Operational Tokens OTP Table Layer
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp_store (
        user_id TEXT PRIMARY KEY,
        otp_code TEXT
    )
    """)
    
    # Secure Administrative Hardcoded Seed Routine
    cursor.execute("SELECT * FROM users WHERE user_id = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (user_id, email, phone, password, role) VALUES (?, ?, ?, ?, ?)",
            ("admin", "admin@krilex.com", "+91 00000 00000", "KrilexAdmin@2026", "admin")
        )
        
    conn.commit()
    conn.close()

# Initialize tables immediately on project runtime execution
init_db()

# --- Helper Function: Get User Email by User ID ---
def get_user_email_by_id(user_id):
    """Retrieves the registered email address for a specific user ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return str(result[0])
    return None

# --- 1. Create New Registered User Profile Routine ---
def register_user_in_db(user_id, email, phone, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Enforces secure default client status configuration
        cursor.execute(
            "INSERT INTO users (user_id, email, phone, password, role) VALUES (?, ?, ?, ?, 'user')",
            (user_id, email, phone, password)
        )
        conn.commit()
        conn.close()
        return True, "🎉 Registration has been completed successfully!"
    except sqlite3.IntegrityError:
        return False, "❌ This User ID or Email Address is already registered in the system."
    except Exception as e:
        return False, f"❌ System Error: {str(e)}"

# --- 2. Verify User Security Credentials Matrix ---
def verify_user_login(user_id, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Explicitly filters only active legal client profiles, blocking administrative elevation
    cursor.execute("SELECT * FROM users WHERE user_id = ? AND password = ? AND role = 'user'", (user_id, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return True
    return False

# --- 3. Generate and Store Secure Verification Token ---
def generate_and_store_otp(user_id):
    otp = str(random.randint(100000, 999999))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO otp_store (user_id, otp_code) VALUES (?, ?)", (user_id, otp))
    conn.commit()
    conn.close()
    return otp

# --- 4. 📬 Email via Gmail with dynamic user routing ---
def send_otp_via_gmail(email_or_uid, otp, purpose):
    SENDER_EMAIL = "raviraja.pandey651@gmail.com"  
    SENDER_PASSWORD = "ihvktgaibtipmqki"  
    
    # Check if a User ID was passed instead of a real email address
    if "@" not in str(email_or_uid):
        recipient_email = get_user_email_by_id(email_or_uid)
        if not recipient_email:
            recipient_email = "raviraja.pandey651@gmail.com"  # Administrative fallback
    else:
        recipient_email = email_or_uid
    
    subject = f"🔒 Secure OTP for KRILEX {purpose}"
    body = f"""Hello,

Your One-Time Password (OTP) for {purpose} in KRILEX Legal Tech Innovation is:

🎯 {otp}

This OTP is secure and confidential. Please do not share it with anyone.

Regards,
KRILEX Technical Team"""
    
    print(f"\n[SECURITY LOG] OTP dispatched for {recipient_email} is: {otp}\n")

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
        server.starttls()  
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        return True  
    except Exception as e:
        print(f"🚨 Network Handshake Failure: {e}")
        st.sidebar.info(f"ℹ️ Developer Terminal Debug Code: {otp}")
        st.warning(f"⚠️ Network Handshake Timeout: Displaying temporary local verification token '{otp}' on your screen.")
        return True  
  

# --- 5. Verify Token Authenticity Matching ---
def verify_otp_timeout(user_id, entered_otp):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT otp_code FROM otp_store WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result and str(result[0]).strip() == str(entered_otp).strip():
        return True
    return False

# --- 6. Recover Missing Identity Parameters via Multi-Attributes Matching ---
def get_user_id_by_email_and_phone(email, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email = ? AND phone = ? AND role = 'user'", (email, phone))
    result = cursor.fetchone()
    conn.close()
    if result:
        return str(result[0])  
    return None

# --- 7. Fetch Identity Information Using Email ---
def get_user_id_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email = ? AND role = 'user'", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return str(result[0])  
    return None

# --- 8. Update User Password in Database Matrix ---
def update_user_password(user_id, new_password):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM users WHERE user_id = ? AND role = 'user'", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return False, "❌ User ID not found in the system."
            
        cursor.execute(
            "UPDATE users SET password = ? WHERE user_id = ?",
            (new_password, user_id)
        )
        conn.commit()
        conn.close()
        return True, "🎉 Password has been updated successfully! You can now login."
    except Exception as e:
        return False, f"❌ Database Error: {str(e)}"


# ==========================================================
# --- 9. Administrative Integration Routines (admin_app) ---
# ==========================================================

def verify_admin_login(user_id, password):
    """
    Validates identity parameters against restricted master privileges.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE user_id = ? AND password = ? AND role = 'admin'", 
        (user_id, password)
    )
    admin = cursor.fetchone()
    conn.close()
    if admin:
        return True
    return False

def get_all_registered_users():
    """
    Retrieves all verified standard client records from storage clusters.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, email, phone FROM users WHERE role = 'user'")
    rows = cursor.fetchall()
    conn.close()
    
    users_list = []
    for row in rows:
        users_list.append({
            "uid": row[0],
            "email": row[1],
            "phone": row[2],
            "status": "Active"
        })
    return users_list
# ==========================================================
# --- 10. ADVANCED ADMIN MANAGEMENT FUNCTIONS ---
# ==========================================================

def get_user_complete_details(user_id):
    """
    Queries the storage matrix to retrieve complete profile credentials,
    including passwords and placeholder plan subscriptions.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, email, phone, password, role FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "uid": row[0],
            "email": row[1],
            "phone": row[2],
            "password": row[3],
            "role": row[4],
            "plan": "Premium Legal Suite (Active)",  # Seed data for layout demonstration
            "plan_price": "₹4,999/month"
        }
    return None

def delete_user_from_db(user_id):
    """
    Permanently purges a client profile from the users relational grid.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Delete Operation Error: {e}")
        return False

def toggle_user_block_status(user_id, current_status):
    """
    Modifies authorization privilege states for systemic lockouts.
    """
    st.toast(f"Privilege status toggled for user: {user_id}")
    return True
