import streamlit as st

def display_carbon_footprint_estimator(key_prefix=""):
    st.markdown("#### 👣 Carbon Footprint Estimator")
    st.markdown("Estimate your carbon footprint based on your daily activities. All values are for **monthly** consumption unless specified.")

    st.markdown("--- ")

    # Home Energy Consumption
    st.markdown("##### 🏠 Home Energy")
    col1, col2 = st.columns(2)
    with col1:
        electricity_kwh = st.number_input("Electricity (kWh)", min_value=0.0, value=100.0, key=f"{key_prefix}electricity_kwh", help="Average monthly electricity consumption in kilowatt-hours.")
    with col2:
        natural_gas_therms = st.number_input("Natural Gas (therms)", min_value=0.0, value=50.0, key=f"{key_prefix}natural_gas_therms", help="Average monthly natural gas consumption in therms.")

    st.markdown("##### 🚗 Transportation")
    col3, col4 = st.columns(2)
    with col3:
        car_miles = st.number_input("Car Travel (miles)", min_value=0.0, value=500.0, key=f"{key_prefix}car_miles", help="Average monthly miles driven by car.")
        bus_miles = st.number_input("Bus Travel (miles)", min_value=0.0, value=50.0, key=f"{key_prefix}bus_miles", help="Average monthly miles traveled by bus.")
    with col4:
        flights_short = st.number_input("Short-haul Flights (per year)", min_value=0, value=0, key=f"{key_prefix}flights_short", help="Number of short-haul flights taken per year (e.g., < 3 hours).")
        flights_long = st.number_input("Long-haul Flights (per year)", min_value=0, value=0, key=f"{key_prefix}flights_long", help="Number of long-haul flights taken per year (e.g., > 3 hours).")

    st.markdown("--- ")

    # Simple emission factors (these are illustrative and can be refined)
    # Source: EPA, various online calculators (values are approximate)
    emission_factor_electricity = 0.4  # kg CO2e/kWh
    emission_factor_natural_gas = 5.3  # kg CO2e/therm
    emission_factor_car = 0.17   # kg CO2e/mile (average car)
    emission_factor_bus = 0.1    # kg CO2e/mile
    emission_factor_flight_short = 100 # kg CO2e/flight (illustrative)
    emission_factor_flight_long = 500  # kg CO2e/flight (illustrative)

    total_carbon_footprint = (
        (electricity_kwh * emission_factor_electricity) +
        (natural_gas_therms * emission_factor_natural_gas) +
        (car_miles * emission_factor_car) +
        (bus_miles * emission_factor_bus) +
        (flights_short * emission_factor_flight_short / 12) + # Convert yearly to monthly
        (flights_long * emission_factor_flight_long / 12)      # Convert yearly to monthly
    )

    st.markdown(f"## 📊 Estimated Monthly Carbon Footprint: <span style='color: var(--primary-color);;'>{total_carbon_footprint:.2f} kg CO2e</span>", unsafe_allow_html=True)

    st.info("This is an estimation based on simplified factors. For a more accurate calculation, consider using a dedicated carbon footprint calculator.")
