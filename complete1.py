import streamlit as st
import db2 as db  # Reads directly from your db2.py file
import time
import os
import base64
import random

# =======================================================
# PART 1: GLOBAL SETUP, SESSION STATES & STYLESHEET
# =======================================================

# 1. Page Configuration and Theme Override (Light Mode Setup)
st.set_page_config(page_title="KRILEX Legal Tech Innovation", layout="centered")

# CSS to force Light Mode and Hide Header Elements
st.markdown("""
    <style>
    /* Force Light Theme Colors */
    .stApp {
        background-color: #FFFFFF !important;
        color: #31333F !important;
    }
    div[data-testid="stSidebar"] {
        background-color: #F0F2F6 !important;
    }
    /* Hide Deploy Button and Header */
    .stAppDeployButton {display: none !important;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Render Server Path Configuration for Logo
LOGO_FILENAME = "photo_6244332980792922580_y"

def load_server_logo(filename):
    extensions = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
    for ext in extensions:
        full_path = filename + ext
        if os.path.exists(full_path):
            try:
                with open(full_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    mime_type = "image/png" if "png" in ext.lower() else "image/jpeg"
                    return f"data:{mime_type};base64,{encoded_string}"
            except Exception:
                return ""
    return ""

# Logo load karein aur display karein
logo_base64 = load_server_logo(LOGO_FILENAME)

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
if logo_base64 and elapsed_time >= 2.5:
    watermark_css = f"""
    .stApp {{
        background-image: url("{logo_base64}") !important;
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
    
    if logo_base64:
        st.markdown(f'<div class="full-page-splash"><img src="{logo_base64}" class="big-splash-logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="full-page-splash"><h1 style="color:#0096ff; font-family:sans-serif; font-size:4rem;">KRILEX Legal Tech</h1></div>', unsafe_allow_html=True)
    
    time.sleep(0.1)
    st.rerun()
    
elif not st.session_state.logged_in:
    
    if st.session_state.page == "main":
        if logo_base64: 
            st.markdown(f'<div class="center-logo-container"><img src="{logo_base64}" width="160"></div>', unsafe_allow_html=True)
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
        if logo_base64: 
            st.markdown(f'<div class="center-logo-container"><img src="{logo_base64}" width="140"></div>', unsafe_allow_html=True)
        st.markdown("### 🔐 User Login")
        
        if not st.session_state.login_otp_dispatched:
            with st.form("login_form_container", clear_on_submit=False):
                uid = st.text_input("Login ID", key="login_uid_field").strip()
                pwd = st.text_input("Password", type="password", key="login_pwd_field")
                remember_me = st.checkbox("Remember Me", key="login_remember_me_checkbox")
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
        if logo_base64: 
            st.markdown(f'<div class="center-logo-container"><img src="{logo_base64}" width="140"></div>', unsafe_allow_html=True)
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
                new_name = st.text_input("Full Name").strip()
                new_email = st.text_input("Email Address").strip()
                new_phone = st.text_input("Phone Number").strip()
                submit_step1 = st.form_submit_button("Send Verification OTP", type="primary", use_container_width=True)
                if submit_step1:
                    if not new_uid or not new_name or not new_email or not new_phone:
                        st.warning("⚠️ All fields are mandatory.")
                    else:
                        st.session_state.temp_reg_data = {"uid": new_uid, "name": new_name, "email": new_email, "phone": new_phone}
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
    # Upper Action Ribbon Strip - Added a Back button next to System Home
    h_col1, h_col2, h_col3 = st.columns(3)

    with h_col1:
        if st.button("🏠 System Home", key="global_home_btn", use_container_width=True):
            st.session_state.footer_page = None
            st.session_state.active_app_tile = None
            st.session_state.selected_court = "--- Choose Jurisdiction ---"
            st.session_state.canvas_sub_page = "editor"
            st.rerun()

    # 🎯 NEW: Widescreen Top Back Button Navigation Added Here
    with h_col2:
        if st.button("🔙 Back to Forum Hub", key="global_top_back_btn", use_container_width=True):
            st.session_state.active_app_tile = None  # Drops active asset layer back to main choice matrix
            st.session_state.canvas_sub_page = "editor"
            st.rerun()

    with h_col3:
        with st.popover("👤 Profile Card", use_container_width=True):
            st.markdown(f"##### Adv. {st.session_state.username}")
            if st.button("🔒 Terminate secure session", key="popover_logout", use_container_width=True, type="primary"):
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
                st.markdown('<div class="legal-tile tile-blue">⚖️ Entire Petition </div>', unsafe_allow_html=True)
                if st.button("Open Entire Petition", key="btn_entire", use_container_width=True, type="primary"): 
                    st.session_state.active_app_tile = "Entire Petition"; st.rerun()
            with r1_col2:
                st.markdown('<div class="legal-tile tile-green">📄 Caveat Application</div>', unsafe_allow_html=True)
                if st.button("Open Caveat Application", key="btn_caveat", use_container_width=True): 
                    st.session_state.active_app_tile = "Caveat Application"; st.rerun()
            with r1_col3:
                st.markdown('<div class="legal-tile tile-red">⏳ Delay Condonation Application</div>', unsafe_allow_html=True)
                if st.button("Open Delay Condonation", key="btn_delay", use_container_width=True): 
                    st.session_state.active_app_tile = "Delay Condonation Application"; st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            r2_col1, r2_col2, r2_col3 = st.columns(3)
            with r2_col1:
                st.markdown('<div class="legal-tile tile-green">🛡️ Stay Application</div>', unsafe_allow_html=True)
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
            
            # Global sub-page routing state parameter initialization for document layout toggle
            if "canvas_sub_page" not in st.session_state:
                st.session_state.canvas_sub_page = "editor"

            # Initialize dynamic tracking counters inside session state if not set
            if "exp_p_count" not in st.session_state: st.session_state.exp_p_count = 1
            if "p_count" not in st.session_state: st.session_state.p_count = 1
            if "r_count" not in st.session_state: st.session_state.r_count = 1

            p_names_list = []
            exp_p_names_list = []
            r_names_list = []
            
            # Permanent default template text structure for editable paragraph blocks
            default_legal_text = (
                "2- That the applicant has not received any copy of the intended application till date.\n\n"
                "3- That the Caveator has strong apprehension that the Proposed Petitioner may seek an ad-interim "
                "ex-parte stay or restraining order without serving prior due notice to the Caveator, which would cause "
                "irreparable loss and injury to the Applicant."
            )

            # Persistent check safely falling back variables mapping
            district_mapped = st.session_state.get("persist_district", "_____________________")
            provision_mapped = st.session_state.get("persist_provision", "Article 226 of the Constitution of India (Writ Petition)")
            c_name_mapped = st.session_state.get("persist_c_name", "_____________________")
            c_addr_mapped = st.session_state.get("persist_c_addr", "_____________________")
            order_date_mapped = st.session_state.get("persist_order_date", "__________")
            additional_paras_mapped = st.session_state.get("persist_additional_paras", default_legal_text)


            # ====================================================
            # SUB-PAGE LAYER A: THE CONTENT COMPILER EDITOR VIEW
            # ====================================================
            if st.session_state.canvas_sub_page == "editor":
                st.markdown("""
                    <style>
                    .block-container {
                        max-width: 95% !important;
                        padding-left: 3rem !important;
                        padding-right: 3rem !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                st.markdown(f"### 📝 Drafting Input Form: **{active_form}**")
                
                # Create an expanded 50/50 split column layout grid structure 
                col_left_form, col_right_form = st.columns(2, gap="large")
                
                # --- LEFT COLUMN: CASE INFORMATION & DISTRICT PARAMETERS ---
                # --- LEFT COLUMN: CASE INFORMATION & DISTRICT PARAMETERS ---
                with col_left_form:
                    st.markdown("##### 📍 Case Information Parameters")
                    
                    # CSS injection to force the date picker calendar popup to render on top without getting cut off
                    st.markdown("""
                        <style>
                        div[data-baseweb="popover"] {
                            z-index: 999999 !important;
                        }
                        div[data-testid="stContainer"] {
                            overflow: visible !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    with st.container(border=True):
                        district_val = st.text_input("📍 FORUM JURISDICTION DISTRICT", placeholder="e.g. PRAYAGRAJ", key="f_district", value="" if district_mapped == "_____________________" else district_mapped).upper()
                        legal_provision = st.selectbox(
                            "📜 Select Article / Rule Provision Standard", 
                            ["Article 226 of the Constitution of India (Writ Petition)", 
                             "Article 227 of the Constitution of India (Misc. Petition)", 
                             "Section 151 of Civil Procedure Code (Civil Misc.)"], 
                            key="f_prov"
                        )
                        # Added explicit format parameter for strict DD/MM/YYYY alignment
                        order_date_val = st.date_input(
                            "📅 SELECT ORDER DATE (CHALLENGED ORDER)", 
                            key="f_order_date",
                            format="DD/MM/YYYY"
                        )
                        formatted_order_date = order_date_val.strftime("%d-%m-%Y")
                        st.session_state.persist_order_date = formatted_order_date


                # --- RIGHT COLUMN: CAVEATOR OR PETITIONER DETAILS ---
                with col_right_form:
                    if active_form == "Caveat Application":
                        st.markdown("##### 👤 Caveator Details")
                        with st.container(border=True):
                            caveator_name_only = st.text_input("Caveator Full Name", placeholder="e.g. NAMAN PANDEY", key="f_caveator_name_only", value="" if c_name_mapped == "_____________________" else c_name_mapped).upper()
                            caveator_address_only = st.text_input("Caveator Full Address & Attestation", placeholder="e.g. S/O ..., R/O ...", key="f_caveator_address_only", value="" if c_addr_mapped == "_____________________" else c_addr_mapped).upper()
                    else:
                        st.markdown("##### 👤 Petitioners / Applicants Stack")
                        with st.container(border=True):
                            for i in range(st.session_state.p_count):
                                val = st.text_input(f"Petitioner No. {i+1} Name & Full Attestation", placeholder="Name S/o ..., R/o ...", key=f"f_p_name_{i}")
                                if val: p_names_list.append(val)
                            if st.button("➕ Add Petitioner Entity", key="add_p_btn", use_container_width=True): 
                                st.session_state.p_count += 1; st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
                
                # --- FULL WIDTH: EXPECTED PETITIONER STACK (ONLY FOR CAVEATS) ---
                if active_form == "Caveat Application":
                    st.markdown("##### 👤 Expected Petitioner / Plaintiff Stack")
                    with st.container(border=True):
                        for k in range(st.session_state.exp_p_count):
                            val_ep = st.text_input(f"Expected Petitioner No. {k+1} Name & Full Attestation", placeholder="Name S/o ..., R/o ...", key=f"f_exp_p_name_{k}")
                            if val_ep: exp_p_names_list.append(val_ep)
                        if st.button("➕ Add Expected Petitioner", key="add_exp_p_btn", use_container_width=True):
                            st.session_state.exp_p_count += 1; st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)

                # --- FULL WIDTH LOWER SECTION: EXPECTED OPPOSITE PARTIES ---
                if active_form == "Caveat Application":
                    st.markdown("##### 👥 Expected Opposite Parties")
                else:
                    st.markdown("##### 👥 Respondents / Defendants Stack")
                    
                with st.container(border=True):
                    for j in range(st.session_state.r_count):
                        val = st.text_input(f"Respondent No. {j+1} Name & Corporate Attestation", placeholder="Name S/o ..., R/o ...", key=f"f_r_name_{j}")
                        if val: r_names_list.append(val)
                    if st.button("➕ Add Respondent Entity", key="add_r_btn", use_container_width=True): 
                        st.session_state.r_count += 1; st.rerun()
                # 🎯 NEW SECTION: Caveator Advocate Professional Profile Registration Box
                # 🎯 NEW OPTION: Dynamic Extra Counsel / Advocate Stack
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### ⚖️ Retained Caveator Advocate / Counsel Profile Stack")
                
                # Initialize counsel counter tracking state safely at the top if not set
                if "counsel_count" not in st.session_state: 
                    st.session_state.counsel_count = 1
                
                adv_names_list = []
                adv_rolls_list = []
                adv_chambers_list = []
                adv_phones_list = []

                with st.container(border=True):
                    for i in range(st.session_state.counsel_count):
                        st.markdown(f"**🔹 Counsel / Advocate No. {i+1}**")
                        
                        # Retaining filled data safely if screen refreshes
                        mapped_name = st.session_state.get(f"persist_adv_name_{i}", "")
                        mapped_roll = st.session_state.get(f"persist_adv_roll_{i}", "")
                        mapped_cham = st.session_state.get(f"persist_adv_chamber_{i}", "")
                        mapped_phone = st.session_state.get(f"persist_adv_phone_{i}", "")
                        
                        # Automatically default the first field to logged-in user name
                        default_name = f"ADV. {st.session_state.username.upper()}" if i == 0 else ""
                        
                        adv_col1, adv_col2 = st.columns(2)
                        with adv_col1:
                            adv_name_val = st.text_input(f"Advocate No. {i+1} Full Name", placeholder="e.g. ADV. NAMAN PANDEY", value=mapped_name if mapped_name else default_name, key=f"f_adv_name_{i}").upper()
                            adv_roll_val = st.text_input(f"Advocate No. {i+1} Roll No.", placeholder="e.g. UP/12345/2026", value=mapped_roll, key=f"f_adv_roll_{i}").upper()
                        with adv_col2:
                            adv_chamber_val = st.text_input(f"Chamber / Office Room No.", placeholder="e.g. CHAMBER NO. 45", value=mapped_cham, key=f"f_adv_chamber_{i}").upper()
                            adv_phone_val = st.text_input(f"Advocate Mobile Number", max_chars=10, placeholder="e.g. 9876543210", value=mapped_phone, key=f"f_adv_phone_{i}").strip()
                        
                        if adv_name_val:
                            adv_names_list.append(adv_name_val)
                            st.session_state[f"persist_adv_name_{i}"] = adv_name_val
                        if adv_roll_val: adv_rolls_list.append(adv_roll_val)
                        if adv_chamber_val: adv_chambers_list.append(adv_chamber_val)
                        if adv_phone_val: adv_phones_list.append(adv_phone_val)
                        st.markdown("---")
                    
                    # 🎯 The functional button to append an extra advocate row instantly
                    if st.button("➕ Add Extra Counsel / Advocate", key="add_extra_counsel_btn", use_container_width=True):
                        st.session_state.counsel_count += 1
                        st.rerun()

                # Joining all counsel metadata cleanly into a single state string for compile tracking
                st.session_state.persist_adv_name = "\n".join(adv_names_list)


                # --- FULL WIDTH: EDITABLE LEGAL PARAGRAPHS BLOCK ---
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### 📝 Additional Custom Legal Paragraphs / Grounds")
                with st.container(border=True):
                    additional_paras_input = st.text_area(
                        "If you want to append or edit statement paragraphs, modify them directly below:",
                        key="f_additional_paras",
                        value=additional_paras_mapped,
                        height=180
                    )

                # 🎯 NEW: Side-by-Side Action Grid for Compile and Cancel Toggles
                st.markdown("<br>", unsafe_allow_html=True)
                form_action_col1, form_action_col2 = st.columns(2)
                
                with form_action_col1:
                    submit_compile = st.button(f"✨ Compile Document & Generate Live Preview Page", type="primary", use_container_width=True)
                
                with form_action_col2:
                    back_to_hub_lower = st.button("🔙 Cancel & Back to Forum Hub", key="lower_form_back_to_hub_btn", use_container_width=True)

                if submit_compile:
                    if not district_val:
                        st.sidebar.warning("⚠️ Processing Denied: Missing Forum Jurisdiction District.")
                    elif active_form == "Caveat Application" and (not caveator_name_only or not caveator_address_only):
                        st.sidebar.warning("⚠️ Processing Denied: Please fill both Caveator Name and Address fields.")
                    elif active_form == "Caveat Application" and not exp_p_names_list:
                        st.sidebar.warning("⚠️ Processing Denied: Add at least one Expected Petitioner.")
                    elif active_form != "Caveat Application" and not p_names_list:
                        st.sidebar.warning("⚠️ Processing Denied: Add at least one Petitioner entity.")
                    elif not r_names_list:
                        st.sidebar.warning("⚠️ Processing Denied: Add at least one Expected Opposite Party / Respondent.")
                    else:
                        st.session_state.persist_district = district_val
                        st.session_state.persist_provision = legal_provision
                        st.session_state.persist_order_date = formatted_order_date
                        st.session_state.persist_additional_paras = additional_paras_input
                        if active_form == "Caveat Application":
                            st.session_state.persist_c_name = caveator_name_only
                            st.session_state.persist_c_addr = caveator_address_only
                            st.session_state.persist_adv_name = "\n".join(adv_names_list)
                            st.session_state.persist_exp_p_formatted = "\n".join([f"{idx+1}. {name}" for idx, name in enumerate(exp_p_names_list)])
                            st.session_state.persist_r_formatted = "\n".join([f"{idx+1}. {name}" for idx, name in enumerate(r_names_list)])
                        else:
                            st.session_state.persist_p_formatted = "\n".join([f"{idx+1}. {name}" for idx, name in enumerate(p_names_list)])
                            st.session_state.persist_r_formatted = "\n".join([f"{idx+1}. {name}" for idx, name in enumerate(r_names_list)])

                        
                        st.session_state.canvas_sub_page = "preview"
                        st.rerun()

                # Action handler logic for lower Cancel navigation trigger
                if back_to_hub_lower:
                    st.session_state.active_app_tile = None
                    st.session_state.canvas_sub_page = "editor"
                    st.rerun()

            # ====================================================
            # SUB-PAGE LAYER B: EXPANDED WIDESCREEN PREVIEW PAGE
            # ====================================================
            elif st.session_state.canvas_sub_page == "preview":
                st.markdown("""
                    <style>
                    .block-container { max-width: 95% !important; padding-left: 3rem !important; padding-right: 3rem !important; }
                    
                    /* 🏛️ LEGAL PREVIEW BLOCK: Set alignment container */
                    code, pre, .stCode, div[data-testid="stCodeBlock"] pre {
                        font-family: 'Times New Roman', Times, serif !important; 
                        font-size: 14pt !important; 
                        line-height: 1.6 !important;
                        background-color: #ffffff !important; 
                        color: #000000 !important; 
                        border: 1px solid #ddd !important;
                        padding: 40px !important; 
                        white-space: pre-wrap !important;
                        display: block !important;
                        width: 100% !important;
                        
                        /* 🚀 FIXED: Default base aligned to standard text, headings filtered inside final_document_string */
                        text-align: justify !important;
                    }
                    button[data-testid="stCopyButton"] { display: none !important; }
                    </style>
                """, unsafe_allow_html=True)

                exp_p_compiled = st.session_state.get("persist_exp_p_formatted", "1. _____________________")
                r_compiled = st.session_state.get("persist_r_formatted", "1. _____________________")
                p_compiled = st.session_state.get("persist_p_formatted", "1. _____________________")
                custom_paras_section = f"\n\n{additional_paras_mapped}" if additional_paras_mapped.strip() else ""
                
                if '(' in provision_mapped:
                    provision_text = provision_mapped.split('(')[0].strip().upper()
                else:
                    provision_text = provision_mapped.upper()
                
                # 🚀 FIXED: Structured spaces injected to center titles while maintaining left-aligned bullet paragraphs
                if active_form == "Caveat Application":
                    final_document_string = f"""                               IN THE HIGH COURT OF JUDICATURE AT ALLAHABAD
                                                      ***********
                                      Civil Misc. Caveat Application no.      of 2026
                (Under section 148-A C.P.C. read with Rule 5 Chapter 22 of High Court Rules)

                                                      On behalf of
                                        {c_name_mapped}    ---- Applicant

                                      Misc. Petition Civil NO-        of 2026 (civil)
                                                      (U/A {provision_text})

                                                   DISTRICT – {district_mapped}

{exp_p_compiled}
- - - - - - - - - - - - - - - - - - - - ---- Proposed Petitioner/plaintiff

                                                        VERSUS

{r_compiled} - - - - - - - - - - - - - - ---- Proposed defendant /Respondent

TO,
    The Hon`ble chief justice and his other companion judges of the aforesaid court.

    The humble application of the above named applicant most respectfully showeth as under.

1- That in the above noted proposed application, the proposed petitioner may file a application before this Hon`ble court against the order dated {order_date_mapped} passed by Civil Judge (SD), {district_mapped}.{custom_paras_section}

PRAYER:
It is, therefore, most respectfully prayed that this Hon'ble Court may be pleased to direct that no ex-parte order or ad-interim relief be granted to the Expected Opposite Parties without giving prior due notice and opportunity of being heard to the Caveator or their Counsel.

                                                       FILED BY:
                                                   ADV. {st.session_state.username.upper()}
                                            COUNSEL FOR APPLICANT/CAVEATOR
                                                   DATED: 09-11-2026"""
                else:
                    final_document_string = f"""                                     BEFORE THE HON'BLE {st.session_state.selected_court.upper()}
                                                   DISTRICT: {district_mapped}

IN THE MATTER OF:
{p_compiled}

                                                        VERSUS
{r_compiled}

                                APPLICATION FOR {active_form.upper()} UNDER {provision_mapped}."""

                st.markdown(f"### 🏛️ Expanded Workstation Preview Stage: **{active_form}**")
                
                act_col1, act_col2 = st.columns(2)
                with act_col1:
                    if st.button("⬅ Return to Editor Layout Panel", use_container_width=True):
                        st.session_state.canvas_sub_page = "editor"
                        st.rerun()
                
                st.markdown("---")
                st.code(final_document_string, language="text")

                
                html_formatted_content = f"""
                <html>
                <head>
                    <style>
                        @page {{ size: A4; margin: 1in; }}
                        body {{ font-family: 'Times New Roman', Times, serif; font-size: 14pt; padding: 20px; line-height: 1.6; white-space: pre-wrap; color: #000000; }}
                    </style>
                </head>
                <body>{final_document_string.replace('\n', '<br>')}</body>
                </html>
                """

                with act_col2:
                    st.download_button(
                        label="📥 Download Generated Petition (PDF)",
                        data=html_formatted_content,
                        file_name=f"{active_form.lower().replace(' ', '_')}_final.pdf",
                        mime="text/html",
                        use_container_width=True,
                        type="primary"
                    )

                
