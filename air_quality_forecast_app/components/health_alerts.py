import streamlit as st

import streamlit as st

def display_health_alert(pm25_value):
    if pm25_value is None:
        st.info("PM2.5 forecast not available for health advisory.")
        return

    # Simplified AQI categories and health advisories based on EPA standards
    # Values are approximate for demonstration
    if pm25_value <= 12.0:
        st.success(f"**Good Air Quality ({pm25_value:.2f} µg/m³):** Air quality is satisfactory, and air pollution poses little or no risk. Enjoy outdoor activities!")
    elif pm25_value <= 35.4:
        st.info(f"**Moderate Air Quality ({pm25_value:.2f} µg/m³):** Air quality is acceptable; however, there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.")
        st.markdown("- **Recommendations:** Unusually sensitive people should consider limiting prolonged outdoor exertion.")
    elif pm25_value <= 55.4:
        st.warning(f"**Unhealthy for Sensitive Groups ({pm25_value:.2f} µg/m³):** Members of sensitive groups may experience health effects. The general public is less likely to be affected.")
        st.markdown("- **Recommendations:** People with heart or lung disease, older adults, and children should reduce prolonged or heavy exertion. Consider wearing a mask outdoors.")
    elif pm25_value <= 150.4:
        st.error(f"**Unhealthy Air Quality ({pm25_value:.2f} µg/m³):** Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.")
        st.markdown("- **Recommendations:** Everyone should reduce prolonged or heavy exertion. Sensitive groups should avoid all outdoor exertion. Keep windows closed and use air purifiers if available.")
    elif pm25_value <= 250.4:
        st.error(f"**Very Unhealthy Air Quality ({pm25_value:.2f} µg/m³):** Health warnings of emergency conditions. The entire population is more likely to be affected.")
        st.markdown("- **Recommendations:** Everyone should avoid all outdoor exertion. Remain indoors and keep activities light. Use N95 masks if you must go outside.")
    else:
        st.error(f"**Hazardous Air Quality ({pm25_value:.2f} µg/m³):** Health alert: everyone may experience more serious health effects.")
        st.markdown("- **Recommendations:** Everyone should avoid all outdoor physical activity. Stay indoors, keep windows and doors closed, and use air purifiers. Seek medical attention if you experience breathing difficulties.")