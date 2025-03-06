import streamlit as st
from pathlib import Path
import re
import requests

# إعداد مفتاح API
api_key = "AIzaSyAlJNTXZz0UzKhTtYCNSYABkD53g_QnPmE"
api_url = "https://api.gemeni.com/v1/xray-analysis"

# إعداد الواجهة
st.set_page_config(page_title="تحليل الصور الطبية", page_icon=":robot:")
st.image("logo.png", width=200)
st.markdown('<h1 style="color: gray;">🔬 تحليل الصور الطبية</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color: slategray;">تطبيق يساعد في تحليل الصور الطبية</h2>', unsafe_allow_html=True)

# رفع الملف
uploaded_file = st.file_uploader("قم برفع صورة الأشعة الطبية", type=["png", "jpg", "jpeg"])
submit_button = st.button("بدء التحليل")

if submit_button:
    if uploaded_file is not None:
        # حفظ الصورة مؤقتًا
        image_path = Path(f"temp_{uploaded_file.name}")
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # إرسال الصورة إلى API
        with open(image_path, "rb") as img:
            response = requests.post(api_url, files={"image": img}, headers={"Authorization": f"Bearer {api_key}"})

        # عرض النتيجة
        if response.status_code == 200:
            st.subheader("📊 نتائج التحليل:")
            st.json(response.json())
        else:
            st.error("فشل في تحليل الصورة. الرجاء المحاولة لاحقًا.")
    else:
        st.error("يرجى رفع ملف قبل بدء التحليل.")
        
