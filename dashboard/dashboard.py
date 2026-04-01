import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch
import seaborn as sns
import os

# -- Page config --
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
)

# -- CSS --
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Background ── */
.main { background-color: var(--background-color); }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px;
}

/* ── KPI Cards: ── */
div[data-testid="metric-container"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(128,128,128,0.2) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.12) !important;
}
div[data-testid="metric-container"] label {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-color) !important;
    opacity: 0.55 !important;
}
div[data-testid="metric-container"] div[data-testid="metric-value"] {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: var(--text-color) !important;
    line-height: 1.15 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
    color: var(--text-color) !important;
    opacity: 0.7;
}

/* ── Headings ── */
h1, h2, h3, h4 {
    color: var(--text-color) !important;
    letter-spacing: -0.03em !important;
}
h2 { font-weight: 800 !important; font-size: 1.6rem !important; }
h3 { font-weight: 700 !important; font-size: 1.2rem !important; }

/* ── Info / Alert boxes ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
    padding: 14px 18px !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}

/* ── Sidebar  ── */
[data-testid="stSidebar"] {
    background: #1e293b !important;  /* lebih terang dari sebelumnya */
    border-right: 1px solid #334155 !important;
}

/* All Text */
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Title */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* Radio option */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent !important;
    border-radius: 8px !important;
    padding: 8px 10px !important;
    transition: 0.2s ease;
}

/* Hover */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.05) !important;
}

/* Selected */
[data-testid="stSidebar"] .stRadio input:checked + div {
    background: rgba(59,130,246,0.2) !important;
    border-radius: 8px !important;
}

/* Multiselect */
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #334155 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}

/* Divider */
[data-testid="stSidebar"] hr {
    border-top: 1px solid #475569 !important;
}

/* Caption */
[data-testid="stSidebar"] .stCaption {
    color: #94a3b8 !important;
}
            
/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 2px solid rgba(128,128,128,0.15) !important;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    height: 40px;
    padding: 0 18px;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    font-size: 0.87rem !important;
    color: var(--text-color) !important;
    opacity: 0.6;
    transition: opacity 0.15s;
}
.stTabs [aria-selected="true"] {
    opacity: 1 !important;
    border-bottom: 2px solid #3b82f6 !important;
    color: var(--text-color) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    color: var(--text-color) !important;
    border-radius: 10px !important;
}

/* ── Dataframe / Table ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }
.stDataFrame thead th {
    background: var(--secondary-background-color) !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(128,128,128,0.18) !important;
    margin: 1.5rem 0 !important;
}

/* ── Section label / subtitle ── */
.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 4px;
}

/* ── Chart titles inside st.markdown ── */
.chart-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 8px;
    opacity: 0.9;
}

/* ── Pyplot container ── */
[data-testid="stImage"] > img,
.stPlotlyChart,
[data-testid="stPyplotContainer"] {
    border-radius: 14px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


# -- Helper: detect dark mode for matplotlib --
def get_plot_style():
    theme = st.get_option("theme.base")

    if theme == "dark":
        return {
            "bg": "#1e293b",
            "text": "#e2e8f0",
            "grid": "#334155",
            "tick": "#94a3b8",
            "spine": "#334155",
            "fig_bg": "#1e293b",
        }
    else:  # LIGHT MODE
        return {
            "bg": "#ffffff",
            "text": "#0f172a",
            "grid": "#e2e8f0",
            "tick": "#475569",
            "spine": "#cbd5e1",
            "fig_bg": "#ffffff",
        }
    
def apply_global_style():
    s = get_plot_style()
    plt.rcParams.update({
        "figure.facecolor": s["fig_bg"],
        "axes.facecolor": s["bg"],
        "axes.edgecolor": s["spine"],
        "axes.labelcolor": s["tick"],
        "xtick.color": s["tick"],
        "ytick.color": s["tick"],
        "text.color": s["text"],
        "grid.color": s["grid"],
        "axes.titleweight": "bold",
        "axes.titlesize": 11,
    })

def style_ax(ax, fig, title="", xlabel="", ylabel=""):
    s = get_plot_style()

    fig.patch.set_facecolor(s["fig_bg"])
    ax.set_facecolor(s["bg"])

    ax.tick_params(colors=s["tick"], labelsize=9)

    for spine in ax.spines.values():
        spine.set_color(s["spine"])

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    if title:
        ax.set_title(title, fontsize=11, pad=10)

    ax.yaxis.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)

    # legend auto adapt
    legend = ax.get_legend()
    if legend:
        legend.get_frame().set_facecolor(s["bg"])
        legend.get_frame().set_edgecolor(s["spine"])


