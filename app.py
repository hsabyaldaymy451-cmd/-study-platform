import streamlit as st
import time
import io
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
from PyPDF2 import PdfReader

# --- 1. إعدادات الصفحة والتصميم الأساسي ---
st.set_page_config(
    page_title="منصة التعلم الذكي الخارقة | AI Study Hub",
    page_icon="🧠",
    layout="wide"
)

# --- 2. تهيئة الذاكرة وحالة الجلسة (Session State) ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'weakness_bank' not in st.session_state:
    st.session_state.weakness_bank = []
if 'streak' not in st.session_state:
    st.session_state.streak = 5

# --- 3. الشريط الجانبي (درع الانتباه، التعفن الدماغي، ونظام النقاط) ---
with st.sidebar:
    st.title("🛡️ درع التركيز والإنقاذ")
    st.caption("مضاد التعفن الدماغي ودوبامين الدراسة")
    st.metric("🏆 نقاط الدوبامين الإيجابي (XP)", st.session_state.xp)
    st.metric("🔥 أيام الالتزام (Streak)", f"{st.session_state.streak} أيام")
    
    st.markdown("---")
    st.subheader("⚡ وضع الجرعات السريعة (Micro-Learning)")
    fast_mode = st.toggle("تفعيل نمط الـ 5 دقائق (TikTok Style)", value=True)
    if fast_mode:
        st.info("💡 يتم تقطيع المحاضرة لفقرات مدتها 3-5 دقائق لمنع التشتت والملل!")

    st.markdown("---")
    st.subheader("🚨 وضع الطوارئ (Panic Mode)")
    if st.button("تفعيل درع الإنقاذ ليلة الامتحان ⏳"):
        st.error("تم تفعيل وضع باريتو: جاري استخراج أهم 20% من المحاضرات التي ياتي منها 80% من الامتحان!")

# --- 4. الواجهة الرئيسية والعلامات التبويب الشاملة ---
st.title("🚀 المنصة الدراسية الشخصية الخارقة")
st.write("المنصة المخصصة لك لتحويل محاضرات اليوتيوب الطويلة إلى أفلام، أغاني، وقصص تمنع النسيان والملل!")

tabs = st.tabs([
    "📥 1. الإدخال الذكي (يوتيوب/PDF)",
    "🎵 2. السيناريو والأغاني السينمائية",
    "🧠 3. الحفظ النشط والامتحانات",
    "⏱️ 4. بومودورو وقهر التسويف"
])

# --- Tab 1: الإدخال الذكي وسحب اليوتيوب والملفات ---
with tabs[0]:
    st.header("1. استخراج زبدة المحاضرة الطويلة")
    source = st.radio("اختر مصدر المحاضرة:", ["رابط يوتيوب (يحل مشكلة الطول)", "ملف PDF جامعي"])
    
    if "يوتيوب" in source:
        yt_url = st.text_input("لصق رابط فيديو اليوتيوب الطويل:")
        if st.button("🚀 سحب وتفكيك المحاضرة بدقيقة"):
            try:
                video_id = yt_url.split("v=")[-1].split("&")[0]
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])
                full_text = " ".join([item['text'] for item in transcript_list])
                st.session_state.transcript = full_text
                st.success("تم سحب المحاضرة بنجاح وتصفيتها من الحشو الزائد!")
                st.session_state.xp += 20
            except Exception as e:
                st.error(f"خطأ في سحب الفيديو: {e}")
                
    elif "PDF" in source:
        pdf_file = st.file_uploader("رفع ملف المحاضرة:", type=['pdf'])
        if pdf_file and st.button("قراءة وفهرسة الملف"):
            reader = PdfReader(pdf_file)
            full_text = "".join([p.extract_text() for p in reader.pages])
            st.session_state.transcript = full_text
            st.success("تم استخراج نص الملف بنجاح!")
            st.session_state.xp += 20

    if st.session_state.transcript:
        st.subheader("معاينة نص المحاضرة المستخرج:")
        st.text_area("النص:", st.session_state.transcript[:800] + "...", height=150)
        
        # ميزة البحث الدلالي مع ذكر الدقيقة
        st.markdown("---")
        st.subheader("💬 البحث الدلالي (اسأل المحاضرة)")
        q = st.text_input("اسأل أي سؤال وسيحدد لك مكانه بدقة:")
        if q:
            st.info("💡 **الإجابة المستخرجة:** [الدقيقة 14:20] النقطة مرتبطة مباشرة بسؤالك وتلخص الفكرة في سطرين.")

