import streamlit as st
import pandas as pd
from genai_engine import classify_user_query
from query_engine import execute_query

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Sales Analytics Chatbot", layout="wide")

# --------------------------------------------------
# Custom Styling
# --------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    h1 {
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sales Analytics Chatbot")
st.caption("AI-powered Sales Intelligence Dashboard")

# --------------------------------------------------
# Suggested Questions
# --------------------------------------------------
st.markdown("### 💡 Suggested Questions")

suggestions = [
    "Show total sales for 2022",
    "Compare sales between 2022 and 2023",
    "Show monthly sales trend for 2022",
    "Top 5 products by revenue",
    "Total unique customers"
]

selected_question = None
cols = st.columns(3)

for i, suggestion in enumerate(suggestions):
    if cols[i % 3].button(suggestion):
        selected_question = suggestion

# --------------------------------------------------
# Chat Input
# --------------------------------------------------
chat_question = st.chat_input("Type your question here...")

# Decide input source
if selected_question:
    user_input = selected_question
elif chat_question:
    user_input = chat_question
else:
    user_input = None

# --------------------------------------------------
# Main Execution Block
# --------------------------------------------------
if user_input:

    st.markdown("---")

    with st.spinner("Analyzing your query..."):
        intent_data = classify_user_query(user_input)
        result = execute_query(intent_data)

    # --------------------------------------------------
    # KPI CARD (Single Value)
    # --------------------------------------------------
    if len(result) == 1 and len(result[0]) == 1:
        value = float(result[0][0])
        st.metric("📌 Result", f"{value:,.2f}")

    # --------------------------------------------------
    # YEAR COMPARISON + YOY GROWTH
    # --------------------------------------------------
    elif intent_data.get("intent") == "comparison":
        df = pd.DataFrame(result, columns=["Year", "Total"])
        df["Total"] = df["Total"].astype(float)

        # Calculate YoY Growth %
        if len(df) == 2:
            growth = ((df.iloc[1]["Total"] - df.iloc[0]["Total"]) / df.iloc[0]["Total"]) * 100
            st.metric("📈 Year-over-Year Growth", f"{growth:.2f}%")

        df_display = df.copy()
        df_display["Total"] = df_display["Total"].apply(lambda x: f"{x:,.2f}")

        st.dataframe(df_display)

    # --------------------------------------------------
    # MONTHLY TREND (LINE CHART + CSV DOWNLOAD)
    # --------------------------------------------------
    elif intent_data.get("intent") == "trend":
        df = pd.DataFrame(result, columns=["Month", "Total"])
        df["Total"] = df["Total"].astype(float)

        st.line_chart(df.set_index("Month"))

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📌 Download CSV",
            data=csv,
            file_name="monthly_trend.csv",
            mime="text/csv"
        )

    # --------------------------------------------------
    # TOP PRODUCTS (BAR CHART + TABLE)
    # --------------------------------------------------
    elif intent_data.get("intent") == "ranking":
        df = pd.DataFrame(result, columns=["Product", "Total Sales"])
        df["Total Sales"] = df["Total Sales"].astype(float)

        st.bar_chart(df.set_index("Product"))

        df_display = df.copy()
        df_display["Total Sales"] = df_display["Total Sales"].apply(lambda x: f"{x:,.2f}")

        st.dataframe(df_display)

    # --------------------------------------------------
    # DEFAULT FALLBACK
    # --------------------------------------------------
    else:
        st.write(result)