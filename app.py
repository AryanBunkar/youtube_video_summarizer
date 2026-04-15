import streamlit as st
from utils import get_video_id, get_transcript, summarize_text
 
st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🎥",
    layout="centered"
)
 
st.markdown("""
<style>
    .title { font-size: 2.2rem; font-weight: 800; }
    .subtitle { color: #888; margin-top: -10px; margin-bottom: 20px; }
    .summary-box {
        background: #f8f9fa;
        border-left: 4px solid #ff4b4b;
        padding: 1.2rem 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .stat-box {
        background: #f0f2f6;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        text-align: center;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)
 
st.markdown('<div class="title">🎥 YouTube Video Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Paste any YouTube link and get a free AI-powered summary instantly.</div>', unsafe_allow_html=True)
st.divider()
 
url = st.text_input(
    "🔗 YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)
 
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    summarize_btn = st.button("✨ Summarize", use_container_width=True, type="primary")
 
if summarize_btn:
    if not url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL.")
    else:
        try:
            with st.status("Processing your video...", expanded=True) as status:
                st.write("🔍 Extracting video ID...")
                video_id = get_video_id(url)
 
                st.write("📝 Fetching transcript...")
                transcript = get_transcript(video_id)
                word_count = len(transcript.split())
 
                st.write("🤖 Generating summary with LLaMA 3 (Free)...")
                summary = summarize_text(transcript)
 
                status.update(label="✅ Done!", state="complete", expanded=False)
 
            # Stats
            st.markdown("#### 📊 Quick Stats")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="stat-box">📄 <b>{word_count:,}</b><br>Transcript Words</div>', unsafe_allow_html=True)
            with c2:
                read_time = max(1, word_count // 200)
                st.markdown(f'<div class="stat-box">⏱️ <b>~{read_time} min</b><br>Video Read Time</div>', unsafe_allow_html=True)
            with c3:
                summary_words = len(summary.split())
                reduction = round((1 - summary_words / word_count) * 100) if word_count else 0
                st.markdown(f'<div class="stat-box">📉 <b>{reduction}%</b><br>Content Reduced</div>', unsafe_allow_html=True)
 
            st.markdown("---")
            st.markdown("#### 📄 Summary")
            st.markdown(summary)
 
            st.download_button(
                label="⬇️ Download Summary as TXT",
                data=summary,
                file_name="youtube_summary.txt",
                mime="text/plain",
                use_container_width=True
            )
 
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("💡 Make sure the video has subtitles/captions enabled and the URL is correct.")
 
st.divider()
st.markdown(
    "<center><small>Powered by Groq (LLaMA 3) — 100% Free 🆓</small></center>",
    unsafe_allow_html=True
)