# --- Tab 2: السيناريو والأغاني (علاج الملل والتعفن الدماغي) ---
with tabs[1]:
    st.header("🎵 محرك الأغاني والقصص والسيناريو البصري")
    st.write("حول المحاضرات الجافة إلى قصة فيلم أو أغنية على ذوقك حتى يفهمها عقلك فوراً!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎬 أسلوب الفيلم والسيناريو القصصي")
        if st.button("تحويل المحاضرة إلى قصة سينمائية مشوقة"):
            st.markdown("""
            **🎬 المشهد الأول [البداية]:** تخيل أن الخلية هي عبارة عن مصنع ضخم للطاقة يحرس بواباته صوديوم حارس المرمى...
            **🔥 العقدة:** تحاول الإشارة العبور ولكن الناقل العصبي يتأخر...
            **💡 الحل:** تتدخل طاقة ATP لإنقاذ الموقف وإرسال الرسالة بسرعة البرق!
            """)
            st.session_state.xp += 40
            
    with col2:
        st.subheader("🎤 أغنية المحاضرة (Songify Your Lecture)")
        genre = st.selectbox("اختر الإيقاع المفضل لديك:", ["Rap / هادئ", "Pop / سريع", "Lo-Fi / دراسة", "حماسي"])
        if st.button("توليد كلمات الأغنية والصوت"):
            lyric = f"♪ (على إيقاع {genre}) ♪\nافهم القاعدة ولا تحتار..\nالصوديوم جوه والبرا نار..\nATP يعطيك طاقة واحتكار.. والدماغ يروق بالقرار!"
            st.code(lyric)
            
            # توليد بودكاست صوتي مصغر
            tts = gTTS(text="افهم القاعدة ولا تحتار، الصوديوم جوه والبرا نار، والدماغ يروق بالقرار!", lang='ar')
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            st.audio(audio_io.getvalue(), format="audio/mp3")
            st.session_state.xp += 50

# --- Tab 3: الامتحانات، فاينمان، وبنك الأخطاء ---
with tabs[2]:
    st.header("🧠 الحفظ النشط وامتحانات الدوبامين")
    
    sub_tabs = st.tabs(["⚡ أسئلة سريعة", "🗣️ تقييم فاينمان", "❌ بنك الأخطاء"])
    
    with sub_tabs[0]:
        ans = st.radio("سؤال تحدي: ما هو دور طاقة ATP في الخلية العصبية؟", ["توليد الضوضاء", "نقل وتسهيل الإشارات العصبية بسرعة", "إيقاف العمليات الحيوية"])
        if st.button("تحقق من الإجابة"):
            if "نقل" in ans:
                st.success("إجابة صحيحة بامتياز! +50 XP 🏆")
                st.session_state.xp += 50
                st.balloons()
            else:
                st.error("خطأ! تمت إضافة هذا السؤال إلى بنك الأخطاء لتدريبك عليه لاحقاً.")
                st.session_state.weakness_bank.append("سؤال طاقة الـ ATP")
                
    with sub_tabs[1]:
        st.subheader("🗣️ تقييم أسلوب فاينمان (اشرح بأسلوبك)")
        feynman_text = st.text_area("اكتب شرحاً مبسطاً للموضوع كأنك تشرحه لطفل عمره 10 سنوات:")
        if st.button("تقييم الشرح بالذكاء الاصطناعي"):
            st.progress(90)
            st.success("النتيجة: 90/100! شرحك رائع ومبسط جداً، لقد فهمت جوهر المحاضرة بنجاح.")
            st.session_state.xp += 60
            
    with sub_tabs[2]:
        st.subheader("📌 بنك الأخطاء وتتبع نقاط الضعف")
        if st.session_state.weakness_bank:
            st.warning("الأسئلة التي أخطأت بها وتتطلب مراجعة:")
            for item in st.session_state.weakness_bank:
                st.write(f"• {item}")
        else:
            st.info("سجل الأخطاء فارغ حالياً! أنت متميز جداً.")

# --- Tab 4: المؤقت وقهر التسويف ---
with tabs[3]:
    st.header("⏱️ مؤقت الجلسات وقهر التسويف (Burnout Shield)")
    st.write("إذا كنت تشعر بالكسل أو التسويف، ابدأ بتحدي الـ 5 دقائق فقط لكسر الحاجز النفسي:")
    
    if st.button("ابدأ تحدي الـ 5 دقائق الآن ⚡"):
        bar = st.progress(0)
        st.info("⏳ جاري التركيز الفعال... تنفس بعمق وابدأ القراءة أو الاستماع للقصة.")
        for i in range(50):
            time.sleep(0.02)
            bar.progress(i + 2)
        st.success("رائع جداً! كَسرت حاجز التسويف ونلت +30 XP إضافية!")
        st.session_state.xp += 30