# -- Color Palette --
C = {
    "blue"   : "#60a5fa",
    "red"    : "#f87171",
    "orange" : "#fb923c",
    "teal"   : "#34d399",
    "green"  : "#4ade80",
    "yellow" : "#fbbf24",
    "gray"   : "#64748b",
    "navy"   : "#1e40af",
    "purple" : "#a78bfa",
    "pink"   : "#f472b6",
}
SEASON_COLORS = {
    "Spring": "#4ade80",
    "Summer": "#fb923c",
    "Fall"  : "#f97316",
    "Winter": "#60a5fa",
}
SEG_COLORS  = {"Low": "#64748b", "Medium": "#60a5fa", "High": "#3b82f6", "Peak": "#1d4ed8"}
HOUR_COLORS = {
    "Off-Peak" : "#475569",
    "Shoulder" : "#fbbf24",
    "Leisure"  : "#38bdf8",
    "Rush Hour": "#f87171",
}


# -- Load Data --
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    day_df   = pd.read_csv(os.path.join(base_dir, "day_clean.csv"))
    hour_df  = pd.read_csv(os.path.join(base_dir, "hour_clean.csv"))
    return day_df, hour_df

day_df, hour_df = load_data()
day_df["year_label"]  = day_df["year_label"].astype(str)
hour_df["year_label"] = hour_df["year_label"].astype(str)


# --Segmentation helpers --
def make_demand_segment(series):
    q1, q2, q3 = series.quantile([0.25, 0.50, 0.75])
    def _seg(v):
        if v <= q1:   return "Low"
        elif v <= q2: return "Medium"
        elif v <= q3: return "High"
        else:         return "Peak"
    return series.apply(_seg)

def hour_segment(hr):
    if   0  <= hr <= 5:  return "Off-Peak"
    elif 6  <= hr <= 9:  return "Rush Hour"
    elif 10 <= hr <= 15: return "Leisure"
    elif 16 <= hr <= 19: return "Rush Hour"
    else:                return "Shoulder"


# -- Sidebar --
with st.sidebar:
    st.markdown("# 🚲 Bike Sharing")
    st.markdown("**Washington D.C. · 2011–2012**")
    st.divider()

    st.markdown("**Filter Data**")
    year_options = st.multiselect(
        "Tahun", options=["2011", "2012"], default=["2011", "2012"]
    )
    season_options = st.multiselect(
        "Musim",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"]
    )
    st.divider()

    st.markdown("**Navigasi**")
    section = st.radio("Pilih Analisis:", [
        "📊 Overview",
        "📈 Tren Bulanan & Musiman",
        "🌤️ Pengaruh Cuaca",
        "👤 Casual vs Registered",
        "🕐 Peak Hours",
        "🔬 Analisis Lanjutan",
    ], label_visibility="collapsed")
    st.divider()
    st.markdown(
    "📊 Dataset: [Bike Sharing Dataset (Kaggle)](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)  \n"
    "👤 Jihan Timmy Nisrina"
)


# -- Filter --
day_f  = day_df[
    day_df["year_label"].isin(year_options) &
    day_df["season_label"].isin(season_options)
]
hour_f = hour_df[
    hour_df["year_label"].isin(year_options) &
    hour_df["season_label"].isin(season_options)
]

if day_f.empty or hour_f.empty:
    st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Pilih minimal satu tahun dan satu musim.")
    st.stop()


# --Header --
st.markdown("## 🚲 Bike Sharing Demand Dashboard")
st.markdown("Analisis pola penggunaan bike sharing di **Washington D.C.** (2011–2012)")
st.divider()

