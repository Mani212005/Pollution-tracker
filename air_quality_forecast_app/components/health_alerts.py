import streamlit as st

def display_health_alert(predicted_pm25):
    """
    Displays health alerts based on forecasted PM2.5 values, aligned with US EPA AQI categories.
    """
    st.markdown("#### Health Advisory:")

    if predicted_pm25 is None:
        st.info("No forecast available to provide health advisory.")
        return

    if predicted_pm25 <= 12.0:
        st.success("**AQI Category: Good**")
        st.write("Air quality is satisfactory, and air pollution poses little or no risk.")
        st.write("\n_Enjoy your outdoor activities!_\n")
    elif predicted_pm25 <= 35.4:
        st.info("**AQI Category: Moderate**")
        st.write("Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.")
        st.write("\n_Consider reducing prolonged or heavy exertion if you are unusually sensitive._\n")
    elif predicted_pm25 <= 55.4:
        st.warning("**AQI Category: Unhealthy for Sensitive Groups**")
        st.write("Members of sensitive groups may experience health effects. The general public is less likely to be affected.")
        st.write("\n_People with lung disease (such as asthma), heart disease, older adults, and children should limit prolonged or heavy outdoor exertion._\n")
    elif predicted_pm25 <= 150.4:
        st.error("**AQI Category: Unhealthy**")
        st.write("Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.")
        st.write("\n_Sensitive groups should avoid all outdoor exertion. Everyone else should limit prolonged or heavy outdoor exertion._\n")
    elif predicted_pm25 <= 250.4:
        st.error("**AQI Category: Very Unhealthy**")
        st.write("Health warnings of emergency conditions. The entire population is more likely to be affected.")
        st.write("\n_Sensitive groups should remain indoors and keep activity levels low. Everyone else should avoid all outdoor exertion._\n")
    else:
        st.error("**AQI Category: Hazardous**")
        st.write("Health alert: everyone may experience more serious health effects.")
        st.write("\n_Everyone should avoid all outdoor exertion. Consider wearing an N95 mask if you must go outside._\n")