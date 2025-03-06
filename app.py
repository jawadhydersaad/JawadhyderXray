import streamlit as st
from pathlib import Path
import re
import requests

# إدخال مفتاح API يدويًا
api_key = st.text_input("AIzaSyAlJNTXZz0UzKhTtYCNSYABkD53g_QnPmE:", type="password")
api_url = "https://api.gemini.com/v1/xray-analysis"  # تأكد من صحة هذا الرابط وفقًا لوثائق API

# إعداد الواجهة
st.set_page_config(page_title="تحليل الصور الطبية", page_icon=":robot:")
st.image("logo.png", width=200)
st.markdown('<h1 style="color: gray;">🔬 تحليل الصور الطبية اعداد الطالب : جواد حيدر سعد</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color: slategray;">تطبيق يساعد في تحليل الصور الطبية</h2>', unsafe_allow_html=True)

# رفع الملف
uploaded_file = st.file_uploader("قم برفع صورة الأشعة الطبية", type=["png", "jpg", "jpeg"])
submit_button = st.button("بدء التحليل")

if submit_button:
    if not api_key:
        st.error("يرجى إدخال مفتاح API أولاً.")
    elif uploaded_file is not None:
        # حفظ الصورة مؤقتًا
        image_path = Path(f"temp_{uploaded_file.name}")
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # إرسال الصورة إلى API
        try:
            with open(image_path, "rb") as img:
                response = requests.post(api_url, files={"image": img}, headers={"Authorization": f"Bearer {api_key}"})

            # عرض النتيجة
            if response.status_code == 200:
                st.subheader("📊 نتائج التحليل:")
                st.json(response.json())
            else:
                st.error(f"فشل في تحليل الصورة. الكود: {response.status_code}, رسالة: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("فشل في الاتصال بالخادم. تحقق من اتصالك بالإنترنت أو صحة رابط API.")
        except Exception as e:
            st.error(f"حدث خطأ غير متوقع: {e}")
    else:
        st.error("يرجى رفع ملف قبل بدء التحليل.")
        
