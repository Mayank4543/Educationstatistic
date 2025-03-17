import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from pymongo import MongoClient
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(layout='wide', page_title='Education Statistics')
st.sidebar.title("Education Statistics")
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["feedback_db"]
collection = db["feedback_collection"]

uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV format)")

# ✅ Session state variable to track whether analysis is shown
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = pd.Index(df.columns).to_series().where(~df.columns.duplicated(), df.columns + '_dup')

    # Sidebar buttons
    if st.sidebar.button("Show Analysis"):
        st.snow()  
        st.session_state.show_analysis = True  

    show_comparison = st.sidebar.button("Show Comparison")

    if st.session_state.show_analysis:
        st.write("### Uploaded Dataset")
        st.dataframe(df)
        # ✅ Handling missing values
        for col in ["Lakh of Population per Institution (University)", 
                    "Lakh of Population per Institution (College)", 
                    "Lakh of Population per Institution (Technical)"]:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())

        # ✅ Remove unwanted column if present
        if "Unnamed: 7" in df.columns:
            df.drop(columns=["Unnamed: 7"], inplace=True)

        # ✅ Convert to numeric (if needed)
        df_numeric = df.select_dtypes(include=['number'])

        # ✅ State-wise Literacy Rate using Plotly
        st.write('<span style="color:#a300cc;">🔁 State-wise Literacy Rate</span>', unsafe_allow_html=True)
        if "State" in df.columns and "Literacy Rate" in df.columns:
            crosstab_data = pd.crosstab(df["State"], df["Literacy Rate"], normalize='columns') * 100
            fig2 = px.imshow(crosstab_data,
                            labels=dict(x="Literacy Rate", y="State", color="Percentage"),
                            x=crosstab_data.columns,
                            y=crosstab_data.index,
                            color_continuous_scale="plasma")

            fig2.update_layout(title="State-wise Literacy Rate Distribution")
            st.plotly_chart(fig2)

        # ✅ Choropleth Map
        st.write("### State-wise Literacy Rate in India (Choropleth Map)")
        geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"

        if "State" in df.columns and "Literacy Rate" in df.columns:
            fig = px.choropleth(df, 
                                geojson=geojson_url,  
                                locations="State",
                                featureidkey="properties.NAME_1",
                                color="Literacy Rate",
                                color_continuous_scale="greens")

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(title="State-wise Literacy Rate in India")
            st.plotly_chart(fig)

        # ✅ Scatter plot using Plotly (Fixed duplicate column error)
        st.write("### Scatter Plot with Regression Line")
        if not df_numeric.empty:
            feature_x = st.selectbox("Select X-axis Feature", df_numeric.columns, key="x_axis")
            feature_y = st.selectbox("Select Y-axis Feature", df_numeric.columns, key="y_axis")

            fig3 = px.scatter(df, x=feature_x, y=feature_y, trendline="ols",
                              labels={feature_x: feature_x, feature_y: feature_y})
            fig3.update_layout(title=f"{feature_x} vs {feature_y} with Regression Line")
            st.plotly_chart(fig3)

      
        st.write("## Share Your Feedback")

        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        feedback_text = st.text_area("Feedback")

        if st.button("Submit Feedback"):
            if full_name and email and feedback_text:
                feedback_data = {
                    "Full Name": full_name,
                    "Email": email,
                    "Feedback": feedback_text
                }
                collection.insert_one(feedback_data) 
                st.success("Thank you for your feedback!")
            else:
                st.error("Please fill out all fields before submitting.")

    # ✅ Comparison Feature (Always Available)
    if show_comparison:
        if "State" in df.columns and "Literacy Rate" in df.columns:
            sorted_df = df.sort_values(by='Literacy Rate', ascending=False)
            top_literacy_states = sorted_df.head(5)
            bottom_literacy_states = sorted_df.tail(5)

            literacy_comparison = pd.concat([top_literacy_states, bottom_literacy_states])

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Literacy Rate', y='State', data=literacy_comparison, palette='viridis', ax=ax)
            ax.set_title('Top 5 and Bottom 5 States by Literacy Rate')
            ax.set_xlabel('Literacy Rate (%)')
            ax.set_ylabel('State')
            st.pyplot(fig)

       
        if "Pupil Teacher Ratio" in df.columns and "State" in df.columns:
            sorted_ratio_df = df.sort_values(by='Pupil Teacher Ratio')
            best_ratio_states = sorted_ratio_df.head(5)
            worst_ratio_states = sorted_ratio_df.tail(5)
            ratio_comparison = pd.concat([best_ratio_states, worst_ratio_states])

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Pupil Teacher Ratio', y='State', data=ratio_comparison, palette='coolwarm', ax=ax)
            ax.set_title('Top 5 and Bottom 5 States by Pupil-Teacher Ratio')
            ax.set_xlabel('Pupil-Teacher Ratio')
            ax.set_ylabel('State')
            st.pyplot(fig)
        else:
            st.warning("⚠️ 'Pupil Teacher Ratio' column not found in the dataset!")

else:

    url = "https://assets9.lottiefiles.com/packages/lf20_M9p23l.json"
    lottie_json = requests.get(url).json()
    st_lottie(lottie_json, loop=True)
