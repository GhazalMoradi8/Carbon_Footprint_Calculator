import streamlit as st

# --- App Config ---
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
# --- Page Title ---
st.title("Welcome to GreenPrint")
st.subheader("Your Personal Carbon Footprint Tracker")

# --- Intro Content ---
st.markdown("""
 
**GreenPrint** is your interactive guide to understanding and reducing your environmental impact.  
With just a few quick questions about how you **live, travel, eat**, and **consume resources**, you'll get:

<br>

✅ **A personalized estimate** of your yearly carbon emissions  
📊 **A clear breakdown** of which habits contribute the most  
🌍 **Comparisons** with your country, Europe, and global averages  
🌞 **Practical tips** to reduce your footprint and live more sustainably.  

<br>

You can also

<be>

📄 **Download a PDF report** containing your calculation and personalized recommendations  
🤖 **Use GreenPrint AI** to help answer your questions about your carbon footprint and offer real-time advice.

<br>

Whether you're just curious or committed to climate action, **GreenPrint** is here to support your journey.

---

### 🔍 What is a Carbon Footprint?

Your **carbon footprint** is the total amount of **greenhouse gases** released into the air because of your everyday activities.

Common activities like:

- 🏠 **Using energy at home** (heating, electricity)
- 🚗 **Getting around** (cars, buses, flights)
- 🍔 **What you eat** (especially meat and dairy)
- 🛍️ **What you buy and throw away** (clothes, electronics, waste)

Your footprint shows how much your actions contribute to climate change. By understanding your footprint, you can take steps to reduce it and make more sustainable choices!

---

### 🚨 Why It Matters

At **GreenPrint**, we believe that our planet is finite, and sustainability is crucial for our future. The consumption of resources leads to greenhouse gas emissions, which are responsible for global warming. These emissions contribute to environmental challenges such as:

- 🌊 Floods
- 🔥 Forest fires
- 🌵 Droughts
- ⚔️ Conflict
- 🌍 Ecological damage

<be>

The higher your carbon footprint, the more you contribute to these issues. By understanding your emissions, you can:

- 🌍 **Reduce your environmental impact**
- 💰 **Save money** through efficient choices
- 🌱 **Join the global effort** to fight climate change and protect the planet 


---

### 🛠️ How This App Works

1. Go to the **Profile** page and create your profile
2. Use the **Calculator** to enter details about your daily habits, get an estimate of your **annual carbon footprint**, and compare your score to **national and global averages**.  
3. Go to **Breakdown** page to see more details about your carbon footprint and receive personalized suggestions on how to **reduce** it.
4. Ask your questions from **GreenPrint AI** for real-time advice on reducing your carbon footprint.

---

### 🌿 Ready to make a difference?

Let's get started! **Click Next →** to begin creating your profile and take the first step in reducing your carbon footprint.
""", unsafe_allow_html=True)

# --- Simulated Redirect to Profile using query param ---
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    if st.button("Next →", use_container_width=False):
        st.experimental_set_query_params(page="Profile")
        st.markdown('<meta http-equiv="refresh" content="0;url=./Profile">', unsafe_allow_html=True)
