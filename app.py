
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from pathlib import Path
from datetime import datetime

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Hospital Operations Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ==================================================
# SQL DATABASE CONNECTION
# ==================================================

DB_PATH = Path(__file__).parent / "hospital.db"

def get_data():

    with sqlite3.connect(DB_PATH) as conn:

        df = pd.read_sql_query(
            """
            SELECT
                Hospital,
                EDPatients,
                Waiting,
                Admitted,
                PIAHours,
                OccupancyPercentage,
                LastUpdated
            FROM vw_ED_LiveMetrics
            ORDER BY Hospital
            """,
            conn
        )

    return df

# ==================================================
# DASHBOARD HEADER
# ==================================================

st.title("🏥 Hospital Operations Dashboard")
st.caption("SQL Connected | Fictional Hospital Data")

st.info("Data Source: vw_ED_LiveMetrics")

# ==================================================
# LIVE DASHBOARD
# ==================================================

@st.fragment(run_every="30s")
def live_dashboard():

    df = get_data()

    if df.empty:
        st.warning("No data found in SQL view.")
        return

    st.caption(
        "Last checked: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # KPI CARDS
    st.subheader("Live Hospital Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total ED Patients",
        int(df["EDPatients"].sum())
    )

    col2.metric(
        "Waiting for Physician",
        int(df["Waiting"].sum())
    )

    col3.metric(
        "Admitted Patients",
        int(df["Admitted"].sum())
    )

    st.divider()

    # HOSPITAL CHARTS
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            df,
            x="Hospital",
            y="EDPatients",
            color="Hospital",
            text="EDPatients",
            title="ED Patients by Hospital"
        )

        st.plotly_chart(fig1, width="stretch")

    with col2:
        fig2 = px.bar(
            df,
            x="Hospital",
            y="Waiting",
            color="Hospital",
            text="Waiting",
            title="Waiting for Physician"
        )

        st.plotly_chart(fig2, width="stretch")

    st.divider()

    # PIA AND OCCUPANCY
    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.bar(
            df,
            x="Hospital",
            y="PIAHours",
            color="Hospital",
            text="PIAHours",
            title="PIA 80th Percentile (Hours)"
        )

        st.plotly_chart(fig3, width="stretch")

    with col4:
        fig4 = px.bar(
            df,
            x="Hospital",
            y="OccupancyPercentage",
            color="Hospital",
            text="OccupancyPercentage",
            title="ED Occupancy (%)"
        )

        st.plotly_chart(fig4, width="stretch")

    st.divider()

    # SQL DATA
    st.subheader("SQL View Data")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

live_dashboard()
