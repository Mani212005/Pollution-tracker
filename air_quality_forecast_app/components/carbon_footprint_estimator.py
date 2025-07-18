import streamlit as st

def display_carbon_footprint_estimator():
    """
    Displays a simplified carbon footprint estimator based on user inputs.
    """
    st.markdown("#### Carbon Footprint Estimator (Simplified)")
    st.info("Estimate your approximate carbon emissions based on a few daily habits.")

    st.subheader("Transportation")
    commute_distance = st.slider("Daily Commute Distance (km)", 0, 100, 10)
    commute_mode = st.selectbox("Primary Commute Mode", ["Car", "Motorcycle", "Public Transport", "Bicycle/Walk"])

    st.subheader("Electricity Consumption")
    monthly_electricity_bill = st.slider("Average Monthly Electricity Bill (INR)", 0, 5000, 1000)

    # --- Simplified Calculation Logic (Arbitrary values for demonstration) ---
    # These values are illustrative and not based on scientific data.
    carbon_emissions = 0.0 # in kg CO2e per month

    # Transportation emissions
    if commute_mode == "Car":
        carbon_emissions += commute_distance * 30 * 0.2 # 0.2 kg CO2e/km for car
    elif commute_mode == "Motorcycle":
        carbon_emissions += commute_distance * 30 * 0.1 # 0.1 kg CO2e/km for motorcycle
    elif commute_mode == "Public Transport":
        carbon_emissions += commute_distance * 30 * 0.05 # 0.05 kg CO2e/km for public transport
    # Bicycle/Walk has negligible direct emissions

    # Electricity emissions (assuming a conversion factor for INR to kWh and then to CO2e)
    # This is highly simplified. Real conversion factors vary by region and energy source.
    carbon_emissions += (monthly_electricity_bill / 10) * 0.5 # Assuming 10 INR/kWh and 0.5 kg CO2e/kWh

    st.subheader("Your Estimated Monthly Carbon Footprint")
    st.metric(label="Estimated CO2e Emissions", value=f"{carbon_emissions:.2f} kg CO2e/month")

    st.markdown("""
    _Note: This is a highly simplified estimation for demonstration purposes only.
    Actual carbon footprints depend on many more factors and require more precise data.
    The values used here are arbitrary._
    """)

    


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Carbon Footprint Estimator Test")
    display_carbon_footprint_estimator()