# 🎥 YouTube Video Summarizer

A free AI-powered YouTube video summarizer built with **Streamlit** and **Groq (LLaMA 3)**. Paste any YouTube URL and get a clean, structured summary in seconds — completely free!

---

## 🚀 Demo

> Paste a YouTube link → Get an AI summary instantly with key points and takeaways.

---

## ✨ Features

- 🆓 **100% Free** — Uses Groq API (free tier, no credit card needed)
- ⚡ **Fast** — Groq's LPU inference is extremely fast
- 🧠 **Smart Summarization** — Powered by LLaMA 3.3 70B model
- 📄 **Structured Output** — What the video is about, key points & main takeaway
- 📊 **Stats** — Word count, estimated read time, content reduction %
- ⬇️ **Download** — Save summary as a `.txt` file
- 🎬 **All YouTube formats** — Supports regular, shorts, and youtu.be links

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI |
| [Groq API](https://groq.com) | Free LLM inference |
| [LLaMA 3.3 70B](https://groq.com) | Summarization model |
| [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) | Fetch YouTube transcripts |

---

## 📁 Project Structure

```
youtube-summarizer/
│
├── app.py          # Streamlit frontend
├── utils.py        # Core logic (transcript fetch + AI summarization)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/youtube-summarizer.git
cd youtube-summarizer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your FREE Groq API key

1. Go to 👉 [console.groq.com](https://console.groq.com)
2. Sign up — free, no credit card required
3. Click **API Keys** → **Create API Key**
4. Copy your key (starts with `gsk_...`)

### 4. Set your API key

**Option A — Direct in code** (quickest):

Open `utils.py` and replace:
```python
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
```
with:
```python
client = Groq(api_key="your_groq_api_key_here")
```

**Option B — Environment variable** (recommended):

```bash
# Windows
set GROQ_API_KEY=your_groq_api_key_here

# Mac / Linux
export GROQ_API_KEY=your_groq_api_key_here
```

**Option C — .env file**:

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Then add to top of `utils.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```
Install: `pip install python-dotenv`

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📦 Requirements

Create a `requirements.txt` file with:

```
streamlit
groq
youtube-transcript-api
python-dotenv
```

---

## 📝 How It Works

```
YouTube URL
    ↓
Extract Video ID
    ↓
Fetch Transcript (youtube-transcript-api)
    ↓
Split into chunks (3000 words each)
    ↓
LLaMA 3.3 extracts key points from each chunk  [Groq API]
    ↓
LLaMA 3.3 merges into final structured summary  [Groq API]
    ↓
Display to user
```

---

## 🎯 Summary Format

Every summary follows this structure:

```
🎯 What This Video Is About
   1-2 sentences about the video's topic

🔑 Key Points
   6-8 bullet points with the most important ideas

💡 Main Takeaway
   The single most important thing to remember
```

---

## ⚠️ Limitations

- Video must have **subtitles/captions enabled** on YouTube
- Works best with **English** videos
- Very short videos (< 1 min) may produce limited summaries
- Groq free tier has **rate limits** (generous for personal use)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) for the free and blazing-fast LLM API
- [Meta](https://ai.meta.com) for the LLaMA 3 model
- [Streamlit](https://streamlit.io) for the easy web UI framework
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for transcript fetching

---

<p align="center">Made with ❤️ | Powered by Groq (LLaMA 3) — 100% Free 🆓</p>
