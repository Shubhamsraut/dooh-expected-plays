import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from io import BytesIO

EXPLAINER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'DM Sans', sans-serif; }
body { background: #0d1117; color: #e6edf3; }
.calc-panel { background: #161b22; border: 1px solid #30363d; border-radius: 14px; padding: 1.6rem 1.75rem; }
.calc-panel-title { font-size: 1rem; font-weight: 700; color: #f0f6fc; margin-bottom: 0.2rem; }
.calc-panel-sub { font-size: 0.82rem; color: #7d8590; margin-bottom: 1.6rem; }
.calc-step { display: flex; align-items: flex-start; gap: 1rem; padding: 1rem 0; border-bottom: 1px solid #21262d; }
.calc-step:last-child { border-bottom: none; padding-bottom: 0; }
.calc-step-num { width: 28px; height: 28px; border-radius: 50%; background: #0d1117; border: 1px solid #30363d; color: #8b949e; font-size: 0.72rem; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 0.05rem; }
.calc-step-body { flex: 1; }
.calc-step-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #7d8590; margin-bottom: 0.3rem; }
.calc-step-val { font-size: 1rem; font-weight: 600; color: #f0f6fc; font-family: 'DM Mono', monospace; margin-bottom: 0.2rem; }
.calc-step-desc { font-size: 0.82rem; color: #7d8590; line-height: 1.5; }
.day-block { margin-bottom: 0.65rem; }
.day-block-name { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #7d8590; margin-bottom: 0.3rem; }
.chip-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem; }
.chip { background: #1f6feb1a; border: 1px solid #1f6feb44; color: #58a6ff; font-size: 0.75rem; font-family: 'DM Mono', monospace; padding: 0.18rem 0.5rem; border-radius: 5px; }
.chip.none { background: #21262d; border-color: #30363d; color: #7d8590; }
.chip-result { font-size: 0.78rem; color: #7d8590; }
.chip-result strong { color: #c9d1d9; }
.formula-box { background: #0d1117; border: 1px solid #21262d; border-radius: 10px; padding: 1rem 1.25rem; margin-top: 0.85rem; font-family: 'DM Mono', monospace; font-size: 0.83rem; color: #8b949e; line-height: 2; }
.formula-box .final { color: #58a6ff; font-weight: 700; font-size: 0.95rem; border-top: 1px solid #21262d; padding-top: 0.7rem; margin-top: 0.5rem; }
</style>
"""




st.set_page_config(page_title="DOOH Expected Plays", page_icon="📺", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.block-container {
    max-width: 1100px !important;
    padding: 2.5rem 2rem 3rem !important;
}

/* ── Header ── */
.app-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #21262d;
}
.app-header-left h1 {
    font-size: 1.6rem; font-weight: 700;
    color: #f0f6fc; letter-spacing: -0.03em; line-height: 1; margin-bottom: 0.35rem;
}
.app-header-left p { color: #7d8590; font-size: 0.88rem; }
.badge {
    background: #161b22; border: 1px solid #30363d; color: #7d8590;
    font-size: 0.75rem; font-family: 'DM Mono', monospace;
    padding: 0.3rem 0.7rem; border-radius: 6px; letter-spacing: 0.04em;
}

/* ── Stepper ── */
.stepper {
    display: flex; align-items: center; gap: 0;
    margin-bottom: 2.25rem;
    background: #161b22; border: 1px solid #21262d;
    border-radius: 12px; padding: 0.5rem;
}
.step-btn {
    flex: 1; display: flex; align-items: center; justify-content: center;
    gap: 0.55rem; padding: 0.6rem 1rem; border-radius: 8px;
}
.step-num {
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700; flex-shrink: 0;
}
.step-label { font-size: 0.875rem; font-weight: 600; letter-spacing: -0.01em; }
.step-btn.inactive .step-num { background: #21262d; color: #7d8590; }
.step-btn.inactive .step-label { color: #7d8590; }
.step-btn.done .step-num { background: #1f6feb33; color: #58a6ff; }
.step-btn.done .step-label { color: #8b949e; }
.step-btn.active { background: #1f2937; border: 1px solid #30363d; }
.step-btn.active .step-num { background: #1f6feb; color: #fff; }
.step-btn.active .step-label { color: #f0f6fc; }
.step-divider { width: 1px; height: 20px; background: #21262d; flex-shrink: 0; margin: 0 0.25rem; }

/* ── Labels & hints ── */
.section-label {
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #7d8590; margin-bottom: 0.75rem; margin-top: 0.25rem;
}
.hint { font-size: 0.84rem; color: #7d8590; margin-bottom: 1.25rem; line-height: 1.5; }

/* ── Metric cards ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.75rem; }
.metric-card {
    flex: 1; background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 1.1rem 1.25rem;
}
.metric-card .mc-label {
    font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #7d8590; margin-bottom: 0.45rem;
}
.metric-card .mc-value {
    font-size: 1.65rem; font-weight: 700; color: #f0f6fc;
    letter-spacing: -0.03em; font-family: 'DM Mono', monospace; line-height: 1;
}
.metric-card .mc-sub { font-size: 0.75rem; color: #7d8590; margin-top: 0.3rem; }
.metric-card.accent { border-color: #1f6feb55; background: #1f6feb0d; }
.metric-card.accent .mc-value { color: #58a6ff; }

/* ── Breakdown panel ── */
.calc-panel {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 14px; padding: 1.6rem 1.75rem; margin-top: 1.25rem;
}
.calc-panel-title {
    font-size: 1rem; font-weight: 700; color: #f0f6fc;
    margin-bottom: 0.2rem; letter-spacing: -0.01em;
}
.calc-panel-sub { font-size: 0.82rem; color: #7d8590; margin-bottom: 1.6rem; }

.calc-step {
    display: flex; align-items: flex-start; gap: 1rem;
    padding: 1rem 0; border-bottom: 1px solid #21262d;
}
.calc-step:last-child { border-bottom: none; padding-bottom: 0; }
.calc-step-num {
    width: 28px; height: 28px; border-radius: 50%;
    background: #0d1117; border: 1px solid #30363d;
    color: #8b949e; font-size: 0.72rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 0.05rem;
}
.calc-step-body { flex: 1; }
.calc-step-label {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #7d8590; margin-bottom: 0.3rem;
}
.calc-step-val {
    font-size: 1rem; font-weight: 600; color: #f0f6fc;
    font-family: 'DM Mono', monospace; margin-bottom: 0.2rem;
}
.calc-step-desc { font-size: 0.82rem; color: #7d8590; line-height: 1.5; }

/* schedule chips */
.day-block { margin-bottom: 0.65rem; }
.day-block-name {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.07em; color: #7d8590; margin-bottom: 0.3rem;
}
.chip-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem; }
.chip {
    background: #1f6feb1a; border: 1px solid #1f6feb44;
    color: #58a6ff; font-size: 0.75rem; font-family: 'DM Mono', monospace;
    padding: 0.18rem 0.5rem; border-radius: 5px;
}
.chip.none { background: #21262d; border-color: #30363d; color: #7d8590; }
.chip-result { font-size: 0.78rem; color: #7d8590; }
.chip-result strong { color: #c9d1d9; }

/* formula box */
.formula-box {
    background: #0d1117; border: 1px solid #21262d;
    border-radius: 10px; padding: 1rem 1.25rem; margin-top: 0.85rem;
    font-family: 'DM Mono', monospace; font-size: 0.83rem;
    color: #8b949e; line-height: 2;
}
.formula-box .final {
    color: #58a6ff; font-weight: 700; font-size: 0.95rem;
    border-top: 1px solid #21262d; padding-top: 0.7rem; margin-top: 0.5rem;
}

/* streamlit overrides */
div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {
    border: 1px solid #21262d !important; border-radius: 10px !important;
    overflow: hidden !important; background: #161b22 !important;
}
.stButton > button {
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.875rem !important; border-radius: 8px !important;
    min-height: 40px !important; width: 100% !important;
}
.stButton > button[kind="primary"] {
    background: #1f6feb !important; border: 1px solid #388bfd !important; color: #fff !important;
}
.stButton > button[kind="secondary"] {
    background: #161b22 !important; border: 1px solid #30363d !important; color: #c9d1d9 !important;
}
.stDownloadButton > button {
    font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.875rem !important; border-radius: 8px !important;
    background: #161b22 !important; border: 1px solid #30363d !important;
    color: #c9d1d9 !important; width: 100% !important; min-height: 40px !important;
}
div[data-testid="stDateInput"] label, div[data-testid="stFileUploader"] label,
div[data-testid="stSelectbox"] label {
    color: #8b949e !important; font-size: 0.8rem !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 0.07em !important;
}
div[data-testid="stDateInput"] input {
    background: #161b22 !important; border: 1px solid #30363d !important;
    color: #f0f6fc !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important;
}
div[data-testid="stFileUploader"] {
    border: 1px dashed #30363d !important; border-radius: 10px !important; background: #161b22 !important;
}
div[data-testid="stMetric"] { display: none !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "step": 1, "sheet_df": None, "result_df": None,
        "uploaded_name": "",
        "campaign_start": datetime.today().date(),
        "campaign_end": (datetime.today() + timedelta(days=13)).date(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "hour_grid" not in st.session_state:
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        hours = [f"{h:02d}" for h in range(24)]
        g = pd.DataFrame(False, index=days, columns=hours)
        g.loc["Monday", ["08","09","14","15"]] = True
        g.loc["Tuesday", ["09","10","11"]] = True
        g.loc["Friday", ["18","19","20","21"]] = True
        st.session_state.hour_grid = g

init_state()
def go(n): st.session_state.step = n

# ── Core helpers ──────────────────────────────────────────────────────────────
def parse_hhmm(value):
    if pd.isna(value): return None
    if isinstance(value, time): return value
    if isinstance(value, pd.Timestamp): return value.time()
    text = str(value).strip()
    for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p"):
        try: return datetime.strptime(text, fmt).time()
        except ValueError: continue
    return None

def parse_operating_hours(text):
    if pd.isna(text): return None, None
    raw = str(text).strip().replace("–","-").replace("—","-")
    parts = raw.split("-")
    if len(parts) != 2: return None, None
    return parse_hhmm(parts[0]), parse_hhmm(parts[1])

def time_to_minutes(t):
    return t.hour * 60 + t.minute if t else None

def overlap_hours(screen_start, screen_end, slot_start, slot_end):
    ss, se = time_to_minutes(screen_start), time_to_minutes(screen_end)
    cs, ce = time_to_minutes(slot_start), time_to_minutes(slot_end)
    if None in (ss, se, cs, ce) or se <= ss or ce <= cs: return 0.0
    return max(0, min(se, ce) - max(ss, cs)) / 60.0

def build_campaign_dates(start_date, end_date):
    return pd.date_range(start=start_date, end=end_date, freq="D")

def validate_columns(df):
    return [c for c in ["Units","Loop Duration (Sec)","Operating Hours"] if c not in df.columns]

def grid_to_slots(grid_df):
    slots = []
    for day in grid_df.index:
        active_hours = [int(col) for col in grid_df.columns if bool(grid_df.loc[day, col])]
        if not active_hours: continue
        start_hour = prev_hour = active_hours[0]
        for hour in active_hours[1:]:
            if hour != prev_hour + 1:
                slots.append([day, f"{start_hour:02d}:00", f"{prev_hour+1:02d}:00"])
                start_hour = hour
            prev_hour = hour
        end_hour = prev_hour + 1
        slots.append([day, f"{start_hour:02d}:00", "00:00" if end_hour == 24 else f"{end_hour:02d}:00"])
    return pd.DataFrame(slots, columns=["Day","Start","End"])

def calculate_expected_plays(screen_df, grid_df, start_date, end_date):
    schedule_slots = grid_to_slots(grid_df)
    date_range = build_campaign_dates(start_date, end_date)
    rows = []
    for _, row in screen_df.iterrows():
        units = pd.to_numeric(row.get("Units", 0), errors="coerce")
        loop_duration = pd.to_numeric(row.get("Loop Duration (Sec)", 0), errors="coerce")
        op_start, op_end = parse_operating_hours(row.get("Operating Hours"))
        total_overlap = 0.0
        if pd.notna(units) and pd.notna(loop_duration) and loop_duration and op_start and op_end:
            for day in date_range:
                weekday = day.strftime("%A")
                for _, slot in schedule_slots[schedule_slots["Day"] == weekday].iterrows():
                    total_overlap += overlap_hours(op_start, op_end, parse_hhmm(slot["Start"]), parse_hhmm(slot["End"]))
            expected = (3600 / loop_duration) * total_overlap * units
        else:
            expected = 0.0
        result_row = row.to_dict()
        result_row["Expected Plays"] = round(expected, 2)
        result_row["Campaign Days"] = len(date_range)
        result_row["Total Overlap Hours"] = round(total_overlap, 2)
        rows.append(result_row)
    result_df = pd.DataFrame(rows)
    if "Expected Plays" in result_df.columns:
        result_df = result_df.sort_values("Expected Plays", ascending=False)
    return result_df

def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")
    output.seek(0)
    return output.getvalue()

def load_test_schedule():
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    hours = [f"{h:02d}" for h in range(24)]
    g = pd.DataFrame(False, index=days, columns=hours)
    g.loc["Monday", ["08","09","14","15"]] = True
    g.loc["Tuesday", ["00","01","02","03","04","05","21","22"]] = True
    g.loc["Wednesday", ["05","06","12","13","14","15","16","17"]] = True
    g.loc["Thursday", [f"{h:02d}" for h in range(6,23)]] = True
    g.loc["Friday", ["23"]] = True
    g.loc["Saturday", ["10","11","18","19","20","21"]] = True
    g.loc["Sunday", ["03","04","22","23"]] = True
    st.session_state.hour_grid = g

def metric_card(label, value, sub="", accent=False):
    cls = "metric-card accent" if accent else "metric-card"
    sub_html = f"<div class='mc-sub'>{sub}</div>" if sub else ""
    return f'<div class="{cls}"><div class="mc-label">{label}</div><div class="mc-value">{value}</div>{sub_html}</div>'

# ── Calculation explainer ─────────────────────────────────────────────────────
def build_explainer(row_data, grid_df, start_date, end_date):
    units = pd.to_numeric(row_data.get("Units", 0), errors="coerce")
    loop_duration = pd.to_numeric(row_data.get("Loop Duration (Sec)", 0), errors="coerce")
    op_hours_raw = row_data.get("Operating Hours", "")
    op_start, op_end = parse_operating_hours(op_hours_raw)
    date_range = build_campaign_dates(start_date, end_date)
    schedule_slots = grid_to_slots(grid_df)

    DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day_overlap = {d: 0.0 for d in DAYS}
    day_count   = {d: 0   for d in DAYS}

    for day in date_range:
        wd = day.strftime("%A")
        day_count[wd] = day_count.get(wd, 0) + 1
        if op_start and op_end:
            for _, slot in schedule_slots[schedule_slots["Day"] == wd].iterrows():
                day_overlap[wd] += overlap_hours(op_start, op_end, parse_hhmm(slot["Start"]), parse_hhmm(slot["End"]))

    total_overlap   = sum(day_overlap.values())
    plays_per_hour  = (3600 / loop_duration) if (loop_duration and pd.notna(loop_duration)) else 0
    expected        = plays_per_hour * total_overlap * units if (pd.notna(units) and plays_per_hour) else 0

    screen_name = next(
        (str(row_data[c]) for c in ["Screen Name","Screen","Name","Location","Site","ID","Screen ID"] if c in row_data and not pd.isna(row_data[c])),
        "Selected Screen"
    )

    # ── Day-by-day schedule rows ──
    days_html = ""
    for day in DAYS:
        day_slots = schedule_slots[schedule_slots["Day"] == day]
        count = day_count.get(day, 0)
        per_occ = (day_overlap[day] / count) if count else 0.0

        if day_slots.empty:
            chips = '<span class="chip none">No campaign slots</span>'
        else:
            chips = "".join(f'<span class="chip">{r["Start"]}–{r["End"]}</span>' for _, r in day_slots.iterrows())

        if count > 0 and per_occ > 0:
            result_note = f'<span class="chip-result">{per_occ:.2f}h overlap/day × {count} day(s) = <strong>{day_overlap[day]:.2f}h</strong></span>'
        elif count > 0:
            result_note = f'<span class="chip-result">0h overlap (no intersection with screen hours) × {count} day(s)</span>'
        else:
            result_note = '<span class="chip-result" style="color:#484f58">Not in campaign range</span>'

        days_html += f"""
        <div class="day-block">
            <div class="day-block-name">{day}</div>
            <div class="chip-row">{chips}{result_note}</div>
        </div>"""

    op_str = str(op_hours_raw) if not (isinstance(op_hours_raw, float) and pd.isna(op_hours_raw)) else "N/A"

    html = f"""
    <div class="calc-panel">
        <div class="calc-panel-title">Breakdown — {screen_name}</div>
        <div class="calc-panel-sub">Step-by-step trace of how <strong style="color:#f0f6fc">{expected:,.2f} expected plays</strong> was computed for this screen.</div>

        <div class="calc-step">
            <div class="calc-step-num">1</div>
            <div class="calc-step-body">
                <div class="calc-step-label">Campaign Period</div>
                <div class="calc-step-val">{start_date.strftime("%d %b %Y")} → {end_date.strftime("%d %b %Y")}</div>
                <div class="calc-step-desc">{len(date_range)} total days in the campaign window.</div>
            </div>
        </div>

        <div class="calc-step">
            <div class="calc-step-num">2</div>
            <div class="calc-step-body">
                <div class="calc-step-label">Screen Operating Hours</div>
                <div class="calc-step-val">{op_str}</div>
                <div class="calc-step-desc">The screen is physically on during these hours only. Campaign slots outside this window do not contribute to plays.</div>
            </div>
        </div>

        <div class="calc-step">
            <div class="calc-step-num">3</div>
            <div class="calc-step-body">
                <div class="calc-step-label">Loop Duration → Plays per Hour</div>
                <div class="calc-step-val">{loop_duration:.0f}s loop &nbsp;→&nbsp; 3600 ÷ {loop_duration:.0f} = {plays_per_hour:.4f} plays / hour</div>
                <div class="calc-step-desc">How many times the ad plays in one hour of active screen time.</div>
            </div>
        </div>

        <div class="calc-step">
            <div class="calc-step-num">4</div>
            <div class="calc-step-body">
                <div class="calc-step-label">Schedule × Screen Hours — Overlap per Day</div>
                <div class="calc-step-desc" style="margin-bottom:0.9rem;">
                    Each campaign time slot is intersected with the screen's operating hours.
                    Only the overlapping portion counts towards plays.
                </div>
                {days_html}
                <div style="margin-top:0.75rem; padding:0.65rem 0.9rem; background:#0d1117; border:1px solid #21262d; border-radius:8px; font-family:'DM Mono',monospace; font-size:0.82rem; color:#7d8590;">
                    Total overlap across all {len(date_range)} campaign days:&nbsp;
                    <strong style="color:#f0f6fc; font-size:0.95rem;">{total_overlap:.4f} hours</strong>
                </div>
            </div>
        </div>

        <div class="calc-step">
            <div class="calc-step-num">5</div>
            <div class="calc-step-body">
                <div class="calc-step-label">Units</div>
                <div class="calc-step-val">{int(units) if pd.notna(units) else "N/A"} screen unit(s)</div>
                <div class="calc-step-desc">Final plays are multiplied by the number of screen units at this location.</div>
            </div>
        </div>

        <div class="calc-step">
            <div class="calc-step-num">6</div>
            <div class="calc-step-body">
                <div class="calc-step-label">Final Formula</div>
                <div class="calc-step-desc">Combining all values:</div>
                <div class="formula-box">
                    <div>Plays / Hour &nbsp;&nbsp;&nbsp;&nbsp;= 3600 ÷ {loop_duration:.0f} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= {plays_per_hour:.4f}</div>
                    <div>Total Overlap &nbsp;&nbsp;&nbsp;= {total_overlap:.4f} hours</div>
                    <div>Units &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= {int(units) if pd.notna(units) else 0}</div>
                    <div class="final">Expected Plays = {plays_per_hour:.4f} × {total_overlap:.4f} × {int(units) if pd.notna(units) else 0} = <strong>{expected:,.2f}</strong></div>
                </div>
            </div>
        </div>

    </div>"""
    return html

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-header-left">
        <h1>DOOH Expected Plays</h1>
        <p>Calculate expected ad plays across your screen network</p>
    </div>
    <span class="badge">v2.0</span>
</div>
""", unsafe_allow_html=True)

# ── Stepper ───────────────────────────────────────────────────────────────────
step = st.session_state.step
steps_list = [("1","Campaign"), ("2","Upload"), ("3","Results")]

def step_cls(i):
    if i+1 == step: return "active"
    if i+1 < step: return "done"
    return "inactive"

sh = '<div class="stepper">'
for i, (num, label) in enumerate(steps_list):
    sh += f'<div class="step-btn {step_cls(i)}"><span class="step-num">{num}</span><span class="step-label">{label}</span></div>'
    if i < len(steps_list)-1: sh += '<div class="step-divider"></div>'
sh += '</div>'
st.markdown(sh, unsafe_allow_html=True)

# ── Step 1 — Campaign ─────────────────────────────────────────────────────────
if step == 1:
    st.markdown('<div class="section-label">Campaign Period</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,0.6])
    with c1:
        start_date = st.date_input("Start Date", value=st.session_state.campaign_start)
    with c2:
        end_date = st.date_input("End Date", value=st.session_state.campaign_end)
    if end_date < start_date:
        st.error("End date must be after start date.")
    else:
        st.session_state.campaign_start = start_date
        st.session_state.campaign_end   = end_date
        with c3:
            st.markdown(f'<div style="margin-top:1.75rem;">{metric_card("Duration", f"{(end_date-start_date).days+1}d", "campaign days")}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:1.75rem;">Hourly Schedule</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Check the hours your campaign should be active for each day of the week.</div>', unsafe_allow_html=True)

    edited_grid = st.data_editor(
        st.session_state.hour_grid, key="hour_grid_editor",
        use_container_width=True, hide_index=False, height=315,
        column_config={col: st.column_config.CheckboxColumn(col, width="small") for col in st.session_state.hour_grid.columns},
    )
    st.session_state.hour_grid = edited_grid.copy()

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Load Test Schedule", use_container_width=True, type="secondary"):
            load_test_schedule(); st.rerun()
    with b2:
        if st.button("Clear All", use_container_width=True, type="secondary"):
            st.session_state.hour_grid.loc[:,:] = False; st.rerun()
    with b3:
        st.button("Continue →", type="primary", use_container_width=True, on_click=go, args=(2,))

# ── Step 2 — Upload ───────────────────────────────────────────────────────────
elif step == 2:
    st.markdown('<div class="section-label">Upload Screen Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Upload an Excel file with these required columns: <strong>Units</strong>, <strong>Loop Duration (Sec)</strong>, <strong>Operating Hours</strong></div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["xlsx","xls"], key="uploader", label_visibility="collapsed")
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name=0)
            missing = validate_columns(df)
            if missing:
                st.error(f"Missing required columns: {', '.join(missing)}")
            else:
                st.session_state.sheet_df    = df.copy()
                st.session_state.uploaded_name = uploaded_file.name
                st.session_state.result_df   = None
        except Exception as e:
            st.error(f"Could not read file: {e}")

    if st.session_state.sheet_df is not None:
        df = st.session_state.sheet_df
        st.markdown(f"""
        <div class="metric-row">
            {metric_card("File", st.session_state.uploaded_name or "Loaded")}
            {metric_card("Rows", f"{len(df):,}", "screens")}
            {metric_card("Columns", str(len(df.columns)), "fields")}
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Preview — first 10 rows</div>', unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, height=300)

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1: st.button("← Back", use_container_width=True, type="secondary", on_click=go, args=(1,))
    with b2: st.button("Continue →", type="primary", use_container_width=True, on_click=go, args=(3,), disabled=st.session_state.sheet_df is None)

# ── Step 3 — Results ──────────────────────────────────────────────────────────
else:
    if st.session_state.sheet_df is None:
        st.warning("No file uploaded. Please go back and upload your screen data.")
        st.button("← Go to Upload", on_click=go, args=(2,))
    else:
        b1, b2 = st.columns([2,1])
        with b1: run = st.button("⚡  Generate Expected Plays", type="primary", use_container_width=True)
        with b2: st.button("← Back", use_container_width=True, type="secondary", on_click=go, args=(2,))

        if run:
            with st.spinner("Calculating expected plays…"):
                st.session_state.result_df = calculate_expected_plays(
                    st.session_state.sheet_df,
                    st.session_state.hour_grid,
                    st.session_state.campaign_start,
                    st.session_state.campaign_end,
                )

        if st.session_state.result_df is not None:
            result_df  = st.session_state.result_df
            total_plays = result_df["Expected Plays"].sum()
            active_hours = int(st.session_state.hour_grid.sum().sum())
            avg_plays   = total_plays / len(result_df) if len(result_df) else 0

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-row">
                {metric_card("Total Expected Plays", f"{total_plays:,.0f}", "across all screens", accent=True)}
                {metric_card("Screens", f"{len(result_df):,}", "in dataset")}
                {metric_card("Active Hours / Week", f"{active_hours}h", "scheduled")}
                {metric_card("Avg Plays / Screen", f"{avg_plays:,.0f}", "expected")}
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-label">Results — sorted by expected plays</div>', unsafe_allow_html=True)
            st.dataframe(result_df, use_container_width=True, height=380)

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            st.download_button(
                "⬇  Download Results as Excel",
                data=to_excel_bytes(result_df),
                file_name="dooh_expected_plays_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

            # ── Calculation Breakdown ──────────────────────────────────────
            st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">Calculation Breakdown</div>', unsafe_allow_html=True)
            st.markdown('<div class="hint">Select any screen from the dropdown to see an exact step-by-step trace of how its Expected Plays value was computed — useful for QA and cross-checking.</div>', unsafe_allow_html=True)

            id_col = next(
                (c for c in ["Screen Name","Screen","Name","Location","Site","ID","Screen ID"] if c in result_df.columns),
                None
            )
            rdf = result_df.reset_index(drop=True)
            if id_col:
                options = [f"{row[id_col]}  ({row['Expected Plays']:,.2f} plays)" for _, row in rdf.iterrows()]
            else:
                options = [f"Screen {i+1}  ({row['Expected Plays']:,.2f} plays)" for i, row in rdf.iterrows()]

            selected_label = st.selectbox("Select screen to inspect", options=options, label_visibility="visible")
            selected_idx   = options.index(selected_label)
            selected_row   = rdf.iloc[selected_idx].to_dict()

            import streamlit.components.v1 as components
            explainer_html = build_explainer(selected_row, st.session_state.hour_grid, st.session_state.campaign_start, st.session_state.campaign_end)
            components.html(EXPLAINER_CSS + explainer_html, height=1000, scrolling=True)
