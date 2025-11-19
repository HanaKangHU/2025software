import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('countriesMBTI_16types.csv')

st.title("MBTI Distribution by Country")

# Select country
country = st.selectbox("Select a country", df['Country'].unique())

country_data = df[df['Country'] == country].iloc[0]
mbti_types = df.columns[1:]
values = country_data[1:].values

# Create dataframe for plotting
plot_df = pd.DataFrame({
    'MBTI': mbti_types,
    'Value': values
})

# Determine colors (1st place = red, others gradient)
plot_df = plot_df.sort_values('Value', ascending=False)
colors = ['red'] + ['rgba(255,150,150,{})'.format(1 - i/len(plot_df)) for i in range(1, len(plot_df))]

fig = px.bar(plot_df, x='MBTI', y='Value', title=f"MBTI Distribution in {country}")
fig.update_traces(marker_color=colors)

st.plotly_chart(fig)
