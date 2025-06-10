import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, chi2

st.set_page_config(page_title="AB Test Analyzer", layout="centered")
st.title("📊 Assessing Campaign Performance Using Chi-Square Test For Independence")

uploaded_file = st.file_uploader("Upload your Excel file (grocery_database.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # IMPORT DATA
        campaign_data = pd.read_excel(uploaded_file, sheet_name='campaign_data')

        # FILTER OUR DATA
        campaign_data = campaign_data.loc[campaign_data["mailer_type"] != "Control"]

        # DISPLAY HEAD
        st.subheader("📄 Filtered Campaign Data")
        st.dataframe(campaign_data.head())

        # SUMMARISE TO GET OUR OBSERVED FREQUENCIES 2x2 metric
        observed_values_df = pd.crosstab(campaign_data["mailer_type"], campaign_data["signup_flag"])
        observed_values = observed_values_df.values

        st.subheader("📊 Observed Frequency Table")
        st.write(observed_values_df)

        # SIGN-UP RATES
        mailer1_signup_rate = 123 / (252 + 123)
        mailer2_signup_rate = 127 / (209 + 127)
        st.write(f"**Mailer 1 (Low Cost) Signup Rate:** {mailer1_signup_rate:.2%}")
        st.write(f"**Mailer 2 (High Cost) Signup Rate:** {mailer2_signup_rate:.2%}")

        # STATE HYPOTHESES & SET ACCEPTANCE CRITERIA 
        null_hypothesis = "There is no relationship between mailer type and signup rate. They are independent."
        alternate_hypothesis = "There is a relationship between mailer type and signup rate. They are not independent."
        acceptance_criteria = 0.05

        st.subheader("📐 Hypotheses")
        st.markdown(f"- **Null Hypothesis**: {null_hypothesis}")
        st.markdown(f"- **Alternate Hypothesis**: {alternate_hypothesis}")
        st.markdown(f"- **Acceptance Criteria (α)**: {acceptance_criteria}")

        # CALCULATE EXPECTED FREQUENCIES & CHI SQUARE STATISTIC 
        chi2_statistic, p_value, dof, expected_value = chi2_contingency(observed_values, correction=False)
        critical_value = chi2.ppf(1 - acceptance_criteria, dof)

        st.subheader("🧮 Chi-Square Test Results")
        st.write(f"**Chi-Square Statistic:** {chi2_statistic:.2f}")
        st.write(f"**Degrees of Freedom:** {dof}")
        st.write(f"**Critical Value:** {critical_value:.2f}")
        st.write(f"**p-value:** {p_value:.4f}")

        # INTERPRET RESULTS
        st.subheader("📌 Conclusion")
        if chi2_statistic >= critical_value:
            st.success(f"As our chi-square statistic of {chi2_statistic:.2f} is higher than our critical value of {critical_value:.2f} - we reject the null hypothesis, and conclude that: {alternate_hypothesis}")
        else:
            st.info(f"As our chi-square statistic of {chi2_statistic:.2f} is lower than our critical value of {critical_value:.2f} - we retain the null hypothesis, and conclude that: {null_hypothesis}")

        if p_value <= acceptance_criteria:
            st.success(f"As our p-value of {p_value:.4f} is lower than our acceptance criteria of {acceptance_criteria} - we reject the null hypothesis, and conclude that: {alternate_hypothesis}")
        else:
            st.info(f"As our p-value of {p_value:.4f} is higher than our acceptance criteria of {acceptance_criteria} - we retain the null hypothesis, and conclude that: {null_hypothesis}")

    except Exception as e:
        st.error(f"Error processing file: {e}")
