import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ==========================================================
# PostgreSQL Connection
# ==========================================================

USERNAME = "postgres"
PASSWORD = quote_plus("Postgres123")      # <-- Apna password

HOST = "localhost"
PORT = "5432"
DATABASE = "mutual_fund"

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

print("✅ Connected to PostgreSQL")

# ==========================================================
# SQL Query
# ==========================================================

query = """
SELECT

    d.full_date,

    f.scheme_name,

    n.nav

FROM fact_nav n

JOIN dim_date d
ON n.date_id = d.date_id

JOIN dim_fund f
ON n.amfi_code = f.amfi_code

ORDER BY

d.full_date,
f.scheme_name;
"""

# ==========================================================
# Load Data
# ==========================================================

df = pd.read_sql(query, engine)

print("\nDataset Loaded Successfully")

print(df.head())

print("\nShape :", df.shape)

print("\nColumns")

print(df.columns)

print("\nDate Range")

print(df["full_date"].min())

print(df["full_date"].max())

print("\nTotal Schemes")

print(df["scheme_name"].nunique())

import plotly.express as px

# ==========================================================
# Create Interactive Plot
# ==========================================================

print("\nCreating Plotly Chart...")

fig = px.line(

    df,

    x="full_date",

    y="nav",

    color="scheme_name",

    title="NAV Trend Analysis (2022–2026) – All Mutual Fund Schemes",

    labels={
        "full_date": "Date",
        "nav": "NAV (₹)",
        "scheme_name": "Scheme"
    }

)

# ==========================================================
# Layout
# ==========================================================

# ==========================================================
# Professional Dashboard Layout
# ==========================================================

fig.update_layout(

    template="plotly_dark",

    width=1900,

    height=1050,

    paper_bgcolor="#0d1117",

    plot_bgcolor="#0d1117",

    hovermode="x unified",

    title=dict(

        text="<b>NAV Trend Analysis (2022–2026)</b><br><sup>All 40 Mutual Fund Schemes</sup>",

        x=0.5,

        y=0.97,

        font=dict(

            size=30,

            color="white"

        )

    ),

    xaxis_title="Date",

    yaxis_title="NAV (₹)",

    font=dict(

        family="Arial",

        size=14,

        color="white"

    ),

    margin=dict(

        l=60,

        r=60,

        t=220,

        b=80

    )

)

# ==========================================================
# Improve Line Style
# ==========================================================

fig.update_traces(

    line=dict(width=1.8),

    hovertemplate=

    "<b>%{fullData.name}</b><br>" +

    "Date : %{x}<br>" +

    "NAV : ₹%{y:.2f}<extra></extra>"

)

# ==========================================================
# Range Slider
# ==========================================================

fig.update_xaxes(

    showgrid=True,

    gridcolor="#30363d",

    rangeslider_visible=True

)

fig.update_yaxes(

    showgrid=True,

    gridcolor="#30363d"

)

print("✅ Plot Created Successfully")

# ==========================================================
# Highlight Market Phases
# ==========================================================

# 2023 Bull Run
fig.add_vrect(

    x0="2023-01-01",
    x1="2024-03-31",

    fillcolor="#00ff55",

    opacity=0.10,

    line_width=0,

    annotation_text="📈 2023 Bull Run",

    annotation_position="top left"

)

# 2024 Market Correction

fig.add_vrect(

    x0="2024-04-01",
    x1="2025-03-31",

    fillcolor="#ff3b30",

    opacity=0.10,

    line_width=0,

    annotation_text="📉 2024 Market Correction",

    annotation_position="top left"

)

# ==========================================================
# Additional Annotations
# ==========================================================

fig.add_annotation(

    x="2023-07-01",

    y=df["nav"].max()*0.95,

    text="Strong Market Rally",

    showarrow=True,

    arrowhead=2,

    font=dict(size=12,color="lime")

)

fig.add_annotation(

    x="2024-09-01",

    y=df["nav"].max()*0.85,

    text="Profit Booking & Volatility",

    showarrow=True,

    arrowhead=2,

    font=dict(size=12,color="red")

)

# ==========================================================
# Better Layout
# ==========================================================

fig.update_layout(

    legend=dict(

    orientation="h",

    yanchor="bottom",

    y=1.33,

    xanchor="center",

    x=0.5,

    bgcolor="rgba(0,0,0,0)",

    font=dict(

        size=10

    ),

    title=dict(

        text="<b>Mutual Fund Schemes</b>",

        font=dict(size=14)

    )

)

)

# ==========================================================
# Save Dashboard
# ==========================================================

fig.write_html(

    "dashboard/nav_trend_dashboard.html"

)

try:

    fig.write_image(

    "dashboard/nav_trend_dashboard.png",

    width=2200,

    height=1200,

    scale=2

)

    print("PNG Saved Successfully")

except Exception as e:

    print("PNG Export Skipped")

    print(e)

# ==========================================================
# Show Dashboard
# ==========================================================

fig.show()

print("\nDashboard Created Successfully!")

print("HTML : dashboard/nav_trend_dashboard.html")

print("PNG  : dashboard/nav_trend_dashboard.png")