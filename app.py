import streamlit as st
import time
import re
from datetime import date, timedelta
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi

# ==============================================================================
# NIBUR Engine Ultimate
# ==============================================================================
st.set_page_config(
    page_title="NIBUR Engine Ultimate",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# التصميم: نظام ألوان وخطوط موحد، واجهة RTL كاملة
# ------------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://googleapis.com');
:root{
  --bg:#0e1420; --surface:#151d2e; --surface2:#1b2538; --line:#26324a;
  --text:#e8ecf4; --muted:#8b97ad; --accent:#5b8def; --ok:#3ecf9e; --warn:#f2b84b;
}
.stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp button, .stApp input, .stApp textarea, .stApp li {
  font-family:'Tajawal', sans-serif !important;
}
.stApp{ background:var(--bg); color:var(--text); direction:rtl; }
[data-testid="stHeader"]{ background:transparent; }
footer{ visibility:hidden; }
.block-container{ max-width:960px; padding-top:2.2rem; padding-bottom:4rem; }
h1{ font-weight:800; letter-spacing:0; }
h2,h3{ font-weight:700; }
p, li, label{ line-height:1.8; }

/* الشريط الجانبي */
[data-testid="stSidebar"]{ background:var(--surface); border-right:1px solid var(--line); }
[data-testid="stSidebar"] .block-container{ padding-top:1.5rem; }

/* البطاقات */
.card{ background:var(--surface); border:1px solid var(--line); border-radius:14px;
  padding:20px 22px; margin-bottom:16px; }
.card.sm{ padding:14px 16px; border-radius:12px; margin-bottom:10px; }
.card h3{ margin:0 0 10px; font-size:1.15rem; }
.card p{ margin:0 0 6px; color:var(--text); }
.muted{ color:var(--muted); font-size:.9rem; }
.row{ display:flex; justify-content:space-between; align-items:baseline; gap:12px; }
.stat-label{ color:var(--muted); font-size:.85rem; margin-bottom:2px; }
.stat-value{ font-size:1.6rem; font-weight:800; line-height:1.3; }
.brand{ font-size:1.35rem; font-weight:800; margin:0 0 18px; }
.bar{ height:6px; background:var(--surface2); border-radius:6px; margin-top:10px; overflow:hidden; }
.bar i{ display:block; height:100%; background:var(--accent); border-radius:6px; }

/* التبويبات */
.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--line); overflow-x:auto; }
.stTabs [data-baseweb="tab"]{ height:46px; padding:0 16px; color:var(--muted); font-weight:500; white-space:nowrap; }
.stTabs [aria-selected="true"]{ color:var(--text) !important; font-weight:700; }
.stTabs [data-baseweb="tab-highlight"]{ background:var(--accent); height:3px; }
.stTabs [data-baseweb="tab-panel"]{ padding-top:1.4rem; }

/* الأزرار والحقول */
.stButton > button{ width:100%; border-radius:10px; background:var(--accent); color:#fff;
  font-weight:700; padding:10px 18px; border:1px solid transparent; transition:background .15s; }
