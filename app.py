import streamlit as st # type: ignore
import random
import sqlite3
import hashlib
import os


# ------------------------------
# DATABASE SETUP
# ------------------------------
conn = sqlite3.connect('farmer_data.db', check_same_thread=False)
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    address TEXT,
    land_proof TEXT,
    bank_details TEXT,
    farming_type TEXT,
    credit_history TEXT,
    verification_doc TEXT,
    interests TEXT,
    agreement TEXT,
    role TEXT NOT NULL,
    org_role TEXT,
    gov_id TEXT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)''')

# Create user credentials table (if needed for Aadhaar-based login)
c.execute('''CREATE TABLE IF NOT EXISTS user_credentials (
    aadhaar TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
)''')

# Create loan history table
c.execute('''CREATE TABLE IF NOT EXISTS loan_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aadhaar TEXT,
    name TEXT,
    amount REAL,
    status TEXT,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP
)''')


# Create credit cards table
c.execute('''CREATE TABLE IF NOT EXISTS credit_cards (
    aadhaar TEXT,
    card_number TEXT,
    limit_amount REAL,
    activation_code TEXT,
    status TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS contributor_rates (
    id INTEGER PRIMARY KEY,
    contributor_username TEXT,
    preferred_rate REAL
)''')
c.execute('''CREATE TABLE IF NOT EXISTS contributor_rates (
    id INTEGER PRIMARY KEY,
    contributor_username TEXT,
    preferred_rate REAL
)
''')
c.execute('''CREATE TABLE IF NOT EXISTS contributor_rates (
    id INTEGER PRIMARY KEY,
    contributor_username TEXT,
    preferred_rate REAL
);
''')


conn.commit()


# ------------------------------
# HELPER FUNCTIONS
# ------------------------------

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    """Verifies the username and password against the database."""
    hashed_pw = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = c.fetchone()
    return user  # Return the user if login is successful, otherwise None


# ------------------------------
# STREAMLIT UI SETUP
# ------------------------------
st.set_page_config(page_title="AgriToken Exchange: Bridging Farmers and Contributors", layout="wide")

import base64

def set_background(image_path, opacity=0.5):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = f"""
    <style>
        /* Full-page background */
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})),
                        url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Ensure content is visible and properly aligned */
        .block-container {{
            padding-top: 2rem !important;  /* Adjust space below the Streamlit header */
            padding-bottom: 2rem !important;
        }}

        /* Remove extra margins that cause gaps */
        header, .st-emotion-cache-z5fcl4 {{
            display: none !important; /* Hides the default Streamlit header */
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set full-page background with adjusted spacing
set_background("background.avif", opacity=0.5) 

# ------------------------------
# SIDEBAR MENU
# ------------------------------
sidebar_img_path = "credit.jpg"  # Replace with your actual path

if os.path.exists(sidebar_img_path):
    st.sidebar.image(sidebar_img_path, use_container_width=True)
else:
    st.sidebar.error("❗ Sidebar image not found! Check the path.")

st.sidebar.title("🌱 AgriToken Exchange: Bridging Farmers and Contributors")

menu = st.sidebar.radio("Choose a feature:", [
    "🏠 Home", 
    "⚙️ Features", 
    "👥 Register", 
    "🔑 Login", 
    "💸 Loan Application",
    "✅ Verification", 
    "💬 Feedback System"
])


# ------------------------------
# MAIN CONTENT BASED ON MENU SELECTION
# ------------------------------

if menu == "🏠 Home":
    # ------------------------------
    # HOME PAGE CONTENT
    # ------------------------------
    home_img_path = "crop_image.jpg"
    st.title("🏡 Welcome to the Tenant Farmer Loan Management System")
    if os.path.exists(home_img_path):
        st.image(home_img_path, use_container_width=True)
    else:
        st.error("❗ Home page image not found! Check the path.")

    
elif menu == "⚙️ Features":
    st.title("✨ System Features Overview")
    
    # Using tabs for different categories of features
    tab1, tab2, tab3 = st.tabs(["Core Features", "User Management", "Analytics & Feedback"])

    with tab1:
        st.markdown("#### Core Features")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("👤 **User Registration**")
            st.write("Register new users with roles and details.")
            
            st.markdown("💸 **Loan Application**")
            st.write("Apply for loans by specifying the amount and details.")
            
            st.markdown("🤖 **Risk Assessment**")
            st.write("AI-based risk analysis for loan approval.")

        with col2:
            st.markdown("💳 **Credit Card Issuance**")
            st.write("Issue credit cards with set limits for users.")
            
            st.markdown("🔐 **Card Activation**")
            st.write("Activate issued cards with one-time code.")

    with tab2:
        st.markdown("#### User Management")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("👤 **User Profile Management**")
            st.write("Manage and view user details.")

        with col2:
            st.markdown("📚 **Loan History**")
            st.write("Track and manage previous loan applications.")

    with tab3:
        st.markdown("#### Analytics & Feedback")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("📊 **Dashboard & Reporting**")
            st.write("View statistics and loan summary reports.")

        with col2:
            st.markdown("📝 **Feedback System**")
            st.write("Allow users to submit feedback on services.")


##########register
elif menu == "👥 Register":
    st.title("User Registration")

    role = st.selectbox("Select Role", ["Farmer", "Contributor", "Admin"])

    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    hashed_pw = hash_password(password)

    if role == "Farmer":
        age = st.number_input("Age", min_value=18, max_value=100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        land_proof = st.file_uploader("Land Ownership Proof")
        bank_details = st.text_input("Bank Account Details")
        farming_type = st.text_input("Type of Farming")
        credit_history = st.text_area("Credit History")

        if st.button("Register Farmer"):
            if full_name and username and password and phone and age and gender and address and land_proof and bank_details and farming_type and credit_history:
                try:
                    c.execute('''INSERT INTO users (full_name, phone, age, gender, address, land_proof, bank_details, farming_type, credit_history, role, username, password)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (full_name, phone, age, gender, address, land_proof.name if land_proof else None,
                               bank_details, farming_type, credit_history, role, username, hashed_pw))
                    conn.commit()
                    st.success("Farmer registered successfully! Please login.")
                except sqlite3.Error as e:
                    st.error(f"Database error: {e}")
            else:
                st.error("Please fill out all the required fields.")

    elif role == "Contributor":
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        verification_doc = st.file_uploader("Verification Document")
        interests = st.text_area("Areas of Interest")
        agreement = st.checkbox("I agree to the terms and compliance")
        preferred_rate = st.number_input("Preferred Rate of Interest (%)", min_value=0.0, max_value=20.0, step=0.1)

        if st.button("Register Contributor"):
            if full_name and username and password and phone and email and verification_doc and interests and agreement:
                if agreement:
                    try:
                        # Insert contributor details into users table
                        c.execute('''INSERT INTO users (full_name, email, phone, verification_doc, interests, agreement, role, username, password)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                  (full_name, email, phone, verification_doc.name if verification_doc else None,
                                   interests, str(agreement), role, username, hashed_pw))
                        conn.commit()

                        # Insert preferred rate into contributor_rates table
                        c.execute('''INSERT INTO contributor_rates (contributor_username, preferred_rate)
                                     VALUES (?, ?)''', (username, preferred_rate))
                        conn.commit()
                        st.success("Contributor registered successfully! Please login.")
                    except sqlite3.Error as e:
                        st.error(f"Database error: {e}")
                else:
                    st.error("You must agree to the terms and compliance.")
            else:
                st.error("Please fill out all required fields.")

elif menu == "🔑 Login":
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user = verify_login(username, password)
        if user:
            st.success(f"Welcome back, {user[1]}! You are logged in as {user[14]}.")  # Changed index to 14 for 'role'
            # Store user information in session state for other pages
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['role'] = user[14]  # Role is at index 14

        else:
            st.error("Invalid username or password.")

# ------------------------------
# LOAN APPLICATION NAVIGATION
# ------------------------------
elif menu == "💸 Loan Application":
    st.title("💸 Loan Application")
    st.write("Empowering Farmers through Accessible Loans")

    # Check if the user is logged in as a farmer
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        role = st.session_state.get('role', None)
        if role == "Farmer":
            # Apply a vibrant background color
            st.markdown("""
                <style>
                    .loan-container {
                        padding: 20px;
                        background-color: #f0f8ff; /* Light Azure */
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="loan-container">', unsafe_allow_html=True)
            st.subheader("Apply for Loan")
            col1, col2 = st.columns([3, 2])  # Adjust column widths for balance

            with col1:  # Main Loan Application Form
                with st.container(): # Use a container for grouping form fields
                    purpose_of_loan = st.text_input("Purpose of Loan", placeholder="e.g., Purchase seeds", help="Describe the loan's purpose")
                    loan_amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=100.0, help="Enter desired loan amount")
                    repayment_period = st.selectbox("Repayment Period", ["6 months", "1 year", "2 years", "3 years", "5 years"], help="Select repayment duration")

                with st.container():
                    annual_income = st.number_input("Annual Income (₹)", min_value=0.0, step=1000.0, help="Enter annual income")
                    existing_loans = st.number_input("Existing Loan Amount (₹)", min_value=0.0, step=1000.0, help="Existing loan amounts")
                    collateral_details = st.text_area("Collateral Details (if applicable)", placeholder="Describe collateral", help="Details of collateral offered")

                with st.container():  # Contributor Section
                    st.subheader("Select a Contributor")
                    c.execute("SELECT u.username, u.interests, u.agreement, cr.preferred_rate FROM users u JOIN contributor_rates cr ON u.username = cr.contributor_username WHERE u.role = 'Contributor'")
                    contributors = c.fetchall()

                    if contributors:
                        contributor_options = {contributor[0]: f"{contributor[0]} - {contributor[1]} - {contributor[2]} - Rate: {contributor[3]}%" for contributor in contributors}
                        selected_contributor = st.selectbox("Choose a Contributor", list(contributor_options.keys()), help="Select a contributor")

                        c.execute("SELECT preferred_rate FROM contributor_rates WHERE contributor_username = ?", (selected_contributor,))
                        preferred_rate = c.fetchone()[0]
                        st.success(f"Selected Contributor's Preferred Rate of Interest: {preferred_rate}%")
                    else:
                        st.error("No contributors available.")

                    # Add Loan Approval and Repayment details as an expander within the container for organization
                    with st.expander("ℹ️ Loan Approval Process & Repayment Conditions"):
                        st.markdown(
                            """
                            **Loan Approval Process:**
                            - Your application will be reviewed by our team.
                            - Field verification may occur.
                            - Creditworthiness assessment will be conducted.
                            - Notification of the outcome via email/SMS.

                            **Loan Repayment Conditions:**
                            - Repayments as per agreed schedule.
                            - Penalties for late payments.
                            - Pre-closure charges may apply for early repayment.
                            """
                        )

            with col2:  # EMI Calculator
                with st.container(): # Group Calculator elements
                    st.subheader("📊 EMI Calculator")
                    with st.expander("Calculate Your EMI", expanded=True):  # Keep it open by default
                        calculator_loan_amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=100.0, key="calculator_amount", help="Loan Amount")
                        calculator_interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=20.0, step=0.1, key="calculator_rate", help="Interest Rate")
                        calculator_repayment_period = st.selectbox("Repayment Period", ["6 months", "1 year", "2 years", "3 years", "5 years"], key="calculator_period", help="Repayment Period")

                        if st.button("Calculate EMI", key="calculate_emi"):
                            # Dynamic Conversion to Months
                            months = int(calculator_repayment_period.split(" ")[0]) * (12 if "year" in calculator_repayment_period else 1)
                            monthly_interest_rate = (calculator_interest_rate / 100) / 12

                            emi = calculator_loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** months / ((1 + monthly_interest_rate) ** months - 1)
                            emi = round(emi, 2)

                            st.metric("Estimated EMI", f"₹{emi}")  # Using metric for prominence

            # Place the submit button outside the columns
            if st.button("Submit Loan Application", use_container_width=True):  # Make it a full-width button
                if purpose_of_loan and loan_amount > 0 and annual_income > 0:
                    try:
                        c.execute('''INSERT INTO loan_history (aadhaar, name, amount, status)
                                     VALUES (?, ?, ?, ?)''',
                                  (st.session_state['username'], purpose_of_loan, loan_amount, "Pending"))
                        conn.commit()
                        st.success("✅ Your loan application has been submitted successfully!")
                    except sqlite3.Error as e:
                        st.error(f"Database error: {e}")
                else:
                    st.error("❗ Please fill out all required fields correctly.")

            st.markdown('</div>', unsafe_allow_html=True) # Closing the container

        else:
            st.warning("This section is only accessible to farmers.")
    else:
        st.warning("Please log in as a farmer to access this section.")


######verificatio

elif menu == "✅ Verification":
    st.title("🔍 Loan Verification")

    # Check if the user is logged in as an admin
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        role = st.session_state.get('role', None)
        if role == "Admin":
            st.subheader("Manage Loan Applications")

            # Fetch all pending loan applications
            c.execute("SELECT * FROM loan_history WHERE status = 'Pending'")
            pending_applications = c.fetchall()

            if pending_applications:
                for application in pending_applications:
                    st.write(f"Application ID: {application[0]}")
                    st.write(f"Aadhaar: {application[1]}")
                    st.write(f"Name: {application[2]}")
                    st.write(f"Amount: ₹{application[3]}")

                    # Approval/Rejection Options
                    approval_status = st.selectbox("Status", ["Approve", "Reject"], key=f"approval_{application[0]}")

                    if st.button("Update Status", key=f"update_{application[0]}"):
                        if approval_status == "Approve":
                            c.execute("UPDATE loan_history SET status = 'Approved' WHERE id = ?", (application[0],))
                            conn.commit()
                            st.success("Application approved successfully!")
                        elif approval_status == "Reject":
                            c.execute("UPDATE loan_history SET status = 'Rejected' WHERE id = ?", (application[0],))
                            conn.commit()
                            st.success("Application rejected successfully!")
            else:
                st.info("No pending applications found.")
        else:
            st.warning("This section is only accessible to admins.")
    else:
        st.warning("Please log in as an admin to access this section.")
# ------------------------------
# FEEDBACK SYSTEM
# ------------------------------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # For Gmail
SMTP_PORT = 587
SENDER_EMAIL = "rathodvidyar@gmail.com"  # Your email
SENDER_PASSWORD = "zabh trfm eqmp zolr"  # Your email password or app password
RECEIVER_EMAIL = "rathodvidyar@gmail.com"  # Email where feedback will be sent

def send_feedback(feedback):
    subject = "New Feedback from Tenant Farmer Loan App"
    message = f"User Feedback:\n\n{feedback}"

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending feedback: {e}")
        return False


# Add Feedback System to menu
if menu == "💬 Feedback System":
    st.title("📝 Feedback System")
    feedback = st.text_area("Enter your feedback or suggestions:")
    
    if st.button("Submit Feedback"):
        if feedback.strip():
            if send_feedback(feedback):
                st.success("✅ Thank you for your feedback! It has been sent to the admin via email.")
            else:
                st.error("❌ Failed to send feedback. Please try again later.")
        else:
            st.error("⚠️ Please enter feedback before submitting.")
