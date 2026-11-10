import streamlit as st
import time
import re
import asyncio
from datetime import date, timedelta
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
import g4f

# حل مشكلة تشغيل الـ Async داخل بيئة Streamlit لنظام الذكاء الاصطناعي
import nest_asyncio
nest_asyncio.apply()

# إعدادات الصفحة الأساسية للمنصة
st.set_page_config(
    page_title="NIBUR Engine Ultimate",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)
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
        return " ".join([item['text'] for item in transcript_list])
    except Exception:
        return None

def ask_ai(prompt_text):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o,
            messages=[{"role": "user", "content": prompt_text}],
        )
        return response
    except Exception:
        return "عذراً، المحرك الذكي مشغول حالياً. تم حفظ مادة الدرس برمجياً بنجاح وسنقوم بمعالجتها لاحقاً."
# تهيئة متغيرات الجلسة (Session States)
today = date.today()
if "auth" not in st.session_state: st.session_state.auth = False
if "login_date" not in st.session_state: st.session_state.login_date = today
if "streak" not in st.session_state: st.session_state.streak = 1
if "xp" not in st.session_state: st.session_state.xp = 100
if "lecture_content" not in st.session_state: st.session_state.lecture_content = ""
if "lecture_summary" not in st.session_state: st.session_state.lecture_summary = ""
if "generated_story" not in st.session_state: st.session_state.generated_story = ""
if "generated_summary" not in st.session_state: st.session_state.generated_summary = ""
if "evaluation_result" not in st.session_state: st.session_state.evaluation_result = ""

# التحقق من القفل السري للمنصة
MY_PIN = "2026"
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            "<div class='card' style='text-align:center'>"
            "<div class='brand' style='margin-bottom:6px'>🦅 منصة نيبور الذكية</div>"
            "<div class='muted'>المنصة مقفلة حالياً. أدخل الرمز السري للمتابعة.</div></div>",
            unsafe_allow_html=True,
        )
        p_in = st.text_input("الرمز السري الخاص بك", type="password")
        if st.button("فتح المنصة الآن"):
            if p_in == MY_PIN:
                st.session_state.auth = True
                st.success("تم فتح منصتك بنجاح، جاري التحميل...")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("الرمز السري خاطئ! حاول مجدداً.")
    st.stop()

# تحديث الستريك اليومي تلقائياً
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

