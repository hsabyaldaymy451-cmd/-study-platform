import streamlit as st
import streamlit.components.v1 as components

# إعدادات واجهة المنصة
st.set_page_config(
    page_title="أكاديمية اللغة الإنكليزية",
    page_icon="📚",
    layout="wide"
)

# عنوان المنصة الرئيسي
st.title("📚 أكاديمية اللغة الإنكليزية - المنصة التفاعلية")
st.write("أهلاً بكم في المنصة الخاصة بمحاضرات ومكالمات مادة اللغة الإنكليزية.")
st.markdown("---")

# القائمة الجانبية للتنقل بين الأقسام
st.sidebar.title("📌 القوائم الرئيسية")
menu = [
    "🎬 المحاضرات والدروس",
    "🎙️ غرف البث المباشر والمكالمات",
    "📝 الاختبارات والواجبات",
    "📇 بطاقات المفردات (Flashcards)"
]
choice = st.sidebar.radio("اختر القسم:", menu)

# 1. قسم المحاضرات المسجلة
if choice == "🎬 المحاضرات والدروس":
    st.header("🎬 المحاضرات والدروس المسجلة")
    st.info("💡 مشاهدة الفيديوهات متاحة لطلاب المنصة حصراً.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("الوحدة الأولى: Present Simple & Grammar")
        # فيديو يوتيوب (Unlisted)
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
    with col2:
        st.subheader("📁 ملحقات الدرس")
        st.write("يمكنك تحميل ملزمة الشرح ورسائل التمارين:")
        st.download_button(
            label="📥 تحميل ملزمة Unit 1 (PDF)",
            data="محتوى ملف الـ PDF هنا",
            file_name="Unit1_Grammar.pdf"
        )

# 2. قسم البث المباشر والمكالمات (Jitsi Meet المجاني بالكامل)
elif choice == "🎙️ غرف البث المباشر والمكالمات":
    st.header("🎙️ البث المباشر والمحادثة التفاعلية")
    st.success("✅ الغرفة جاهزة للمكالمة. اضغط على خيار السماح للميكروفون والكاميرا للدخول.")
    
    # تضمين خدمة البث المباشر المجانية
    jitsi_room_html = """
    <iframe src="https://meet.jit.si/MomEnglishAcademy2026" 
            height="620px" 
            width="100%" 
            style="border:none; border-radius:12px;"
            allow="camera; microphone; display-capture; autoplay">
    </iframe>
    """
    components.html(jitsi_room_html, height=640)

# 3. قسم الاختبارات
elif choice == "📝 الاختبارات والواجبات":
    st.header("✍️ كويز سريع في قواعد اللغة")
    
    q1 = st.radio(
        "اختر الخيار الصحيح للجملة التالية: She ___ to school every day.",
        ["go", "goes", "going", "gone"]
    )
    
    if st.button("تسليم الإجابة"):
        if q1 == "goes":
            st.success("إجابة صحيحة! 🎉 المميز في زمن المضارع البسيط إضافة s للفاعل المفرد.")
        else:
            st.error("إجابة خاطئة! حاول مرة أخرى.")

# 4. قسم المفردات
elif choice == "📇 بطاقات المفردات (Flashcards)":
    st.header("📇 مراجعة وحفظ المفردات السريعة")
    
    st.subheader("الكلمة: Fluency")
    with st.expander("اضغط لإظهار المعنى والنطق الصوتية"):
        st.write("📖 **المعنى:** الطلاقة (في التحدث والتعبير)")
        st.write("🔊 **النطق الصوتية:** /ˈfluː.ən.si/")
