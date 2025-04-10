import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- App Config ---
st.set_page_config(
    page_title="Green Tomorrow",
    page_icon="🌿",
    layout="centered"
)

# --- Sidebar Logo Styling ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"]::before {
            content: "";
            display: block;
            background-image: url('https://raw.githubusercontent.com/GhazalMoradi8/Carbon_Footprint_Calculator/main/GreenPrint_logo.png');
            background-size: 90% auto;
            background-repeat: no-repeat;
            background-position: center;
            height: 140px;
            margin: 1.5rem auto -4rem auto;
        }

        section[data-testid="stSidebar"] {
            background-color: #d6f5ec;
        }

        .stApp {
            background-color: white;
        }

        .button-row button {
            margin: 0 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load Data ---
csv_url = "https://raw.githubusercontent.com/keanyaoha/Final_Project_WBS/main/emission_factor_formated.csv"
csv_url_1 = "https://raw.githubusercontent.com/keanyaoha/Final_Project_WBS/main/per_capita_filtered_monthly.csv"

try:
    df = pd.read_csv(csv_url)
    df1 = pd.read_csv(csv_url_1)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

available_countries = [col for col in df.columns if col != "Activity"]

# --- Format Activity Names ---
def format_activity_name(activity):
    mapping = {
        "Domestic flight": "How many km of Domestic Flights taken the last month",
        "International flight": "How many km of International Flights taken the last month",
        "km_diesel_local_passenger_train_traveled": "How many km traveled by diesel-powered local passenger trains",
        "km_diesel_long_distance_passenger_train_traveled": "How many km traveled by diesel-powered long-distance passenger trains",
        "km_electric_passenger_train_traveled": "How many km traveled by electric-powered passenger trains",
        "km_bus_traveled": "How many km traveled by bus",
        "km_petrol_car_traveled": "How many km traveled by petrol-powered car",
        "km_Motorcycle_traveled": "How many km traveled by motorcycle",
        "km_ev_scooter_traveled": "How many km traveled by electric scooter",
        "km_ev_car_traveled": "How many km traveled by electric-powered car",
        "diesel_car_traveled": "How many km traveled by diesel-powered car",
        "water_consumed": "How much water consumed in liters",
        "electricity_used": "How much electricity used in kWh",
        "hotel_stay": "How many nights stayed in hotels"
    }
    return mapping.get(activity, activity.replace("_", " ").capitalize())

# --- App Interface ---
st.title("Carbon Footprint Calculator")
st.markdown("Calculate your carbon footprint and compare it to national and global averages!")

st.markdown("### 🌍 Select your country of residence:")
def_country = "-- Select --"
country = st.selectbox(" ", [def_country] + available_countries)

if country != def_country:
    st.success("✅ **Next steps:**\nPlease go through the **Travel**, **Food**, **Energy & Water**, and **Other** tabs.\nFill in any values relevant to you. When you're ready, click *“Calculate My Carbon Footprint”* at the bottom.")

    if "tab_index" not in st.session_state:
        st.session_state.tab_index = 0

    tabs = ["🚗 Travel", "🥦 Food", "⚡ Energy & Water", "🏨 Other"]
    current_tab = st.session_state.tab_index

    st.header(tabs[current_tab].split(" ", 1)[1])

    if current_tab == 0:
        for activity in [
            "Domestic flight", "International flight", "km_diesel_local_passenger_train_traveled",
            "km_diesel_long_distance_passenger_train_traveled", "km_electric_passenger_train_traveled",
            "km_bus_traveled", "km_petrol_car_traveled", "km_Motorcycle_traveled",
            "km_ev_scooter_traveled", "km_ev_car_traveled", "diesel_car_traveled"
        ]:
            st.number_input(format_activity_name(activity), min_value=0.0, key=f"travel_{activity}")

    elif current_tab == 1:
        diet_type = st.selectbox("🥗 What is your diet type?", ["Select...", "Vegan", "Vegetarian", "Pescatarian", "Omnivore", "Heavy Meat Eater"])
        if diet_type != "Select...":
            st.markdown("#### Please enter your monthly consumption for the following foods:")
            base_foods = ["processed_rice_consumed", "sugar_consumed", "vegetable_oils_fats_consumed", "other_food_products_consumed", "beverages_consumed"]
            diet_foods = {
                "Vegan": [],
                "Vegetarian": ["dairy_products_consumed", "other_meat_products_consumed"],
                "Pescatarian": ["fish_products_consumed", "dairy_products_consumed"],
                "Omnivore": ["beef_products_consumed", "poultry_products_consumed", "pork_products_consumed", "dairy_products_consumed", "fish_products_consumed"],
                "Heavy Meat Eater": ["beef_products_consumed", "poultry_products_consumed", "pork_products_consumed", "dairy_products_consumed", "fish_products_consumed", "other_meat_products_consumed"]
            }
            food_activities = base_foods + diet_foods.get(diet_type, [])
            for activity in food_activities:
                label = activity.replace("_", " ").replace("products", "").replace("consumed", "").strip().capitalize()
                st.number_input(f"{label}", min_value=0.0, key=f"food_{activity}", format="%.1f")

    elif current_tab == 2:
        for activity in ["electricity_used", "water_consumed"]:
            st.number_input(format_activity_name(activity), min_value=0.0, key=f"energy_{activity}")

    elif current_tab == 3:
        st.number_input(format_activity_name("hotel_stay"), min_value=0.0, key="other_hotel_stay")
        st.markdown("---")
        confirmed = st.checkbox("I have reviewed all fields and want to calculate my footprint")
        calculate = st.button("Calculate My Carbon Footprint", disabled=not confirmed)

        if calculate:
            st.session_state.emission_values = {}
            for key in st.session_state.keys():
                if "_" in key and any(key.startswith(p) for p in ["travel_", "food_", "energy_", "other_"]):
                    activity_name = key.split("_", 1)[1]
                    if activity_name in df["Activity"].values:
                        factor = df.loc[df["Activity"] == activity_name, country].values[0]
                        user_input = st.session_state[key]
                        st.session_state.emission_values[activity_name] = user_input * factor

            total_emission = sum(st.session_state.emission_values.values())
            st.subheader(f"🌍 Your Carbon Footprint: {total_emission:.1f} kg CO₂")

            trees_cut = total_emission / 21.77
            st.markdown(f"🌳 **Equivalent to cutting down ~{trees_cut:.0f} trees!**")

            def get_avg(name):
                row = df1[df1["Country"] == name]
                return row["PerCapitaCO2"].values[0] if not row.empty else None

            country_avg = get_avg(country)
            eu_avg = get_avg("European Union (27)")
            world_avg = get_avg("World")

            labels = ['You', country, 'EU', 'World']
            values = [total_emission, country_avg or 0, eu_avg or 0, world_avg or 0]
            colors = ['#4CAF50' if total_emission < values[3] else '#FF4B4B'] + ['#4682B4'] * 3

            labels, values, colors = labels[::-1], values[::-1], colors[::-1]
            fig, ax = plt.subplots(figsize=(8, 3.2))
            bars = ax.barh(labels, values, color=colors, height=0.6)
            ax.set_xlim(0, max(values) * 1.1)
            for bar in bars:
                ax.annotate(f'{bar.get_width():.1f}', xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                            xytext=(5, 0), textcoords='offset points', ha='left', va='center')
            ax.set_xlabel("Tons CO₂ per year")
            ax.xaxis.grid(True, linestyle='--', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            st.markdown("<div style='text-align: center; color: gray;'>Comparison of your estimated annual carbon footprint with national and global averages.</div>", unsafe_allow_html=True)

    # --- Navigation Buttons ---
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        prev_disabled = current_tab == 0
        next_disabled = current_tab == len(tabs) - 1
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("← Previous", disabled=prev_disabled, use_container_width=True):
                st.session_state.tab_index -= 1
                st.rerun()
        with col_next:
            if st.button("Next →", disabled=next_disabled, use_container_width=True):
                st.session_state.tab_index += 1
                st.rerun()
