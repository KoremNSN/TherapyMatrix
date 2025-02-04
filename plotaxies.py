import streamlit as st
import pandas as pd
import plotly.express as px
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import io

st.title("Interactive Data Playground")

# Initialize example data
df = pd.read_csv('therapies.csv')

# Allow users to edit
edited_df = st.data_editor(df, num_rows='dynamic')

# Plot from edited_df, not df
fig = px.scatter(
    edited_df,
    x="Closeness",
    y="Intensity",
    error_x="SD X",
    error_y="SD Y",
    hover_name="Name",
    text='Name',
    title="Scatter Plot with Standard Deviations"
)

# Add black lines at x=0, y=0
fig.add_vline(x=0, line_color="black")
fig.add_hline(y=0, line_color="black")

# Enhance label styling
fig.update_traces(
    textposition="top left",
    textfont=dict(
        family="Arial Black",
        size=14,
        color="black"
    )
)

fig.update_layout(
    xaxis_title="<b>Closeness</b>",
    yaxis_title="<b>Intensity</b>",
    xaxis=dict(range=[0, 10]),
    yaxis=dict(range=[0, 10]),
    font=dict(
        family="Arial",  # Set a font
        size=14,         # Set the font size
    )
)

st.plotly_chart(fig)

# --- EMAIL FORM ---
st.write("**Send the final table**")

username = st.secrets["email_credentials"]["email"]
password = st.secrets["email_credentials"]["token"]

with st.form(key="email_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    user_email = st.text_input("Your Email")
    date_filled = st.date_input()

    submit_button = st.form_submit_button(label="Send final response")

    if submit_button:
        # Build CSV from current edited DataFrame
        csv_buffer = io.StringIO()
        edited_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        csv_content = csv_buffer.read()

        # Construct the email
        msg = MIMEMultipart()
        msg["From"] = "nawow1@gmail.com"         
        msg["To"] = "nawow1@gmail.com"           # The fixed recipient
        msg["Subject"] = "Edited Data CSV"

        # Email body: includes user name, last name, and their email
        body_text = (
            f"Hello,\n\n"
            f"The user has entered:\n"
            f"Name: {first_name} {last_name}\n"
            f"Email: {user_email}\n\n"
            f"Date: {date_filled}\n\n"
            f"Below is the current CSV data:\n\n"
            f"{csv_content}"
        )
        msg.attach(MIMEText(body_text, "plain"))

        # Send the email (Gmail example with SSL)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                # For production, use secrets or environment variables
                server.login(username, password)
                server.send_message(msg)
            st.success("CSV table sent to Dori Rubinstein PhD!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