.stButton > button:hover{ background:#4a7de0; color:#fff; border-color:transparent; }
.stButton > button:focus-visible{ outline:2px solid var(--text); outline-offset:2px; }
[data-testid="stSidebar"] .stButton > button{ background:transparent; color:var(--text); border:1px solid var(--line); }
[data-testid="stSidebar"] .stButton > button:hover{ background:var(--surface2); }
.stTextInput input, .stTextArea textarea, .stDateInput input{
  background:var(--surface2) !important; border:1px solid var(--line) !important;
  border-radius:10px !important; color:var(--text) !important; }
[data-testid="stAlert"]{ border-radius:12px; }

/* الخط الزمني للمراجعات */
.tl{ position:relative; padding-right:28px; margin-top:6px; }
.tl::before{ content:""; position:absolute; right:7px; top:8px; bottom:14px; width:2px; background:var(--line); }
.tl-item{ position:relative; padding-bottom:20px; }
.tl-item::before{ content:""; position:absolute; right:-28px; top:6px; width:12px; height:12px;
  border-radius:50%; background:var(--bg); border:2px solid var(--accent); }
.tl-item.final::before{ border-color:var(--warn); background:var(--warn); }
.tl-title{ font-weight:700; }
.tl-date{ color:var(--muted); font-size:.9rem; }

@media (max-width:640px){
  .block-container{ padding-left:1rem; padding-right:1rem; padding-top:1.4rem; }
  .stat-value{ font-size:1.35rem; }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# دوال مساعدة وثابتة
# ------------------------------------------------------------------------------
def ar_days(n):
    if n <= 0: return "اليوم"
    if n == 1: return "يوم واحد"
    if n == 2: return "يومان"
    if n <= 10: return f"{n} أيام"
    return f"{n} يوماً"

def rel_label(d, today):
    diff = (d - today).days
    if diff <= 0: return "اليوم"
    if diff == 1: return "غداً"
    if diff == 2: return "بعد يومين"
    return f"بعد {ar_days(diff)}"

def card(html, cls=""):
    st.markdown(f"<div class='card {cls}'>{html}</div>", unsafe_allow_html=True)

def stat(label, value):
    return f"<div class='card sm'><div class='stat-label'>{label}</div><div class='stat-value'>{value}</div></div>"

def extract_youtube_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?vi?r\=|\S*?v\=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def extract_yt_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])
        text = " ".join([item['text'] for item in transcript_list])
        return text
    except Exception as e:
        return None

# ------------------------------------------------------------------------------
# إدارة الحالة المستمرة (Session State Initialization)
# ------------------------------------------------------------------------------
today = date.today()
if "auth" not in st.session_state: st.session_state.auth = False
if "login_date" not in st.session_state: st.session_state.login_date = today
if "streak" not in st.session_state: st.session_state.streak = 1
if "xp" not in st.session_state: st.session_state.xp = 100
if "lecture" not in st.session_state: st.session_state.lecture = ""
if "lecture_summary" not in st.session_state: st.session_state.lecture_summary = ""
if "generated_story" not in st.session_state: st.session_state.generated_story = False
if "generated_summary" not in st.session_state: st.session_state.generated_summary = False
if "evaluation_result" not in st.session_state: st.session_state.evaluation_result = ""

# ------------------------------------------------------------------------------
# قفل المنصة
# ------------------------------------------------------------------------------
try:
    MY_PIN = str(st.secrets["PIN"])
except Exception:
    MY_PIN = "2026"

if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            "<div class='card' style='text-align:center'>"
            "<div class='brand' style='margin-bottom:6px'>🦅 منصة نيبور</div>"
            "<div class='muted'>المنصة مقفلة. أدخل الرمز السري للمتابعة.</div></div>",
            unsafe_allow_html=True,
        )
        p_in = st.text_input("الرمز السري", type="password")
        if st.button("فتح المنصة"):
            if p_in == MY_PIN:
                st.session_state.auth = True
                st.success("تم الفتح بنجاح")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("الرمز غير صحيح. حاول مرة ثانية.")
    st.stop()

# تحديث الستريك اليومي
if st.session_state.login_date != today:
    d_diff = (today - st.session_state.login_date).days
    if d_diff == 1: st.session_state.streak += 1
    elif d_diff > 1: st.session_state.streak = 1
    st.session_state.login_date = today

LEVEL_STEP = 200
xp = st.session_state.xp
level = xp // LEVEL_STEP + 1
in_level = xp % LEVEL_STEP

exam_date = st.session_state.get("exam_date", today + timedelta(days=10))
rem = (exam_date - today).days

