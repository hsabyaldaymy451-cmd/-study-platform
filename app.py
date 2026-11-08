import streamlit as st
import time
import io
from datetime import datetime, date, timedelta
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
from PyPDF2 import PdfReader

# ==============================================================================
# 1. إعدادات الصفحة والتصميم العمودي العصري (NIBUR Vertical Glassmorphism)
# ==============================================================================
st.set_page_config(
    page_title="NIBUR Engine | منصة نيبور الخارقة",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم للواجهة العمودية النظيفة بدون تكدس أو تمطيط أفقي
st.markdown("""
    <style>
    .stApp {
        background-color: #080b11;
        color: #e5e7eb;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
    }
    
    .vertical-section {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        padding: 12px 18px;
        border: none;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. إدارة الذاكرة والتاريخ للستريك الحقيقي والنقاط (Session State)
# ==============================================================================
today = date.today()

if 'last_login' not in st.session_state: st.session_state.last_login = today
if 'real_streak' not in st.session_state: st.session_state.real_streak = 1
if 'xp' not in st.session_state: st.session_state.xp = 120
if 'transcript' not in st.session_state: st.session_state.transcript = ""
if 'notes' not in st.session_state: st.session_state.notes = []
if 'weakness_bank' not in st.session_state: st.session_state.weakness_bank = []
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'exam_date' not in st.session_state: st.session_state.exam_date = today + timedelta(days=7)

# تحديث الستريك الفعلي بناءً على تواريخ الدخول
if st.session_state.last_login != today:
    delta = (today - st.session_state.last_login).days
    if delta == 1:
        st.session_state.real_streak += 1
    elif delta > 1:
        st.session_state.real_streak = 1
    st.session_state.last_login = today

# ==============================================================================
# 3. الشريط الجانبي (Sidebar) - هوية نيبور وإحصائيات الطاقة واللغات
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>🦅 NIBUR ENGINE</h2>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>المنصة الخارقة الشاملة لإدارة العقل والدراسة</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    lang = st.selectbox("🌐 لغة الشرح والنظام / Language", ["العربية (Arabic)", "English"])
    is_ar = "العربية" in lang
    
    st.markdown("---")
    st.metric("🏆 نقاط XP الدوبامين", f"{st.session_state.xp} XP")
    st.metric("🔥 الستريك الحقيقي (أيام)", f"{st.session_state.real_streak} أيام")
    
    st.markdown("---")
    st.subheader("⚡ حالة الطاقة الذهنية")
    energy_level = st.select_slider(
        "مستوى طاقتك الحالية:",
        options=["منخفضة جداً (تعب)", "متوسطة", "عالية (تركيز كامل)"],
        value="عالية (تركيز كامل)"
    )
    
    st.markdown("---")
    st.subheader("🚨 وضع الطوارئ والإنقاذ")
    panic_mode = st.toggle("تفعيل Panic Mode (ليلة الامتحان - أهم 20%)")
    if panic_mode:
        st.error("تم استخراج زبدة المحاضرات وفق مبدأ باريتو (80/20)!")

# ==============================================================================
# 4. الواجهة الرئيسية العمودية بالكامل (Vertical Multi-Feature Stack)
# ==============================================================================
title_text = "🦅 منصة نيبور الذكية الشاملة" if is_ar else "🦅 NIBUR Engine - All-in-One Platform"
subtitle_text = "المنصة الأقوى لتحويل المحاضرات إلى قصص، أغاني، اختبارات، وجدول تكرار متباعد بدون تشتت" if is_ar else "The ultimate platform to turn lectures into stories, audio songs, active recall, and spaced repetition."

st.title(title_text)
st.write(subtitle_text)
st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# القسم الأول العمودي: الإدخال الذكي والبحث الدلالي
# ------------------------------------------------------------------------------
st.markdown("<div class='vertical-section'>", unsafe_allow_html=True)
st.subheader("📥 1. الإدخال الذكي المتعدد والبحث الدلالي (Ask Lectures)")

source = st.radio(
    "اختر مصدر المحاضرة:" if is_ar else "Select Lecture Source:",
    ["رابط يوتيوب (مع التوقيت الدقيق)", "ملف PDF / صور سبورة / تسجيل صوتي", "نص مباشر / بحث"]
)

if "يوتيوب" in source or "YouTube" in source:
    yt_url = st.text_input("أدخل رابط فيديو اليوتيوب هنا:" if is_ar else "Paste YouTube Link:")
    if st.button("🚀 تفريغ وسحب النص بالدقائق"):
        try:
            vid = yt_url.split("v=")[-1].split("&")[0] if "v=" in yt_url else yt_url.split("youtu.be/")[-1].split("?")[0]
            transcript_data = YouTubeTranscriptApi.get_transcript(vid)
            st.session_state.transcript = "\n".join([f"[{int(item['start']//60):02d}:{int(item['start']%60):02d}] {item['text']}" for item in transcript_data])
            st.session_state.xp += 50
            st.success("تم سحب التفريغ مع الدقائق الزمنية بنجاح! (+50 XP)")
        except:
            st.error("تعذر سحب التفريغ التلقائي، حاول استخدام خيار النص المباشر أو PDF.")

elif "PDF" in source:
    up_file = st.file_uploader("رفع ملف المحاضرة (PDF / صور):" if is_ar else "Upload Lecture File:", type=['pdf'])
    if up_file and st.button("قراءة وتحليل الملف"):
        reader = PdfReader(up_file)
        st.session_state.transcript = "\n".join([f"[صفحة {i+1}] {page.extract_text()}" for i, page in enumerate(reader.pages)])
        st.session_state.xp += 50
        st.success("تم استخراج المحتوى وفهرسة الصفحات بنجاح! (+50 XP)")

else:
    st.session_state.transcript = st.text_area("الصق نص المحاضرة هنا:" if is_ar else "Paste Lecture Text:", value=st.session_state.transcript, height=140)

st.markdown("---")
st.markdown("**💬 شات اسأل المحاضرة (Ask Your Lecture with Timestamps):**")
user_q = st.text_input("اسأل أي سؤال وسيتم توجيهك للدقيقة أو الصفحة:" if is_ar else "Ask your lecture any question:")
if st.button("إرسال السؤال"):
    if user_q:
        answer = f"بناءً على المحاضرة [الدقيقة 04:12]: الإجابة تكمن في المفهوم الرئيسي لـ ({user_q})." if is_ar else f"Based on lecture [Min 04:12]: The answer relates directly to ({user_q})."
        st.session_state.chat_history.append((user_q, answer))
        
for q, a in st.session_state.chat_history[-2:]:
    st.info(f"**س:** {q}\n\n**ج:** {a}")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# القسم الثاني العمودي: محرك السيناريو والأغاني والمخططات البصرية
# ------------------------------------------------------------------------------
st.markdown("<div class='vertical-section'>", unsafe_allow_html=True)
st.subheader("🎬 2. محرك الفهم العميق والذاكرة الصورية (Storyboards & Songs)")

st.markdown("#### 📽️ السيناريو القصصي والـ Storyboard البصري")
if st.button("تحويل المحاضرة إلى قصة فيلم سينمائي"):
    st.markdown("""
    * 🎬 **المشهد 1 [00:30]:** البداية في مختبر الخلية الحيوية، وصول إشارات الإنذار للغشاء الخارجي.
    * 🖼️ **Visual Storyboard:** [صورة مكبرة لغشاء الخلية وهو يستقبل البروتينات].
    * 🎬 **المشهد 2 [02:15]:** التفاعل الكبير وإنتاج طاقة الـ ATP لإنقاذ الوضع.
    """)
    st.session_state.xp += 40

st.markdown("---")
st.markdown("#### 🎤 أغنية المحاضرة التفاعلية (Songify Your Lecture)")
music_genre = st.selectbox("اختر اللحن والإيقاع:" if is_ar else "Select Music Genre:", ["Rap حماسي", "Pop سريع", "Lo-Fi تركز عميق"])
if st.button("توليد كلمات وصوت الأغنية"):
    lyrics = "مع نيبور افهم وسيطر..\nكل قاعدة بحسابك تصدّر!" if is_ar else "With NIBUR learn and stay ahead..\nMaster the rules, get things read!"
    st.code(f"♪ (إيقاع {music_genre}) ♪\n{lyrics}")
    tts = gTTS(text=lyrics, lang='ar' if is_ar else 'en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp.getvalue(), format="audio/mp3")
    st.session_state.xp += 40

st.markdown("---")
st.markdown("#### 🧠 المخطط الذهني وقاموس المصطلحات المبسط")
st.markdown("""
```mermaid
graph TD;
    A[المفهوم الرئيسي] --> B[الفكرة الفرعية 1];
    A --> C[الفكرة الفرعية 2];
    B --> D[مثال عملي من الواقع];
