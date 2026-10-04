
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Nassau Candy Factory Optimization", layout="wide")

DATA = "nassau_cleaned_working.csv"
SCEN = "factory_scenario_results.csv"
REC = "factory_recommendations.csv"

df = pd.read_csv(DATA)
scen = pd.read_csv(SCEN)
rec = pd.read_csv(REC)

st.title("🍫 Nassau Candy — Factory Reallocation & Shipping Optimization")
st.caption("Decision-support prototype. Alternate-factory results are scenario/proxy estimates because the source dataset contains no historical factory field.")

# Sidebar
st.sidebar.header("Controls")
products = ["All"] + sorted(df["Product Name"].dropna().unique().tolist())
product = st.sidebar.selectbox("Product", products)
regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
region = st.sidebar.selectbox("Region", regions)
modes = ["All"] + sorted(df["Ship Mode"].dropna().unique().tolist())
mode = st.sidebar.selectbox("Ship Mode", modes)
priority = st.sidebar.slider("Speed priority", 0, 100, 70)
st.sidebar.caption("0 = profit/risk priority • 100 = speed priority")

f = df.copy()
if product != "All": f = f[f["Product Name"] == product]
if region != "All": f = f[f["Region"] == region]
if mode != "All": f = f[f["Ship Mode"] == mode]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Rows", f"{len(f):,}")
c2.metric("Sales", f"${f['Sales'].sum():,.0f}")
c3.metric("Gross Profit", f"${f['Gross Profit'].sum():,.0f}")
c4.metric("Avg Proxy Lead Time", f"{f['Proxy Lead Time (days)'].mean():.2f} days" if len(f) else "—")

st.subheader("Factory Optimization Simulator")
if product != "All":
    s = scen[scen["Product Name"] == product].copy()
    st.dataframe(
        s[["Candidate Factory","Distance Proxy (mi)","Distance Improvement %",
          "Scenario Lead Time (proxy days)","Lead Time Reduction %",
          "Profit Impact Risk","Confidence"]].sort_values("Scenario Lead Time (proxy days)"),
        use_container_width=True, hide_index=True
    )
else:
    st.info("Select a product to compare all candidate factories.")

st.subheader("Recommendation Dashboard")
r = rec.copy()
if product != "All": r = r[r["Product Name"] == product]
st.dataframe(r[["Product Name","Current Factory","Candidate Factory",
                "Distance Improvement %","Lead Time Reduction %",
                "Profit Margin %","Profit Impact Risk","Confidence"]].head(20),
             use_container_width=True, hide_index=True)

st.subheader("What-If Scenario Analysis")
if product != "All":
    current = scen[(scen["Product Name"]==product) & (scen["Candidate Factory"]==scen["Current Factory"])]
    candidates = scen[(scen["Product Name"]==product) & (scen["Candidate Factory"]!=scen["Current Factory"])]
    if not current.empty and not candidates.empty:
        best = candidates.sort_values("Scenario Lead Time (proxy days)").iloc[0]
        cur = current.iloc[0]
        a,b,c = st.columns(3)
        a.metric("Current Factory", cur["Current Factory"])
        b.metric("Recommended Factory", best["Candidate Factory"])
        c.metric("Lead-Time Reduction", f"{best['Lead Time Reduction %']:.1f}%")
        st.write(f"Estimated proxy lead time: **{cur['Current Avg Lead Time (proxy days)']:.2f} → {best['Scenario Lead Time (proxy days)']:.2f} days**")

st.subheader("Risk & Impact")
st.warning("Important: source data has no historical factory/origin column and its raw Order→Ship dates span ~900–1,600 days. Therefore this dashboard uses a transparent proxy lead-time/scenario model rather than claiming causal ML predictions from historical factory changes.")

st.subheader("Project Notes")
st.markdown("""
- **Current assignment** comes from the project brief's Product → Factory mapping.
- **Scenario distance** uses factory coordinates and regional destination centroids.
- **Alternate-factory lead time** is a conservative proxy derived from relative distance.
- For a production-grade model, collect actual factory assignment, destination coordinates, freight cost, and true shipment timestamps.
""")
