import streamlit as st

# Set page configuration
st.set_page_config(page_title="Data Science Dashboard", layout="wide")

# Mock user credentials
USERNAME = "harippriya"
PASSWORD = "hp"

# CSS for centered layout and background for all pages
page_bg_css = """
<style>
body {
    background-image: url("background_image.png"); /* Replace with your background image */
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
.centered-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #333;
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# Initialize session state for login
if "login" not in st.session_state:
    st.session_state["login"] = False

# Login form
if not st.session_state["login"]:
    st.title("Login")
    
    # Center-align the login fields using Streamlit columns
    col1, col2 = st.columns([2, 1.5])
    with col1:
        username = st.text_input("Username")
    with col2:
        password = st.text_input("Password", type="password")
    
    # Login button
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["login"] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")
else:
    # Home page with centered introduction
    st.markdown('<div class="centered-content">', unsafe_allow_html=True)
    st.image("home_icon.png", use_column_width=False, width=100)  # Add home page icon
    st.title("Welcome to the Air Quality Dashboard")
    st.write("""
        This dashboard provides insights into air quality levels worldwide, helping you monitor environmental 
        conditions and promote awareness about pollution and its effects on public health.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Button to go to the dashboard
    if st.button("Go to Dashboard"):
        st.session_state["show_dashboard"] = True

    # Power BI Dashboard
    if "show_dashboard" in st.session_state and st.session_state["show_dashboard"]:
        st.title("Air Quality Dashboard")
        st.write("This is an embedded Power BI dashboard for monitoring global air quality.")

        # Embed Power BI dashboard as an HTML iframe
        powerbi_dashboard_url = "https://app.powerbi.com/reportEmbed?reportId=0646091c-5577-4334-ab61-c39588ab8d97&autoAuth=true&ctid=8fcbc147-4e0b-4bf5-94ab-bc5733d4b8ed"
        st.components.v1.html(
            f"""
            <iframe title="Air_Quality" width="1140" height="541.25" src="{powerbi_dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
            """,
            height=800,
        )

        # Download buttons
        st.write("### Download Data")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(label="Download CSV", data="sample_csv_data", file_name="air_quality.csv", mime="text/csv")
        with col2:
            st.download_button(label="Download Power BI File", data="sample_powerbi_data", file_name="air_quality.pbix", mime="application/octet-stream")

        # Feedback and rating section with checkboxes
        st.write("### Feedback & Rating")
        feedback = st.text_area("Please share your feedback here:")
        rating = st.radio("Rate our dashboard:", [1, 2, 3, 4, 5], index=2)
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")

    # Logout button
    if st.button("Logout"):
        st.session_state["login"] = False
        st.session_state["show_dashboard"] = False
