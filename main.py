import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, chi2

st.set_page_config(page_title="AB Test Analyzer", layout="centered")
st.title("🧪 AB Test Analyzer for Grocery Campaign")

uploaded_file = st.file_uploader("Upload the 'grocery_database.xlsx' file", type=["xlsx"])

if uploaded_file:
    try:
        # Optional: display available sheets for confirmation
        xls = pd.ExcelFile(uploaded_file)
        st.write("📋 Available Sheets:", xls.sheet_names)

        # ✅ Use the correct sheet name
        campaign_data = pd.read_excel(uploaded_file, sheet_name="delivery_club_campaign")

        # ✅ Ensure required columns exist
        if "mailer_type" not in campaign_data.columns or "signup_flag" not in campaign_data.columns:
            st.error("❌ 'mailer_type' or 'signup_flag' column is missing in 'delivery_club_campaign'.")
        else:
            # Filter out Control Group
            campaign_data = campaign_data[campaign_data["mailer_type"] != "Control Group"]

            st.subheader("1️⃣ Observed Signup Counts")
            observed_table = pd.crosstab(campaign_data["mailer_type"], campaign_data["signup_flag"])
            st.dataframe(observed_table)

            # Store observed frequencies as array
            observed_values = observed_table.values

            # Run Chi-Square Test
            chi2_stat, p_value, dof, expected = chi2_contingency(observed_values)

            # Display results
            st.subheader("2️⃣ Chi-Square Test Results")
            st.write(f"Chi-Square Statistic: `{chi2_stat:.2f}`")
            st.write(f"Degrees of Freedom: `{dof}`")
            st.write(f"P-Value: `{p_value:.4f}`")

            # Determine critical value
            critical_value = chi2.ppf(0.95, dof)
            st.write(f"Critical Value (0.05 level): `{critical_value:.2f}`")

            # Interpretation
            st.subheader("3️⃣ Interpretation")
            if chi2_stat >= critical_value:
                st.success("✅ We reject the null hypothesis: There **is a relationship** between mailer type and signup rate.")
            else:
                st.info("ℹ️ We retain the null hypothesis: There **is no strong evidence** of a relationship.")

            if p_value <= 0.05:
                st.success("✅ Based on p-value, we reject the null hypothesis as it's less than 0.05.")
            else:
                st.info("ℹ️ Based on p-value, we retain the null hypothesis as it's greater than 0.05.")

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")
