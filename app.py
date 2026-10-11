import streamlit as st 
import pandas as pd 
import plotly.express as px 
 
st.set_page_config( 
    page_title="AI Financial Dashboard", 
    page_icon="💰", 
    layout="wide" 
) 
 
st.title("💰 AI Financial Performance Dashboard") 
st.write("Upload your business financial dataset.") 
 
uploaded_file = st.file_uploader( 
    "Upload CSV or Excel file", 
    type=["csv", "xlsx"] 
) 
 
if uploaded_file is not None: 
    try: 
        if uploaded_file.name.endswith(".csv"): 
            df = pd.read_csv(uploaded_file) 
        else: 
            df = pd.read_excel(uploaded_file) 
 
        df.columns = df.columns.str.strip() 
 
        required = ["Month", "Revenue", "Expenses"] 
 
        if not all(col in df.columns for col in required): 
            st.error( 
                "Your file must contain these columns: " 
                "Month, Revenue, Expenses" 
            ) 
        else: 
            df["Revenue"] = pd.to_numeric( 
                df["Revenue"], errors="coerce" 
            ) 
            df["Expenses"] = pd.to_numeric( 
                df["Expenses"], errors="coerce" 
            ) 
            df = df.dropna( 
                subset=["Month", "Revenue", "Expenses"] 
            ).copy() 
 
            if df.empty: 
                st.error("No valid financial records found.") 
            else: 
                df["Profit"] = df["Revenue"] - df["Expenses"] 
 
                st.success("Dataset uploaded successfully!") 
 
                c1, c2, c3 = st.columns(3) 
                c1.metric( 
                    "Total Revenue", 
                    f"₹{df['Revenue'].sum():,.0f}" 
                ) 
                c2.metric( 
                    "Total Expenses", 
                    f"₹{df['Expenses'].sum():,.0f}" 
                ) 
                c3.metric( 
                    "Total Profit", 
                    f"₹{df['Profit'].sum():,.0f}" 
                ) 
 
                st.subheader("Revenue vs Expenses") 
                fig = px.bar( 
                    df, x="Month", 
                    y=["Revenue", "Expenses"], 
                    barmode="group" 
                ) 
                st.plotly_chart(fig, use_container_width=True) 
 
                st.subheader("Profit Trend") 
                profit_fig = px.line( 
                    df, x="Month", y="Profit", 
                    markers=True 
                ) 
                st.plotly_chart( 
                    profit_fig, use_container_width=True 
                ) 
 
                st.subheader("Financial Records") 
                st.dataframe(df, use_container_width=True) 
 
                csv = df.to_csv(index=False).encode("utf-8") 
                st.download_button( 
                    "Download processed dataset", 
                    data=csv, 
                    file_name="financial_report.csv", 
                    mime="text/csv" 
                ) 
 
    except Exception as e: 
        st.error(f"Could not read the file: {e}") 
else: 
    st.info("Upload your financial_data.csv file to begin.")