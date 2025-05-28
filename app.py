import streamlit as st

# זמני ברירת מחדל (בדקות)
TIMES = {
    'video_shooting': 1,  # לדקה של ניתוח
    'tools_model_simple': 180,
    'tools_model_complex': 600,
    'tool_request': 3,
    'tools_upload': 2,
    'script_build': 180,
    'video_editing': 120,
    'voice_recording': 90,
    'scenario_creation': 60
}

def calculate_total_time(data):
    time = 0
    time += data['duration'] * TIMES['video_shooting']
    time += data['tool_requests'] * TIMES['tool_request']
    time += data['simple_models'] * TIMES['tools_model_simple']
    time += data['complex_models'] * TIMES['tools_model_complex']

    if data['build_script']:
        time += TIMES['script_build']
    if data['edit_video']:
        time += TIMES['video_editing']
    if data['record_voice']:
        time += TIMES['voice_recording']
    if data['upload_tools']:
        time += data['tools_used'] * TIMES['tools_upload']
    if data['create_scenario']:
        time += TIMES['scenario_creation']

    return time

# UI
st.set_page_config(page_title="מחשבון זמן הפקת ניתוח VR", layout="centered")

st.title("🕒 מחשבון זמן הפקת סימולציית ניתוח VR")
st.markdown("מלא את הנתונים הבאים וחשב את משך הזמן הכולל להפקת סימולציית ניתוח במציאות מדומה.")

with st.form("vr_calc_form"):
    name = st.text_input("🔬 שם הניתוח", value="ניתוח לדוגמה")
    duration = st.number_input("⏱ משך הניתוח הרצוי (בדקות)", min_value=1, value=10)
    tools_used = st.number_input("🔧 מספר הכלים בניתוח", min_value=0, value=5)
    tool_requests = st.number_input("📣 מספר בקשות לכלים במהלך הניתוח", min_value=0, value=10)
    simple_models = st.number_input("🛠 מספר כלים פשוטים חדשים למידול", min_value=0, value=1)
    complex_models = st.number_input("⚙️ מספר כלים מורכבים חדשים למידול", min_value=0, value=1)

    build_script = st.checkbox("✍️ בניית תסריט עם אח בכיר", value=True)
    edit_video = st.checkbox("🎞 עריכת וידאו", value=True)
    record_voice = st.checkbox("🎙 הקלטת קריינות ושיפור סאונד", value=True)
    upload_tools = st.checkbox("📤 העלאת כלים למערכת", value=True)
    create_scenario = st.checkbox("🧪 יצירת תרחיש חדש במערכת", value=True)

    submitted = st.form_submit_button("חשב זמן")

if submitted:
    inputs = {
        'duration': duration,
        'tools_used': tools_used,
        'tool_requests': tool_requests,
        'simple_models': simple_models,
        'complex_models': complex_models,
        'build_script': build_script,
        'edit_video': edit_video,
        'record_voice': record_voice,
        'upload_tools': upload_tools,
        'create_scenario': create_scenario
    }

    total_minutes = calculate_total_time(inputs)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    st.success(f"⏳ זמן הפקה מוערך ל״{name}״: {hours} שעות ו-{minutes} דקות.")

