import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

# Create two columns: one for the title and one for the logo
col1, col2 = st.columns([10, 1], vertical_alignment="bottom")

with col1:
    st.title("Artisma Dash")

with col2:
    logo_path = "Artisma+Transperant+WHITE.png"
    st.image(logo_path, width=170)


# Load the data
df = pd.read_csv("Project_List.csv")

# Convert 'Invoice Date' to datetime
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])

# Sort the DataFrame by 'Invoice Date' for proper cumulative sum calculation
df = df.sort_values(by='Invoice Date')

# Extract the week from the invoice date
df['Invoice Week'] = df['Invoice Date'].dt.to_period('W').apply(lambda r: r.start_time)

# Group by the invoice week and status, then sum the invoice amounts
grouped_df = df.groupby(['Invoice Week', 'Status'])['Invoice Amount'].sum().reset_index()

# Define the color mapping for each status
color_discrete_map = {
    'Proposed': '#69bbdc',  # Assuming Pending should be Proposed
    'Confirmed': '#de945f',
    'Complete': '#d969bc',
    'Paid': '#9adc9f'
}

# Create a stacked bar chart with custom colors
bar_fig = px.bar(
    grouped_df,
    x='Invoice Week',
    y='Invoice Amount',
    color='Status',
    title="Weekly Revenue",
    labels={'Invoice Week': 'Invoice Date Week', 'Invoice Amount': 'Invoice Amount ($)'},
    color_discrete_map=color_discrete_map
)

# Set the default tool to pan for the bar chart
bar_fig.update_layout(
    dragmode="pan"
)

# Calculate the cumulative sum of the 'Invoice Amount'
df['Cumulative Invoice Amount'] = df['Invoice Amount'].cumsum()

# Create an area chart using go.Scatter for more control
area_fig = go.Figure()

area_fig.add_trace(go.Scatter(
    x=df['Invoice Date'],
    y=df['Cumulative Invoice Amount'],
    mode='lines',
    line=dict(color='#9adc9f', width=4),  # Thicker line
    fill='tozeroy',
    fillcolor='rgba(154, 220, 159, 0.6)',  # Fill with 60% transparency
    name="Cumulative Invoice Amount",
    line_shape='spline'  # Smooth interpolation
))

# Set the layout for the area chart
area_fig.update_layout(
    title="Cumulative Revenue",
    xaxis_title="Invoice Date",
    yaxis_title="Cumulative Invoice Amount ($)",
    dragmode="pan",
    height=900
)

# Display the bar chart first
st.plotly_chart(bar_fig)

# Display the area chart below the bar chart
st.plotly_chart(area_fig)
