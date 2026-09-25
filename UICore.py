import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(page_title="Movie Info Extractor", page_icon="🎬", layout="centered")

# ---------------- Styling ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    .hero {
        text-align: center;
        padding: 2rem 1rem 1.5rem 1rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
        margin-bottom: 1.8rem;
    }
    .hero h1 {
        color: white;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: #e0e0e0;
        font-size: 1rem;
        margin: 0;
    }

    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #ddd !important;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #ff512f, #dd2476);
        color: white;
        font-weight: 600;
        padding: 0.6rem 0;
        border: none;
        transition: 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 14px rgba(221, 36, 118, 0.4);
        color: white;
    }

    .movie-card {
        background: white;
        border-radius: 18px;
        padding: 1.8rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    .movie-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1f1c2c;
        margin-bottom: 0.2rem;
    }
    .movie-year {
        color: #888;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        background: #f0e6ff;
        color: #6a3fbf;
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 0.15rem 0.3rem 0.15rem 0;
    }
    .cast-badge {
        display: inline-block;
        background: #e6f4ff;
        color: #1a6fb5;
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.15rem 0.3rem 0.15rem 0;
    }
    .rating-box {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #fff7e0;
        color: #b8860b;
        padding: 0.4rem 1rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
    }
    .section-label {
        font-weight: 600;
        color: #444;
        margin-top: 1.1rem;
        margin-bottom: 0.4rem;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .summary-text {
        color: #333;
        line-height: 1.6;
        font-size: 0.98rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>🎬 Movie Info Extractor</h1>'
    '<p>Paste any paragraph about a movie and get clean, structured details instantly</p></div>',
    unsafe_allow_html=True,
)


class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


@st.cache_resource
def get_model():
    return ChatGroq(model="openai/gpt-oss-120b")


model = get_model()
parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ('system', """
Extract movie information from the paragraph
     {format_instructions}
"""),
    ("human", "{paragraph}")
])

para = st.text_area(
    "Paragraph",
    height=170,
    placeholder="e.g. Inception is a 2010 sci-fi thriller directed by Christopher Nolan, starring Leonardo DiCaprio...",
    label_visibility="collapsed",
)

extract_clicked = st.button("✨ Extract Movie Info")

if extract_clicked:
    if not para.strip():
        st.warning("Please enter a paragraph first.")
    else:
        with st.spinner("Reading between the lines..."):
            try:
                final_prompt = prompt.invoke(
                    {
                        "paragraph": para,
                        "format_instructions": parser.get_format_instructions(),
                    }
                )
                response = model.invoke(final_prompt)
                movie_data = parser.parse(response.content)

                genre_html = "".join(f'<span class="badge">{g}</span>' for g in movie_data.genre) or "<span style='color:#aaa;'>Unknown</span>"
                cast_html = "".join(f'<span class="cast-badge">{c}</span>' for c in movie_data.cast) or "<span style='color:#aaa;'>Unknown</span>"
                rating_html = f'⭐ {movie_data.rating}/10' if movie_data.rating is not None else "⭐ N/A"
                director_html = movie_data.director or "Unknown"
                year_html = movie_data.release_year or "Year unknown"

                card_html = (
                    f'<div class="movie-card">'
                    f'<div class="movie-title">{movie_data.title}</div>'
                    f'<div class="movie-year">{year_html} &nbsp;•&nbsp; Directed by {director_html}</div>'
                    f'<div class="rating-box">{rating_html}</div>'
                    f'<div class="section-label">Genre</div>'
                    f'<div>{genre_html}</div>'
                    f'<div class="section-label">Cast</div>'
                    f'<div>{cast_html}</div>'
                    f'<div class="section-label">Summary</div>'
                    f'<div class="summary-text">{movie_data.summary}</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                with st.expander("🔍 Raw structured data (JSON)"):
                    st.json(movie_data.model_dump())

            except Exception as e:
                st.error(f"Failed to extract movie info: {e}")