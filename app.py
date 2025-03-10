import streamlit as st
from PIL import Image
import google.generativeai as genai
from configs import SYSTEM_PROMPT, SAFETY_SETTINGS, GENERATION_CONFIG, MODEL_NAME

def configure_model():
    genai.configure(api_key="AIzaSyByxD3APIGmf1aA_PnTzR7jpl53FvUzwlk")
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
        system_instruction=SYSTEM_PROMPT
    )

# إعداد الصفحة
st.set_page_config(page_title='تحليل الأشعة السينية', page_icon='⚕️', layout='wide')
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #2E8B57;
        }
        .subheader {
            text-align: center;
            font-size: 20px;
            color: #555;
        }
        .stButton>button {
            width: 100%;
            background: #2E8B57;
            color: white;
            font-size: 18px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">الاعداد : جواد حيدر سعد تحليل الأشعة السينية بالذكاء الاصطناعي</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">رفع صورة الأشعة السينية وتحليلها لاكتشاف الأمراض المحتملة</p>', unsafe_allow_html=True)

# تقسيم الصفحة
col1, col2 = st.columns([1, 2])
uploaded_file = col1.file_uploader("📤 رفع صورة الأشعة السينية:", type=['png', 'jpg', 'jpeg'])
submit_btn = col1.button("🔎 تحليل الصورة")

if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        col2.image(image, caption='📷 الصورة المرفوعة', use_column_width=True)
    except Exception as e:
        st.error(f"❌ خطأ في تحميل الصورة: {e}")
        image = None

if submit_btn and uploaded_file:
    if image:
        model = configure_model()
        chat_session = model.start_chat()

        content = [
            "هذه صورة أشعة سينية لمريض. قم بتحليلها لاكتشاف أي أمراض محتملة، مثل الالتهاب الرئوي، الكسور، الأورام، السل، أمراض القلب أو أي حالات غير طبيعية أخرى. قدم تقريرًا طبيًا شاملًا.",
            image
        ]

        response = chat_session.send_message(content)
        st.success("✅ تم تحليل الصورة بنجاح!")
        st.markdown("### 📝 التقرير الطبي:")
        st.write(response.text)
    else:
        st.error("⚠️ يرجى تحميل صورة صالحة قبل التحليل.")
        
