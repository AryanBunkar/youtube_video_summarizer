import os
from urllib.parse import parse_qs, urlparse

import streamlit as st
from groq import Groq
from dotenv import load_dotenv, find_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

load_dotenv(find_dotenv())


# ─────────────────────────────────────────────
# URL → Video ID
# ─────────────────────────────────────────────
def get_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/")

    if parsed.hostname in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        query = parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]
        path_parts = [p for p in parsed.path.split("/") if p]
        if len(path_parts) >= 2 and path_parts[0] == "shorts":
            return path_parts[1]
        for part in path_parts:
            if len(part) == 11:
                return part

    return url.split("/")[-1].split("?")[0]


# ─────────────────────────────────────────────
# Video ID → Transcript text
# ─────────────────────────────────────────────
def get_transcript(video_id: str) -> str:
    from youtube_transcript_api.proxies import WebshareProxyConfig

    # ✅ Read from Streamlit secrets (cloud) or .env (local)
    proxy_username = st.secrets.get("kshtgnwc") or os.environ.get("kshtgnwc")
    proxy_password = st.secrets.get("lt53a94h6vxx") or os.environ.get("lt53a94h6vxx")

    proxy_config = WebshareProxyConfig(
        proxy_username=proxy_username,
        proxy_password=proxy_password,
    )
# AFTER (fixed)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id, proxies=proxy_config)  # ← proxies goes here
    except TranscriptsDisabled:
        raise RuntimeError("Transcripts are disabled for this video. Try another video.")
    except Exception as exc:
        raise RuntimeError(f"Unable to fetch transcript: {exc}") from exc

    transcript = None
    for finder in ("find_transcript", "find_generated_transcript", "find_manually_created_transcript"):
        if hasattr(transcript_list, finder):
            try:
                transcript = getattr(transcript_list, finder)(["en", "en-US", "en-GB"])
                break
            except Exception:
                continue

    if transcript is None:
        transcript = next(iter(transcript_list), None)

    if transcript is None:
        raise RuntimeError("No transcript available for this video.")

    try:
        fetched = transcript.fetch()
    except Exception as exc:
        raise RuntimeError(f"Could not fetch transcript content: {exc}") from exc

    parts = []
    for item in fetched:
        text = item.get("text", "") if isinstance(item, dict) else getattr(item, "text", "")
        if text:
            parts.append(text)

    full_text = " ".join(parts).strip()
    if not full_text:
        raise RuntimeError("Transcript is empty.")
    return full_text


# ─────────────────────────────────────────────
# Chunk long transcripts
# ─────────────────────────────────────────────
def _chunk_text(text: str, max_words: int = 3000) -> list:
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


# ─────────────────────────────────────────────
# Groq-powered summarization (FREE)
# ─────────────────────────────────────────────
def summarize_text(text: str) -> str:
    # ✅ Works on both local (.env) and Streamlit Cloud (st.secrets)
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env file or Streamlit secrets."
        )

    client = Groq(api_key=api_key)
    chunks = _chunk_text(text, max_words=3000)

    # ── Step 1: Extract key points from each chunk ────────────────────────
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        prompt = f"""You are an expert video summarizer.

Below is part {i + 1} of {len(chunks)} of a YouTube video transcript.
Extract the most important key points from this section.

TRANSCRIPT:
{chunk}

Return ONLY a clear bullet-point list of key ideas. Be specific and informative."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.3,
        )
        chunk_summaries.append(response.choices[0].message.content.strip())

    # ── Step 2: Merge into final polished summary ─────────────────────────
    if len(chunk_summaries) == 1:
        combined_input = chunk_summaries[0]
    else:
        combined_input = "\n\n".join(
            f"Section {i+1}:\n{s}" for i, s in enumerate(chunk_summaries)
        )

    final_prompt = f"""You are an expert YouTube video summarizer.

Below are key points extracted from a YouTube video transcript.
Write a high-quality, accurate, and well-structured summary.

EXTRACTED NOTES:
{combined_input}

Write your summary in this EXACT format:

## 🎯 What This Video Is About
(Write 1-2 clear sentences describing the video's topic and purpose)

## 🔑 Key Points
(Write 6-8 specific bullet points with the most important ideas, facts, and insights from the video)

## 💡 Main Takeaway
(Write 1 powerful sentence — the single most important thing to remember)

Rules:
- Be specific, not vague
- Use simple and clear language
- Do NOT use filler phrases like "the video discusses" or "the speaker mentions"
- Write as if explaining to someone who hasn't watched the video"""

    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": final_prompt}],
        max_tokens=1000,
        temperature=0.3,
    )

    return final_response.choices[0].message.content.strip()
