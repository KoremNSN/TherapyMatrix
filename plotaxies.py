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