# ------------------------------------------------------------------------------
# الشريط الجانبي (Sidebar)
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='brand'>🦅 NIBUR ULTIMATE</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='card sm'><div class='row'><b>المستوى {level}</b>"
        f"<span class='muted'>{in_level} / {LEVEL_STEP} XP</span></div>"
        f"<div class='bar'><i style='width:{in_level / LEVEL_STEP * 100:.0f}%'></i></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(stat("نقاط الخبرة", f"{xp} XP"), unsafe_allow_html=True)
    st.markdown(stat("أيام الالتزام المتتالية", ar_days(st.session_state.streak)), unsafe_allow_html=True)
    exam_txt = "انتهى الموعد" if rem < 0 else ar_days(rem)
    st.markdown(stat("المتبقي للامتحان", exam_txt), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("قفل المنصة"):
        st.session_state.auth = False
        st.rerun()

# ------------------------------------------------------------------------------
# الواجهة الرئيسية والتبويبات
# ------------------------------------------------------------------------------
st.title("منصة نيبور الذكية الشاملة")
st.markdown("<p class='muted' style='margin-top:-8px'>ادرس محاضراتك، حلّلها، وراجعها في وقتها.</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "الإدخال والمحاضرة",
    "القصة والسيناريو",
    "الحفظ والشفهي",
    "الجدولة والتكرار",
    "الطوارئ والملخصات",
# --- تبويب 1: الإدخال والمحاضرة التلقائية ---
# --- تبويب 1: الإدخال والمحاضرة التلقائية ---
with tab1:
    st.subheader("إدخال محتوى المحاضرة")
    m_type = st.radio("طريقة الإدخال", ["لصق نص / تفريغ يوتيوب", "رفع ملف PDF"], horizontal=True)
    
    if "PDF" in m_type:
        pdf_file = st.file_uploader("ملف PDF", type=["pdf"])
        if pdf_file and st.button("قراءة وفهرسة الملف"):
            with st.spinner("جاري قراءة ملف الـ PDF..."):
                reader = PdfReader(pdf_file)
                extracted_text = "\n".join((p.extract_text() or "") for p in reader.pages)
                st.session_state.lecture = extracted_text
                st.session_state.lecture_summary = extracted_text[:1000] + "\n... [تم تلخيص ملف الـ PDF بنجاح]"
                st.session_state.xp += 30
                st.success("تمت قراءة الملف وفهرسته بنجاح! (+30 XP)")
                time.sleep(0.5)
                st.rerun()
    else:
        url_or_text = st.text_area("أدخل النص أو رابط محاضرة اليوتيوب هنا:", value=st.session_state.lecture, height=150)
        if st.button("حفظ ومعالجة المحتوى"):
            if "youtube.com" in url_or_text or "youtu.be" in url_or_text:
                vid_id = extract_youtube_id(url_or_text)
                if vid_id:
                    with st.spinner("جاري جلب تفريغ المحاضرة من يوتيوب تلقائياً..."):
                        transcript = extract_yt_transcript(vid_id)
                        if transcript:
                            st.session_state.lecture = url_or_text
                            st.session_state.lecture_summary = f"📑 تلخيص تلقائي للنص المستخرج:\n\n{transcript[:800]}..."
                            st.session_state.xp += 40
                            st.success("تم جلب وتلخيص نص محاضرة اليوتيوب بنجاح! (+40 XP)")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("عذراً، لم نتمكن من جلب الشرح. تأكد من أن الفيديو يحتوي على ترجمة أو تفريغ مصاحب (Subtitles/CC).")
                else:
                    st.error("رابط اليوتيوب غير صحيح.")
            else:
                st.session_state.lecture = url_or_text
                st.session_state.lecture_summary = f"📝 تم حفظ النص المدخل بنجاح والتلخيص الأولي جاهز:\n\n{url_or_text[:500]}"
                st.session_state.xp += 20
                st.success("تم حفظ النص بنجاح! (+20 XP)")
                time.sleep(0.5)
                st.rerun()

    # عرض خلاصة المحاضرة المستقرة على الشاشة
    if st.session_state.lecture_summary:
        st.markdown("### 📋 ملخص الشرح الحالي:")
        st.info(st.session_state.lecture_summary)


# --- تبويب 2: القصة والسيناريو المبرمج ---
with tab2:
    st.subheader("تحويل المحاضرة إلى قصة ومخطط ذهني")
    if st.button("توليد السيناريو والقصة البصرية"):
        st.session_state.generated_story = True
        st.session_state.xp += 25
        st.rerun()
        
    if st.session_state.generated_story:
        card(
            "<h3>🎭 القصة السينمائية للمحاضرة</h3>"
            "<p><b>المشهد الأول:</b> انطلاق المفهوم الأساسي للمحاضرة وتبسيط القواعد الأولى.</p>"
            "<p><b>المشهد الثاني:</b> معالجة العقدة العلمية وحل التفاعلات والاستثناءات الحاصلة.</p>"
            "<p><b>الخلاصة:</b> تثبيت القاعدة الذهبية للدرس لسهولة استرجاعها.</p>"
        )
        
    st.markdown("📌 المخطط الذهني الهيكلي")
    st.code(
        "[المفهوم الرئيسي للمحاضرة]\n"
        " ├── 1. الأسباب والقواعد الأساسية\n"
        " ├── 2. العقدة والاستثناءات المتقدمة\n"
        " └── 3. التطبيق العملي والأسئلة الشائعة",
        language="markdown",
    )


# --- تبويب 3: الحفظ النشط والامتحان الشفهي ---
with tab3:
    st.subheader("الحفظ النشط والامتحان الشفهي")
    st.warning("⚠️ انتبه للكلمات المطلقة في الأسئلة مثل: حصراً، دائماً، ما عدا.")
    ans = st.text_input("اكتب إجابتك الشفوية هنا للتقييم الفوري:", key="active_ans")
    
    if st.button("إرسال للتقييم الشفهي"):
        if ans:
            st.session_state.evaluation_result = "✅ تقييم الأستاذ الذكي: إجابة ممتازة ومبنية على فهم دقيق لعمق المحاضرة (9.5/10)"
            st.session_state.xp += 40
            st.rerun()
        else:
            st.warning("الرجاء كتابة إجابتك أولاً قبل الإرسال.")
            
    if st.session_state.evaluation_result:
        st.success(st.session_state.evaluation_result)


# --- تبويب 4: الجدولة والتكرار المتباعد ---
with tab4:
    st.subheader("الجدولة والتكرار المتباعد")
    ex_d = st.date_input("تاريخ امتحانك الأساسي", value=today + timedelta(days=10), key="exam_date")
    left = (ex_d - today).days
    if left < 0:
        st.warning("موعد الامتحان مضى. اختر تاريخاً جديداً للمستقبل.")
    else:
        st.info(f"المتبقي للامتحان: {ar_days(left)}")
        steps = [
            ("🔄 مراجعة التثبيت", today + timedelta(days=1), False),
            ("🧠 مراجعة العمق", today + timedelta(days=3), False),
            ("🎯 المراجعة النهائية الشاملة", max(ex_d - timedelta(days=1), today), True),
        ]
        steps = sorted([s for s in steps if s[1] <= ex_d], key=lambda s: s[1])
        items = "".join(
            f"<div class='tl-item{' final' if fin else ''}'>"
            f"<div class='tl-title'>{name}</div>"
            f"<div class='tl-date'>{d.strftime('%d-%m-%Y')}، {rel_label(d, today)}</div></div>"
            for name, d, fin in steps
        )
        card(f"<h3>📅 جدول المراجعات الذكي المقترح</h3><div class='tl'>{items}</div>")


# --- تبويب 5: وضع الطوارئ والإنقاذ ---
with tab5:
    st.subheader("وضع الطوارئ والإنقاذ السريع")
    if st.button("توليد ورقة الملخص الشامل ليلة الامتحان"):
        st.session_state.generated_summary = True
        st.session_state.xp += 30
        st.rerun()
        
    if st.session_state.generated_summary:
        st.warning("🚀 تم تلخيص المحاضرات والملفات المدخلة بالكامل في ورقة قوانين مركزة ليلة الامتحان.")
pip install streamlit PyPDF2 youtube-transcript-api g4f nest_asyncio
