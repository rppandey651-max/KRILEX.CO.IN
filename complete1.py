import streamlit as st
import streamlit.components.v1 as components
import db2 as db  # Reads directly from your db2.py file
import time
import os
import base64
import random

# =======================================================
# PART 1: GLOBAL SETUP, SESSION STATES & STYLESHEET
# =======================================================

# 1. Page Configuration and Theme Override (Light Mode Setup)
st.set_page_config(page_title="KRILEX Legal Tech Innovation", layout="wide")

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
    .service-card {{
        background-color: #F8FAFC; padding: 20px; border-radius: 10px;
        border: 1px solid #E2E8F0; text-align: center; height: 100%;
    }}
    .testimonial-box {{
        background-color: #EFF6FF; padding: 15px; border-left: 5px solid #1E3A8A;
        border-radius: 5px; margin: 15px 0;
    }}
    .footer-section {{
        background-color: #1F2937; color: #F3F4F6; padding: 20px;
        border-radius: 8px; margin-top: 30px; text-align: center;
    }}
    .cmd-welcome-banner {{
        background: linear-gradient(90deg, #0F294A 0%, #1E3A8A 100%);
        color: #FFFFFF;
        padding: 16px 24px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        margin: 12px 0 20px 0;
        box-shadow: 0 4px 12px rgba(15, 41, 74, 0.18);
    }}
    .kpi-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        height: 100%;
    }}
    .kpi-green {{ border-top: 4px solid #16A34A; }}
    .kpi-blue {{ border-top: 4px solid #2563EB; }}
    .kpi-amber {{ border-top: 4px solid #D97706; }}
    .kpi-purple {{ border-top: 4px solid #7C3AED; }}
    .tpl-card {{
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .badge-pill {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        float: right;
    }}
    .badge-green {{ background: #DCFCE7; color: #166534; }}
    .badge-amber {{ background: #FEF3C7; color: #92400E; }}
    .badge-blue {{ background: #DBEAFE; color: #1E40AF; }}
                  
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
# =======================================================
# VOICE COMMAND COMPONENT FOR LEGAL PARAGRAPHS
# =======================================================
def voice_input_component():
    custom_speech_html = """
    <div style="font-family: sans-serif; margin-bottom: 10px;">
        <button id="mic-btn" style="
            background-color: #f0f2f6; 
            border: 1px solid #d3d3d3; 
            padding: 8px 12px; 
            border-radius: 5px; 
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 14px;
        ">
            🎤 Click to Speak
        </button>
        <p id="status" style="font-size: 12px; color: grey; margin: 5px 0 0 0;"></p>
    </div>

    <script>
        const btn = document.getElementById('mic-btn');
        const status = document.getElementById('status');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            btn.style.display = 'none';
            status.innerText = "Speech recognition not supported in this browser. Please use Chrome/Edge.";
        } else {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'en-US';
            recognition.interimResults = false;

            btn.addEventListener('click', () => {
                recognition.start();
                btn.style.backgroundColor = '#ff4b4b';
                btn.style.color = 'white';
                btn.innerText = '🔴 Listening...';
                status.innerText = "Speaking now...";
            });

            recognition.onresult = (event) => {
                // FIXED: Handled strict nested array extraction matrix for accurate web audio speech
                const transcript = event.results[0][0].transcript;
                
                // Directly search and inject the string text into your parent Streamlit text area field
                const textarea = window.parent.document.querySelector('textarea[aria-label="If you want to append or edit statement paragraphs, modify them directly below:"]');
                if (textarea) {
                    textarea.value += (textarea.value ? " " : "") + transcript;
                    // Trigger dynamic structural tracking framework reload input update event
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                }

                status.innerText = "Text captured: " + transcript;
            };

            recognition.onspeechend = () => {
                recognition.stop();
                resetButton();
            };

            recognition.onerror = (event) => {
                status.innerText = "Error occurred: " + event.error;
                resetButton();
            };
            
            function resetButton() {
                btn.style.backgroundColor = '#f0f2f6';
                btn.style.color = 'black';
                btn.innerText = '🎤 Click to Speak';
            }
        }
    </script>
    """
    components.html(custom_speech_html, height=80)



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
        # 1. Header Section (Persistent Home & Centered Logo)
        col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
        with col_h1:
            if st.button("🏠 Home", key="nav_home"):
                st.session_state.page = "main"
                st.rerun()
        with col_h2:
            if logo_base64:
                st.markdown(f'<div class="center-logo-container"><img src="{logo_base64}" width="130"></div>', unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin: 0;'>KRILEX</h2>", unsafe_allow_html=True)
        with col_h3:
            nav_c1, nav_c2 = st.columns(2)
            with nav_c1:
                if st.button("Register", key="nav_register", use_container_width=True):
                    st.session_state.page = "register"
                    st.session_state.otp_timestamp = None
                    st.rerun()
            with nav_c2:
                if st.button("Login / CTA", key="nav_login", type="primary", use_container_width=True):
                    st.session_state.page = "login"
                    st.session_state.login_otp_dispatched = False
                    st.session_state.otp_timestamp = None
                    st.rerun()

        st.divider()

        # 2. Hero Section
        hero_left, hero_right = st.columns([3, 2])
        with hero_left:
            st.title("Smart & Accurate Legal Drafting with Krilex")
            st.write(
                "Generate court-ready Caveat Applications, Stay Applications, and legal petitions "
                "in minutes with live preview and Times New Roman (Size 14) PDF formatting."
            )
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("🔐 Get Started (Login)", type="primary", use_container_width=True, key="landing_login_trigger"):
                    st.session_state.page = "login"
                    st.session_state.login_otp_dispatched = False
                    st.session_state.otp_timestamp = None
                    st.rerun()
            with btn2:
                if st.button("🚀 Explore Demo Workspace", use_container_width=True, key="landing_demo_bypass_trigger"):
                    st.session_state.logged_in = True
                    st.session_state.username = "DemoGuest"
                    st.session_state.full_name = "reg_name.strip()"
                    st.session_state.username = "reg_name.strrip()"
                    st.session_state.page = "dashboard"
                    st.toast("Authenticated via Instant Demo Clearance!")
                    st.rerun()
        with hero_right:
            st.info(
                "**KRILEX Legal Tech Preview**\n\n"
                "- Instant Court-Ready PDF Export\n"
                "- Editable Permanent Legal Clauses\n"
                "- Voice Dictation & Auto-Numbering\n"
                "- Secure Gmail OTP Verification"
            )

        st.divider()

        # 3. Services / Features Section
        st.markdown("<h3 style='text-align: center;'>OUR SERVICES / FEATURES</h3>", unsafe_allow_html=True)
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            st.markdown("""
                <div class="service-card">
                    <h4>📄 Caveat Applications</h4>
                    <p>Dedicated module with permanent editable lines, advocate profile stack, and instant court-ready PDF export.</p>
                </div>
            """, unsafe_allow_html=True)
        with s_col2:
            st.markdown("""
                <div class="service-card">
                    <h4>🛡️ Stay Applications</h4>
                    <p>Separate and structured workflow designed specifically for urgent stay petitions without formatting errors.</p>
                </div>
            """, unsafe_allow_html=True)
        with s_col3:
            st.markdown("""
                <div class="service-card">
                    <h4>⚖️ Entire Petitions & Notices</h4>
                    <p>Quick templates for Delay Condonation, Exemption, Urgency Listing, and Writ Petitions with live preview.</p>
                </div>
            """, unsafe_allow_html=True)

        st.divider()

        # 4. About Section
        about_img, about_text = st.columns([1, 2])
        with about_img:
            st.markdown("""
                <div class="service-card">
                    <h4>🏛️ Trusted Legal Tech</h4>
                    <p>100% Secure & Confidential</p>
                    <p>High Court & Supreme Court Formats</p>
                </div>
            """, unsafe_allow_html=True)
        with about_text:
            st.subheader("WHO WE ARE (About Krilex)")
            st.write(
                "Krilex is a specialized legal drafting application built to save time for advocates and legal professionals. "
                "With secure Gmail OTP authentication, voice-to-text drafting, and precise court formatting, we simplify daily judicial documentation."
            )

        st.divider()

        # 5. Testimonials Section
        st.markdown("<h3 style='text-align: center;'>WHAT OUR USERS SAY</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div class="testimonial-box">
                <strong>"Very clean interface and accurate Caveat PDF formatting! Saves hours of manual typing."</strong> — Rahul, Legal Practitioner ⭐⭐⭐⭐⭐
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # 6. Contact / CTA Form Section
        st.subheader("CONTACT US")
        if "contact_submitted" not in st.session_state:
            st.session_state.contact_submitted = False

        if not st.session_state.contact_submitted:
            with st.form("krilex_contact_form", clear_on_submit=True):
                c_name = st.text_input("Full Name")
                c_contact = st.text_input("Email or Phone Number")
                c_msg = st.text_area("Your Message or Query")
                submitted = st.form_submit_button("Send Message", type="primary")
                if submitted:
                    if c_name and c_contact and c_msg:
                        import requests
                        try:
                            # Direct email dispatch via Formspree API (Works reliably on Render)
                            requests.post(
                                "https://formsubmit.co",
                                json={
                                    "name": c_name,
                                    "contact": c_contact,
                                    "message": c_msg,
                                    "_subject": f"New Krilex Inquiry from {c_name}"
                                },
                                timeout=5
                            )
                        except Exception:
                            pass
                        st.session_state.contact_submitted = True
                        st.rerun()
                    else:
                        st.warning("Please fill in all fields before submitting.")
        else:
            st.success("Thank you! Your message has been sent directly to the Krilex support team.")

        # Define Pop-up Dialogs for Helpdesk and About
        @st.dialog("Helpdesk Support")
        def show_helpdesk_popup():
            st.write("Need assistance with Krilex legal drafting or account recovery? Use the Contact Us form or reach out to our support desk.")
            st.info("Support Email: support@krilex.com")

        @st.dialog("About Krilex")
        def show_about_popup():
            st.write(
                "Krilex is a legal drafting application engineered to simplify and digitalize procedural drafting "
                "workflows across Indian court systems. Generate court-ready Caveat Applications, Stay Applications, "
                "and legal petitions in standard Times New Roman (Size 14) formatting."
            )


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
    # 1. Top Header Bar (Logo Left | Court Dropdown Center | Profile Right)
    hdr_c1, hdr_c2, hdr_c3 = st.columns([1.5, 2.5, 1.5])
    with hdr_c1:
        if logo_base64:
            st.markdown(f'<div style="display:flex; align-items:center; gap:10px;"><img src="{logo_base64}" width="45"><div><strong style="font-size:18px; color:#0F294A;">KRILEX</strong><br><span style="font-size:12px; color:#64748B;">Legal Tech</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:#0F294A; margin:0;'>⚖️ KRILEX <span style='font-size:13px; color:#64748B; font-weight:normal;'>Legal Tech</span></h3>", unsafe_allow_html=True)

    with hdr_c2:
        courts_list = get_all_indian_courts()
        current_idx = courts_list.index(st.session_state.selected_court) if st.session_state.selected_court in courts_list else 2
        selected_forum = st.selectbox("Active Workspace", courts_list, index=current_idx, label_visibility="collapsed", key="top_court_switcher")
        if selected_forum != st.session_state.selected_court and selected_forum != "--- Choose Jurisdiction ---":
            st.session_state.selected_court = selected_forum
            st.rerun()

    with hdr_c3:
        with st.popover(f"👤 Adv. {st.session_state.username}", use_container_width=True):
            st.markdown(f"##### Adv. {st.session_state.username}")
            if st.button("🏠 Dashboard Home", key="pop_dash_home", use_container_width=True):
                st.session_state.active_app_tile = None
                st.session_state.footer_page = None
                st.session_state.canvas_sub_page = "editor"
                st.rerun()
            if st.button("🔒 Logout", key="popover_logout", use_container_width=True, type="primary"):
                st.session_state.logged_in = False
                st.session_state.page = "main"
                st.rerun()

    st.markdown("<hr style='margin: 10px 0 20px 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)

    if "sidebar_tab" not in st.session_state:
        st.session_state.sidebar_tab = "dashboard"

    rail_col, main_col = st.columns([0.55, 9.45], gap="medium")

    with rail_col:
        st.markdown("""
            <style>
            /* Left Rail ko Floating aur Expandable banana */
            div[data-testid="stColumn"]:has(.left-rail-marker) {
                position: fixed !important;
                left: 18px !important;
                top: 95px !important;
                width: 58px !important;
                min-width: 58px !important;
                max-width: 58px !important;
                background-color: #FFFFFF !important;
                border-radius: 14px !important;
                padding: 14px 8px !important;
                border: 1px solid #E2E8F0 !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
                min-height: 76vh !important;
                z-index: 99999 !important; /* Dashboard ke upar float karne ke liye */
                overflow: hidden !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }

            /* Mouse le jaane (Hover) par Sidebar poora khulega */
            div[data-testid="stColumn"]:has(.left-rail-marker):hover {
                width: 235px !important;
                min-width: 235px !important;
                max-width: 235px !important;
                box-shadow: 10px 0 30px rgba(15, 41, 74, 0.18) !important;
            }

            /* Buttons ko left-align karna taaki icon pehle aur text baad mein dikhe */
            div[data-testid="stColumn"]:has(.left-rail-marker) button {
                border: none !important;
                background: transparent !important;
                padding: 10px 11px !important;
                border-radius: 10px !important;
                color: #475569 !important;
                box-shadow: none !important;
                margin-bottom: 6px !important;
                display: flex !important;
                justify-content: flex-start !important;
                align-items: center !important;
                width: 100% !important;
                overflow: hidden !important;
            }

            /* Button ke andar ka text nowrap rakhna taaki neeche na gire */
            div[data-testid="stColumn"]:has(.left-rail-marker) button p {
                font-size: 15px !important;
                font-weight: 600 !important;
                white-space: nowrap !important;
                margin: 0 !important;
                letter-spacing: 0.2px !important;
            }

            /* Hover state on individual button */
            div[data-testid="stColumn"]:has(.left-rail-marker) button:hover {
                background-color: #EFF6FF !important;
                color: #1D4ED8 !important;
            }

            /* Active Selected Tab Style */
            div[data-testid="stColumn"]:has(.left-rail-marker) button[kind="primary"] {
                background-color: #EFF6FF !important;
                color: #1D4ED8 !important;
                border-left: 3px solid #1D4ED8 !important;
            }

            /* Main content ko thoda right shift karna taaki collapsed bar ke neeche na dabey */
            div[data-testid="stColumn"]:has(.left-rail-marker) + div[data-testid="stColumn"] {
                margin-left: 72px !important;
                width: calc(100% - 72px) !important;
                flex: 1 1 calc(100% - 72px) !important;
            }
            </style>
            <div class="left-rail-marker"></div>
        """, unsafe_allow_html=True)


        if st.button("⊞  Dashboard Home", key="rail_dash", type="primary" if st.session_state.sidebar_tab == "dashboard" else "secondary", use_container_width=True):
            st.session_state.sidebar_tab = "dashboard"
            st.session_state.active_app_tile = None
            st.session_state.footer_page = None
            st.rerun()

        if st.button("👥  Client Directory", key="rail_clients", type="primary" if st.session_state.sidebar_tab == "clients" else "secondary", use_container_width=True):
            st.session_state.sidebar_tab = "clients"
            st.session_state.active_app_tile = None
            st.rerun()

        if st.button("📄  Saved Drafts", key="rail_drafts", type="primary" if st.session_state.sidebar_tab == "drafts" else "secondary", use_container_width=True):
            st.session_state.sidebar_tab = "drafts"
            st.session_state.active_app_tile = None
            st.rerun()

        if st.button("📋  Daily Cause List", key="rail_causelist", type="primary" if st.session_state.sidebar_tab == "causelist" else "secondary", use_container_width=True):
            st.session_state.sidebar_tab = "causelist"
            st.session_state.active_app_tile = None
            st.rerun()

        if st.button("💼  Case Briefs", key="rail_briefs", type="primary" if st.session_state.sidebar_tab == "briefs" else "secondary", use_container_width=True):
            st.session_state.sidebar_tab = "briefs"
            st.session_state.active_app_tile = None
            st.rerun()

        if st.button("⚙️  Profile & Settings", key="rail_settings", type="primary" if st.session_state.sidebar_tab == "settings" else "secondary", use_container_width=True):
            st.session_state.sidebar_tab = "settings"
            st.session_state.active_app_tile = None
            st.rerun()

        st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

        if st.button("↪️  Logout", key="rail_logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "main"
            st.rerun()


    with main_col:
        if st.session_state.sidebar_tab == "clients":
            st.markdown('<div class="dash-section-box">', unsafe_allow_html=True)
            st.markdown("### 👥 Client & Party Directory")
            st.info("Saved Caveators, Petitioners, and Opposite Parties from your drafts will appear here.")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.sidebar_tab == "drafts":
            st.markdown('<div class="dash-section-box">', unsafe_allow_html=True)
            st.markdown("### 📄 Saved Legal Drafts")
            st.write(f"**1. Caveat Application** — {st.session_state.get('persist_c_name', 'Draft Ready')}")
            if st.button("Open Latest Caveat Draft", type="primary"):
                st.session_state.sidebar_tab = "dashboard"
                st.session_state.active_app_tile = "Caveat Application"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.sidebar_tab == "causelist":
            st.markdown('<div class="dash-section-box">', unsafe_allow_html=True)
            st.markdown("### 📋 Daily Court Cause List")
            st.write("• **Court No. 34:** Fresh List — 2 Cases")
            st.write("• **Court No. 12:** Supplementary List — 1 Case")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.sidebar_tab == "briefs":
            st.markdown('<div class="dash-section-box">', unsafe_allow_html=True)
            st.markdown("### 💼 Case Briefs & Notes")
            st.text_area("Quick Courtroom Notes", placeholder="Write case hearing notes here...")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.sidebar_tab == "settings":
            st.markdown('<div class="dash-section-box">', unsafe_allow_html=True)
            st.markdown("### ⚙️ Advocate Profile Settings")
            st.text_input("Advocate Name", value=f"Adv. {st.session_state.username}")
            st.text_input("Default Court", value=st.session_state.selected_court)
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.active_app_tile is None:
            # 2. Today's Courtroom Board Banner
            st.markdown("""
                <div style="background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%); padding: 20px; border-radius: 12px; color: white; margin-bottom: 22px; box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);">
                    <h4 style="margin: 0 0 15px 0; color: #FFFFFF; font-weight: 600;">🏛️ Today's Courtroom Board</h4>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                        <div style="background: rgba(15, 23, 42, 0.45); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12);">
                            <div style="font-size: 16px; font-weight: 700;">Fresh List: 2 Cases</div>
                            <div style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">(Court No. 34)</div>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.14); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.18);">
                            <div style="font-size: 16px; font-weight: 700;">Supplementary List: 1 Case</div>
                            <div style="font-size: 13px; color: #E2E8F0; margin-top: 4px;">(Court No. 12)</div>
                        </div>
                        <div style="background: #CA8A04; padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.25);">
                            <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">Urgent Mentioning Pending (1)</div>
                            <div style="display: inline-block; background: #FEF9C3; color: #854D0E; font-size: 12px; font-weight: 700; padding: 3px 10px; border-radius: 5px; margin-top: 6px;">Mentioning Slip Ready</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 3. One-Tap Drafting Templates Section
            with st.container(border=True):
                st.markdown("#### ⚡ One-Tap Drafting Templates")
                t_col1, t_col2, t_col3, t_col4 = st.columns(4)

                with t_col1:
                    st.markdown("""
                        <div style="background: #1E293B; color: white; padding: 18px; border-radius: 10px; min-height: 125px; margin-bottom: 8px;">
                            <div style="font-weight: 700; font-size: 15px;">📕 Caveat Application</div>
                            <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">(Civil / Criminal)</div>
                            <div style="font-size: 12px; color: #CBD5E1; margin-top: 8px;">U/S 148-A CPC & High Court Rules</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Open Caveat ➔", key="ot_caveat", use_container_width=True, type="primary"):
                        st.session_state.active_app_tile = "Caveat Application"
                        st.rerun()

                with t_col2:
                    st.markdown("""
                        <div style="background: #0D9488; color: white; padding: 18px; border-radius: 10px; min-height: 125px; margin-bottom: 8px;">
                            <div style="font-weight: 700; font-size: 15px;">🛡️ Stay Application</div>
                            <div style="font-size: 11px; color: #CCFBF1; margin-top: 2px;">(Interim Relief)</div>
                            <div style="font-size: 12px; color: #F0FDFA; margin-top: 8px;">Urgent Stay & Restraining Order Petition</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Open Stay ➔", key="ot_stay", use_container_width=True):
                        st.session_state.active_app_tile = "Stay Application"
                        st.rerun()

                with t_col3:
                    st.markdown("""
                        <div style="background: #2563EB; color: white; padding: 18px; border-radius: 10px; min-height: 125px; margin-bottom: 8px;">
                            <div style="font-weight: 700; font-size: 15px;">⚖️ Writ Petition</div>
                            <div style="font-size: 11px; color: #DBEAFE; margin-top: 2px;">(Article 226 / 227)</div>
                            <div style="font-size: 12px; color: #EFF6FF; margin-top: 8px;">Complete Writ & Miscellaneous Petition</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Open Writ ➔", key="ot_writ", use_container_width=True):
                        st.session_state.active_app_tile = "Entire Petition"
                        st.rerun()

                with t_col4:
                    st.markdown("""
                        <div style="background: #CA8A04; color: white; padding: 18px; border-radius: 10px; min-height: 125px; margin-bottom: 8px;">
                            <div style="font-weight: 700; font-size: 15px;">🚔 Quashing / Delay</div>
                            <div style="font-size: 11px; color: #FEF08A; margin-top: 2px;">(482 / BNSS / Sec. 5)</div>
                            <div style="font-size: 12px; color: #FEFCE8; margin-top: 8px;">FIR Quashing, Delay & Urgency Listing</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Open Quashing/Misc ➔", key="ot_quash", use_container_width=True):
                        st.session_state.active_app_tile = "Delay Condonation Application"
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # 4. 90-Day Caveat Watchlist Table
            with st.container(border=True):
                st.markdown("#### ⏳ 90-Day Caveat Watchlist")
                wh1, wh2, wh3, wh4 = st.columns([3, 1.5, 1, 1.3])
                wh1.markdown("**Entry Name**")
                wh2.markdown("**Progress**")
                wh3.markdown("**Status**")
                wh4.markdown("**Action**")
                st.divider()

                # Row 1 (Expiring Soon Warning)
                r1_c1, r1_c2, r1_c3, r1_c4 = st.columns([3, 1.5, 1, 1.3])
                r1_c1.markdown(f"**Adv. {st.session_state.username} vs. State of U.P.** — Day 82/90 <span style='color:#DC2626; font-weight:600;'>(Expires Soon)</span>", unsafe_allow_html=True)
                r1_c2.progress(82 / 90)
                r1_c3.markdown("<span style='color:#16A34A; font-weight:700;'>Active</span>", unsafe_allow_html=True)
                if r1_c4.button("One-Click Renew", key="renew_cav_1", type="primary", use_container_width=True):
                    st.session_state.active_app_tile = "Caveat Application"
                    st.rerun()

                st.markdown("<hr style='margin: 8px 0; border-color: #F1F5F9;'>", unsafe_allow_html=True)

                # Row 2 (Normal Active Caveat)
                saved_cav_party = st.session_state.get("persist_c_name", "")
                row2_title = f"{saved_cav_party} vs. State of U.P." if (saved_cav_party and saved_cav_party != "_____________________") else "Ramesh Kumar vs. State of U.P."
                r2_c1, r2_c2, r2_c3, r2_c4 = st.columns([3, 1.5, 1, 1.3])
                r2_c1.markdown(f"**{row2_title}** — Day 71/90")
                r2_c2.progress(71 / 90)
                r2_c3.markdown("<span style='color:#2563EB; font-weight:700;'>71/90 Days</span>", unsafe_allow_html=True)
                if r2_c4.button("One-Click Renew", key="renew_cav_2", use_container_width=True):
                    st.session_state.active_app_tile = "Caveat Application"
                    st.rerun()

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
            # --- TOP SEPARATE BOX FOR CIVIL / CRIMINAL (CAVEAT APPLICATION) ---
                if active_form == "Caveat Application":
                    st.markdown("##### ⚖️ Caveat Case Category")
                    with st.container(border=True):
                        saved_cat = st.session_state.get("persist_caveat_category", "Civil")
                        caveat_category = st.radio(
                            "Select Caveat Application Type:",
                            options=["Civil", "Criminal"],
                            index=0 if saved_cat == "Civil" else 1,
                            horizontal=True,
                            key="f_caveat_category"
                        )
                        st.session_state.persist_caveat_category = caveat_category
                    st.markdown("<br>", unsafe_allow_html=True)

                # Create an expanded 50/50 split column layout grid structure 
                col_left_form, col_right_form = st.columns(2, gap="large")
                
                # --- LEFT COLUMN: CASE INFORMATION & DISTRICT PARAMETERS ---
                with col_left_form:
                    st.markdown("##### 📍 Case Information Parameters")
                    
                    st.markdown("""
                        <style>
                        div[data-baseweb="popover"] {
                            z-index: 999999 !important;
                            top: 120px !important;
                        }
                        div[data-baseweb="calendar"] header {
                            visibility: visible !important;
                            display: flex !important;
                            background-color: #f8fafc !important;
                            padding: 8px !important;
                        }
                        div[data-baseweb="calendar"] button svg {
                            fill: #000000 !important;
                            visibility: visible !important;
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
                        order_date_val = st.date_input(
                            "📅 SELECT ORDER DATE (CHALLENGED ORDER)", 
                            key="f_order_date",
                            format="DD/MM/YYYY"
                        )
                        formatted_order_date = order_date_val.strftime("%d-%m-%Y")
                        st.session_state.persist_order_date = formatted_order_date

                    # 🎯 UPDATED: CASE CRIME DETAILS (Alag Crime No & Year, Bina Thana/District ke)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("##### 🚔 Case Crime Details")

                    if "crime_count" not in st.session_state:
                        st.session_state.crime_count = 1

                    crime_details_list = []

                    with st.container(border=True):
                        for idx in range(st.session_state.crime_count):
                            if st.session_state.crime_count > 1:
                                st.markdown(f"**🔹 Crime Detail No. {idx+1}**")

                            c_col1, c_col2 = st.columns(2)
                            with c_col1:
                                crime_no_val = st.text_input(
                                    "Case Crime No.",
                                    placeholder="e.g. 0145",
                                    value=st.session_state.get(f"persist_crime_no_{idx}", ""),
                                    key=f"f_crime_no_{idx}"
                                ).upper()

                                sections_val = st.text_input(
                                    "Under Sections",
                                    placeholder="e.g. 115(2), 352 BNS",
                                    value=st.session_state.get(f"persist_sections_{idx}", ""),
                                    key=f"f_under_sections_{idx}"
                                ).upper()

                            with c_col2:
                                year_options = [str(y) for y in range(2026, 1989, -1)]
                                saved_year = st.session_state.get(f"persist_crime_year_{idx}", "2026")
                                default_year_idx = year_options.index(saved_year) if saved_year in year_options else 0

                                crime_year_val = st.selectbox(
                                    "Crime Year",
                                    options=year_options,
                                    index=default_year_idx,
                                    key=f"f_crime_year_{idx}"
                                )

                                nature_val = st.selectbox(
                                    "Nature of Case / Offence",
                                    [
                                        "Criminal / FIR",
                                        "Cognizable Offence",
                                        "Non-Cognizable (NCR)",
                                        "Civil Nature / Dispute",
                                        "Matrimonial / Domestic",
                                        "Financial / Fraud",
                                        "Other"
                                    ],
                                    key=f"f_crime_nature_{idx}"
                                )

                            # Full width dropdown for Relief / Writ Type
                            writ_relief_val = st.selectbox(
                                "Relief / Writ Type",
                                [
                                    "Quashing of FIR / Proceedings",
                                    "Mandamus (Fair Investigation / Protection)",
                                ],
                                key=f"f_writ_relief_{idx}"
                            )

                            # Session mein save rakhein taaki refresh par data na ude
                            st.session_state[f"persist_crime_no_{idx}"] = crime_no_val
                            st.session_state[f"persist_crime_year_{idx}"] = crime_year_val
                            st.session_state[f"persist_sections_{idx}"] = sections_val

                            if crime_no_val or crime_year_val or sections_val:
                                crime_details_list.append({
                                    "crime_no": crime_no_val,
                                    "crime_year": crime_year_val,
                                    "sections": sections_val,
                                    "nature": nature_val,
                                    "relief": writ_relief_val
                                })

                            if idx < st.session_state.crime_count - 1:
                                st.markdown("---")

                        # ➕ Plus button to add another Crime Detail entry
                        if st.button("➕ Add Another Crime Detail", key="add_crime_detail_btn", use_container_width=True):
                            st.session_state.crime_count += 1
                            st.rerun()



                # --- RIGHT COLUMN: CAVEATOR OR PETITIONER DETAILS ---
                with col_right_form:
                    if active_form == "Caveat Application":
                        st.markdown("##### 👤 Caveator Details")
                        if "caveator_count" not in st.session_state:
                            st.session_state.caveator_count = 1
                        
                        caveators_list = []
                        with st.container(border=True):
                            for c_idx in range(st.session_state.caveator_count):
                                if st.session_state.caveator_count > 1:
                                    st.markdown(f"**🔹 Caveator No. {c_idx+1}**")
                                
                                default_cname = "" if (c_idx > 0 or c_name_mapped == "_____________________") else c_name_mapped
                                default_caddr = "" if (c_idx > 0 or c_addr_mapped == "_____________________") else c_addr_mapped
                                
                                c_name_i = st.text_input(
                                    f"Caveator No. {c_idx+1} Full Name",
                                    placeholder="e.g. NAMAN PANDEY",
                                    value=st.session_state.get(f"persist_cav_name_{c_idx}", default_cname),
                                    key=f"f_caveator_name_{c_idx}"
                                ).upper()
                                
                                c_addr_i = st.text_input(
                                    f"Caveator No. {c_idx+1} Full Address & Attestation",
                                    placeholder="e.g. S/O ..., R/O ...",
                                    value=st.session_state.get(f"persist_cav_addr_{c_idx}", default_caddr),
                                    key=f"f_caveator_addr_{c_idx}"
                                ).upper()
                                
                                st.session_state[f"persist_cav_name_{c_idx}"] = c_name_i
                                st.session_state[f"persist_cav_addr_{c_idx}"] = c_addr_i
                                
                                if c_name_i and c_addr_i:
                                    caveators_list.append((c_name_i, c_addr_i))
                                
                                if c_idx < st.session_state.caveator_count - 1:
                                    st.markdown("---")
                                    
                            if st.button("➕ Add Another Caveator", key="add_caveator_btn", use_container_width=True):
                                st.session_state.caveator_count += 1
                                st.rerun()

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
                # --- FILING / CAVEAT DATE BOX ---
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### 📅 Filing / Caveat Date")
                with st.container(border=True):
                    from datetime import date
                    filing_date_val = st.date_input(
                        "Select Caveat / Filing Date (Will appear opposite to FILED BY)",
                        value=st.session_state.get("persist_filing_date_obj", date.today()),
                        format="DD/MM/YYYY",
                        key="f_filing_date"
                    )
                    st.session_state.persist_filing_date_obj = filing_date_val
                    st.session_state.persist_filing_date = filing_date_val.strftime("%d-%m-%Y")

                # --- FULL WIDTH: EDITABLE LEGAL PARAGRAPHS BLOCK WITH VOICE & AUTO-NUMBERING ---
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### 📝 Additional Custom Legal Paragraphs / Grounds")
                
                if "f_additional_paras" not in st.session_state:
                    st.session_state.f_additional_paras = additional_paras_mapped

                with st.container(border=True):
                    st.write("🎤 **Dictate Paragraph (Click Mic to Record & Stop to Type):**")
                    audio_value = st.audio_input("Record your legal statement", label_visibility="collapsed")
                    
                    if audio_value is not None:
                        audio_id = hash(audio_value.getvalue())
                        if st.session_state.get("last_processed_audio") != audio_id:
                            import speech_recognition as sr
                            import re
                            recognizer = sr.Recognizer()
                            try:
                                with sr.AudioFile(audio_value) as source:
                                    audio_data = recognizer.record(source)
                                    spoken_text = recognizer.recognize_google(audio_data, language="en-IN")
                                    
                                    current_txt = st.session_state.f_additional_paras.rstrip()
                                    # Automatically detect last paragraph number and append on a new numbered line
                                    nums = re.findall(r'(?:^|\n)(\d+)-', current_txt)
                                    if nums:
                                        next_num = int(nums[-1]) + 1
                                        updated_txt = f"{current_txt}\n\n{next_num}- {spoken_text}"
                                    else:
                                        updated_txt = f"{current_txt} {spoken_text}".strip()
                                        
                                    st.session_state.f_additional_paras = updated_txt
                                    st.session_state.persist_additional_paras = updated_txt
                                    st.session_state.last_processed_audio = audio_id
                                    st.rerun()
                            except sr.UnknownValueError:
                                st.warning("⚠️ Could not understand audio. Please speak clearly and try again.")
                            except Exception as e:
                                st.error(f"⚠️ Voice processing error: {e}")

                    additional_paras_input = st.text_area(
                        "If you want to append or edit statement paragraphs, modify them directly below:",
                        key="f_additional_paras",
                        height=180
                    )
                    st.session_state.persist_additional_paras = additional_paras_input

                    import streamlit.components.v1 as secure_bridge_components
                    auto_number_js = """
                    <script>
                    setTimeout(() => {
                        const textareas = window.parent.document.querySelectorAll('textarea');
                        textareas.forEach(textarea => {
                            if (textarea.dataset.autoNumAttached) return;
                            textarea.dataset.autoNumAttached = "true";
                            
                            textarea.addEventListener('keydown', function(e) {
                                if (e.key === 'Enter') {
                                    const pos = this.selectionStart;
                                    const textBefore = this.value.substring(0, pos);
                                    const textAfter = this.value.substring(pos);
                                    
                                    const lines = textBefore.split('\\n');
                                    const lastLine = lines[lines.length - 1].trim();
                                    
                                    const match = lastLine.match(/^(\\d+)-/);
                                    if (match) {
                                        e.preventDefault();
                                        const currentNum = parseInt(match[1], 10);
                                        const nextNum = currentNum + 1;
                                        const insertText = `\n\n${nextNum}- `;
                                        const newValue = textBefore + insertText + textAfter;
                                        
                                        // Use native React value setter so Streamlit state locks the new line permanently
                                        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                                        nativeSetter.call(this, newValue);
                                        this.selectionStart = this.selectionEnd = pos + insertText.length;
                                        this.dispatchEvent(new Event('input', { bubbles: true }));
                                    }
                                }
                            });
                        });
                    }, 800);
                    </script>
                    """
                    secure_bridge_components.html(auto_number_js, height=0)




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
                    elif active_form == "Caveat Application" and not caveators_list:
                        st.sidebar.warning("⚠️ Processing Denied: Please fill at least one Caveator's Name and Address.")
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
                        st.session_state.persist_crime_list = crime_details_list

                        if active_form == "Caveat Application":
                            st.session_state.persist_caveat_category = caveat_category
                            st.session_state.persist_c_name = caveators_list[0][0]
                            st.session_state.persist_c_addr = caveators_list[0][1]
                            if len(caveators_list) == 1:
                                st.session_state.persist_caveators_formatted = f"{caveators_list[0][0]}, {caveators_list[0][1]}"
                            else:
                                st.session_state.persist_caveators_formatted = "\n".join(
                                    [f"{i+1}. {name}, {addr}" for i, (name, addr) in enumerate(caveators_list)]
                                )
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
                    button[data-testid="stCopyButton"] { display: none !important; }
                    </style>
                """, unsafe_allow_html=True)

                from datetime import datetime
                today_str = st.session_state.get("persist_filing_date", datetime.now().strftime("%d-%m-%Y"))

                exp_p_compiled = st.session_state.get("persist_exp_p_formatted", "1. _____________________")
                r_compiled = st.session_state.get("persist_r_formatted", "1. _____________________")
                p_compiled = st.session_state.get("persist_p_formatted", "1. _____________________")
                custom_paras_section = f"\n\n{additional_paras_mapped}" if additional_paras_mapped.strip() else ""

                # Advocate details form se nikalna
                adv_full_block = []
                # Advocate details form se nikalna (Right side ke liye)
                adv_full_block = []
                for idx in range(st.session_state.get("counsel_count", 1)):
                    a_name = st.session_state.get(f"f_adv_name_{idx}", "").strip()
                    a_roll = st.session_state.get(f"f_adv_roll_{idx}", "").strip()
                    a_cham = st.session_state.get(f"f_adv_chamber_{idx}", "").strip()
                    a_mob = st.session_state.get(f"f_adv_phone_{idx}", "").strip()
                    if a_name:
                        # Naam ke aage ADV. lagayein taaki right alignment match ho
                        disp_name = a_name if a_name.upper().startswith("ADV.") else f"ADV. {a_name}"
                        adv_full_block.append(disp_name)
                        if a_roll:
                            adv_full_block.append(f"Adv. Roll: {a_roll}")
                        if a_cham:
                            # Chamber ke aage Chamber: lagayein taaki right alignment match ho
                            disp_cham = a_cham if "CHAMBER" in a_cham.upper() else f"Chamber: {a_cham}"
                            adv_full_block.append(disp_cham)
                        if a_mob:
                            adv_full_block.append(f"Mob: {a_mob}")
                        adv_full_block.append("")
                adv_signature_text = "\n".join(adv_full_block).strip() if adv_full_block else f"ADV. {st.session_state.username.upper()}"

                if '(' in provision_mapped:
                    provision_text = provision_mapped.split('(')[0].strip().upper()
                else:
                    provision_text = provision_mapped.upper()

                caveat_cat_mapped = st.session_state.get("persist_caveat_category", "Civil")
                caveat_title_line = f"{caveat_cat_mapped} Misc. Caveat Application No. ______ of {datetime.now().year}"
                misc_petition_line = f"IN\nProposed Misc. Petition No. ______ of {datetime.now().year} ({caveat_cat_mapped})"
                if active_form == "Caveat Application":
                    final_document_string = f"""IN THE HIGH COURT OF JUDICATURE AT ALLAHABAD
***********
{caveat_title_line}
(Under Section 148-A C.P.C. read with Rule 5, Chapter XXII of High Court Rules)

On behalf of:
{st.session_state.get("persist_caveators_formatted", f"{c_name_mapped}, {c_addr_mapped}")}
---- Applicant / Caveator


{misc_petition_line}
(Under {provision_text})

DISTRICT – {district_mapped}

{exp_p_compiled}
---- Proposed Petitioner / Plaintiff

VERSUS

{r_compiled}
---- Proposed Opposite Party / Respondent

TO,
    The Hon'ble Chief Justice and his other companion Judges of the aforesaid Court.

    The humble application of the above-named Applicant / Caveator most respectfully showeth as under:

1- That in the above-noted proposed petition/application, the Proposed Petitioner is likely to file a petition before this Hon'ble Court against the order dated {order_date_mapped} passed by the Court below, District {district_mapped}.{custom_paras_section}

PRAYER:
    It is, therefore, most respectfully prayed that this Hon'ble Court may graciously be pleased to direct that no ex-parte order or ad-interim relief be granted to the Proposed Petitioner / Opposite Parties without giving prior due notice and an opportunity of being heard to the Caveator or his Counsel.

SPLIT_ROW|DATED: {today_str}|FILED BY:
{adv_signature_text}
COUNSEL FOR APPLICANT / CAVEATOR"""

                else:
                    final_document_string = f"""BEFORE THE HON'BLE {st.session_state.selected_court.upper()}
DISTRICT: {district_mapped}

IN THE MATTER OF:
{p_compiled}
---- Petitioner(s)

VERSUS

{r_compiled}
---- Respondent(s)

APPLICATION FOR {active_form.upper()} UNDER {provision_mapped}."""

                st.markdown(f"### 🏛️ Legal Paper Preview Stage (8.5\" x 14\"): **{active_form}**")

                act_col1, act_col2 = st.columns(2)
                with act_col1:
                    if st.button("⬅ Return to Editor Layout Panel", use_container_width=True):
                        st.session_state.canvas_sub_page = "editor"
                        st.rerun()

                bold_lines = [
                    "IN THE HIGH COURT OF JUDICATURE AT ALLAHABAD",
                    "***********",
                    caveat_title_line
                ]

                center_screen_lines = [
                    "IN THE HIGH COURT",
                    "***********",
                    "Caveat Application No.",
                    "(Under Section 148-A",
                    *[line for line in st.session_state.get("persist_caveators_formatted", c_name_mapped).split("\n") if line.strip()],
                    "On behalf of:",
                    "Proposed Misc. Petition",
                    "(Under ",
                    "VERSUS",
                    "PRAYER:",
                    "BEFORE THE HON'BLE",
                    "APPLICATION FOR"
                ]

                right_screen_lines = [
                    "DISTRICT –",
                    "---- Applicant",
                    "---- Proposed Petitioner",
                    "---- Proposed Opposite Party",
                    "---- Petitioner(s)",
                    "---- Respondent(s)",
                    "FILED BY:",
                    "ADV.",
                    "Adv. Roll:",
                    "Chamber:",
                    "CHAMBER",
                    "Mob:",
                    "COUNSEL FOR",
                ]

                import re
                formatted_html_lines = []
                for line in final_document_string.split("\n"):
                    stripped = line.strip()
                    if stripped == "":
                        formatted_html_lines.append("<div style='height: 14px;'></div>")
                        continue
                formatted_html_lines = []
                for line in final_document_string.split("\n"):
                    stripped = line.strip()
                    if stripped == "":
                        formatted_html_lines.append("<div style='height: 14px;'></div>")
                        continue
                    elif stripped.startswith("SPLIT_ROW|"):
                        _, left_part, right_part = stripped.split("|")
                        formatted_html_lines.append(
                            f"<div style='display: flex; justify-content: space-between; width: 100%;'>"
                            f"<span>{left_part}</span><span>{right_part}</span></div>"
                        )
                        continue

                    content = f"<b>{stripped}</b>" if any(b_text in stripped for b_text in bold_lines) else stripped

                    if stripped == "IN" or any(c_text in stripped for c_text in center_screen_lines):
                        formatted_html_lines.append(f"<div style='text-align: center;'>{content}</div>")
                    elif any(r_text.upper() in stripped.upper() for r_text in right_screen_lines):
                        formatted_html_lines.append(f"<div style='text-align: right;'>{content}</div>")
                    elif re.match(r'^\d+-', stripped):
                        # Har numbered paragraph ke neeche 2-line ka proper court gap
                        formatted_html_lines.append(f"<div style='text-align: justify; margin-bottom: 18px;'>{content}</div>")
                    else:
                        formatted_html_lines.append(f"<div style='text-align: justify;'>{content}</div>")

                preview_body_html = "".join(formatted_html_lines)



                st.markdown("---")
                st.markdown(
                    f"""
                    <div style="
                        font-family: 'Times New Roman', Times, serif;
                        font-size: 14pt;
                        line-height: 2.0;
                        background-color: #ffffff;
                        color: #000000;
                        border: 1px solid #cbd5e1;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                        max-width: 850px;
                        margin: auto;
                        padding: 60px 70px;
                        white-space: pre-wrap;
                    ">{preview_body_html}</div>
                    """,
                    unsafe_allow_html=True
                )
                # =======================================================
                # LEGAL PAPER PDF GENERATOR (8.5 x 14 INCHES, COMPLETE)
                # =======================================================
                try:
                    import re
                    from fpdf import FPDF

                    # Legal Paper Size: 215.9 mm x 355.6 mm
                    pdf = FPDF(format=(215.9, 355.6), unit="mm")
                    left_m = 38.1   # 1.5 inch left binding margin
                    right_m = 25.4  # 1 inch right margin
                    top_m = 25.4    # 1 inch top margin
                    usable_w = 215.9 - left_m - right_m  # Exact 152.4 mm width

                    pdf.set_margins(left=left_m, top=top_m, right=right_m)
                    pdf.set_auto_page_break(auto=True, margin=25.4)
                    pdf.add_page()

                    clean_text = (
                        final_document_string.replace("–", "-")
                        .replace("—", "-")
                        .replace("`", "'")
                        .replace("’", "'")
                        .replace("“", '"')
                        .replace("”", '"')
                    )
                    safe_text = clean_text.encode("latin-1", "replace").decode("latin-1")

                    center_keywords = [
                        "IN THE HIGH COURT",
                        "***********",
                        "Caveat Application No.",
                        "(Under Section 148-A",
                        "On behalf of:",
                        *[line for line in st.session_state.get("persist_caveators_formatted", c_name_mapped).split("\n")if line.strip()],
                        "Proposed Misc. Petition",
                        "(Under ",
                        "VERSUS",
                        "PRAYER:",
                        "BEFORE THE HON'BLE",
                        "APPLICATION FOR"
                    ]

                    right_keywords = [
                        "DISTRICT -",
                        "---- Applicant",
                        "---- Proposed Petitioner",
                        "---- Proposed Opposite Party",
                        "---- Petitioner(s)",
                        "---- Respondent(s)",
                        "FILED BY:",
                        "ADV.",
                        "Adv. Roll:",
                        "Chamber:",
                        "CHAMBER",
                        "Mob:",
                        "COUNSEL FOR",
                    ]

                    for raw_line in safe_text.split("\n"):
                        stripped = raw_line.strip()

                        if stripped == "":
                            pdf.ln(4)
                            continue

                        pdf.set_x(left_m)

                        if any(b_text in stripped for b_text in bold_lines):
                            pdf.set_font("Times", style="B", size=14)
                        else:
                            pdf.set_font("Times", style="", size=14)

                        if stripped.startswith("SPLIT_ROW|"):
                            _, left_part, right_part = stripped.split("|")
                            current_y = pdf.get_y()
                            pdf.cell(usable_w / 2, 9, text=left_part, align="L")
                            pdf.set_xy(left_m + (usable_w / 2), current_y)
                            pdf.cell(usable_w / 2, 9, text=right_part, align="R", new_x="LMARGIN", new_y="NEXT")
                        elif stripped == "IN" or any(c_key in stripped for c_key in center_keywords):
                            pdf.multi_cell(usable_w, 9, text=stripped, align="C")

                        elif any(r_key.upper() in stripped.upper() for r_key in right_keywords):
                            pdf.multi_cell(usable_w, 8, text=stripped, align="R")
                        elif re.match(r'^\d+-', stripped):
                            pdf.multi_cell(usable_w, 10, text=stripped, align="J")
                            pdf.ln(6)
                        elif stripped.startswith("It is, therefore"):
                            pdf.multi_cell(usable_w, 10, text=stripped, align="J")
                        else:
                            pdf.multi_cell(usable_w, 9, text=stripped, align="L")

                    real_pdf_bytes = bytes(pdf.output())

                    with act_col2:
                        st.download_button(
                            label="📥 Download Legal Paper PDF (8.5\" x 14\")",
                            data=real_pdf_bytes,
                            file_name=f"{active_form.lower().replace(' ', '_')}_legal.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                except Exception as pdf_err:
                    with act_col2:
                        st.error(f"⚠️ PDF Error: {pdf_err}")




# =======================================================
# GLOBAL PERSISTENT FOOTER (APPEARS ON EVERY PAGE)
# =======================================================
if elapsed_time >= 2.5:
    @st.dialog("Helpdesk Support")
    def global_helpdesk_popup():
        st.write("Need assistance with Krilex legal drafting or account recovery? Check quick tips below or send us a direct message.")
        
        st.markdown("""
        **Quick Help:**
        * **OTP Not Received?** Check your Gmail Spam folder or wait 90 seconds to resend.
        * **PDF Formatting:** Ensure all required fields are filled before generating the preview.
        """)
        
        st.info("Direct Email: support@krilex.com | Response Time: Within 24 Hours")

        with st.form("popup_helpdesk_form", clear_on_submit=True):
            u_contact = st.text_input("Your Email or Phone Number")
            u_issue = st.text_area("Describe Your Issue", height=80)
            if st.form_submit_button("Send Support Request", type="primary", use_container_width=True):
                if u_contact and u_issue:
                    import requests
                    try:
                        requests.post(
                            "https://formsubmit.co",
                            json={
                                "contact": u_contact,
                                "issue": u_issue,
                                "_subject": "Krilex Helpdesk Support Ticket"
                            },
                            timeout=5
                        )
                    except Exception:
                        pass
                    st.success("Your request has been sent! Our support team will contact you soon.")
                else:
                    st.warning("Please enter both your contact details and issue.")

    @st.dialog("About Krilex")
    def global_about_popup():
        st.write(
            "Krilex is a legal drafting application engineered to simplify and digitalize procedural drafting "
            "workflows across Indian court systems."
        )
        st.markdown("""
        **Why Choose Krilex?**
        * **Court-Ready Formatting:** Instant generation of Caveat, Stay, and Writ petitions in standard Times New Roman (Size 14).
        * **Smart Drafting Tools:** Built-in voice dictation and auto-numbering to save manual typing hours.
        * **100% Secure & Confidential:** Protected with two-step OTP verification so your client details stay private.
        """)

    st.markdown("""
        <style>
        .krilex-dark-footer {
            background-color: #1F2937;
            color: #F3F4F6;
            padding: 22px 20px 10px 20px;
            border-radius: 8px 8px 0 0;
            margin-top: 40px;
            text-align: center;
        }
        div[data-testid="stHorizontalBlock"]:has(button[kind="tertiary"]) {
            background-color: #1F2937;
            padding: 5px 20px 20px 20px;
            border-radius: 0 0 8px 8px;
            margin-top: -16px;
        }
        button[kind="tertiary"] {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            padding: 0px !important;
            min-height: 0px !important;
        }
        button[kind="tertiary"]:hover {
            color: #93C5FD !important;
            text-decoration: underline !important;
        }
        </style>
        <div class="krilex-dark-footer">
            <p style="margin: 0 0 8px 0; font-size: 13px; color: #D1D5DB;">Support: support@krilex.com</p>
            <p style="margin: 0; font-size: 12px; color: #9CA3AF;">© 2026 Krilex Legal Tech Solution. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

    sp_left, col_f1, col_f2, col_f3, sp_right = st.columns([3, 1, 1, 1, 3])
    with col_f1:
        if st.button("Home", key="global_footer_home", type="tertiary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "main"
            st.session_state.active_app_tile = None
            st.rerun()
    with col_f2:
        if st.button("Helpdesk", key="global_footer_helpdesk", type="tertiary", use_container_width=True):
            global_helpdesk_popup()
    with col_f3:
        if st.button("About", key="global_footer_about", type="tertiary", use_container_width=True):
            global_about_popup()

                