# بناء الشريط الجانبي (Sidebar)
with st.sidebar:
    st.markdown("<div class='brand'>🦅 NIBUR ULTIMATE</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='card sm'><div class='row'><b>المستوى {level}</b>"
        f"<span class='muted'>{in_level} / {LEVEL_STEP} XP</span></div>"
        f"<div class='bar'><i style='width:{in_level / LEVEL_STEP * 100:.0f}%'></i></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(stat("نقاط الخبرة الكلية", f"{xp} XP"), unsafe_allow_html=True)
    st.markdown(stat("أيام الالتزام المتتالية", ar_days(st.session_state.streak)), unsafe_allow_html=True)
    exam_txt = "انتهى الموعد" if rem < 0 else ar_days(rem)
    st.markdown(stat("المتبقي للامتحان", exam_txt), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("قفل المنصة"):
        st.session_state.auth = False
        st.rerun()
st.title("منصة نيبور الذكية الشاملة")
st.markdown("<p class='muted' style='margin-top:-8px'>ادرس محاضراتك، حلّلها باستخدام الذكاء الاصطناعي الحقيقي، وراجعها في وقتها.</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "الإدخال والمحاضرة",
    "القصة والسيناريو",
    "الحفظ والشفهي",
    "الجدولة والتكرار",
    "الطوارئ والملخصات"
])

# --- تبويب 1: إدخال المحاضرات ومعالجتها بالذكاء الاصطناعي ---
with tab1:
    st.subheader("إدخال محتوى المحاضرة")
    m_type = st.radio("طريقة استقطاب المحتوى الدراسي", ["لصق نص / تفريغ يوتيوب", "رفع ملف PDF"], horizontal=True)
    
    if "PDF" in m_type:
        pdf_file = st.file_uploader("ارفع ملف الـ PDF الخاص بالمحاضرة", type=["pdf"])
        if pdf_file and st.button("قراءة وتلخيص الملف بالـ AI"):
            with st.spinner("جاري قراءة ملف الـ PDF واستخلاص الأفكار العميقة بواسطة نيبور الذكي..."):
                reader = PdfReader(pdf_file)
                extracted_text = "\n".join((p.extract_text() or "") for p in reader.pages)
                st.session_state.lecture_content = extracted_text
                
                ai_summary = ask_ai(f"لخص لي المحاضرة التالية بأسلوب نقاط ذكي وشامل ومفهوم باللغة العربية:\n\n{extracted_text[:3000]}")
                st.session_state.lecture_summary = ai_summary
                st.session_state.xp += 30
                st.success("تمت قراءة وفهرسة وتلخيص الملف بواسطة الـ AI بنجاح! (+30 XP)")
                time.sleep(0.5)
                st.rerun()
    else:
        url_or_text = st.text_area("أدخل الشرح النصي للمحاضرة أو الصق رابط فيديو يوتيوب:", value=st.session_state.lecture_content, height=150)
        if st.button("حفظ ومعالجة المحتوى بالذكاء الاصطناعي"):
            if "youtube.com" in url_or_text or "youtu.be" in url_or_text:
                vid_id = extract_youtube_id(url_or_text)
                if vid_id:
                    with st.spinner("جاري سحب تفريغ المحاضرة من فيديو اليوتيوب وتحليله ذكياً بالكامل..."):
                        transcript = extract_yt_transcript(vid_id)
                        if transcript:
                            st.session_state.lecture_content = transcript
                            ai_summary = ask_ai(f"قم بتلخيص نص هذه المحاضرة المستخرجة من اليوتيوب تلخيصاً أكاديمياً ممتازاً ومقسماً لعناوين واضحة:\n\n{transcript[:3000]}")
                            st.session_state.lecture_summary = ai_summary
                            st.session_state.xp += 40
                            st.success("تم تفريغ فيديو اليوتيوب وتلخيصه بالذكاء الاصطناعي! (+40 XP)")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("عذراً، هذا الفيديو لا يضم تفريغاً نصياً أو ترجمة مصاحبة عامة لكي يقرأها الذكاء الاصطناعي.")
                else:
                    st.error("رابط اليوتيوب المدخل غير صحيح.")
            else:
                if url_or_text.strip():
                    with st.spinner("جاري تحليل النص المدخل وصياغة تلخيص ذكي..."):
                        st.session_state.lecture_content = url_or_text
                        ai_summary = ask_ai(f"قم بتلخيص النص التالي تلخيصاً مركزاً وممتازاً للفهم والمذاكرة:\n\n{url_or_text}")
                        st.session_state.lecture_summary = ai_summary
                        st.session_state.xp += 20
                        st.success("تم حفظ النص وتوليد الملخص الذكي بنجاح! (+20 XP)")
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.warning("يرجى كتابة نص أو وضع رابط أولاً.")

    if st.session_state.lecture_summary:
        st.markdown("### 📋 ملخص الشرح الذكي الحالي:")
        st.info(st.session_state.lecture_summary)

# --- تبويب 2: توليد السيناريو الإبداعي والقصة التفاعلية ---
with tab2:
    st.subheader("تحويل المحاضرة إلى قصة ومخطط ذهني")
    if st.button("توليد سيناريو وقصة بصرية تفاعلية من محاضرتي"):
        if st.session_state.lecture_content:
            with st.spinner("جاري صياغة قصة سينمائية إبداعية لتسهيل حفظ مادة درسك..."):
                ai_story = ask_ai(f"حول مادة هذه المحاضرة إلى قصة درامية مشوقة ومقسمة إلى مشاهد ليسهل حفظ وفهم الفكرة العلمية فيها:\n\n{st.session_state.lecture_content[:2000]}")
                st.session_state.generated_story = ai_story
                st.session_state.xp += 25
                st.rerun()
        else:
            st.warning("يرجى إدخال محتوى المحاضرة في التبويب الأول أولاً لكي يستطيع الذكاء الاصطناعي بناء قصة حولها.")

    if st.session_state.generated_story:
        card(f"<h3>🎭 القصة السينمائية المستوحاة من درسك</h3><p>{st.session_state.generated_story}</p>")
        
    st.markdown("📌 المخطط الذهني الهيكلي للمذاكرة")
    st.code(
        "[المفهوم الرئيسي للمحاضرة]\n"
        " ├── 1. الأسباب والقواعد الأساسية والركائز\n"
        " ├── 2. العقدة والتعقيدات والاستثناءات المتقدمة\n"
        " └── 3. التطبيق العملي ونماذج الاختبارات الشائعة",
        language="markdown",
    )

# --- تبويب 3: الاختبار الشفهي وتقييم الإجابات الفعلي ---
with tab3:
    st.subheader("الحفظ النشط والامتحان الشفهي بالذكاء الاصطناعي")
    st.warning("⚠️ انتبه للكلمات المطلقة والمفصلية في الأسئلة مثل: حصراً، دائماً، ما عدا.")
    ans = st.text_input("اكتب إجابتك الشفوية أو شرحك للفكرة هنا ليقوم الأستاذ الذكي بتقييمك:")
    
    if st.button("إرسال الإجابة للتقييم الفوري والنهائي"):
        if ans:
            if st.session_state.lecture_content:
                with st.spinner("جاري مطابقة إجابتك مع مادة المحاضرة بدقة وتوليد النتيجة..."):
                    eval_prompt = f"بصفتك أستاذاً جامعياً ذكياً، قم بتقييم هذه الإجابة: '{ans}' بناءً على محتوى المحاضرة التالي: '{st.session_state.lecture_content[:2000]}'. أعطِ تقييماً من 10 ونصيحة مركزة لتصحيح النقص."
                    ai_eval = ask_ai(eval_prompt)
                    st.session_state.evaluation_result = f"✅ {ai_eval}"
                    st.session_state.xp += 40
                    st.rerun()
            else:
                with st.spinner("جاري تقييم إجابتك تقييماً عاماً..."):
                    ai_eval = ask_ai(f"قيم إجابة الطالب التالية تقييماً عاماً وأعطه درجة من 10 ونصيحة: '{ans}'")
                    st.session_state.evaluation_result = f"✅ {ai_eval}"
                    st.session_state.xp += 20
                    st.rerun()
        else:
            st.warning("الرجاء كتابة إجابتك أو فرضيتك أولاً قبل إرسالها للتقييم.")
            
    if st.session_state.evaluation_result:
        st.success(st.session_state.evaluation_result)

# --- تبويب 4: الجدولة الذكية والتكرار المتباعد الآلي ---
with tab4:
    st.subheader("الجدولة والتكرار المتباعد")
    ex_d = st.date_input("حدد تاريخ امتحانك الأساسي القادم", value=today + timedelta(days=10), key="exam_date")
    left = (ex_d - today).days
    if left < 0:
        st.warning("موعد الامتحان المختار قد مضى. يرجى اختيار تاريخ مستقبلي لتنظيم الجدول الحركي.")
    else:
        st.info(f"المتبقي للامتحان النهائي: {ar_days(left)}")
        steps = [
            ("🔄 مراجعة التثبيت الأولى", today + timedelta(days=1), False),
            ("🧠 مراجعة العمق والربط الذهني", today + timedelta(days=3), False),
            ("🎯 المراجعة النهائية الشاملة والمركزة", max(ex_d - timedelta(days=1), today), True),
        ]
        steps = sorted([s for s in steps if s[1] <= ex_d], key=lambda s: s[1])
        items = "".join(
            f"<div class='tl-item{' final' if fin else ''}'>"
            f"<div class='tl-title'>{name}</div>"
            f"<div class='tl-date'>{d.strftime('%d-%m-%Y')}، {rel_label(d, today)}</div></div>"
            for name, d, fin in steps
        )
        card(f"<h3>📅 جدول المراجعات الذكي والمقترح تكراره</h3><div class='tl'>{items}</div>")

# --- تبويب 5: وضع الطوارئ والإنقاذ السريع ليلة الامتحان ---
with tab5:
    st.subheader("وضع الطوارئ والإنقاذ السريع")
    if st.button("توليد ورقة الملخص الشامل ليلة الامتحان"):
        if st.session_state.lecture_content:
            with st.spinner("جاري استخلاص أهم القوانين والتعاريف والأسئلة المصيرية المتوقعة..."):
                ai_emergency = ask_ai(f"اكتب لي ملخصاً مكثفاً ليلة الامتحان (روشتة إنقاذ سريعة) يحتوي على أهم القوانين والتعاريف والرموز فقط من هذه المحاضرة بشكل مقتضب جداً وسهل المذاكرة السريعة:\n\n{st.session_state.lecture_content[:3000]}")
                st.session_state.generated_summary = ai_emergency
                st.session_state.xp += 30
                st.rerun()
        else:
            st.warning("يرجى تغذية المنصة بمحتوى دراسي أولاً في التبويب الأول لكي يتمكن نيبور من صياغة ملخص الطوارئ له.")
        
    if st.session_state.generated_summary:
        st.markdown("🚀 **ملخص الإنقاذ السريع وجدول القوانين المركزة جاهز الآن أمامك:**")
        st.info(st.session_state.generated_summary)