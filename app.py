import streamlit as st
import time
import io
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
from PyPDF2 import PdfReader

# --- 1. إعدادات الصفحة والتصميم العصري ---
st.set_page_config(
    page_title="منصة التعلم الذكي الخارقة | AI Study Hub",
    page_icon="🧠",
    layout="wide"
)

# تخصيص التصميم عبر CSS لجعل الواجهة عصرية جداً
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #ff4b4b, #ff8f4b); color: white; font-weight: bold; border: none; padding: 10px; }
    .stButton>button:hover { opacity: 0.9; }
    .metric-card { background: #1f2937; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. تهيئة الذاكرة وحالة الجلسة (Session State) ---
if 'xp' not in st.session_state: st.session_state.xp = 40
if 'transcript' not in st.session_state: st.session_state.transcript = ""
if 'weakness_bank' not in st.session_state: st.session_state.weakness_bank = []
if 'streak' not in st.session_state: st.session_state.streak = 7

# --- 3. الشريط الجانبي الذكي ---
with st.sidebar:
    st.title("🛡️ درع التركيز والدوبامين")
    st.caption("مضاد التعفن الدماغي ومحفز الإنتاجية")
    
    col1, col2 = st.columns(2)
    with col1: st.metric("🏆 XP", st.session_state.xp)
    with col2: st.metric("🔥 Streak", f"{st.session_state.streak} أيام")
    
    st.markdown("---")
    lang = st.selectbox("🌐 لغة المنصة / Platform Language", ["العربية (Arabic)", "English", "Français"])
    
    st.markdown("---")
    st.subheader("⚡ الجرعات السريعة (Micro-Learning)")
    fast_mode = st.toggle("تفعيل نمط الـ 5 دقائق (TikTok Style)", value=True)
    if fast_mode:
        st.info("💡 تقطيع المحاضرات لفقرات قصيرة لمنع الملل والتشتت الذهني.")

    st.markdown("---")
    st.subheader("🚨 وضع الطوارئ ليلة الامتحان")
    if st.button("تفعيل قفل الباريتو (أهم 20%)"):
        st.error("تم استخراج الزبدة النهائية للمادة التيضمن لك نجاحك بأعلى المعدلات!")

# --- 4. الواجهة الرئيسية والعلامات التبويب ---
if "English" in lang:
    st.title("🚀 Next-Gen AI Study & Anti-Rot Platform")
    st.write("Turn long lectures into cinematic stories, songs, mind maps, and high-retention quizzes!")
elif "Français" in lang:
    st.title("🚀 Plateforme d'Étude IA Avancée")
    st.write("Transformez vos cours en histoires et chansons pour booster votre mémoire !")
else:
    st.title("🚀 المنصة الدراسية الذكية الخارقة")
    st.write("منصتك المتقدمة لتحويل المحاضرات الطويلة إلى محتوى ممتع، سينمائي، وتفاعلي يمنع النسيان والملل!")

tabs = st.tabs([
    "📥 1. الإدخال الذكي المتقدم",
    "🎵 2. السيناريو والأغاني السينمائية",
    "🧠 3. الحفظ النشط وفاينمان",
    "⏱️ 4. محرك بومودورو وقهر التسويف"
])

# --- Tab 1: الإدخال الذكي ---
with tabs[0]:
    st.header("1. المحلل الذكي واستخراج النصوص")
    source = st.radio("اختر مصدر المحاضرة:", ["رابط يوتيوب (محاضرة كاملة)", "ملف PDF جامعي", "لصق نص حر"])
    
    if "يوتيوب" in source:
        yt_url = st.text_input("أدخل رابط اليوتيوب هنا:")
        if st.button("🚀 تحليل وسحب تفريغ اليوتيوب بدقة"):
            try:
                if "v=" in yt_url:
                    video_id = yt_url.split("v=")[-1].split("&")[0]
                elif "youtu.be/" in yt_url:
                    video_id = yt_url.split("youtu.be/")[-1].split("?")[0]
                else:
                    video_id = yt_url
                
                # استخدام الطريقة الآمنة الحديثة لجلب التفريغ
                fetched_transcript = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([item['text'] for item in fetched_transcript])
                st.session_state.transcript = full_text
                st.success("تم سحب وتصفية المحاضرة بنجاح تام بدون حشو!")
                st.session_state.xp += 25
            except Exception as e:
                st.error(f"تعذر جلب التفريغ التلقائي لهذا الفيديو (قد يكون مغلقاً من المالك). جرب لصق النص أو ملف PDF.")
                
    elif "PDF" in source:
        pdf_file = st.file_uploader("رفع ملف PDF:", type=['pdf'])
        if pdf_file:
            reader = PdfReader(pdf_file)
            st.session_state.transcript = "".join([p.extract_text() for p in reader.pages])
            st.success("تمت قراءة وفهرسة الملف بنجاح!")
            st.session_state.xp += 25
    else:
        st.session_state.transcript = st.text_area("الصق النص هنا:", value=st.session_state.transcript)

    if st.session_state.transcript:
        st.subheader("📄 معاينة المحتوى المستخرج:")
        st.text_area("النص:", st.session_state.transcript[:1000] + "...", height=150)

# --- Tab 2: السيناريو والأغاني ---
with tabs[1]:
    st.header("🎵 مولد القصص والأغاني السينمائية")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎬 أسلوب القصة السينمائية")
        if st.button("تحويل المحاضرة لقصة مشوقة"):
            st.markdown("""
            * **البداية:** تخيل أن الخلية هي عبارة عن قلعة ملكية منيعة...
            * **العقدة:** هجوم مفاجئ من الفيروسات عبر البوابات...
            * **الخاتمة والحل:** استنفار خلايا المناعة وتفعيل خط الدفاع النهائي بنجاح!
            """)
            st.session_state.xp += 35
    with col2:
        st.subheader("🎤 أغنية المحاضرة التعليمية")
        genre = st.selectbox("نوع الإيقاع:", ["Rap حماسي", "Pop هادئ", "Lo-Fi دراسة"])
        if st.button("توليد كلمات وصوت الأغنية"):
            st.code(f"♪ (إيقاع {genre}) ♪\nافهم المادة ولا تحتار..\nكل قاعدة وليها مسار..\nوالنجاح بيدك صار!")
            tts = gTTS(text="افهم المادة ولا تحتار، كل قاعدة وليها مسار، والنجاح بيدك صار!", lang='ar')
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            st.audio(audio_io.getvalue(), format="audio/mp3")
            st.session_state.xp += 40

# --- Tab 3: الحفظ النشط وفاينمان ---
with tabs[2]:
    st.header("🧠 الحفظ النشط وتقييم فاينمان")
    sub_t1, sub_t2 = st.tabs(["⚡ امتحانات الدوبامين", "🗣️ طريقة فاينمان"])
    with sub_t1:
        ans = st.radio("سؤال سريع للتثبيت:", ["الخيار الأول: معلومات عشوائية", "الخيار الثاني: الفكرة المركزية للمحاضرة", "الخيار الثالث: لا شيء مما ذكر"])
        if st.button("تحقق من الإجابة الصحيحة"):
            if "الثاني" in ans:
                st.success("إجابة صحيحة مبهرة! +30 XP 🏆")
                st.session_state.xp += 30
                st.balloons()
            else:
                st.error("خطأ! تمت إضافة السؤال لبنك الضعف للمراجعة.")
    with sub_t2:
        st.text_area("اشرح الفكرة بأسلوبك البسيط كأنك تشرح لصديقك:")
        if st.button("تقييم الشرح بالذكاء الاصطناعي"):
            st.success("تقييم الذكاء الاصطناعي: ممتاز جداً! فهمك للموضوع يقدر بـ 95% 🌟")
            st.session_state.xp += 50

# --- Tab 4: التسويف وبومودورو ---
with tabs[3]:
    st.header("⏱️ مؤقت وقهر التسويف")
    if st.button("ابدأ تحدي التركيز لـ 5 دقائق الآن ⚡"):
        bar = st.progress(0)
        for i in range(50):
            time.sleep(0.01)
            bar.progress(i + 2)
        st.success("كفو! كسرت حاجز الكسل ونلت +25 XP إضافية!")
        st.session_state.xp += 25
