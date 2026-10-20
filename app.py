import streamlit as st
import pandas as pd
from datetime import datetime
import time
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="SafeTown | Smart Township Navigation",
    page_icon="🛡️",
    layout="wide"
)

# ---------- RESTORE SETTINGS MENU & FIX THEME CONTRAST ----------
st.markdown("""
<style>
    /* Unhide top header bar & make transparent so Theme Toggle (Settings) works */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 99999 !important;
    }
    footer {
        visibility: hidden;
        height: 0px;
    }

    /* Page Padding */
    .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* MAIN HEADER CARD: Deep Navy -> Royal Blue -> Teal Glossy 3D Card */
    .glossy-header {
        background: linear-gradient(135deg, #0A192F 0%, #1E3A8A 50%, #0D9488 100%);
        border-radius: 22px;
        padding: 1.4rem 2rem;
        color: #FFFFFF;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 18px 36px -8px rgba(10, 25, 47, 0.5),
            0 8px 16px -6px rgba(0, 0, 0, 0.3),
            inset 0 3px 3px 0px rgba(255, 255, 255, 0.45),
            inset 0 -3px 6px 0px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    .glossy-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 48%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.28) 0%, rgba(255, 255, 255, 0) 100%);
        border-radius: 22px 22px 100% 100% / 22px 22px 20% 20%;
        pointer-events: none;
    }
    .header-title {
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.5px;
        color: #FFFFFF !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    .header-sub {
        font-size: 0.9rem;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 500;
    }

    /* GLOSSY 3D METRIC BUBBLE CARDS */
    .glossy-metric-card {
        border-radius: 20px;
        padding: 1.25rem 1.4rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        cursor: default;
    }
    .glossy-metric-card:hover {
        transform: translateY(-4px) scale(1.02);
    }
    .glossy-metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 48%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.38) 0%, rgba(255, 255, 255, 0) 100%);
        border-radius: 20px 20px 100% 100% / 20px 20px 20% 20%;
        pointer-events: none;
    }
    .metric-card-title {
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        opacity: 0.92;
        margin-bottom: 0.4rem;
        color: #FFFFFF !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    .metric-card-value {
        font-size: 2.25rem;
        font-weight: 900;
        line-height: 1;
        letter-spacing: -1px;
        color: #FFFFFF !important;
        text-shadow: 0 2px 5px rgba(0,0,0,0.4);
    }
    .metric-card-badge {
        display: inline-block;
        margin-top: 0.5rem;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 800;
        background: rgba(255, 255, 255, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: #FFFFFF !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    /* Metric Card Color Variations */
    .metric-sapphire {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #06B6D4 100%);
        border: 1px solid #60A5FA;
        box-shadow: 
            0 14px 28px -4px rgba(37, 99, 235, 0.45),
            0 6px 10px -4px rgba(0, 0, 0, 0.2),
            inset 0 3px 3px 0px rgba(255, 255, 255, 0.6),
            inset 0 -3px 6px 0px rgba(0, 0, 0, 0.4);
    }
    .metric-violet {
        background: linear-gradient(135deg, #4C1D95 0%, #7C3AED 50%, #A855F7 100%);
        border: 1px solid #C084FC;
        box-shadow: 
            0 14px 28px -4px rgba(124, 58, 237, 0.45),
            0 6px 10px -4px rgba(0, 0, 0, 0.2),
            inset 0 3px 3px 0px rgba(255, 255, 255, 0.6),
            inset 0 -3px 6px 0px rgba(0, 0, 0, 0.4);
    }
    .metric-coral {
        background: linear-gradient(135deg, #881337 0%, #E11D48 50%, #F43F5E 100%);
        border: 2px solid #FDA4AF;
        box-shadow: 
            0 14px 28px -4px rgba(225, 29, 72, 0.5),
            0 6px 10px -4px rgba(0, 0, 0, 0.2),
            inset 0 3px 3px 0px rgba(255, 255, 255, 0.7),
            inset 0 -3px 6px 0px rgba(0, 0, 0, 0.4);
    }
    .metric-emerald {
        background: linear-gradient(135deg, #064E3B 0%, #10B981 50%, #059669 100%);
        border: 1px solid #6EE7B7;
        box-shadow: 
            0 14px 28px -4px rgba(16, 185, 129, 0.45),
            0 6px 10px -4px rgba(0, 0, 0, 0.2),
            inset 0 3px 3px 0px rgba(255, 255, 255, 0.6),
            inset 0 -3px 6px 0px rgba(0, 0, 0, 0.4);
    }

    /* DASHBOARD PANELS (DARK SLATE GLOSS FOR HIGH CONTRAST) */
    div[data-testid="stContainer"] {
        background: linear-gradient(160deg, #0F172A 0%, #1E293B 100%) !important;
        border-radius: 22px !important;
        border: 2px solid #0EA5E9 !important;
        box-shadow: 
            0 18px 36px -8px rgba(14, 165, 233, 0.25),
            0 6px 12px -4px rgba(0, 0, 0, 0.4),
            inset 0 2px 3px 0px rgba(255, 255, 255, 0.2),
            inset 0 -3px 6px 0px rgba(0, 0, 0, 0.5) !important;
        padding: 1.3rem !important;
    }

    /* Typography Contrast Inside Panels */
    div[data-testid="stContainer"] h1, 
    div[data-testid="stContainer"] h2, 
    div[data-testid="stContainer"] h3, 
    div[data-testid="stContainer"] h4, 
    div[data-testid="stContainer"] p, 
    div[data-testid="stContainer"] span, 
    div[data-testid="stContainer"] label {
        color: #F8FAFC !important;
    }

    /* Glossy Tab Buttons */
    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 6px 16px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        border: 1px solid #38BDF8 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- 5 TOWNSHIP LOCATIONS (SIMULATED MAP DATA) ----------
TOWNSHIP_MAP_CENTER = [3.1705, 101.5204]

TOWNSHIP_LOCATIONS = {
    "Residential Complex (Home)": {
        "coords": [3.1712, 101.5195],
        "icon": "home",
        "color": "green",
        "desc": "Block A, Level 2 (Unit A-12)"
    },
    "Township Management Office": {
        "coords": [3.1685, 101.5180],
        "icon": "briefcase",
        "color": "blue",
        "desc": "Hackathon Township Admin Hub"
    },
    "Guard House & Security Post": {
        "coords": [3.1698, 101.5215],
        "icon": "shield",
        "color": "red",
        "desc": "Main Gate 24/7 Security Command"
    },
    "Recreational Park & Lake": {
        "coords": [3.1730, 101.5210],
        "icon": "tree",
        "color": "purple",
        "desc": "Central Park & Elderly Walking Track"
    },
    "Community Wellness & Health Clinic": {
        "coords": [3.1725, 101.5230],
        "icon": "plus-square",
        "color": "orange",
        "desc": "First-Aid & Senior Wellness Center"
    }
}

# ---------- DEMO RESIDENT DATABASE ----------
RESIDENT_PROFILES = {
    "RES-8821": {
        "Name": "Ahmad Ariff",
        "Emergency Contact": "Farah Ahmad (Daughter)",
        "Phone": "+60 12-345 6789"
    },
    "RES-4032": {
        "Name": "Wong Jun Kai",
        "Emergency Contact": "Wong Jun Wai (Son)",
        "Phone": "+60 17-888 9900"
    },
    "RES-4132": {
        "Name": "Karthick Raman",
        "Emergency Contact": "Adithyaa Raman (Son)",
        "Phone": "+60 17-888 7700"
    }
}

# ---------- SESSION DATA INITIALIZATION ----------
if "incidents" not in st.session_state:
    st.session_state.incidents = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 101

def create_alert(resident_id, origin_loc, event, details, priority="High"):
    profile = RESIDENT_PROFILES.get(resident_id, RESIDENT_PROFILES["RES-8821"])
    incident = {
        "ID": f"INC-{st.session_state.next_id}",
        "Timestamp": datetime.now(),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Resident ID": resident_id,
        "Resident Name": profile["Name"],
        "Location": origin_loc,
        "Emergency Contact": profile["Emergency Contact"],
        "Contact Phone": profile["Phone"],
        "Event": event,
        "Priority": priority,
        "Status": "Awaiting response",
        "Details": details,
        "Escalated": False,
        "Dismissed": False
    }
    st.session_state.incidents.insert(0, incident)
    st.session_state.next_id += 1

# ---------- SINGLE-TRIGGER SLA ESCALATION LOGIC ----------
needs_timer = False
time_left = 10.0

now = datetime.now()
for inc in st.session_state.incidents:
    if inc["Status"] == "Awaiting response" and not inc.get("Dismissed", False):
        elapsed = (now - inc["Timestamp"]).total_seconds()
        if elapsed >= 10:
            if not inc.get("Escalated", False):
                inc["Escalated"] = True
                inc["Priority"] = "CRITICAL (ESCALATED)"
        else:
            needs_timer = True
            time_left = min(time_left, max(0.1, 10.0 - elapsed))

# ---------- 3D GLOSSY HEADER BUBBLE ----------
st.markdown("""
<div class="glossy-header">
    <div class="header-title">🛡️ SafeTown Command Center</div>
    <div class="header-sub">Hackathon Township — Interactive Navigation & Elderly Response</div>
</div>
""", unsafe_allow_html=True)

# ---------- 3D GLOSSY METRIC BUBBLE CARDS ----------
all_incidents = st.session_state.incidents
visible_incidents = [i for i in all_incidents if not i.get("Dismissed", False)]
active_queue = [i for i in visible_incidents if i["Status"] != "Resolved"]
unack_queue = [i for i in visible_incidents if i["Status"] == "Awaiting response"]

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="glossy-metric-card metric-sapphire">
        <div class="metric-card-title">Total Cases Logged</div>
        <div class="metric-card-value">{len(all_incidents)}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="glossy-metric-card metric-violet">
        <div class="metric-card-title">Active Response Queue</div>
        <div class="metric-card-value">{len(active_queue)}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    badge_html = '<div class="metric-card-badge">⚠️ Immediate Action Needed</div>' if unack_queue else ''
    st.markdown(f"""
    <div class="glossy-metric-card metric-coral">
        <div class="metric-card-title">Awaiting Response</div>
        <div class="metric-card-value">{len(unack_queue)}</div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="glossy-metric-card metric-emerald">
        <div class="metric-card-title">Cases Resolved</div>
        <div class="metric-card-value">{sum(1 for i in all_incidents if i["Status"] == "Resolved")}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- TWO-PANEL 3D GLASS DASHBOARD ----------
left, right = st.columns([1, 1.2], gap="large")

# --------------------------------------------------
# PANEL A: ELDERLY RESIDENT DEVICE INTERFACE
# --------------------------------------------------
with left:
    with st.container(border=True):
        st.subheader("⌚ Resident Device Companion")

        selected_res_id = st.selectbox(
            "Active Resident Profile:",
            options=list(RESIDENT_PROFILES.keys()),
            format_func=lambda x: f"{RESIDENT_PROFILES[x]['Name']} ({x})"
        )

        origin_name = st.selectbox(
            "📍 Resident's Current Location:",
            options=list(TOWNSHIP_LOCATIONS.keys()),
            index=3  # Default to Recreational Park
        )

        tab_sos, tab_voice, tab_nav = st.tabs(["🚨 Emergency SOS", "🎙️ Voice Assistant", "🗺️ Safe Wayfinding Map"])

        # TAB 1: EMERGENCY SOS
        with tab_sos:
            st.caption("Press to trigger an immediate fall alert from your current location.")
            if st.button("🔴 SIMULATE FALL DETECTED", type="primary", use_container_width=True):
                create_alert(
                    selected_res_id,
                    origin_name,
                    "Automated Fall Detection",
                    f"Impact sensor threshold exceeded at {origin_name}."
                )
                st.toast(f"Emergency Fall Alert dispatched from {origin_name}!", icon="🚨")
                st.rerun()

        # TAB 2: VOICE ASSISTANT
        with tab_voice:
            command = st.text_input("Voice Input Console:", placeholder="e.g. Help me I fell down")
            if st.button("Process Voice Command", use_container_width=True):
                if command.strip():
                    text = command.lower().strip()
                    if any(word in text for word in ["help", "emergency", "hurt", "fell", "fall", "pain"]):
                        create_alert(
                            selected_res_id,
                            origin_name,
                            "Voice SOS Triggered",
                            f"Transcribed phrase at {origin_name}: '{command}'"
                        )
                        st.toast("Voice SOS Alert Transmitted!", icon="⚠️")
                        st.rerun()
                    elif any(word in text for word in ["home", "navigate", "direction", "route", "security"]):
                        st.success("Safe Wayfinding map updated! Switch to the Navigation tab.")
                    else:
                        st.info("Inquiry logged. Connecting to Township Concierge.")
                else:
                    st.warning("Please type or speak a phrase first.")

        # TAB 3: DYNAMIC SAFE NAVIGATION
        with tab_nav:
            st.caption("Select destination to generate a sheltered safe route.")

            dest_options = [loc for loc in TOWNSHIP_LOCATIONS.keys() if loc != origin_name]
            dest_name = st.selectbox(
                "🏁 Destination:",
                options=dest_options,
                index=0
            )

            orig_data = TOWNSHIP_LOCATIONS[origin_name]
            dest_data = TOWNSHIP_LOCATIONS[dest_name]

            st.info(f"➡️ **Sheltered Safe Walkway:** {origin_name} ➔ Rest Bench B2 ➔ {dest_name}")

            nav_map = folium.Map(location=TOWNSHIP_MAP_CENTER, zoom_start=16, tiles="CartoDB positron")

            folium.Marker(
                orig_data["coords"],
                popup=f"Origin: {origin_name}",
                tooltip=f"📍 YOU ARE HERE ({origin_name})",
                icon=folium.Icon(color="green", icon="user", prefix="fa")
            ).add_to(nav_map)

            folium.Marker(
                dest_data["coords"],
                popup=f"Destination: {dest_name}",
                tooltip=f"🏁 DESTINATION ({dest_name})",
                icon=folium.Icon(color="blue", icon="flag", prefix="fa")
            ).add_to(nav_map)

            for name, loc in TOWNSHIP_LOCATIONS.items():
                if name not in [origin_name, dest_name]:
                    folium.Marker(
                        loc["coords"],
                        popup=name,
                        tooltip=name,
                        icon=folium.Icon(color="gray", icon=loc["icon"], prefix="fa")
                    ).add_to(nav_map)

            folium.PolyLine(
                locations=[orig_data["coords"], dest_data["coords"]],
                color="#0D9488",
                weight=5,
                opacity=0.8,
                dash_array="8"
            ).add_to(nav_map)

            st_folium(
                nav_map,
                height=280,
                width=None,
                use_container_width=True,
                key="safe_nav_map",
                returned_objects=[]
            )

# --------------------------------------------------
# PANEL B: EMERGENCY RESPONSE CENTRE
# --------------------------------------------------
with right:
    with st.container(border=True):
        st.subheader("🏢 Emergency Response Centre")

        escalated_active = [i for i in visible_incidents if i.get("Escalated") and i["Status"] == "Awaiting response"]
        if escalated_active:
            st.error(f"🚨 **CRITICAL SLA ESCALATION:** {len(escalated_active)} case(s) unacknowledged for >10s!")

        tab_cases, tab_audit = st.tabs(["🚨 Active Live Cases", "📋 Audit Log & Exports"])

        with tab_cases:
            if not visible_incidents:
                st.info("🟢 Safe Status: No active emergency cases in the response queue.")
            else:
                for idx, incident in enumerate(visible_incidents):
                    with st.container(border=True):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.markdown(f"### **{incident['ID']}** — {incident['Event']}")
                        with c2:
                            if "CRITICAL" in incident["Priority"]:
                                st.error("🚨 CRITICAL SLA")
                            else:
                                st.warning(f"Priority: {incident['Priority']}")

                        st.write(f"👤 **Resident:** {incident['Resident Name']} (`{incident['Resident ID']}`)")
                        st.write(f"📍 **Location:** {incident['Location']} | ⏱️ **Time:** {incident['Time']}")
                        st.markdown(f"📞 **Next-of-Kin Contact:** {incident['Emergency Contact']} (`{incident['Contact Phone']}`)")

                        status_options = ["Awaiting response", "Acknowledged", "Responding", "Resolved"]
                        selected_status = st.selectbox(
                            "Update Incident Status:",
                            status_options,
                            index=status_options.index(incident["Status"]),
                            key=f"status_{incident['ID']}_{idx}"
                        )

                        if selected_status != incident["Status"]:
                            incident["Status"] = selected_status
                            # AUTOMATIC DISMISSAL ON RESOLUTION
                            if selected_status == "Resolved":
                                incident["Dismissed"] = True
                                st.toast(f"✅ Case {incident['ID']} marked Resolved & automatically cleared from queue!", icon="🟢")
                            else:
                                st.toast(f"{incident['ID']} status updated to {selected_status}")
                            st.rerun()

        with tab_audit:
            if all_incidents:
                df_log = pd.DataFrame(all_incidents)
                audit_df = df_log[[
                    "ID", "Time", "Resident ID", "Resident Name",
                    "Event", "Location", "Status", "Emergency Contact", "Contact Phone"
                ]]
                st.dataframe(audit_df, use_container_width=True, hide_index=True, height=220)

                csv_data = audit_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Export Full Audit Log (CSV)",
                    data=csv_data,
                    file_name=f"SafeTown_Audit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.caption("No historical records logged yet.")

st.caption("ℹ️ *SafeTown Prototype: All emergency payloads, fall detection events, and wayfinding data are simulated software events.*")

# ---------- EXECUTE SINGLE TIMER RERUN FOR SLA ----------
if needs_timer:
    time.sleep(time_left)
    st.rerun()