# -- KPI Cards --
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Penyewaan",     f"{day_f['cnt'].sum():,}")
k2.metric("Rata-rata Harian",    f"{int(day_f['cnt'].mean()):,}")
k3.metric("% Registered",        f"{day_f['registered'].sum()/day_f['cnt'].sum()*100:.1f}%")
k4.metric("Rata-rata Suhu",      f"{day_f['temp_c'].mean():.1f}°C")
k5.metric("Hari Dianalisis",     f"{len(day_f):,}")
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if section == "📊 Overview":
    st.subheader("📊 Overview Dataset")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="chart-title">Distribusi Penyewaan Harian</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 4.2))
        ax.hist(day_f["cnt"], bins=35, color=C["blue"], edgecolor="#1e293b", linewidth=0.5, alpha=0.9)
        ax.axvline(day_f["cnt"].mean(),   color=C["red"],    linestyle="--", linewidth=2,
                   label=f'Mean: {int(day_f["cnt"].mean()):,}')
        ax.axvline(day_f["cnt"].median(), color=C["yellow"], linestyle="--", linewidth=2,
                   label=f'Median: {int(day_f["cnt"].median()):,}')
        ax.legend()
        style_ax(ax, fig, xlabel="Jumlah Penyewaan", ylabel="Frekuensi")
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.markdown('<div class="chart-title">Penyewaan per Musim & Tahun</div>', unsafe_allow_html=True)
        pivot = day_f.groupby(["season_label", "year_label"])["cnt"].mean().unstack(fill_value=0)
        season_order = [s for s in ["Spring", "Summer", "Fall", "Winter"] if s in pivot.index]
        pivot = pivot.reindex(season_order)
        fig, ax = plt.subplots(figsize=(7, 4.2))
        x = np.arange(len(pivot))
        width = 0.35
        yr_colors = {"2011": C["blue"], "2012": C["red"]}
        for i, yr in enumerate(pivot.columns):
            bars = ax.bar(x + (i - 0.5) * width, pivot[yr], width,
                          label=yr, color=yr_colors.get(yr, C["gray"]),
                          edgecolor="#1e293b", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(season_order, color="#94a3b8", fontsize=9)
        ax.legend(title="Tahun")
        style_ax(ax, fig, ylabel="Rata-rata Penyewaan Harian")
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    st.info(
        f"📌 **Ringkasan:** Dalam {len(day_f)} hari, tercatat total **{day_f['cnt'].sum():,}** penyewaan sepeda. "
        f"Rata-rata harian mencapai **{int(day_f['cnt'].mean()):,}** (median **{int(day_f['cnt'].median()):,}**), "
        f"dengan **81.2%** pengguna merupakan registered user. "
        f"Suhu rata-rata **15.3°C**, dan distribusi penyewaan cenderung **right-skewed** akibat lonjakan pada hari-hari tertentu."
    )

# ══════════════════════════════════════════════════════════════════════════════
# TREN BULANAN
# ══════════════════════════════════════════════════════════════════════════════
elif section == "📈 Tren Bulanan & Musiman":
    st.subheader("📈 Tren Penyewaan Sepeda per Bulan (2011–2012)")

    col1, col2 = st.columns(2)
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    with col1:
        st.markdown('<div class="chart-title">Tren Bulanan Penyewaan Sepeda</div>', unsafe_allow_html=True)
        monthly   = day_f.groupby(["year_label", "mnth"])["cnt"].sum().reset_index()
        colors_yr = {"2011": C["blue"], "2012": C["red"]}
        fig, ax   = plt.subplots(figsize=(7, 4.2))
        for yr, grp in monthly.groupby("year_label"):
            ax.plot(grp["mnth"], grp["cnt"], marker="o", markersize=5,
                    linewidth=2.5, label=yr, color=colors_yr.get(yr, C["gray"]))
            ax.fill_between(grp["mnth"], grp["cnt"],
                            alpha=0.12, color=colors_yr.get(yr, C["gray"]))
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(month_labels, rotation=30, ha="right", color="#94a3b8", fontsize=8.5)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.legend(title="Tahun")
        style_ax(ax, fig, xlabel="Bulan", ylabel="Total Penyewaan")
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    with col2:
        s = get_plot_style()
        st.markdown('<div class="chart-title">Rata-rata Penyewaan Harian per Musim</div>', unsafe_allow_html=True)
        season_order = [s for s in ["Spring","Summer","Fall","Winter"] if s in day_f["season_label"].values]
        season_avg   = day_f.groupby("season_label")["cnt"].mean().reindex(season_order).dropna()
        fig, ax = plt.subplots(figsize=(7, 4.2))
        bars = ax.bar(season_avg.index, season_avg.values,
                      color=[SEASON_COLORS[s] for s in season_avg.index],
                      edgecolor="#1e293b", linewidth=0.5, width=0.55)
        for bar, val in zip(bars, season_avg.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                    f"{val:,.0f}", ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color=s["text"])
        ax.set_xticklabels(season_order, color="#94a3b8", fontsize=9)
        style_ax(ax, fig, xlabel="Musim", ylabel="Rata-rata Penyewaan/Hari")
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    total_per_tahun = day_f.groupby("year_label")["cnt"].sum()
    season_mean     = day_f.groupby("season_label")["cnt"].mean()
    best_season     = season_mean.idxmax()
    worst_season    = season_mean.idxmin()
    tahun_str       = " dan tahun ".join([f"{yr}: **{cnt:,}**" for yr, cnt in total_per_tahun.items()])
    st.info(
        f"📌 **Insight:** Total penyewaan pada tahun {tahun_str}. "
        f"Musim **{best_season}** mencatat rata-rata harian tertinggi ({season_mean[best_season]:,.0f}/hari), "
        f"sedangkan **{worst_season}** terendah ({season_mean[worst_season]:,.0f}/hari)."
    )

# ══════════════════════════════════════════════════════════════════════════════
# PENGARUH CUACA
# ══════════════════════════════════════════════════════════════════════════════
elif section == "🌤️ Pengaruh Cuaca":
    st.subheader("🌤️ Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan")

    col3, col4, col5 = st.columns(3)
    weather_vars = [
        ("temp_c",   "Suhu (°C)",             C["red"],    col3),
        ("hum_pct",  "Kelembaban (%)",         C["blue"],   col4),
        ("wind_kmh", "Kecepatan Angin (km/h)", C["teal"],   col5),
    ]
    for col_name, xlabel, color, col in weather_vars:
        with col:
            st.markdown(f'<div class="chart-title">Penyewaan vs {xlabel}</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(5, 4.2))
            ax.scatter(day_f[col_name], day_f["cnt"],
                       alpha=0.4, s=14, color=color, edgecolors="none")
            m, b    = np.polyfit(day_f[col_name], day_f["cnt"], 1)
            x_range = np.linspace(day_f[col_name].min(), day_f[col_name].max(), 200)
            ax.plot(x_range, m * x_range + b, color="#ffffff", linewidth=1.8, linestyle="--", alpha=0.8)
            corr = day_f[[col_name, "cnt"]].corr().iloc[0, 1]
            ax.text(0.05, 0.93, f"r = {corr:.2f}", transform=ax.transAxes,
                    fontsize=12, color="#e2e8f0", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.35", facecolor="#0f172a",
                              alpha=0.85, edgecolor="#334155"))
            style_ax(ax, fig, xlabel=xlabel, ylabel="Jumlah Penyewaan")
            plt.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()

    s = get_plot_style()
    st.markdown('<div class="chart-title" style="margin-top:12px">Rata-rata Penyewaan per Kondisi Cuaca</div>', unsafe_allow_html=True)
    weather_avg = day_f.groupby("weather_label")["cnt"].mean().sort_values(ascending=False)
    bar_colors  = [C["teal"], C["blue"], C["orange"], C["red"]][:len(weather_avg)]
    fig, ax = plt.subplots(figsize=(10, 3.2))
    bars = ax.barh(weather_avg.index, weather_avg.values,
                   color=bar_colors, edgecolor="#1e293b", linewidth=0.5, height=0.5)
    for bar, val in zip(bars, weather_avg.values):
        ax.text(val + 30, bar.get_y() + bar.get_height()/2,
                f"{val:,.0f}/hari", va="center", fontsize=10,
                fontweight="bold", color=s["text"])
    ax.set_yticklabels(weather_avg.index, color="#94a3b8", fontsize=9)
    style_ax(ax, fig, xlabel="Rata-rata Penyewaan Harian")
    plt.tight_layout(pad=1.5)
    st.pyplot(fig)
    plt.close()

    corr_temp = day_f[["temp_c","cnt"]].corr().iloc[0,1]
    corr_hum  = day_f[["hum_pct","cnt"]].corr().iloc[0,1]
    corr_wind = day_f[["wind_kmh","cnt"]].corr().iloc[0,1]
    best_w    = weather_avg.idxmax()
    worst_w   = weather_avg.idxmin()
    st.info(
        f"📌 **Insight:** Suhu memiliki pengaruh paling dominan terhadap penyewaan (r = {corr_temp:.2f}), "
        f"menunjukkan bahwa cuaca yang lebih hangat meningkatkan jumlah penyewaan. "
        f"Sebaliknya, kecepatan angin (r = {corr_wind:.2f}) dan kelembaban (r = {corr_hum:.2f}) "
        f"berkorelasi negatif, sehingga kondisi berangin dan lembab cenderung menurunkan permintaan. "
        f"Kondisi **{best_w}** mencatat rata-rata tertinggi ({weather_avg[best_w]:,.0f}/hari), "
        f"sedangkan **{worst_w}** terendah ({weather_avg[worst_w]:,.0f}/hari), "
        f"menunjukkan perbedaan permintaan yang signifikan antar kondisi cuaca."
    )

# ══════════════════════════════════════════════════════════════════════════════
# CASUAL VS REGISTERED
# ══════════════════════════════════════════════════════════════════════════════
elif section == "👤 Casual vs Registered":
    st.subheader("👤 Pola Casual vs Registered User")

    col6, col7 = st.columns(2)
    weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    with col6:
        st.markdown('<div class="chart-title">Rata-rata Penyewaan per Hari</div>', unsafe_allow_html=True)
        user_weekday = day_f.groupby("weekday_label")[["casual","registered"]].mean()
        user_weekday = user_weekday.reindex(weekday_order).dropna()
        fig, ax = plt.subplots(figsize=(7, 4.2))
        x     = np.arange(len(user_weekday))
        width = 0.38
        ax.bar(x - width/2, user_weekday["casual"],     width,
               label="Casual",     color=C["orange"], edgecolor="#1e293b", linewidth=0.5)
        ax.bar(x + width/2, user_weekday["registered"], width,
               label="Registered", color=C["blue"],   edgecolor="#1e293b", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels([d[:3] for d in user_weekday.index], color="#94a3b8", fontsize=9)
        ax.legend()
        style_ax(ax, fig, ylabel="Rata-rata Penyewaan")
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    with col7:
        st.markdown('<div class="chart-title">Proporsi Total Penyewaan</div>', unsafe_allow_html=True)
        totals = [day_f["casual"].sum(), day_f["registered"].sum()]
        s = get_plot_style()
        fig, ax = plt.subplots(figsize=(7, 4.2))
        fig.patch.set_facecolor(s["fig_bg"])
        ax.set_facecolor(s["bg"])

        wedges, texts, autotexts = ax.pie(
            totals,
            labels=["Casual", "Registered"],
            colors=[C["orange"], C["blue"]],
            autopct="%1.1f%%",
            startangle=140,
            textprops={"color": s["text"]}
        )

        for t in autotexts:
            t.set_color(s["text"])
            t.set_fontweight("bold")
        ax.set_facecolor("#1e293b")
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    st.markdown('<div class="chart-title" style="margin-top:12px">Tren Bulanan: Casual vs Registered</div>', unsafe_allow_html=True)
    monthly_user = day_f.groupby("mnth")[["casual","registered"]].mean()
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.plot(monthly_user.index, monthly_user["casual"],     marker="o", markersize=4.5,
            linewidth=2.5, color=C["orange"], label="Casual")
    ax.plot(monthly_user.index, monthly_user["registered"], marker="o", markersize=4.5,
            linewidth=2.5, color=C["blue"],   label="Registered")
    ax.fill_between(monthly_user.index, monthly_user["casual"],     alpha=0.12, color=C["orange"])
    ax.fill_between(monthly_user.index, monthly_user["registered"], alpha=0.12, color=C["blue"])
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_labels, color="#94a3b8", fontsize=9)
    ax.legend()
    style_ax(ax, fig, xlabel="Bulan", ylabel="Rata-rata Penyewaan")
    plt.tight_layout(pad=1.5)
    st.pyplot(fig)
    plt.close()

    total_casual = day_f["casual"].sum()
    total_reg    = day_f["registered"].sum()
    total_all    = day_f["cnt"].sum()
    peak_cas     = user_weekday["casual"].idxmax()     if not user_weekday.empty else "-"
    peak_reg     = user_weekday["registered"].idxmax() if not user_weekday.empty else "-"
    st.info(
        f"📌 **Insight:** Registered user mendominasi **{total_reg/total_all*100:.1f}%** ({total_reg:,}) "
        f"dari total penyewaan dengan pola stabil di hari kerja (commuting). "
        f"Sementara itu, casual user cenderung meningkat pada hari **{peak_cas}**, "
        f"menunjukkan pola penggunaan untuk rekreasi. "
        f"Perbedaan pola ini mengindikasikan kebutuhan strategi operasional dan promosi yang berbeda."
    )

# ══════════════════════════════════════════════════════════════════════════════
# PEAK HOURS
# ══════════════════════════════════════════════════════════════════════════════
elif section == "🕐 Peak Hours":
    st.subheader("🕐 Peak Hours Penggunaan Sepeda")

    col8, col9 = st.columns(2)
    with col8:
        st.markdown('<div class="chart-title">Rata-rata Penyewaan per Jam</div>', unsafe_allow_html=True)
        hourly    = hour_f.groupby(["hr","workingday_label"])["cnt"].mean().reset_index()
        color_map = {"Working Day": C["blue"], "Weekend/Holiday": C["orange"]}
        wd_data   = hourly[hourly["workingday_label"]=="Working Day"]
        we_data   = hourly[hourly["workingday_label"]=="Weekend/Holiday"]
        fig, ax   = plt.subplots(figsize=(7, 4.2))
        for label, grp in hourly.groupby("workingday_label"):
            ax.plot(grp["hr"], grp["cnt"], marker="o", markersize=4,
                    linewidth=2.5, label=label, color=color_map.get(label, C["gray"]))
            ax.fill_between(grp["hr"], grp["cnt"],
                            alpha=0.1, color=color_map.get(label, C["gray"]))
        if not wd_data.empty:
            wr = wd_data.loc[wd_data["cnt"].idxmax()]
            ax.annotate(f"Peak Kerja\nJam {int(wr['hr'])}.00",
                        xy=(wr["hr"], wr["cnt"]),
                        xytext=(wr["hr"]-5, wr["cnt"]+20),
                        fontsize=8, color=C["blue"], fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=C["blue"], lw=1.2))
        if not we_data.empty:
            wer = we_data.loc[we_data["cnt"].idxmax()]
            ax.annotate(f"Peak Weekend\nJam {int(wer['hr'])}.00",
                        xy=(wer["hr"], wer["cnt"]),
                        xytext=(wer["hr"]+1, wer["cnt"]+20),
                        fontsize=8, color=C["orange"], fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=C["orange"], lw=1.2))
        ax.set_xticks(range(0, 24, 2))
        ax.set_xticklabels(range(0, 24, 2), color="#94a3b8", fontsize=8.5)
        ax.legend()
        style_ax(ax, fig, xlabel="Jam", ylabel="Rata-rata Penyewaan")
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    with col9:
        st.markdown('<div class="chart-title">Heatmap: Jam × Hari dalam Seminggu</div>', unsafe_allow_html=True)
        heatmap_data = hour_f.pivot_table(
            values="cnt", index="weekday_label", columns="hr", aggfunc="mean"
        ).reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        s = get_plot_style()
        fig, ax = plt.subplots(figsize=(7, 4.2))
        fig.patch.set_facecolor(s["fig_bg"])
        ax.set_facecolor(s["bg"])
        sns.heatmap(
            heatmap_data,
            cmap="YlOrRd",
            ax=ax,
            cbar_kws={"label": "Avg Rentals"}
        )
        ax.tick_params(colors=s["tick"])
        ax.set_xlabel("Jam", color=s["tick"])
        ax.set_ylabel("")
        ax.set_title("Heatmap: Jam × Hari", color=s["text"])
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(colors="#94a3b8", labelsize=8)
        cbar.set_label("Avg Rentals", color="#94a3b8", fontsize=9)
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

    wd_peak_hr  = int(wd_data.loc[wd_data["cnt"].idxmax(),"hr"])  if not wd_data.empty else "-"
    wd_peak_cnt = int(wd_data["cnt"].max())                        if not wd_data.empty else "-"
    we_peak_hr  = int(we_data.loc[we_data["cnt"].idxmax(),"hr"])  if not we_data.empty else "-"
    we_peak_cnt = int(we_data["cnt"].max())                        if not we_data.empty else "-"
    st.info(
        f"📌 **Insight:** Pada hari kerja menunjukkan pola **bimodal** dengan puncak pada jam "
        f"**{wd_peak_hr:02d}.00** (~{wd_peak_cnt}/jam), mencerminkan aktivitas berangkat dan pulang kerja. "
        f"Sementara itu, akhir pekan memiliki puncak pada jam **{we_peak_hr:02d}.00** "
        f"(~{we_peak_cnt}/jam) dengan pola yang lebih merata, menunjukkan penggunaan rekreasi. "
        f"Pola ini penting untuk optimalisasi distribusi sepeda berdasarkan waktu dan jenis hari."
    )

