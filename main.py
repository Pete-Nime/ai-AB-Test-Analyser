
### 🖥️ Streamlit Version of AB Test Analyzer (`main.py`)

##Save this in your Streamlit project folder as `main.py`:

##```python
import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, chi2

st.set_page_config(page_title="AB Test Analyzer", layout="centered")
st.title("📈 AB Test Analyzer")

uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)

        # Filter out 'Control' group if present
        df = df[df["mailer_type"].str.lower() != "control"]

        st.subheader("1️⃣ First 5 Rows of Data")
        st.dataframe(df.head())

        # Crosstab for observed frequencies
        observed = pd.crosstab(df["mailer_type"], df["signup_flag"])
        st.subheader("2️⃣ Observed Signup Rates")
        st.write(observed)

        # Run Chi-Square Test
        chi2_stat, p_value, dof, expected = chi2_contingency(observed.values)
        critical_value = chi2.ppf(1 - 0.05, dof)

        st.subheader("3️⃣ Results")

        if chi2_stat >= critical_value:
            st.error(f"Reject Null Hypothesis ❌ — Mailer Type Affects Signups (Chi² = {chi2_stat:.2f}, p = {p_value:.4f})")
        else:
            st.success(f"Fail to Reject Null Hypothesis ✅ — No Evidence Mailer Affects Signups (Chi² = {chi2_stat:.2f}, p = {p_value:.4f})")

        st.info(f"Degrees of Freedom: {dof}, Critical Value: {critical_value:.2f}")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.warning("Please upload a valid Excel or CSV file.")

