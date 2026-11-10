import streamlit as st
import time
import re
import asyncio
import concurrent.futures
from datetime import date, timedelta
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
import g4f

import nest_asyncio
nest_asyncio.apply()

st.set_page_config(
    page_title="NIBUR Engine Ultimate",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
:root{
  --bg:#0e1420; --surface:#151d2e; --surface2:#1b2538; --line:#26324a;
  --text:#e8ecf4; --muted:#8b97ad; --accent:#5b8def; --ok:#3ecf9e; --warn:#f2b84b;
}
.stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp button, .stApp input, .stApp textarea, .stApp li {
  font-family:'Tajawal', sans-serif !important;
}
.stApp{ background:var(--bg); color:var(--text); direction:ltr; }
[data-testid="stHeader"]{ background:transparent; }
footer{ visibility:hidden; }
.block-container{ max-width:960px; padding-top:2.2rem; padding-bottom:4rem; }
h1{ font-weight:800; letter-spacing:0; }
h2,h3{ font-weight:700; }
p, li, label{ line-height:1.8; }

[data-testid="stSidebar"]{ background:var(--surface); border-right:1px solid var(--line); }
[data-testid="stSidebar"] .block-container{ padding-top:1.5rem; }

.card{ background:var(--surface); border:1px solid var(--line); border-radius:14px; padding:20px 22px; margin-bottom:16px; }
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

.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--line); overflow-x:auto; }
.stTabs [data-baseweb="tab"]{ height:46px; padding:0 16px; color:var(--muted); font-weight:500; white-space:nowrap; }
.stTabs [aria-selected="true"]{ color:var(--text) !important; font-weight:700; }
.stTabs [data-baseweb="tab-highlight"]{ background:var(--accent); height:3px; }
.stTabs [data-baseweb="tab-panel"]{ padding-top:1.4rem; }