# ══════════════════════════════════════════════════════════════════════════════
# ANALISIS LANJUTAN
# ══════════════════════════════════════════════════════════════════════════════
elif section == "🔬 Analisis Lanjutan":
    st.subheader("🔬 Analisis Lanjutan: Demand & Hour-of-Day Segmentation")

    st.markdown(
        "Dua pendekatan **rule-based clustering** tanpa machine learning:\n\n"
        "- **Demand Segmentation**: Mengelompokkan hari berdasarkan tingkat penyewaan (kuantil) "
        "→ *Low*, *Medium*, *High*, *Peak*\n"
        "- **Hour-of-Day Segmentation**: Mengelompokkan jam ke 4 periode operasional "
        "→ *Off-Peak*, *Shoulder*, *Rush Hour*, *Leisure*"
    )
    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "📦 Demand Segmentation",
        "⏱️ Hour-of-Day Segmentation",
        "🔥 Heatmap Korelasi",
    ])

    # -- Tab 1 --
    with tab1:
        st.markdown("#### Demand Segmentation — Binning Tingkat Penyewaan Harian")
        st.markdown(
            "Membagi hari ke **4 segmen** berdasarkan distribusi kuantil `cnt`: "
            "`Low` (≤Q1) · `Medium` (Q1–Q2) · `High` (Q2–Q3) · `Peak` (>Q3)"
        )

        day_seg = day_f.copy()
        day_seg["demand_segment"] = make_demand_segment(day_seg["cnt"])
        seg_order = ["Low","Medium","High","Peak"]

        seg_stats = day_seg.groupby("demand_segment").agg(
            jumlah_hari    = ("cnt","count"),
            rata2_cnt      = ("cnt","mean"),
            rata2_temp     = ("temp_c","mean"),
            rata2_hum      = ("hum_pct","mean"),
            rata2_wind     = ("wind_kmh","mean"),
            pct_workingday = ("workingday","mean"),
        ).reindex(seg_order)
        seg_stats["pct_workingday"] = (seg_stats["pct_workingday"] * 100).round(1)

        st.dataframe(
            seg_stats.rename(columns={
                "jumlah_hari"   : "Jumlah Hari",
                "rata2_cnt"     : "Avg Penyewaan",
                "rata2_temp"    : "Avg Suhu (°C)",
                "rata2_hum"     : "Avg Kelembaban (%)",
                "rata2_wind"    : "Avg Angin (km/h)",
                "pct_workingday": "% Hari Kerja",
            }).round(1),
            use_container_width=True,
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            s = get_plot_style()
            st.markdown('<div class="chart-title">Distribusi Hari per Segmen</div>', unsafe_allow_html=True)
            counts = day_seg["demand_segment"].value_counts().reindex(seg_order)
            fig, ax = plt.subplots(figsize=(5, 4))
            bars = ax.bar(seg_order, counts.values,
                          color=[SEG_COLORS[s] for s in seg_order],
                          edgecolor="#1e293b", width=0.6)
            for bar, val in zip(bars, counts.values):
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
                        f"{val} hari", ha="center", va="bottom",
                        fontsize=9, fontweight="bold", color=s["text"])
            ax.set_xticklabels(seg_order, color="#94a3b8", fontsize=9)
            style_ax(ax, fig, ylabel="Jumlah Hari")
            plt.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()

        with col_b:
            s = get_plot_style()
            st.markdown('<div class="chart-title">Rata-rata Penyewaan per Segmen</div>', unsafe_allow_html=True)
            avg_cnt = seg_stats["rata2_cnt"]
            fig, ax = plt.subplots(figsize=(5, 4))
            bars = ax.bar(seg_order, avg_cnt.values,
                          color=[SEG_COLORS[s] for s in seg_order],
                          edgecolor="#1e293b", width=0.6)
            for bar, val in zip(bars, avg_cnt.values):
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+25,
                        f"{val:,.0f}", ha="center", va="bottom",
                        fontsize=9, fontweight="bold", color=s["text"])
            ax.set_xticklabels(seg_order, color="#94a3b8", fontsize=9)
            style_ax(ax, fig, ylabel="Rata-rata cnt")
            plt.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()

        with col_c:
            st.markdown('<div class="chart-title">Profil Cuaca & Hari Kerja</div>', unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(5, 4))
            x = range(len(seg_order))
            w = 0.28

            # Bar chart (kelembaban & working day)
            b1 = ax.bar([i - w/2 for i in x], seg_stats["rata2_hum"], width=w,
                        label="Kelembaban (%)", color=C["blue"], alpha=0.9, edgecolor="#1e293b")
            
            b2 = ax.bar([i + w/2 for i in x], seg_stats["pct_workingday"], width=w,
                        label="% Hari Kerja", color=C["teal"], alpha=0.9, edgecolor="#1e293b")

            ax.set_xticks(list(x))
            ax.set_xticklabels(seg_order, color="#94a3b8", fontsize=9)
            style_ax(ax, fig, ylabel="Nilai (%)")

            #  Twin axis untuk suhu
            ax2 = ax.twinx()
            ax2.plot(x, seg_stats["rata2_temp"], color=C["red"], marker="o",
                    linewidth=2.5, label="Suhu (°C)")

            for i, val in enumerate(seg_stats["rata2_temp"]):
                ax2.text(i, val + 0.3, f"{val:.1f}°C",
                        ha="center", fontsize=8, color=C["red"])

            ax2.set_ylabel("Suhu (°C)", color=C["red"])
            ax2.tick_params(axis='y', labelcolor=C["red"])

            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8)

            plt.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()

        q1, q2, q3 = day_f["cnt"].quantile([0.25, 0.50, 0.75])
        st.info(
            f"📌 **Insight:** Segmentasi permintaan berdasarkan kuartil menunjukkan batas "
            f"Q1: **{q1:.0f}**, Median: **{q2:.0f}**, dan Q3: **{q3:.0f}**. "
            f"Segmen **Peak** terjadi pada suhu rata-rata ~**{seg_stats.loc['Peak','rata2_temp']:.1f}°C** "
            f"dengan **{seg_stats.loc['Peak','pct_workingday']:.0f}%** hari kerja, "
            f"mengindikasikan permintaan tinggi saat cuaca hangat dan hari aktif. "
            f"Sebaliknya, segmen **Low** berkaitan dengan kondisi lebih dingin dan lembab. "
            f"Insight ini dapat dimanfaatkan untuk perencanaan armada berbasis prakiraan cuaca."
        )

    # -- Tab 2--
    with tab2:
        st.markdown("#### Hour-of-Day Segmentation — 24 Jam ke 4 Periode")
        st.markdown(
            "🔴 `Rush Hour` (06–09 & 16–19) · 🔵 `Leisure` (10–15) · "
            "🟡 `Shoulder` (20–23) · ⚫ `Off-Peak` (00–05)"
        )

        hour_seg = hour_f.copy()
        hour_seg["hour_segment"] = hour_seg["hr"].apply(hour_segment)
        hour_order = ["Off-Peak","Shoulder","Leisure","Rush Hour"]

        hour_seg_stats = hour_seg.groupby("hour_segment").agg(
            rata2_cnt        = ("cnt","mean"),
            total_cnt        = ("cnt","sum"),
            rata2_casual     = ("casual","mean"),
            rata2_registered = ("registered","mean"),
        ).reindex(hour_order)
        hour_seg_stats["pct_total"] = \
            (hour_seg_stats["total_cnt"] / hour_seg_stats["total_cnt"].sum() * 100).round(1)

        col_d, col_e, col_f = st.columns(3)

        with col_d:
            st.markdown('<div class="chart-title">Penyewaan per Jam (warna = segmen)</div>', unsafe_allow_html=True)
            hourly_avg = hour_f.groupby("hr")["cnt"].mean()
            fig, ax = plt.subplots(figsize=(5, 4))
            for hr, val in hourly_avg.items():
                seg = hour_segment(hr)
                ax.bar(hr, val, color=HOUR_COLORS[seg], width=0.85,
                       edgecolor="#1e293b", linewidth=0.4)
            ax.set_xticks(range(0, 24, 3))
            ax.set_xticklabels(range(0, 24, 3), color="#94a3b8", fontsize=8.5)
            legend_els = [Patch(facecolor=HOUR_COLORS[s], label=s) for s in hour_order]
            ax.legend(handles=legend_els, fontsize=8, loc="upper left")
            style_ax(ax, fig, xlabel="Jam", ylabel="Rata-rata Penyewaan")
            plt.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()

        with col_e:
            st.markdown('<div class="chart-title">Proporsi Penyewaan per Segmen</div>', unsafe_allow_html=True)

            s = get_plot_style()
            pct = hour_seg_stats["pct_total"].reindex(hour_order)

            fig, ax = plt.subplots(figsize=(5, 4))
            fig.patch.set_facecolor(s["fig_bg"])
            ax.set_facecolor(s["bg"])

            wedges, texts, autotexts = ax.pie(
                pct,
                labels=hour_order,
                colors=[HOUR_COLORS[s_] for s_ in hour_order],
                autopct="%1.1f%%",
                startangle=140,
                wedgeprops={
                    "edgecolor": s["spine"],
                    "linewidth": 1.5
                },
                textprops={
                    "fontsize": 9,
                    "color": s["text"]
                }
            )

            for at in autotexts:
                at.set_fontweight("bold")
                at.set_color(s["text"])

            plt.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()
        
        with col_f:
            st.markdown('<div class="chart-title">Casual vs Registered per Segmen</div>', unsafe_allow_html=True)
            x     = range(len(hour_order))
            width = 0.38
            casual_v = hour_seg_stats["rata2_casual"].reindex(hour_order)
            reg_v    = hour_seg_stats["rata2_registered"].reindex(hour_order)
            fig, ax  = plt.subplots(figsize=(5, 4))
            ax.bar([i-width/2 for i in x], casual_v, width,
                   label="Casual",     color=C["orange"], edgecolor="#1e293b")
            ax.bar([i+width/2 for i in x], reg_v,    width,
                   label="Registered", color=C["blue"],   edgecolor="#1e293b")
            ax.set_xticks(list(x))
            ax.set_xticklabels(hour_order, color="#94a3b8", fontsize=8.5)
            ax.legend(fontsize=9)
            style_ax(ax, fig, ylabel="Rata-rata Penyewaan/Jam")
            plt.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()

        rush_pct    = hour_seg_stats.loc["Rush Hour","pct_total"]
        leisure_pct = hour_seg_stats.loc["Leisure","pct_total"]
        st.info(
            f"📌 **Insight:** **Rush Hour** menyumbang **{rush_pct:.1f}%** dari total penyewaan "
            f"dalam waktu terbatas (±8 jam/hari), dengan dominasi **registered user**. "
            f"Sementara itu, periode **Leisure** ({leisure_pct:.1f}%) didominasi oleh **casual user**, "
            f" yang mencerminkan aktivitas rekreasi. "
            f"Sedangkan periode **Off-Peak & Shoulder** menjadi waktu optimal untuk pemeliharaan dan redistribusi armada."
        )
    # --Tab 3 --
    with tab3:
        st.markdown("#### Heatmap Korelasi Antar Variabel")

        s = get_plot_style()

        corr_cols   = ["temp_c","atemp_c","hum_pct","wind_kmh","casual","registered","cnt"]
        corr_matrix = day_f[corr_cols].corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor(s["fig_bg"])
        ax.set_facecolor(s["bg"])

        heatmap = sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            ax=ax,
            linewidths=0.6,
            linecolor=s["spine"],
            vmin=-1,
            vmax=1,
            cbar_kws={"label": "Korelasi"},
            annot_kws={
                "size": 9,
                "color": s["text"]
            }
        )

        # axis styling
        ax.tick_params(colors=s["tick"], labelsize=9)
        ax.set_title("Heatmap Korelasi Antar Variabel",
                    color=s["text"], fontsize=12, pad=12)

        # colorbar styling
        cbar = heatmap.collections[0].colorbar
        cbar.ax.tick_params(colors=s["tick"], labelsize=8.5)
        cbar.set_label("Korelasi", color=s["tick"], fontsize=9)

        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()

        corr_reg  = day_f[["registered","cnt"]].corr().iloc[0,1]
        corr_temp = day_f[["temp_c","cnt"]].corr().iloc[0,1]

        st.info(
            f"📌 **Insight:** Variabel **registered** memiliki korelasi sangat tinggi dengan total penyewaan "
            f"(r = {corr_reg:.2f}), menunjukkan bahwa pertumbuhan permintaan terutama didorong oleh registered user. "
            f"Suhu juga berpengaruh signifikan (r = {corr_temp:.2f}), "
            f"sementara kelembaban dan kecepatan angin berkorelasi negatif terhadap jumlah penyewaan."
        )

# -- Footer --
st.divider()
st.markdown(
    "📊 Bike Sharing Dataset (2011–2012, Washington D.C.) · "
    "[Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset) · "
    "UCI Machine Learning Repository · "
    "Jihan Timmy Nisrina"
)