import streamlit as st
import smtplib
from email.mime.text import MIMEText
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Mock user credentials
USERNAME = "harippriya"
PASSWORD = "hp"

# Background CSS
page_bg = """
<style>
body {
    background-image: url("background.webp");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Initialize session states
if "login" not in st.session_state:
    st.session_state["login"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Drill-through navigation (arrow buttons) for pages after login
def drill_through_navigation():
    if st.session_state["page"] != "home":
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            if st.button("← Back"):
                st.session_state["page"] = "home" if st.session_state["page"] == "dashboard" else "dashboard"

# Login form
if not st.session_state["login"]:
    st.title("Login")
    
    # Column layout for username and password fields
    col1, col2 = st.columns([2, 1.5])
    with col1:
        username = st.text_input("Username")
    with col2:
        password = st.text_input("Password", type="password")
    
    # Login button
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["login"] = True
            st.session_state["page"] = "home"
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

# Home Page after login
elif st.session_state["page"] == "home":
    st.title("HOME")
    st.title("Welcome to the Air Quality Dashboard")
    st.write("""
        The Air Quality Insights Dashboard allows users to monitor, analyze, and understand
        the current state of air quality through real-time data visualization.
        
        Our system tracks various air quality indicators, including:
        - PM2.5 and PM10 (particulate matter)
        - NO, NO2, NOx, NH3 (nitrogen compounds)
        - CO, SO2 (carbon monoxide and sulfur dioxide)

        Using this data, users can better understand pollution trends and take action toward 
        creating a cleaner and healthier environment.
    """)
    
    # Go to Dashboard button with arrow
    if st.button("➡️ Go to Dashboard"):
        st.session_state["page"] = "dashboard"

# Dashboard Page
# Dashboard Page
# Dashboard Page
elif st.session_state["page"] == "dashboard":
    st.title("Air Quality Dashboard")
    st.write("This is an embedded Power BI dashboard for monitoring global air quality.")
    
    drill_through_navigation()  # Add drill-through navigation

    # CSS to center-align the iframe
    st.markdown("""
    <style>
    .dashboard-iframe {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: -20px;  /* Reduce space before Download Data section */
    }
    </style>
    """, unsafe_allow_html=True)

    # Embed Power BI dashboard with even larger dimensions
    powerbi_dashboard_url = "https://app.powerbi.com/reportEmbed?reportId=0646091c-5577-4334-ab61-c39588ab8d97&autoAuth=true&ctid=8fcbc147-4e0b-4bf5-94ab-bc5733d4b8ed"
    st.components.v1.html(
        f"""
        <iframe title="Air_Quality" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=0646091c-5577-4334-ab61-c39588ab8d97&autoAuth=true&ctid=8fcbc147-4e0b-4bf5-94ab-bc5733d4b8ed" frameborder="0" allowFullScreen="true"></iframe>
        """,
        height=950,  # Adjust the height to make it larger and center it vertically
    )

    # Reduced space before Download buttons, bringing it closer to the dashboard
    st.markdown("### Download Data")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(label="Download CSV", data="sample_csv_data", file_name="air_quality.csv", mime="text/csv")
    with col2:
        st.download_button(label="Download Power BI File", data="sample_powerbi_data", file_name="air_quality.pbix", mime="application/octet-stream")

    
    # Feedback Form button
    if st.button("Feedback Form"):
        st.session_state["page"] = "feedback"
# Feedback Form Page (last page with Logout button)
elif st.session_state["page"] == "feedback":
    st.title("Feedback Form")

    # Add a Back button to navigate back to the dashboard
    if st.button("← Back to Dashboard"):
        st.session_state["page"] = "dashboard"

    # Feedback section using star rating
    st.header("Rate Your Experience")
    rating = st.slider("Select your rating (1 to 5)", min_value=1, max_value=5)
    
    def display_star_rating(rating):
        return "⭐" * rating
    
    st.write(f"Your rating: {display_star_rating(rating)} ({rating}/5)")

    # Speedometer chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rating,
        title={"text": "Rating"},
        gauge={
            "axis": {"range": [None, 5]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 1], "color": "lightcoral"},
                {"range": [1, 3], "color": "yellow"},
                {"range": [3, 5], "color": "lightgreen"}
            ],
        }
    ))
    st.plotly_chart(fig)

    # Additional feedback checkboxes
    st.header("Additional Feedback")
    easy_to_use = st.checkbox("The air quality data presented is clear and easy to understand")
    user_friendly = st.checkbox("The interface is user-friendly & download options for data are useful")
    recommend = st.checkbox("The colors and visuals used are appealing")

   
    
    subject = st.text_input('Name')
    body = st.text_area('Message')

    # Send Email button
    if st.button("Send Email"):
        try:
            msg = MIMEText(body)
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            st.success('Email sent successfully! 🚀')
        except Exception as e:
            st.error(f"Error sending email: {e}")

    # Logout button (only visible on Feedback page)
    if st.button("Logout"):
        st.session_state["login"] = False
        st.session_state["page"] = "login"
