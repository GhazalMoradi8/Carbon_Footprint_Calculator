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
        /* --- Styling for all buttons --- */
        div[data-testid="stButton"] button {
            background-color: #61c2a2;  /* Green background */
            color: white;               /* White text */
            border: none;
            padding: 0.5rem 1rem;       /* Adjust padding */
            border-radius: 0.25rem;
            cursor: pointer;
        }

        div[data-testid="stButton"] button:hover {
            background-color: #52a58a;  /* Darker green on hover */
        }

        div[data-testid="stButton"] button:focus {
            outline: none;              /* Remove the default focus outline */
            box-shadow: 0 0 0 0.3rem rgba(26, 152, 80, 0.5); /* Green shadow on focus */
        }

        /* Apply custom styles to the form submit button specifically */
        div[data-testid="stFormSubmitButton"] button {
            background-color: #61c2a2;
            color: white;
            border: none;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            background-color: #52a58a;
        }

        div[data-testid="stFormSubmitButton"] button:focus {
            outline: none;
            box-shadow: 0 0 0 0.3rem rgba(26, 152, 80, 0.5);
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