.stButton > button{ width:100%; border-radius:10px; background:var(--accent); color:#fff; font-weight:700; padding:10px 18px; border:1px solid transparent; transition:background .15s; }
.stButton > button:hover{ background:#4a7de0; color:#fff; border-color:transparent; }
[data-testid="stSidebar"] .stButton > button{ background:transparent; color:var(--text); border:1px solid var(--line); }
[data-testid="stSidebar"] .stButton > button:hover{ background:var(--surface2); }
.stTextInput input, .stTextArea textarea, .stDateInput input{ background:var(--surface2) !important; border:1px solid var(--line) !important; border-radius:10px !important; color:var(--text) !important; }
</style>
""", unsafe_allow_html=True)

def ask_ai(prompt_text):
    def _call_g4f():
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": prompt_text}],
            )
            return response
        except Exception as e:
            return f"Error connecting to AI engine: {str(e)}"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(_call_g4f)
        return future.result()

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

today = date.today()
if "auth" not in st.session_state: st.session_state.auth = False
if "streak" not in st.session_state: st.session_state.streak = 1
if "xp" not in st.session_state: st.session_state.xp = 100
if "lecture_content" not in st.session_state: st.session_state.lecture_content = ""
if "lecture_summary" not in st.session_state: st.session_state.lecture_summary = ""
if "generated_story" not in st.session_state: st.session_state.generated_story = ""
if "generated_summary" not in st.session_state: st.session_state.generated_summary = ""
if "evaluation_result" not in st.session_state: st.session_state.evaluation_result = ""

MY_PIN = "2026"

if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns(3)
    with mid:
        st.markdown(
            "<div class='card' style='text-align:center'>"
            "<div class='brand' style='margin-bottom:6px'>🦅 NIBUR Study Platform</div>"
            "<div class='muted'>Platform is locked. Enter PIN to continue.</div></div>",
            unsafe_allow_html=True,
        )
        p_in = st.text_input("Enter Secret PIN", type="password")
        if st.button("Unlock Platform"):
            if p_in == MY_PIN:
                st.session_state.auth = True
                st.success("Unlocked successfully!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Incorrect PIN! Try again.")
    st.stop()

LEVEL_STEP = 200
xp = st.session_state.xp
level = xp // LEVEL_STEP + 1
in_level = xp % LEVEL_STEP

with st.sidebar:
    st.markdown("<div class='brand'>🦅 NIBUR ULTIMATE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card sm'><b>Level {level}</b><br>{in_level} / {LEVEL_STEP} XP</div>", unsafe_allow_html=True)
    if st.button("Lock Platform"):
        st.session_state.auth = False
        st.rerun()

st.title("NIBUR Smart Study Platform")
st.markdown("<p class='muted'>Study your lectures, analyze them using AI, and translate them instantly.</p>", unsafe_allow_html=True)

# خيار الترجمة العربية العامة
translate_to_arabic = st.checkbox("🌐 Translate AI responses to Arabic (ترجمة الردود إلى العربية تلقائياً)")

tab1, tab2, tab3 = st.tabs(["Lecture & AI Summary", "Story & Mindmap", "Emergency Review"])

with tab1:
    st.subheader("Lecture Input & Analysis")
    input_type = st.radio("Choose source type", ["Paste Text / YouTube URL", "Upload PDF"], horizontal=True)
    
    if "PDF" in input_type:
        pdf_file = st.file_uploader("Upload Lecture PDF", type=["pdf"])
        if pdf_file and st.button("Read & Summarize PDF"):
            with st.spinner("Processing PDF file..."):
                reader = PdfReader(pdf_file)
                extracted_text = "\n".join((p.extract_text() or "") for p in reader.pages)
                st.session_state.lecture_content = extracted_text
                
                lang_instruction = " Translate the final summary into clear Arabic language." if translate_to_arabic else ""
                ai_summary = ask_ai(f"Summarize the following lecture into key structured points:{lang_instruction}\n\n{extracted_text[:3000]}")
                st.session_state.lecture_summary = ai_summary
                st.session_state.xp += 30
                st.success("PDF processed successfully! (+30 XP)")
                st.rerun()
    else:
        text_input = st.text_area("Paste lecture text or YouTube link:", value=st.session_state.lecture_content, height=150)
        if st.button("Process Content with AI"):
            if "youtube.com" in text_input or "youtu.be" in text_input:
                vid_id = extract_youtube_id(text_input)
                if vid_id:
                    with st.spinner("Extracting YouTube transcript..."):
                        transcript = extract_yt_transcript(vid_id)
                        if transcript:
                            st.session_state.lecture_content = transcript
                            lang_instruction = " Translate the summary into clear Arabic language." if translate_to_arabic else ""
                            ai_summary = ask_ai(f"Summarize this YouTube transcript academically:{lang_instruction}\n\n{transcript[:3000]}")
                            st.session_state.lecture_summary = ai_summary
                            st.session_state.xp += 40
                            st.success("YouTube video transcribed and summarized! (+40 XP)")
                            st.rerun()
                        else:
                            st.error("Could not fetch transcript for this video.")
                else:
                    st.error("Invalid YouTube URL.")
            else:
                if text_input.strip():
                    with st.spinner("Analyzing text..."):
                        st.session_state.lecture_content = text_input
                        lang_instruction = " Translate the summary into clear Arabic language." if translate_to_arabic else ""
                        ai_summary = ask_ai(f"Summarize the following text clearly:{lang_instruction}\n\n{text_input}")
                        st.session_state.lecture_summary = ai_summary
                        st.session_state.xp += 20
                        st.success("Summary generated successfully! (+20 XP)")
                        st.rerun()
                else:
                    st.warning("Please enter text or a link first.")

    if st.session_state.lecture_summary:
        st.markdown("### 📋 AI Summary:")
        st.info(st.session_state.lecture_summary)

with tab2:
    st.subheader("Story & Creative Visualization")
    if st.button("Generate Interactive Story from Lecture"):
        if st.session_state.lecture_content:
            with st.spinner("Generating story..."):
                lang_instruction = " Write the story in clear Arabic language." if translate_to_arabic else ""
                ai_story = ask_ai(f"Turn this lecture into an engaging story to make it easy to remember:{lang_instruction}\n\n{st.session_state.lecture_content[:2000]}")
                st.session_state.generated_story = ai_story
                st.session_state.xp += 25
                st.rerun()
        else:
            st.warning("Please provide lecture content in Tab 1 first.")

    if st.session_state.generated_story:
        st.markdown(f"### 🎭 Story Mode\n{st.session_state.generated_story}")

with tab3:
    st.subheader("Emergency Night-Before-Exam Summary")
    if st.button("Generate Emergency Cheat Sheet"):
        if st.session_state.lecture_content:
            with st.spinner("Extracting vital definitions and laws..."):
                lang_instruction = " Provide the final output in clear Arabic language." if translate_to_arabic else ""
                ai_emergency = ask_ai(f"Create a concise emergency cheat sheet containing only core laws, definitions, and critical points:{lang_instruction}\n\n{st.session_state.lecture_content[:3000]}")
                st.session_state.generated_summary = ai_emergency
                st.session_state.xp += 30
                st.rerun()
        else:
            st.warning("Please provide lecture content first.")
        
    if st.session_state.generated_summary:
        st.markdown("🚀 **Emergency Cheat Sheet Ready:**")
        st.info(st.session_state.generated_summary)
