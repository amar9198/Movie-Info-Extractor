# 🎬 Movie Info Extractor — CineSage

CineSage is an AI-powered Movie Information Extractor built with **Python, Streamlit, LangChain, and Groq**.

The application takes a natural-language description of a movie and automatically extracts structured information such as the movie title, release year, genre, director, cast, rating, and a short summary.

---

## 🚀 Features

- 🎬 Extract movie information from natural-language text
- 🧠 AI-powered information extraction using LLMs
- 📅 Extract release year
- 🎭 Extract movie genres
- 🎥 Extract director information
- 👥 Extract main cast members
- ⭐ Extract rating when mentioned
- 📝 Generate a concise movie summary
- 📊 Display extracted information in a structured UI
- 📦 Display raw JSON output
- 🌐 Streamlit-based web interface
- ⚡ Powered by Groq's fast LLM inference

---

## 🌐 Live Demo

Try the deployed application:

**Movie Info Extractor — CineSage**

https://movie-info-extractor-tgeftfjpptoatquleivprt.streamlit.app/

The application is deployed using **Streamlit Community Cloud** and uses **Groq's LLM** to extract structured movie information from natural-language descriptions.

### How to use

1. Open the live application.
2. Enter a description of a movie.
3. Click the extraction button.
4. CineSage extracts:

   * 🎬 Movie title
   * 📅 Release year
   * 🎭 Genre
   * 🎥 Director
   * 👥 Cast
   * ⭐ Rating
   * 📝 Summary
5. The extracted information is displayed in a structured format.


## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web user interface |
| LangChain | LLM application framework |
| LangChain Core | Prompt and output processing |
| LangChain Groq | Groq LLM integration |
| Groq | Large Language Model inference |
| Pydantic | Structured data validation |
| python-dotenv | Environment variable management |

---

## 🏗️ Project Structure

```text
CineSage/
│
├── UICore.py
├── requirements.txt
├── .gitignore
└── README.md
