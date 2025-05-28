import streamlit as st
from datetime import timedelta
import json
import os

st.set_page_config(page_title="מחשבון זמן הפקת ניתוח VR", layout="centered")

st.markdown("""
    <style>
        body, .stApp { direction: rtl; text-align: right; }
        .stButton>button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🕒 מחשבון זמן הפקת סימולציית ניתוח VR")
st.markdown("מלא את הנתונים הבאים כדי לחשב את זמן ההפקה המשוער")

# קובץ לשמירת הגדרות זמני ברירת מחדל
SETTINGS_FILE = "time_settings.json"

# הגדרות ברירת מחדל
DEFAULT_TIMES = {
    'video_shooting_per_min': 1,
    'tool_request': 3,
    'tools_model_simple': 480,  # דקות
    'tools_model_complex': 1440,
    'script_build': 180,
    'video_editing': 120,
    'voice_recording': 90,
    'tools_upload_per_tool': 2,
    'scenario_creation': 60
}

# טען הגדרות אם קיימות
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        time_settings = json.load(f)
else:
    time_settings = DEFAULT_TIMES.copy()

with st.expander("⚙️ הגדר זמני משימות (בדקות)"):
    for key in time_settings:
        label = {
            'video_shooting_per_min': '⏱ זמן צילום לדקת ניתוח',
            'tool_request': '📣 זמן לבקשת כלי',
            'tools_model_simple': '🛠 זמן מידול כלי פשוט',
            'tools_model_complex': '⚙️ זמן מידול כלי מורכב',
            'script_build': '✍️ זמן לבניית תסריט',
            'video_editing': '🎞 זמן עריכת וידאו',
            'voice_recording': '🎙 זמן קריינות ושיפור סאונד',
            'tools_upload_per_tool': '📤 זמן העלאת כלי',
            'scenario_creation': '🧪 זמן יצירת תרחיש'
        }[key]
        time_settings[key] = st.number_input(label, min_value=0, value=time_settings[key], step=5)

    # שמירה
    if st.button("💾 שמור הגדרות זמן"):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(time_settings, f, ensure_ascii=False)
        st.success("ההגדרות נשמרו בהצלחה")

# טופס הזנת נתוני ניתוח
with st.form("vr_calc_form"):
    name = st.text_input("🔬 שם הניתוח", value="ניתוח לדוגמה")
    duration = st.number_input("משך הניתוח הרצוי (בדקות)", min_value=1, value=10)
    tools_used = st.number_input("מספר הכלים בניתוח", min_value=0, value=5)
    tool_requests = st.number_input("מספר בקשות לכלים במהלך הניתוח", min_value=0, value=10)
    simple_models = st.number_input("מספר כלים פשוטים חדשים למידול", min_value=0, value=1)
    complex_models = st.number_input("מספר כלים מורכבים חדשים למידול", min_value=0, value=1)

    build_script_time = st.number_input("⏳ זמן לבניית תסריט (בדקות)", min_value=0, value=time_settings['script_build'])
    edit_video_time = st.number_input("⏳ זמן עריכת וידאו (בדקות)", min_value=0, value=time_settings['video_editing'])
    voice_recording_time = st.number_input("⏳ זמן קריינות ושיפור סאונד (בדקות)", min_value=0, value=time_settings['voice_recording'])
    scenario_creation_time = st.number_input("⏳ זמן יצירת תרחיש חדש (בדקות)", min_value=0, value=time_settings['scenario_creation'])

    submitted = st.form_submit_button("חשב זמן")

if submitted:
    total_minutes = 0
    total_minutes += duration * time_settings['video_shooting_per_min']
    total_minutes += tool_requests * time_settings['tool_request']
    total_minutes += simple_models * time_settings['tools_model_simple']
    total_minutes += complex_models * time_settings['tools_model_complex']
    total_minutes += tools_used * time_settings['tools_upload_per_tool']
    total_minutes += build_script_time
    total_minutes += edit_video_time
    total_minutes += voice_recording_time
    total_minutes += scenario_creation_time

    total_time = timedelta(minutes=total_minutes)
    hours, minutes = divmod(total_time.seconds // 60, 60)

    st.success(f"⏳ זמן הפקה מוערך ל־\"{name}\": {total_time.days * 24 + hours} שעות ו-{minutes} דקות")
