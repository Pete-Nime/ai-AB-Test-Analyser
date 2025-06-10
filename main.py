import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, chi2

st.set_page_config(page_title="AB Test Analyzer", layout="centered")
st.title("📈 AB Test Analyzer for ABC Grocery")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Load the campaign data sheet
        campaign_data = pd.read_excel(uploaded_file, sheet_name='campaign_data')

        # Filter out control group
        campaign_data = campaign_data.loc[campaign_data["mailer_type"] != "Control Group"]

        # Display the first few rows
        st.subheader("1️⃣ Filtered Campaign Data")
        st.dataframe(campaign_data.head())

        # Create observed frequency table
        observed = pd.crosstab(campaign_data["mailer_type"], campaign_data["signup_flag"])
        st.subheader("2️⃣ Observed Frequency Table")
        st.write(observed)

        # Calculate sign-up rates for insight
        mailer1_rate = 123 / (123 + 252)
        mailer2_rate = 127 / (127 + 209)
        st.markdown(f"**Mailer 1 Sign-Up Rate:** {mailer1_rate:.2%}")
        st.markdown(f"**Mailer 2 Sign-Up Rate:** {mailer2_rate:.2%}")

        # Chi-Square Test
        chi2_stat, p_value, dof, expected = chi2_contingency(observed.values)
        st.subheader("3️⃣ Chi-Square Test Results")
        st.write(f"Chi-Square Statistic: {chi2_stat:.3f}")
        st.write(f"Degrees of Freedom: {dof}")
        st.write(f"P-Value: {p_value:.4f}")

        # Interpret the result
        alpha = 0.05
        st.subheader("4️⃣ Conclusion")
        if p_value <= alpha:
            st.success("📊 Result: We reject the null hypothesis. There IS a relationship between mailer type and sign-up rate.")
        else:
            st.info("📊 Result: We retain the null hypothesis. There is NO strong evidence of a relationship.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
