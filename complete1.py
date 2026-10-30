import streamlit as st
import db2 as db  # Reads directly from your db2.py file
import time
import os
import base64
import random

# ====================================================
# PART 1: GLOBAL SETUP, SESSION STATES & STYLESHEET
# ====================================================

# Page Configuration Setup - Set to 'centered' view layout model matching 1.py structure
st.set_page_config(page_title="KRILEX Legal Tech Innovation", layout="centered")

# Exact Local Desktop Asset Destination Path Configuration
BASE_PATH = r"C:\Users\hp\Desktop\photo_6244332980792922580_y"

def load_desktop_logo(base_path):
    extensions = [".jpg", ".jpeg", ".png", ".JPG", ".PNG"]
    for ext in extensions:
        full_path = base_path + ext
        if os.path.exists(full_path):
            try:
                with open(full_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    mime_type = "png" if ext.lower() == ".png" else "jpeg"
                    return f"data:image/{mime_type};base64,{encoded_string}"
            except Exception:
                return ""
    return ""

LOGO_BASE64 = load_desktop_logo(BASE_PATH)

# Global Session State System Tracking Initializations
if "page" not in st.session_state: st.session_state.page = "main"
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "login_otp_dispatched" not in st.session_state: st.session_state.login_otp_dispatched = False
if "forgot_otp_dispatched" not in st.session_state: st.session_state.forgot_otp_dispatched = False
if "forgot_otp_verified" not in st.session_state: st.session_state.forgot_otp_verified = False
if "forgot_uid_dispatched" not in st.session_state: st.session_state.forgot_uid_dispatched = False
if "forgot_uid_verified" not in st.session_state: st.session_state.forgot_uid_verified = False
if "reg_success_msg" not in st.session_state: st.session_state.reg_success_msg = ""
if "generated_otp" not in st.session_state: st.session_state.generated_otp = ""
if "target_email" not in st.session_state: st.session_state.target_email = ""
if "target_phone" not in st.session_state: st.session_state.target_phone = ""
if "target_uid" not in st.session_state: st.session_state.target_uid = ""
if "temp_reg_data" not in st.session_state: st.session_state.temp_reg_data = {}
if "start_time" not in st.session_state: st.session_state.start_time = time.time()
if "otp_timestamp" not in st.session_state: st.session_state.otp_timestamp = None

# Dashboard Active Framework Sub-Navigation Session States
if "selected_court" not in st.session_state: st.session_state.selected_court = "--- Choose Jurisdiction ---"
if "active_app_tile" not in st.session_state: st.session_state.active_app_tile = None
if "p_count" not in st.session_state: st.session_state.p_count = 1
if "r_count" not in st.session_state: st.session_state.r_count = 1
if "footer_page" not in st.session_state: st.session_state.footer_page = None

elapsed_time = time.time() - st.session_state.start_time
watermark_css = ""
if LOGO_BASE64 and elapsed_time >= 2.5:
    watermark_css = f"""
    .stApp {{
        background-image: url("{LOGO_BASE64}") !important;
        background-repeat: no-repeat !important;
        background-position: center 65% !important;
        background-size: 35% !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stAppViewContainer"] {{ background-color: rgba(255, 255, 255, 0.96) !important; }}
    """

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: #ffffff; }}
    {watermark_css}
    .block-container {{ padding-top: 2rem; }}
    .footer-text {{ font-size: 14px; color: #555; font-weight: 500; }}
    .center-logo-container {{ display: flex; justify-content: center; align-items: center; margin-bottom: 20px; }}
    .workstation-container {{
        background: #ffffff; padding: 25px; border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-top: 5px solid #8B0000;
        margin-bottom: 25px; margin-top: 15px;
    }}
    .legal-tile {{
        padding: 20px; border-radius: 8px; color: #222222; font-weight: bold;
        font-size: 15px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.05); min-height: 65px;
        background-color: rgba(255, 255, 255, 0.9);
    }}
    .tile-green {{ background-color: rgba(232, 245, 233, 0.95) !important; border-left: 5px solid #2E7D32 !important; }}
    .tile-red {{ background-color: rgba(255, 235, 238, 0.95) !important; border-left: 5px solid #C62828 !important; }}
    .tile-blue {{ background-color: rgba(227, 242, 253, 0.95) !important; border-left: 5px solid #1565C0 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

def get_all_indian_courts():
    return [
        "--- Choose Jurisdiction ---",
        "Supreme Court of India (New Delhi)",
        "Allahabad High Court (Principal Bench)",
        "Allahabad High Court (Lucknow Bench)",
        "Andhra Pradesh High Court",
        "Bombay High Court",
        "Calcutta High Court",
        "Delhi High Court",
        "Gujarat High Court",
        "Karnataka High Court",
        "Madras High Court",
        "Patna High Court",
        "Punjab and Haryana High Court",
        "Rajasthan High Court"
    ]

# ====================================================
# PART 2: SPLASH SCREEN ENGINE & SECURE AUTH INTERFACE
# ====================================================

if elapsed_time < 2.5:
    st.markdown("""
        <style>
        [data-testid="stHeader"], [data-testid="stSidebar"], .stAppHeader { display: none !important; }
        .full-page-splash {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #ffffff; display: flex; justify-content: center; align-items: center; z-index: 999999;
        }
        .big-splash-logo {
            width: 850px; max-width: 95vw; height: auto;
            transform: perspective(1200px) rotateY(15deg);
            animation: glow3DAnimation 2s infinite alternate ease-in-out;
        }
        @keyframes glow3DAnimation {
            0% { transform: perspective(1200px) rotateY(15deg) scale(0.96); filter: drop-shadow(0 0 25px rgba(0, 150, 255, 0.3)); }
            100% { transform: perspective(1200px) rotateY(-15deg) scale(1.04); filter: drop-shadow(0 0 10px rgba(0, 200, 255, 0.6)); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    if LOGO_BASE64:
        st.markdown(f'<div class="full-page-splash"><img src="{LOGO_BASE64}" class="big-splash-logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="full-page-splash"><h1 style="color:#0096ff; font-family:sans-serif; font-size:4rem;">KRILEX Legal Tech</h1></div>', unsafe_allow_html=True)
    
    time.sleep(0.1)
    st.rerun()
    
elif not st.session_state.logged_in:
    
    if st.session_state.page == "main":
        if LOGO_BASE64: 
            st.markdown(f'<div class="center-logo-container"><img src="{LOGO_BASE64}" width="160"></div>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>KRILEX Legal Tech Innovation</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #334155;'>Welcome to the Digital Legal Petition Generator.</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        landing_col1, landing_col2 = st.columns(2)
        with landing_col1:
            if st.button("🔐 Login Panel Gateway", type="primary", use_container_width=True, key="landing_login_trigger"):
                st.session_state.page = "login"
                st.session_state.login_otp_dispatched = False
                st.session_state.otp_timestamp = None  # Purana time saaf kiya
                st.rerun()
        with landing_col2:
            if st.button("📝 Register New Account", use_container_width=True, key="landing_register_trigger"):
                st.session_state.page = "register"
                st.session_state.otp_timestamp = None  # Purana time saaf kiya
                st.rerun()
        # --- PROMOTION WORKFLOW FEATURE: INSTANT DEMO ACCOUNT BYPASS ---
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Explore Demo Workspace (Instant Access)", type="secondary", use_container_width=True, key="landing_demo_bypass_trigger"):
            st.session_state.logged_in = True
            st.session_state.username = "DemoGuest"
            st.session_state.page = "dashboard"
            st.toast("Authenticated via Instant Demo Clearance! 🎉")
            st.rerun()

    elif st.session_state.page == "login":
        if LOGO_BASE64: 
            st.markdown(f'<div class="center-logo-container"><img src="{LOGO_BASE64}" width="140"></div>', unsafe_allow_html=True)
        st.markdown("### 🔐 User Login")
        
        if not st.session_state.login_otp_dispatched:
            with st.form("login_form_container", clear_on_submit=False):
                uid = st.text_input("Login ID", key="login_uid_field").strip()
                pwd = st.text_input("Password", type="password", key="login_pwd_field")
                submit_login = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if submit_login:
                    if uid == "" or pwd == "":
                        st.warning("⚠️ All fields are required.")
                    else:
                        if db.verify_user_login(uid, pwd):
                            otp_token = db.generate_and_store_otp(uid)
                            st.session_state.generated_otp = otp_token
                            st.session_state.target_uid = uid
                            st.session_state.target_email = db.get_user_email_by_id(uid)
                            
                            if db.send_otp_via_gmail(st.session_state.target_email, st.session_state.generated_otp, "Login Verification"):
                                st.session_state.login_otp_dispatched = True
                                st.session_state.otp_timestamp = time.time()  # Timer yahan shuru hoga
                                st.success("📧 Real OTP code successfully dispatched to your email address!")
                                st.rerun()
                            else:
                                st.error("❌ Live Mail Handshake Failure: Connection blocked by external server constraints.")
                        else:
                            st.error("❌ Login failed! Incorrect User ID or Password.")
            if st.button("Cancel", use_container_width=True, key="login_cancel_global_action"):
                st.session_state.page = "main"
                st.rerun()
                
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Forgot Password?", key="forgot_password_nav_link", use_container_width=True):
                    st.session_state.page = "forgot_password"
                    st.session_state.forgot_otp_dispatched = False
                    st.session_state.forgot_otp_verified = False
                    st.session_state.otp_timestamp = None
                    st.rerun()
            with c2:
                if st.button("Forgot User ID?", key="forgot_uid_nav_link", use_container_width=True):
                    st.session_state.page = "forgot_userid"
                    st.session_state.forgot_uid_dispatched = False
                    st.session_state.forgot_uid_verified = False
                    st.session_state.otp_timestamp = None
                    st.rerun()
            with c3:
                if st.button("New User? Register", key="register_nav_link", use_container_width=True):
                    st.session_state.page = "register"
                    st.session_state.otp_timestamp = None
                    st.rerun()
        else:
            st.markdown("#### 🔒 Enter 2-Step Verification Code")
            
            @st.fragment(run_every=1.0)
            def render_otp_countdown_view():
                if st.session_state.otp_timestamp is not None:
                    time_passed = time.time() - st.session_state.otp_timestamp
                    seconds_left = max(0, int(90 - time_passed))
                else:
                    seconds_left = 0
                
                with st.form("login_otp_verification_form"):
                    otp_entered = st.text_input("Enter 6-Digit OTP Code Sent to Email", max_chars=6).strip()
                    submit_otp = st.form_submit_button("Verify & Login", type="primary", use_container_width=True)
                    
                    if submit_otp:
                        # --- PROMOTION WORKFLOW FEATURE: MASTER OTP BYPASS CODE ---
                        if otp_entered == "999999":
                            st.session_state.logged_in = True
                            st.session_state.username = st.session_state.target_uid if st.session_state.target_uid else "DemoUser"
                            st.session_state.page = "dashboard"
                            st.toast("Authenticated via Demo Master Access Token! 🚀")
                            st.rerun()

                        if seconds_left == 0:
                            st.error("❌ This OTP has expired! Please click the 'Resend OTP' button below.")
                        elif str(st.session_state.generated_otp).strip() == str(otp_entered).strip():
                            st.session_state.logged_in = True
                            st.session_state.username = st.session_state.target_uid
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            st.error("❌ Incorrect OTP entered. Please try again.")

                time_layout_col, action_layout_col = st.columns(2)
                with time_layout_col:
                    if seconds_left > 0:
                        st.info(f"⏳ Time Remaining: **{seconds_left}s**")
                    else:
                        st.error("🚨 OTP Expired")
                        
                with action_layout_col:
                    if seconds_left == 0:
                        if st.button("🔄 Resend OTP Code", type="secondary", use_container_width=True, key="resend_action_trigger"):
                            otp_token = db.generate_and_store_otp(st.session_state.target_uid)
                            st.session_state.generated_otp = otp_token
                            
                            if db.send_otp_via_gmail(st.session_state.target_email, st.session_state.generated_otp, "Login Verification"):
                                st.session_state.otp_timestamp = time.time()
                                st.success("📧 A fresh verification token has been dispatched!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("❌ Network error: Could not complete dispatch.")
                    else:
                        st.button(f"🔒 Resend Locked", disabled=True, use_container_width=True, key="resend_action_disabled")

            render_otp_countdown_view()

            if st.button("Back to Login", use_container_width=True, key="otp_back_to_login_form"):
                st.session_state.login_otp_dispatched = False
                st.session_state.otp_timestamp = None
                st.rerun()

    elif st.session_state.page == "register":
        if LOGO_BASE64: 
            st.markdown(f'<div class="center-logo-container"><img src="{LOGO_BASE64}" width="140"></div>', unsafe_allow_html=True)
        st.markdown("### 📝 New User Registration")
        if st.session_state.reg_success_msg:
            st.success(st.session_state.reg_success_msg)
            st.balloons()
            if st.button("Go to Login", type="primary", use_container_width=True, key="reg_success_redirect_btn"):
                st.session_state.reg_success_msg = ""
                st.session_state.page = "login"
                st.rerun()
        else:
            with st.form("reg_step1_form"):
                new_uid = st.text_input("Choose Unique Login ID").strip()
                new_email = st.text_input("Email Address").strip()
                new_phone = st.text_input("Phone Number").strip()
                submit_step1 = st.form_submit_button("Send Verification OTP", type="primary", use_container_width=True)
                if submit_step1:
                    if not new_uid or not new_email or not new_phone:
                        st.warning("⚠️ All fields are mandatory.")
                    else:
                        st.session_state.temp_reg_data = {"uid": new_uid, "email": new_email, "phone": new_phone}
                        st.session_state.generated_otp = str(random.randint(100000, 999999))
                        if db.send_otp_via_gmail(new_email, st.session_state.generated_otp, "Registration Framework Setup"):
                            st.session_state.page = "register_otp"
                            st.session_state.otp_timestamp = time.time()
                            st.rerun()
            if st.button("Back to Main Menu", use_container_width=True, key="reg_form_cancel_btn"):
                st.session_state.page = "main"
                st.rerun()

    elif st.session_state.page == "register_otp":
        st.markdown("### 🔒 Verify Your Email Address")
        
        @st.fragment(run_every=1.0)
        def render_registration_countdown_view():
            if st.session_state.otp_timestamp is not None:
                time_passed = time.time() - st.session_state.otp_timestamp
                seconds_left = max(0, int(90 - time_passed))

            else:
                seconds_left = 0
                
            with st.form("reg_otp_verification_form"):
                otp_entered = st.text_input("Enter 6-Digit Registration OTP", max_chars=6).strip()
                verify_reg_btn = st.form_submit_button("Verify OTP Code", type="primary", use_container_width=True)
                if verify_reg_btn:
                    if seconds_left == 0:
                        st.error("❌ Registration token expired. Please use the resend button.")
                    elif otp_entered == st.session_state.generated_otp:
                        st.session_state.page = "register_password"
                        st.rerun()
                    else:
                        st.error("❌ Incorrect OTP entered.")
                        
            time_layout_col, action_layout_col = st.columns(2)
            with time_layout_col:
                if seconds_left > 0:
                    st.info(f"⏳ Time Remaining: **{seconds_left}s**")
                else:
                    st.error("🚨 Registration Token Expired")
            with action_layout_col:
                if seconds_left == 0:
                    if st.button("🔄 Resend OTP Code", type="secondary", use_container_width=True, key="resend_reg_trigger"):
                        st.session_state.generated_otp = str(random.randint(100000, 999999))
                        if db.send_otp_via_gmail(st.session_state.temp_reg_data["email"], st.session_state.generated_otp, "Registration Framework Setup"):
                            st.session_state.otp_timestamp = time.time()
                            st.success("📧 Fresh registration token dispatched successfully!")
                            time.sleep(1)
                            st.rerun()
                else:
                    st.button(f"🔒 Resend Locked", disabled=True, use_container_width=True, key="resend_reg_disabled")
                    
        render_registration_countdown_view()
        
        if st.button("Back", use_container_width=True, key="reg_otp_back_nav"):
            st.session_state.page = "register"
            st.rerun()

    elif st.session_state.page == "register_password":
        st.markdown("### 🔒 Configure Account Password")
        with st.form("reg_password_setup_form"):
            new_pwd = st.text_input("Password", type="password")
            confirm_pwd = st.text_input("Confirm Password", type="password")
            submit_final_reg = st.form_submit_button("Create Account & Finish", type="primary", use_container_width=True)
            if submit_final_reg:
                if new_pwd != confirm_pwd:
                    st.error("❌ Passwords do not match.")
                else:
                    r_data = st.session_state.temp_reg_data
                    success_flag, feedback_msg = db.register_user_in_db(r_data["uid"], r_data["email"], r_data["phone"], new_pwd)
                    if success_flag:
                        st.session_state.reg_success_msg = feedback_msg
                        st.session_state.page = "register"
                        st.rerun()
                    else:
                        st.error(feedback_msg)
    elif st.session_state.page == "forgot_password":
        st.markdown("### 🔑 Recover Password (OTP Verification)")
        if not st.session_state.forgot_otp_dispatched:
            with st.form("forgot_pwd_request"):
                uid_input = st.text_input("Enter your Login ID").strip()
                email_input = st.text_input("Enter your Registered Email").strip()
                send_btn = st.form_submit_button("Send Recovery OTP", type="primary", use_container_width=True)
                
                if send_btn:
                    if uid_input and email_input:
                        st.session_state.generated_otp = str(random.randint(100000, 999999))
                        st.session_state.target_email = email_input
                        st.session_state.target_uid = uid_input
                        if db.send_otp_via_gmail(email_input, st.session_state.generated_otp, "Password Recovery Mode"):
                            st.session_state.forgot_otp_dispatched = True
                            st.session_state.otp_timestamp = time.time()
                            st.rerun()
                    else:
                        st.warning("⚠️ Please fill all details.")
        elif not st.session_state.forgot_otp_verified:
            @st.fragment(run_every=1.0)
            def render_forgot_countdown_view():
                if st.session_state.otp_timestamp:
                    time_passed = time.time() - st.session_state.otp_timestamp
                    seconds_left = max(0, int(90 - time_passed))
                else:
                    seconds_left = 0
                    
                with st.form("verify_pwd_otp_form"):
                    otp_entered = st.text_input("Enter 6-Digit OTP", max_chars=6).strip()
                    verify_btn = st.form_submit_button("Verify OTP", type="primary", use_container_width=True)
                    if verify_btn:
                        if seconds_left == 0:
                            st.error("❌ Recovery token expired. Please select the recovery button below.")
                        elif otp_entered == st.session_state.generated_otp:
                            st.session_state.forgot_otp_verified = True
                            st.success("✅ OTP Verified Successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid OTP.")
                            
                time_layout_col, action_layout_col = st.columns(2)
                with time_layout_col:
                    if seconds_left > 0:
                        st.info(f"⏳ Time Remaining: **{seconds_left}s**")
                    else:
                        st.error("🚨 Token Expired")
                with action_layout_col:
                    if seconds_left == 0:
                        if st.button("🔄 Resend Recovery OTP", type="secondary", use_container_width=True, key="resend_forgot_trigger"):
                            st.session_state.generated_otp = str(random.randint(100000, 999999))
                            if db.send_otp_via_gmail(st.session_state.target_email, st.session_state.generated_otp, "Password Recovery Mode"):
                                st.session_state.otp_timestamp = time.time()
                                st.success("📧 Recovery verification token dispatched successfully!")
                                time.sleep(1)
                                st.rerun()
                    else:
                        st.button(f"🔒 Resend Locked", disabled=True, use_container_width=True, key="resend_forgot_disabled")
            
            render_forgot_countdown_view()

        else:
            with st.form("reset_pwd_form"):
                new_p = st.text_input("New Password", type="password")
                conf_p = st.text_input("Confirm New Password", type="password")
                update_btn = st.form_submit_button("Update Password", type="primary", use_container_width=True)
                if update_btn:
                    if new_p == conf_p and new_p != "":
                        success, message = db.update_user_password(st.session_state.target_uid, new_p)
                        if success:
                            st.success(message)
                            time.sleep(1.5)
                            st.session_state.page = "login"
                            st.session_state.login_otp_dispatched = False
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("❌ Passwords do not match or are empty.")

        if st.button("Back to Login", use_container_width=True, key="forgot_pwd_back_to_login"): 
            st.session_state.page = "login"
            st.session_state.login_otp_dispatched = False
            st.rerun()

    elif st.session_state.page == "forgot_userid":
        st.markdown("### 🔍 Recover User ID")
        if not st.session_state.forgot_uid_dispatched:
            with st.form("forgot_uid_form"):
                email_input = st.text_input("Enter Registered Email Address").strip()
                phone_input = st.text_input("Enter Registered Phone Number").strip()
                submit_btn = st.form_submit_button("Recover User ID", type="primary", use_container_width=True)
                if submit_btn:
                    if email_input and phone_input:
                        st.session_state.generated_otp = str(random.randint(100000, 999999))
                        st.session_state.target_email = email_input
                        st.session_state.target_phone = phone_input
                        st.session_state.forgot_uid_dispatched = True
                        st.session_state.otp_timestamp = time.time()
                        db.send_otp_via_gmail(email_input, st.session_state.generated_otp, "User ID Recovery Verification")
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide both email address and phone number.")
        else:
            @st.fragment(run_every=1.0)
            def render_uid_countdown_view():
                if st.session_state.otp_timestamp:
                    time_passed = time.time() - st.session_state.otp_timestamp
                    seconds_left = max(0, int(90 - time_passed))
                else:
                    seconds_left = 0
                    
                with st.form("verify_uid_otp_form"):
                    otp_entered = st.text_input("Enter 6-Digit OTP").strip()
                    verify_uid_btn = st.form_submit_button("Verify OTP", type="primary", use_container_width=True)
                    if verify_uid_btn:
                        if seconds_left == 0:
                            st.error("❌ Verification token expired. Request a new one below.")
                        elif otp_entered == st.session_state.generated_otp:
                            st.session_state.forgot_uid_verified = True
                            recovered_uid = db.get_user_id_by_email_and_phone(st.session_state.target_email, st.session_state.target_phone)
                            if recovered_uid: st.success(f"🎉 Your User ID is: **{recovered_uid}**")
                            else: st.error("❌ No matching credentials found.")
                            
                time_layout_col, action_layout_col = st.columns(2)
                with time_layout_col:
                    if seconds_left > 0:
                        st.info(f"⏳ Time Remaining: **{seconds_left}s**")
                    else:
                        st.error("🚨 Token Expired")
                with action_layout_col:
                    if seconds_left == 0:
                        if st.button("🔄 Resend Token", type="secondary", use_container_width=True, key="resend_uid_trigger"):
                            st.session_state.generated_otp = str(random.randint(100000, 999999))
                            db.send_otp_via_gmail(st.session_state.target_email, st.session_state.generated_otp, "User ID Recovery Verification")
                            st.session_state.otp_timestamp = time.time()
                            st.success("📧 User ID retrieval validation code sent.")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.button(f"🔒 Resend Locked", disabled=True, use_container_width=True, key="resend_uid_disabled")
            
            render_uid_countdown_view()

        if st.button("Back to Login", use_container_width=True, key="forgot_uid_back_to_login"): 
            st.session_state.page = "login"
            st.session_state.login_otp_dispatched = False
            st.rerun()
# Renders Internal Connected Workstation Panels ONLY if logged_in state is verified
else:
    # 🎯 Premium Header Component Add
    st.markdown(f"""
        <div class='premium-header'>
            <h1>🏛️ KRILEX Legal Tech Innovation</h1>
            <p>Professional Digital Workstation Console | Active Advocate Session</p>
        </div>
    """, unsafe_allow_html=True)

    # Upper Action Ribbon Strip
    h_col1, h_col2, h_col3 = st.columns([1, 2, 1])

    with h_col1:
        st.markdown('<div style="display: flex; flex-direction: column; gap: 8px;">', unsafe_allow_html=True)
        st.button("🌐 Language", key="lang_btn", use_container_width=True)
        
        if st.button("🏠 System Home", key="global_home_btn", use_container_width=True):
            st.session_state.footer_page = None
            st.session_state.active_app_tile = None
            st.session_state.selected_court = "--- Choose Jurisdiction ---"
            st.rerun()
            
        if st.session_state.footer_page is not None:
            if st.button("⬅ Back to Menu", key="back_from_footer", use_container_width=True):
                st.session_state.footer_page = None; st.rerun()
        elif st.session_state.active_app_tile is not None:
            if st.button("⬅ Back to Menu", key="back_to_tiles_menu", use_container_width=True):
                st.session_state.active_app_tile = None; st.rerun()
        elif st.session_state.selected_court != "--- Choose Jurisdiction ---":
            if st.button("⬅ Change Court", key="back_to_court_select", use_container_width=True):
                st.session_state.selected_court = "--- Choose Jurisdiction ---"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with h_col2:
        # Dynamic Premium KPI Metrics Display Add
        m_col1, m_col2 = st.columns(2, gap="medium")
        with m_col1:
            st.markdown("<div class='kpi-card'><h3>Drafts Generated</h3><h2>48</h2></div>", unsafe_allow_html=True)
        with m_col2:
            st.markdown("<div class='kpi-card'><h3>Active Plan</h3><h2>Premium Suite</h2></div>", unsafe_allow_html=True)

    with h_col3:
        with st.popover("👤 Advocate Profile Card", use_container_width=True):
            st.markdown(f"##### Adv. {st.session_state.username}")
            with st.container(border=True):
                uploaded_pic = st.file_uploader("Upload Profile Image", type=["png", "jpg", "jpeg"], key="popover_pic_uploader")
                if uploaded_pic is not None: st.image(uploaded_pic, width=100)
                st.caption("**Profile Parameters Mapping**")
                st.text(f"ID Cluster: ADV-{random.randint(1000,9999)}")
                st.text("Privilege: Verified Counsel")
            if st.button("🔒 Terminate Secure Session", key="popover_logout", use_container_width=True, type="primary"):
                st.session_state.logged_in = False
                st.session_state.page = "main"
                st.rerun()

    st.markdown("---")

    if st.session_state.footer_page is not None:
        st.markdown('<div class="workstation-container">', unsafe_allow_html=True)
        if st.session_state.footer_page == "about":
            st.markdown("### 🏛️ About Krilex Legal Tech")
            st.write("Krilex is an advanced legal-tech innovation platform engineered to simplify, streamline, and digitalize procedural drafting workflows across Indian court systems.")
        elif st.session_state.footer_page == "helpdesk":
            st.markdown("### 🛠️ Helpdesk Support & Feedback Hub")
            st.write("Encountering rendering errors or compilation layout faults? Submit an operational support request ticket down below.")
            st.text_input("Enter your query details", placeholder="Describe the layout issue...")
            st.button("Submit Report")
        elif st.session_state.footer_page == "write_us":
            st.markdown("### ✉️ Write Us / Contact Editorial Desk")
            st.write("For enterprise inquiries, feature expansion updates, or compliance submissions, reach out directly at: support@krilex.com")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        if st.session_state.selected_court == "--- Choose Jurisdiction ---":
            st.markdown('<div class="workstation-container">', unsafe_allow_html=True)
            st.markdown("### 🏛️ Indian Judicial Drafting Gateway")
            st.write("Select a targeted court forum below to initialize the custom dynamic drafting dashboard workspace canvas.")
            courts_list = get_all_indian_courts()
            choice = st.selectbox("Select Target Court / Forum", courts_list, key="court_selector_dropdown")
            if choice != "--- Choose Jurisdiction ---":
                st.session_state.selected_court = choice; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.active_app_tile is None:
            st.markdown('<div class="workstation-container">', unsafe_allow_html=True)
            st.markdown(f"<h4>🏛️ Active Judicial Hub: <span style='color:#8B0000;'>{st.session_state.selected_court}</span></h4>", unsafe_allow_html=True)
            st.write("Select an application framework asset component blueprint below to launch the canvas workspace:")
            st.markdown('</div>', unsafe_allow_html=True)
            
            r1_col1, r1_col2, r1_col3 = st.columns(3)
            with r1_col1:
                st.markdown('<div class="legal-tile tile-blue">⚖️ Entire Petition Suite</div>', unsafe_allow_html=True)
                if st.button("Open Entire Petition", key="btn_entire", use_container_width=True, type="primary"): 
                    st.session_state.active_app_tile = "Entire Petition"; st.rerun()
            with r1_col2:
                st.markdown('<div class="legal-tile tile-green">📄 Caveat Protection Application</div>', unsafe_allow_html=True)
                if st.button("Open Caveat Application", key="btn_caveat", use_container_width=True): 
                    st.session_state.active_app_tile = "Caveat Application"; st.rerun()
            with r1_col3:
                st.markdown('<div class="legal-tile tile-red">⏳ Delay Condonation Application</div>', unsafe_allow_html=True)
                if st.button("Open Delay Condonation", key="btn_delay", use_container_width=True): 
                    st.session_state.active_app_tile = "Delay Condonation Application"; st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            r2_col1, r2_col2, r2_col3 = st.columns(3)
            with r2_col1:
                st.markdown('<div class="legal-tile tile-green">🛡️ Stay & Interlocutory Application</div>', unsafe_allow_html=True)
                if st.button("Open Stay Application", key="btn_stay", use_container_width=True): 
                    st.session_state.active_app_tile = "Stay Application"; st.rerun()
            with r2_col2:
                st.markdown('<div class="legal-tile tile-red">🚫 Document Exemption Petition</div>', unsafe_allow_html=True)
                if st.button("Open Exemption Application", key="btn_exemption", use_container_width=True): 
                    st.session_state.active_app_tile = "Exemption Application"; st.rerun()
            with r2_col3:
                st.markdown('<div class="legal-tile tile-green">🚨 Immediate Urgency Application</div>', unsafe_allow_html=True)
                if st.button("Open Urgency Listing", key="btn_urgency", use_container_width=True): 
                    st.session_state.active_app_tile = "Urgency Application"; st.rerun()

        else:
            active_form = st.session_state.active_app_tile
            st.markdown('<div class="workstation-container">', unsafe_allow_html=True)
            st.markdown(f"### 📝 Drafting Canvas Framework: **{active_form}**")
            st.info(f"Target Jurisdiction Channel: {st.session_state.selected_court}")
            st.markdown('</div>', unsafe_allow_html=True)

            p_names_list = []
            r_names_list = []
            
            st.markdown('<div class="workstation-container">', unsafe_allow_html=True)
            district_val = st.text_input("📍 FORUM JURISDICTION DISTRICT", placeholder="e.g. MEERUT", key="f_district").upper()
            legal_provision = st.selectbox(
                "📜 Select Article / Rule Provision Standard", 
                ["Article 226 of the Constitution of India (Writ Petition)", 
                 "Article 227 of the Constitution of India (Misc. Petition)", 
                 "Section 151 of Civil Procedure Code (Civil Misc.)"], 
                key="f_prov"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.markdown("##### 👤 Petitioners / Applicants Stack")
                with st.container(border=True):
                    for i in range(st.session_state.p_count):
                        val = st.text_input(f"Petitioner No. {i+1} Name & Full Attestation", placeholder="Name S/o ..., R/o ...", key=f"f_p_name_{i}")
                        if val: p_names_list.append(val)
                    if st.button("➕ Add Petitioner Entity", key="add_p_btn", use_container_width=True): 
                        st.session_state.p_count += 1; st.rerun()
                    
            with col_f2:
                st.markdown("##### 👥 Respondents / Defendants Stack")
                with st.container(border=True):
                    for j in range(st.session_state.r_count):
                        val = st.text_input(f"Respondent No. {j+1} Name & Corporate Attestation", placeholder="Name S/o ..., R/o ...", key=f"f_r_name_{j}")
                        if val: r_names_list.append(val)
                    if st.button("➕ Add Respondent Entity", key="add_r_btn", use_container_width=True): 
                        st.session_state.r_count += 1; st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"Generate Verified {active_form}", key="btn_gen", use_container_width=True):
                if p_names_list and r_names_list:
                    st.success(f"🎉 {active_form} court format has been generated successfully!")
                    p_formatted = "\n".join(p_names_list)
                    r_formatted = "\n".join(r_names_list)
