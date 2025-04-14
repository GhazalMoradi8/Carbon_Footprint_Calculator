import streamlit as st
import re

# --- App Config ---
st.set_page_config(
    page_title="Green Tomorrow",
    page_icon="🌿",
    layout="centered"
)

# --- Force Logo to Appear at Top of Sidebar ---
st.markdown("""
    <style>
        /* --- Sidebar Logo --- */
        [data-testid="stSidebar"]::before {
            content: ""; display: block;
            background-image: url('https://raw.githubusercontent.com/GhazalMoradi8/Carbon_Footprint_Calculator/main/GreenPrint_logo.png');
            background-size: 90% auto; background-repeat: no-repeat;
            background-position: center; height: 140px;
            margin: 1.5rem auto -4rem auto;
        }
        section[data-testid="stSidebar"] { background-color: #d6f5ec; }
        .stApp { background-color: white; }

        /* --- Tab-like Radio Buttons --- */
        div[role="radiogroup"] > label > div:first-child { display: none; }
        div[role="radiogroup"] > label {
            margin: 0 !important; padding: 0.5rem 1rem; border: 1px solid #ddd;
            border-bottom: none; border-radius: 5px 5px 0 0; background-color: #f0f2f6;
            cursor: pointer; transition: background-color 0.3s ease;
        }
        div[role="radiogroup"] > label:hover { background-color: #e0e2e6; }

        /* --- Control the color of the selected tab --- */
        div[role="radiogroup"] input[type="radio"]:checked + label {
            background-color: #f0f2f6;
            font-weight: bold;
            color: #52a58a;  /* Change the color of selected tab text (Green in this case) */
        }

        /* --- Add bottom border for tabs container --- */
        div.stRadio > div {
            border-bottom: 1px solid #ddd;
            padding-bottom: 1rem;
        }

        /* --- Styling for the Next and Previous buttons --- */
        div[data-testid="stButton"] button {
            background-color: #61c2a2;  /* Green background */
            color: white;              /* White text */
            border: none;
            padding: 0.5rem 1rem;      /* Adjust padding */
            border-radius: 0.25rem;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #52a58a;  /* Darker green on hover */
        }

        /* Focus state for buttons */
        div[data-testid="stButton"] button:focus {
            outline: none;  /* Remove the default focus outline */
            box-shadow: 0 0 0 0.3rem rgba(26, 152, 80, 0.5); /* Green shadow on focus */
        }

    </style>
""", unsafe_allow_html=True)

# ✅ Fixed Email Validation
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


# --- Profile Page Content ---
st.title("Create Your Profile")
st.write("Please fill out the following information to help us calculate your carbon footprint.")

# Profile Form
with st.form("profile_form"):
    name = st.text_input("Your Name *", key="name")
    age = st.number_input("Age *", min_value=0, max_value=120, step=1, key="age")
    gender = st.selectbox("Gender *", ["-- Select --", "Female", "Male", "Other", "Prefer not to say"], key="gender")
    email = st.text_input("Email Address *", key="email")
    consent = st.checkbox("I agree to participate in the carbon footprint analysis and share anonymous data for research.", key="consent")

    submitted = st.form_submit_button("Save Profile")

# --- Handle Form Submission ---
if submitted:
    if not name or not email or gender == "-- Select --":
        st.warning("⚠️ Please fill in all required fields.")
    elif age == 0:
        st.warning("⚠️ Please enter a valid age.")
    elif not email:
        st.warning("⚠️ Please enter a valid email address.")
    else:
        st.success(f"Thank you, {name}! Your profile has been saved.")

        # Save user profile in session state
        st.session_state["user_profile"] = {
            "name": name,
            "age": age,
            "gender": gender,
            "email": email,
            "consent": consent
        }

      
        # ✅ Trigger "redirect" to calculator page
        st.session_state["go_to_calculator"] = True
        st.rerun()  

# --- Simulated Redirect ---
if st.session_state.get("go_to_calculator"):
    st.session_state["go_to_calculator"] = False  # reset flag

    st.markdown("✅ Profile saved. Redirecting to Calculator page...")
    st.markdown(
        """
        <meta http-equiv="refresh" content="0; url=/Calculator">
        """,
        unsafe_allow_html=True
    )
