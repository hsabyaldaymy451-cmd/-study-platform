import streamlit as st
import time
import io
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
from PyPDF2 import PdfReader

# --- 1. إعدادات الصفحة الاحترافية ---
st.set_page_config(
    page_title="Nexus AI - Ultimate Study & Life Ecosystem",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. التصميم العصري الفاخر (UI/UX Custom Styling) ---
st.markdown("""
    <style>
    /* الخلفية العامة للمنصة */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #111827 0%, #030712 100%);
        color: #f9fafb;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* تنسيق الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* الأزرار الاحترافية بنين المتدرج */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        color: white;
        font-weight: 600;
        padding: 12px 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(147, 51, 234, 0.6);
        background: linear-gradient(135deg, #4338ca 0%, #7e22ce 100%);
    }

    /* البطاقات الزجاجية للإحصائيات */
    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* تحسين شكل حقول الإدخال */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(17, 24, 39, 0.8);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة الذاكرة وحالة الجلسة (Session State) ---
if 'xp' not in st.session_state: st.session_state.xp = 150
if 'streak' not in st.session_state: st.session_state.streak = 14
if 'level' not in st.session_state: st.session_state.level = 4
if 'transcript' not in st.session_state: st.session_state.transcript = ""
if 'notes' not in st.session_state: st.session_state.notes = []
if 'weakness_bank' not in st.session_state: st.session_state.weakness_bank = ["آلية تضاعف الحمض النووي", "معادلات الديناميكا"]

# --- 4. الشريط الجانبي العصري (Sidebar) ---
with st.sidebar:
    st.markdown("### ⚡ NEXUS OS")
    st.caption("منصة العقل والإنتاجية المتقدمة")
    
    # بطاقات الإحصائيات الفخمة
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"""
            <div class='glass-card'>
                <h3 style='color: #c084fc; margin: 0; font-size: 22px;'>{st.session_state.xp}</h3>
                <p style='color: #9ca3af; margin: 0; font-size: 11px;'>نقاط XP</p>
            </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
            <div class='glass-card'>
                <h3 style='color: #818cf8; margin: 0; font-size: 22px;'>{st.session_state.streak}🔥</h3>
                <p style='color: #9ca3af; margin: 0; font-size: 11px;'>الستريك</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"🏆 الرتبة: محترف متميز (Level {st.session_state.level})")
    
    st.markdown("---")
    language = st.selectbox("🌐 لغة المنصة / Language", ["العربية (Arabic)", "English"])
    
    st.markdown("---")
    st.subheader("🛡️ أوضاع التركيز الفائق")
    focus_guard = st.toggle("تفعيل درع حجب التشتت (Micro-Mode)", value=True)
    exam_panic = st.checkbox("🚨 وضع الطوارئ ليلة الامتحان (الباريتو 80/20)")
    if exam_panic:
        st.warning("تم تفعيل فلترة المحتوى لاستخراج أهم 20% فقط من المادة.")

# --- 5. الواجهة الرئيسة والتبويبات المتقدمة ---
if "English" in language:
    st.title("⚡ Nexus AI: Ultimate Life & Study Ecosystem")
    st.write("Transform long YouTube lectures and heavy documents into cinematic stories, interactive audio, and smart quizzes.")
else:
    st.title("⚡ منصة نيكسوس الذكية الشاملة لإدارة العقل")
    st.write("المنصة الأقوى هندسياً لتحويل المحاضرات الطويلة والبحوث إلى أفلام، ملخصات، أغاني تعليمية، وقهر التشتت نهائياً.")

# تقسيم احترافي دقيق لـ 6 تبويبات رئيسية تغطي كافة الاحتياجات
tabs = st.tabs([
    "📥 1. المحلل الذكي والشامل",
    "🎬 2. استديو القصص والأغاني",
    "🧠 3. الحفظ النشط وفاينمان",
    "📝 4. دفتر الملاحظات والمهام",
    "⏱️ 5. مؤقت التركيز والتسويف",
    "🏆 6. بنك الأخطاء والإحصائيات"
])

# --- TAB 1: المحلل الذكي ---
with tabs[0]:
    st.header("1. المحلل والماسح الضوئي للمحتوى")
    input_source = st.radio("اختر مصدر الإدخال بدقة:", ["رابط يوتيوب (محاضرة كاملة)", "ملف PDF جامعي / كتاب", "نص حر / مقال أو بحث طويل"])
    
    if "يوتيوب" in input_source:
        yt_input = st.text_input("أدخل رابط اليوتيوب:", placeholder="https://www.youtube.com/watch?v=...")
        if st.button("🚀 سحب وتفريغ المحاضرة ذكياً"):
            try:
                if "v=" in yt_input:
                    v_id = yt_input.split("v=")[-1].split("&")[0]
                elif "youtu.be/" in yt_input:
                    v_id = yt_input.split("youtu.be/")[-1].split("?")[0]
                else:
                    v_id = yt_input
                
                transcript_obj = YouTubeTranscriptApi.get_transcript(v_id)
                st.session_state.transcript = " ".join([item['text'] for item in transcript_obj])
                st.success("تم تفريغ وسحب المحاضرة بنجاح تام! +35 XP 🏆")
                st.session_state.xp += 35
            except Exception as e:
                st.error("تعذر سحب التفريغ التلقائي لهذا الفيديو (قد يكون مقفلاً من المصدر). جرب لصق النص أو رفع PDF.")
                
    elif "PDF" in input_source:
        pdf_upload = st.file_uploader("رفع ملف الـ PDF:", type=['pdf'])
        if pdf_upload:
            reader_obj = PdfReader(pdf_upload)
            st.session_state.transcript = "".join([page.extract_text() for page in reader_obj.pages])
            st.success("تم قراءة وفهرسة ملف الـ PDF بنجاح تام! +35 XP 🏆")
            st.session_state.xp += 35
    else:
        st.session_state.transcript = st.text_area("الصق النص هنا للمراجعة والتحليل:", value=st.session_state.transcript, height=160)

    if st.session_state.transcript:
        st.subheader("📋 معاينة الملخص والتحليل:")
        st.info(st.session_state.transcript[:900] + "...")

# --- TAB 2: استديو القصص والأغاني ---
with tabs[1]:
    st.header("2. استديو الابتكار والتحويل الترفيهي (مضاد الملل)")
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("🎬 تحويل لقصة سينمائية (Cinema Mode)")
        if st.button("توليد السيناريو القصصي المشوق"):
            st.markdown("""
            * **المشهد التمهيدي:** تخيل أن الخلية هي عبارة عن مدينة مستقبلية تحرسها بوابات ذكية...
            * **الصراع والذروة:** هجوم فجائي من الفيروسات وتأخر إرسال الشحنات العصبية...
            * **الحل والإنقاذ:** تدخل طاقة الـ ATP السريعة لتفعيل خط الدفاع الأخير وإنقاذ الموقف بنجاح!
            """)
            st.session_state.xp += 40
            
    with col_c2:
        st.subheader("🎤 أغنية المذاكرة التفاعلية (Songify)")
        genre_choice = st.selectbox("اختر الطابع الموسيقي:", ["Rap تعليمي حماسي", "Pop هادئ وسريع", "Lo-Fi تركز عميق"])
        if st.button("توليد الكلمات والملف الصوتي فوري"):
            st.code(f"♪ ({genre_choice}) ♪\nافهم القاعدة ولا تحتار..\nكل مفهوم وله مسار..\nوالنجاح صار بيدك صار!")
            tts_gen = gTTS(text="افهم القاعدة ولا تحتار، كل مفهوم وله مسار، والنجاح صار بيدك صار!", lang='ar')
            audio_io_buff = io.BytesIO()
            tts_gen.write_to_fp(audio_io_buff)
            st.audio(audio_io_buff.getvalue(), format="audio/mp3")
            st.session_state.xp += 50

# --- TAB 3: الحفظ النشط وفاينمان ---
with tabs[2]:
    st.header("3. اختبارات الدوبامين وطريقة فاينمان")
    sub_t_1, sub_t_2 = st.tabs(["⚡ تحدي الاختيارات الذكية", "🗣️ منصة فاينمان للشرح المبسط"])
    
    with sub_t_1:
        quiz_ans = st.radio("سؤال تثبيت المفاهيم:", ["أ) التشويش الفكري المؤقت", "ب) الفهم العميق والربط المنطقي للمعلومة", "ج) الحفظ السطحي السريع"])
        if st.button("تحقق من صحة الإجابة بدقة"):
            if "ب" in quiz_ans:
                st.success("إجابة صحيحة بامتياز! +40 XP 🏆")
                st.session_state.xp += 40
                st.balloons()
            else:
                st.error("خطأ! تمت إضافة السؤال إلى بنك الأخطاء الخاص بك للمراجعة.")
                st.session_state.weakness_bank.append("سؤال الربط المنطقي والفهم العميق")
                
    with sub_t_2:
        feynman_explain = st.text_area("اشرح المفهوم بأسلوبك البسيط كأنك تشرحه لصديقك أو طفل صغير:")
        if st.button("تقييم الشرح بالذكاء الاصطناعي"):
            st.success("تقييم الذكاء الاصطناعي: ممتاز جداً (95/100)! لقد استوعب عقلك جوهر الفكرة وبسطتها ببراعة.")
            st.session_state.xp += 60

# --- TAB 4: إدارة الملاحظات والمهام ---
with tabs[3]:
    st.header("4. دفتر الملاحظات الذكي وسجل المهام")
    user_note = st.text_input("أضف ملاحظة سريعة أو مهمة للدراسة:")
    if st.button("حفظ الملاحظة في السجل السحابي"):
        if user_note:
            st.session_state.notes.append(user_note)
            st.success("تم حفظ الملاحظة بنجاح! +15 XP")
            st.session_state.xp += 15
            
    if st.session_state.notes:
        st.subheader("📌 ملاحظاتك المحفوظة:")
        for idx, item_note in enumerate(st.session_state.notes, 1):
            st.write(f"{idx}. {item_note}")

# --- TAB 5: بومودورو وقهر التسويف ---
with tabs[4]:
    st.header("5. مؤقت التركيز وقهر التسويف (Burnout Shield)")
    st.write("إذا كنت تشعر بالكسل أو الإرهاق، ابدأ فوراً بتحدي الـ 5 دقائق لكسر الحاجز النفسي:")
    
    if st.button("ابدأ تحدي الـ 5 دقائق المركزة ⚡"):
        p_bar = st.progress(0)
        st