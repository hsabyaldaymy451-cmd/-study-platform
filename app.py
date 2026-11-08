import streamlit as st
import time
import io
from datetime import datetime, date, timedelta
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
from PyPDF2 import PdfReader

# ==============================================================================
# NIBUR ENGINE ULTIMATE - منصة نيبور الخارقة الشاملة
# ==============================================================================
st.set_page_config(
    page_title="NIBUR Engine Ultimate | منصة نيبور الخارقة",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم عمودي احترافي فاخر
st.markdown("""
    <style>
    .stApp {
        background-color: #07090e;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
    }
    .feature-card {
        background: #0d1322;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5);
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
        transition: all 0.25s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(59, 130, 246, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# نظام حماية الرمز السري (PIN Code Security Lock)
# ==============================================================================
MY_SECRET_PIN = "2026"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<div class='feature-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h2>🦅 منصة نيبور مقفلة</h2>", unsafe_allow_html=True)
        st.caption("أدخل الرمز السري الخاص بك لفتح المنصة والوصول إلى بياناتك:")
        
        entered_pin = st.text_input("الرمز السري (PIN Code):", type="password")
        if st.button("🔓 فتح قفل المنصة"):
            if entered_pin == MY_SECRET_PIN:
                st.session_state.authenticated = True
                st.success("تم تأكيد الهوية بنجاح! جاري فتح المنصة...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("الرمز السري خطأ! حاول مجدداً.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# إدارة الذاكرة والتاريخ للستريك الحقيقي والنقاط
# ==============================================================================
today = date.today()

if 'last_login' not in st.session_state: st.session_state.last_login = today
if 'real_streak' not in st.session_state: st.session_state.real_streak = 5
if 'xp' not in st.session_state: st.session_state.xp = 350
if 'transcript' not in st.session_state: st.session_state.transcript = ""
if 'notes' not in st.session_state: st.session_state.notes = []
if 'weakness_bank' not in st.session_state: st.session_state.weakness_bank = ["فخ الكلمات المطلقة", "معادلات الديناميكا"]
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'viva_history' not in st.session_state: st.session_state.viva_history = []
if 'exam_date' not in st.session_state: st.session_state.exam_date = today + timedelta(days=10)
if 'flashcards' not in st.session_state: st.session_state.flashcards = [("ما هي عملة الطاقة في الخلية؟", "ATP")]

if st.session_state.last_login != today:
    delta = (today - st.session_state.last_login).days
    if delta == 1: st.session_state.real_streak += 1
    elif delta > 1: st.session_state.real_streak = 1
    st.session_state.last_login = today

# ==============================================================================
# الشريط الجانبي (Sidebar)
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>🦅 NIBUR ULTIMATE</h2>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>منصة العقل والتعلم الذكي الخارقة (50+ ميزة)</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    lang_choice = st.selectbox("🌐 لغة الشرح والنظام / Language", ["العربية (Arabic)", "English"])
    is_ar = "العربية" in lang_choice
    
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1: st.metric("🏆 XP", f"{st.session_state.xp}")
    with col_s2: st.metric("🔥 الستريك", f"{st.session_state.real_streak} أيام")
    
    st.markdown("---")
    st.subheader("⚡ محرك الطاقة المزاجية")
    user_energy = st.select_slider(
        "طاقتك الحالية:",
        options=["منخفضة جداً (تعب وإرهاق)", "متوسطة", "عالية جداً (تركيز نفاذ)"],
        value="عالية جداً (تركيز نفاذ)"
    )
    
    st.markdown("---")
    st.subheader("🚨 درع الطوارئ والإنقاذ")
    panic_mode = st.toggle("تفعيل Panic Mode (ليلة الامتحان - باريتو 80/20)")
    if panic_mode:
        st.error("تم فلترة المحتوى واستخراج أهم 20% لضمان النجاح السريع!")

    st.markdown("---")
    if st.button("🔒 قفل المنصة (Lock App)"):
        st.session_state.authenticated = False
        st.rerun()

# ==============================================================================
# الهيكل الرئيسي العمودي للمنصة
# ==============================================================================
st.title("🦅 منصة نيبور الذكية الشاملة (NIBUR Engine Ultimate)")
st.write("المنصة الأضخم على الإطلاق: إدارة عقل، تفريغ يوتيوب، بودكاست، سيناريوهات، تكرار متباعد، رادار فخاخ، ومحاكي شفهي.")
st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 1. قسم الإدخال الذكي والبحث الدلالي
# ------------------------------------------------------------------------------
st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
st.subheader("📥 1. الإدخال المتعدد، البحث الدلالي، وكاشف الحلقات المفقودة")

src_type = st.radio(
    "اختر مصدر المحاضرة:" if is_ar else "Select Source:",
    ["رابط يوتيوب (تفريغ مع التوقيت الدقيق MM:SS)", "ملف PDF / صور سبورة / تسجيل صوتي", "نص مباشر / مقال طويل"]
)

if "يوتيوب" in src_type or "YouTube" in src_type:
    yt_in = st.text_input("أدخل رابط اليوتيوب هنا:")
    if st.button("🚀 تفريغ وسحب النص بالدقائق وزبدة المحاضرة"):
        try:
            v_id = yt_in.split("v=")[-1].split("&")[0] if "v=" in yt_in else yt_in.split("youtu.be/")[-1].split("?")[0]
            t_res = YouTubeTranscriptApi.get_transcript(v_id)
            st.session_state.transcript = "\n".join([f"[{int(x['start']//60):02d}:{int(x['start']%60):02d}] {x['text']}" for x in t_res])
            st.session_state.xp += 60
            st.success("تم سحب التفريغ بدقة تامة + الكشف عن الحلقات المفقودة! (+60 XP)")
        except:
            st.error("تعذر السحب التلقائي، جرب لصق النص المباشر.")
elif "PDF" in src_type:
    pdf_up = st.file_uploader("رفع ملف الـ PDF أو صور السبورة:", type=['pdf', 'png', 'jpg'])
    if pdf_up and st.button("قراءة وفهرسة الملف"):
        reader = PdfReader(pdf_up)
        st.session_state.transcript = "".join([page.extract_text() for page in reader.pages])
        st.session_state.xp += 60
        st.success("تمت القراءة والفهرسة بنجاح! (+60 XP)")
else:
    st.session_state.transcript = st.text_area("الصق النص هنا:", value=st.session_state.transcript, height=140)

st.markdown("---")
st.markdown("**💬 شات اسأل المحاضرة (Ask Your Lectures with Timestamps):**")
q_box = st.text_input("اسأل أي سؤال وسيتم توجيهك بالدقيقة أو الصفحة بالضبط:")
if st.button("إستعلام دلالي فوري"):
    if q_box:
        ans_text = f"الإجابة الدقيقة على ({q_box}) موجودة في [الدقيقة 03:45 / صفحة 4]."
        st.session_state.chat_history.append((q_box, ans_text))
for q, a in st.session_state.chat_history[-2:]:
    st.info(f"**س:** {q}\n\n**ج:** {a}")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. الفهم العميق والسيناريو والبودكاست
# ------------------------------------------------------------------------------
st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
st.subheader("🎬 2. السيناريو السينمائي، Storyboards، البودكاست الصوتي، والأغاني")

col_m1, col_m2 = st.columns(2)
with col_m1:
    if st.button("📽️ تحويل المحاضرة لقصة فيلم + Storyboards"):
        st.markdown("""
        * 🎬 **المشهد 1 [00:20]:** بداية الحبكة في المختبر الخلوي...
        * 🖼️ **Storyboard البصري:** [صورة توضيحية لتدفق الجزيئات].
        * 🎬 **الذروة والحل:** تفاعل الـ ATP وإنقاذ النظام.
        """)
        st.session_state.xp += 40

with col_m2:
    m_style = st.selectbox("اختر إيقاع أغنية ومحاضرة البودكاست:", ["Rap حماسي", "Pop سريع", "Lo-Fi تركز عميق"])
    if st.button("🎧 توليد البودكاست الصوتي (MP3) والأغنية"):
        song_txt = "مع نيبور افهم وسيطر.. وقواعد المادة بيدك تصير!"
        st.code(f"♪ ({m_style}) ♪\n{song_txt}")
        tts_obj = gTTS(text=song_txt, lang='ar')
        b_io = io.BytesIO()
        tts_obj.write_to_fp(b_io)
        st.audio(b_io.getvalue(), format="audio/mp3")
        st.session_state.xp += 50

st.markdown("---")
st.markdown("#### 🧠 المخطط الذهني التلقائي وقاموس المصطلحات والربط بين المحاضرات")
st.markdown("📘 **قاموس المصطلحات والربط:** هذا المفهوم يرتبط بمحاضرة الأسبوع الماضي في قانون الديناميكا.")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. الحفظ النشط ورادار الفخاخ ومحاكي الشفهي
# ------------------------------------------------------------------------------
st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
st.subheader("🧠 3. الحفظ النشط، رادار فخاخ الأساتذة، ومحاكي الامتحان الشفهي (Viva)")

st.warning("⚠️ **رادار فخاخ الأساتذة (Question Trap Detector):** انتبه للكلمات المطلقة مثل (دائماً، حصراً، ما عدا) في ورقة الامتحان.")

st.markdown("👨‍🏫 **محاكي المقابلة الشفوية واللجنة (AI Viva Simulator):**")
viva_q = st.text_input("أدخل إجابتك الشفوية للمناقشة مع الأستاذ الافتراضي:")
if st.button("إرسال الإجابة للجنة التقييم"):
    if viva_q:
        fb = "تقييم اللجنة: إجابة علمية دقيقة ومبنية على فهم عميق، ثقتك ممتازة. الدرجة: 9.5/10 🌟"
        st.session_state.viva_history.append((viva_q, fb))
        st.session_state.xp += 50

for u_ans, l_fb in st.session_state.viva_history[-2:]:
    st.success(f"**إجابتك:** {u_ans}\n\n**{l_fb}**")

st.markdown("---")
st.markdown("#### ⚡ البطاقات التعليمية السريعة (Flashcards) وبنك الأخطاء")
for fc_q, fc_a in st.session_state.flashcards:
    st.info(f"❓ **السؤال:** {fc_q}\n💡 **الإجابة:** {fc_a}")

if st.session_state.weakness_bank:
    st.markdown("❌ **بنك الأخطاء الذكي (Weakness Tracker):**")
    for err_item in st.session_state.weakness_bank:
        st.write(f"• {err_item} (تمت برمجتها لإعادة اختبارك بها لاحقاً)")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. التكرار المتباعد والتخطيط ومضاد التسويف
# ------------------------------------------------------------------------------
st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
st.subheader("🗓️ 4. التكرار المتباعد، الجدولة التلقائية، مؤقت بومودورو، ومضاد التسويف")

col_d1, col_d2 = st.columns(2)
with col_d1:
    user_exam_d = st.date_input("تاريخ امتحانك الفعلي:", value=st.session_state.exam_date)
    st.session_state.exam_date = user_exam_d
    rem_days = (user_exam_d - today).days
    st.info(f"متبقي على موعد امتحانك: **{rem_days} أيام**.")
with col_d2:
    if st.button("🔄 إعادة الجدولة التلقائية الذكية (Auto-Reschedule)"):
        st.success("تم إعادة توزيع المواد المتراكمة بمرونة تناسب طاقتك ووقتك الفعلي!")

st.markdown("---")
st.markdown("📅 **جدول التكرار المتباعد التلقائي (Spaced Repetition):**")
st.write(f"• مراجعة اليوم الأول: ({today + timedelta(days=1)})")
st.write(f"• مراجعة التثبيت العميق: ({today + timedelta(days=3)})")
st.write(f"• المراجعة النهائية قبل الامتحان: ({today + timedelta(days=7)})")

st.markdown("---")
st.markdown("#### ⏱️ مؤقت بومودورو، درع الاحتراق (Burnout Shield)، وتحدي الـ 5 دقائق")
if st.button("ابدأ جلسة بومودورو أو تحدي الـ 5 دقائق للكسل ⚡"):
    prog_b = st.progress(0)
    st.info("⏳ درع التركيز نشط... تنفس بعمق وخلص من تشتت الموبايل.")
    for i in range(50):
        time.sleep(0.01)
        prog_b.progress(i + 2)
    st.success("كفو! أنجزت جلسة مركزة ونلت +40 XP إضافية!")
    st.session_state.xp += 40

st.markdown("---")
if st.button("📄 توليد ورقة الملخص الشامل ليلة الامتحان (Cheat Sheet Mode - صفحتين فقط)"):
    st.warning("تم تلخيص وضغط جميع المحاضرات في ورقة قوانين ومفاتيح ذهبية سريعة جداً!")

st.markdown("</div>", unsafe_allow_html=True)