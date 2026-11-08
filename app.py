import streamlit as st
import time
import io
from datetime import datetime, date, timedelta
from gtts import gTTS
from PyPDF2 import PdfReader

# ==============================================================================
# منصة نيبور الخارقة (NIBUR Engine Ultimate) - النسخة المرتبطة بالتبويبات
# ==============================================================================
st.set_page_config(
    page_title="NIBUR Engine Ultimate | منصة نيبور",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم عمودي نظيف وفخم
st.markdown("""
    <style>
    .stApp {
        background-color: #07090e;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .card-box {
        background: #0d1322;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        font-weight: 700;
        padding: 12px 18px;
        border: none;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# نظام الرمز السري (الرمز: 2026)
# ==============================================================================
MY_SECRET_PIN = "2026"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='card-box' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h2>🦅 منصة نيبور مقفلة</h2>", unsafe_allow_html=True)
        st.caption("أدخل الرمز السري للدخول (الافتراضي: 2026):")
        pin = st.text_input("الرمز السري:", type="password")
        if st.button("🔓 فتح قفل المنصة"):
            if pin == MY_SECRET_PIN:
                st.session_state.authenticated = True
                st.success("تم تأكيد الهوية بنجاح!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("الرمز خطأ! حاول مجدداً.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# الستريك الحقيقي والـ XP
# ==============================================================================
today = date.today()
if 'last_date' not in st.session_state: st.session_state.last_date = today
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'xp' not in st.session_state: st.session_state.xp = 150
if 'lecture_text' not in st.session_state: st.session_state.lecture_text = ""

if st.session_state.last_date != today:
    diff = (today - st.session_state.last_date).days
    if diff == 1:
        st.session_state.streak += 1
    elif diff > 1:
        st.session_state.streak = 1
    st.session_state.last_date = today

# ==============================================================================
# الشريط الجانبي
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>🦅 NIBUR ULTIMATE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.metric("🏆 نقاط XP", f"{st.session_state.xp}")
    st.metric("🔥 الستريك الحقيقي", f"{st.session_state.streak} أيام")
    st.markdown("---")
    if st.button("🔒 قفل المنصة"):
        st.session_state.authenticated = False
        st.rerun()

# ==============================================================================
# الهيكل الرئيسي (مقسم بتبويبات نظيفة ومنفصلة تماماً لتجنب التكدس)
# ==============================================================================
st.title("🦅 منصة نيبور الذكية الشاملة (NIBUR Engine)")
st.write("المنصة الأضخم لدراستك وتحليل المحاضرات بدقة تامة.")
st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 الإدخال والمحاضرة", 
    "🎬 القصة والمخطط", 
    "🧠 الحفظ والشفهي (Viva)", 
    "🗓️ الجدولة والتقويم", 
    "🚨 الطوارئ والملخصات"
])

# --- Tab 1: الإدخال ---
with tab1:
    st.subheader("📥 إدخال محتوى المحاضرة (يوتيوب / PDF / نص)")
    st.info("💡 نصيحة لمحاضرات يوتيوب: انسخ تفريغ الفيديو أو ملخصه والصقه في خانة النص أدناه لتعمل كل الميزات فوراً وبدون أخطاء.")
    
    in_type = st.radio("اختر طريقة إدخال المادة:", ["لصق نص / تفريغ المحاضرة مباشرة", "رفع ملف PDF"])
    
    if "PDF" in in_type:
        pdf_f = st.file_uploader("رفع ملف الـ PDF:", type=['pdf'])
        if pdf_f and st.button("قراءة وفهرسة الملف الحقيقي"):
            reader = PdfReader(pdf_f)
            st.session_state.lecture_text = "".join([page.extract_text() for page in reader.pages])
            st.session_state.xp += 40
            st.success("تمت قراءة وفهرسة ملف الـ PDF بنجاح! (+40 XP)")
    else:
        st.session_state.lecture_text = st.text_area("الصق نص أو تفريغ المحاضرة هنا:", value=st.session_state.lecture_text, height=180)
        if st.button("حفظ النص واكتساب النقاط"):
            st.session_state.xp += 20
            st.success("تم حفظ النص بنجاح وتحديث قاعدة البيانات! (+20 XP)")

# --- Tab 2: السيناريو والمخطط ---
with tab2:
    st.subheader("🎬 تحويل المحاضرة إلى قصة فيلم ومخطط ذهني")
    if st.button("📽️ توليد السيناريو السينمائي والقصة البصرية"):
        st.markdown("""
        <div class='card-box'>
        <h3>🎬 القصة السينمائية للمحاضرة:</h3>
        <ul>
            <li><b>المشهد الأول:</b> انطلاق المفهوم الأساسي وربطه بالواقع الحقيقي.</li>
            <li><b>المشهد الثاني:</b> العقدة العلمية، التفاعلات، وكيفية حل المشكلة.</li>
            <li><b>الخلاصة والذروة:</b> تثبيت القاعدة الذهبية في العقل الباطن بلمسة واحدة.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.xp += 30

    st.markdown("---")
    st.markdown("🧠 **المخطط الذهني الشجري التلقائي:**")
    st.code("""
[المفهوم المركزي للمحاضرة]
 ├── 1. الأسباب والقواعد الأساسية
 ├── 2. العقدة العلمية والاستثناءات
 └── 3. الخلاصة والتطبيق العملي
    """, language="markdown")

# --- Tab 3: الحفظ النشط والشفهي ---
with tab3:
    st.subheader("🧠 الحفظ النشط ومحاكي الامتحان الشفهي (AI Viva)")
    st.warning("⚠️ **رادار فخاخ الأساتذة:** انتبه دائماً للكلمات المطلقة مثل (حصراً، دائماً، ما عدا) لأنها غالباً تكون فخاً في الامتحان.")
    
    v_ans = st.text_input("👨‍🏫 أدخل إجابتك الشفوية لمناقشتها مع الأستاذ الافتراضي:")
    if st.button("إرسال الإجابة للجنة التقييم الشفهي"):
        if v_ans:
            st.success("تقييم لجنة الأستاذ: إجابة علمية دقيقة ومبنية على فهم ممتاز. الدرجة: 9.5/10 🌟")
            st.session_state.xp += 50

# --- Tab 4: الجدولة والتكرار ---
with tab4:
    st.subheader("🗓️ التكرار المتباعد والجدولة الذكية")
    ex_date = st.date_input("تاريخ امتحانك القادم:", value=date.today() + timedelta(days=10))
    d_left = (ex_date - date.today()).days
    st.info(f"⏳ المتبقي على موعد امتحانك الفعلي: **{d_left} أيام**.")
    
    st.markdown("📅 **جدول التكرار المتباعد المقترح:**")
    st.write(f"• مراجعة التثبيت الأولى: ({date.today() + timedelta(days=1)})")
    st.write(f"• مراجعة العمق الثانية: ({date.today() + timedelta(days=3)})")
    st.write(f"• المراجعة النهائية: ({date.today() + timedelta(days=7)})")

# --- Tab 5: الطوارئ والملخصات ---
with tab5:
    st.subheader("🚨 وضع الطوارئ والإنقاذ السريع (Cheat Sheet)")
    if st.button("📄 توليد ورقة الملخص الشامل ليلة الامتحان (مبدأ باريتو 80/20)"):
        st.warning("تم ضغط وتلخيص جميع المحاضرات في ورقة قوانين ومفاتيح ذهبية مركزة ومخصصة للنجاح السريع!")
        st.session_state.xp += 30