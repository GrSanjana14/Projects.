#Mood-Based Song & Quote Recommender 
import streamlit as st
import requests
import urllib3
import ssl

# Disable SSL warnings (temporary workaround)
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

MOOD_TO_QUOTE_TAG = {
    "Happy 😊": "happiness",
    "Sad 😢": "life",
    "Motivated 💪": "inspirational",
    "Anxious 😰": "life",
    "Relaxed 😌": "happiness",
    "Angry 😠": "wisdom"
}

MOOD_BACKGROUND = {
    "Happy 😊": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
    "Sad 😢": "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)",
    "Motivated 💪": "linear-gradient(135deg, #fbc7a4 0%, #fe6a6a 100%)",
    "Anxious 😰": "linear-gradient(135deg, #d7d2cc 0%, #304352 100%)",
    "Relaxed 😌": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
    "Angry 😠": "linear-gradient(135deg, #ff9966 0%, #ff5e62 100%)",
}

def fetch_quote(tag: str) -> dict:
    url = f"https://api.quotable.io/random?tags={tag}"
    try:
        r = requests.get(url, timeout=15, verify=False)
        if r.status_code != 200:
            raise ValueError(f"Quotable API error {r.status_code}: {r.text}")
        data = r.json()
        return {
            "quote": data.get("content", ""),
            "author": data.get("author", "")
        }
    except Exception as e:
        raise RuntimeError(f"Could not fetch a quote: {e}")

def fetch_song(mood: str) -> dict:
    params = {
        "term": mood,
        "entity": "song",
        "limit": 1
    }
    try:
        r = requests.get("https://itunes.apple.com/search", params=params, timeout=15)
        if r.status_code != 200:
            raise ValueError(f"iTunes API error {r.status_code}: {r.text}")
        results = r.json().get("results", [])
        if not results:
            raise ValueError("No song found for that mood.")
        track = results[0]
        return {
            "trackName": track.get("trackName", ""),
            "artistName": track.get("artistName", ""),
            "trackViewUrl": track.get("trackViewUrl", ""),
            "previewUrl": track.get("previewUrl", ""),
        }
    except Exception as e:
        raise RuntimeError(f"Could not fetch a song: {e}")

st.title("🎵 Mood-Based Song & Quote Recommender")

st.markdown("""
<div class="main centered">
    <p>Select your mood and get:</p>
    <ol>
        <li>A quote that matches your mood 🎯</li>
        <li>A song suggestion that resonates 🎶</li>
    </ol>
</div>
""", unsafe_allow_html=True)

mood_options = list(MOOD_TO_QUOTE_TAG.keys())
selected = st.selectbox("Select your mood:", [""] + mood_options)
custom = st.text_input("Or type your mood:")

if selected:
    mood_text = selected.split()[0]
    quote_tag = MOOD_TO_QUOTE_TAG[selected]
    bg_gradient = MOOD_BACKGROUND.get(selected, "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)")
elif custom.strip():
    mood_text = custom.strip()
    quote_tag = "inspirational"
    bg_gradient = "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)"
else:
    mood_text = ""
    quote_tag = ""
    bg_gradient = "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)"

st.markdown(f"""
    <style>
    body, .stApp {{
        background: {bg_gradient};
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
        transition: background 0.5s ease;
    }}
    .main {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }}
    .centered {{
        text-align: center;
    }}

    /* Style the Get Recommendations button */
    div.stButton > button:first-child {{
        background: linear-gradient(90deg, #f2709c, #ff9472);
        color: white;
        font-weight: 600;
        padding: 0.6em 1.5em;
        border-radius: 12px;
        border: none;
        box-shadow: 0 5px 15px rgba(255, 148, 114, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
        margin-top: 20px;
    }}
    div.stButton > button:first-child:hover {{
        background: linear-gradient(90deg, #ff9472, #f2709c);
        box-shadow: 0 8px 20px rgba(255, 148, 114, 0.7);
        transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)

if st.button("🎧 Get Recommendations"):
    if not mood_text:
        st.warning("Please select or enter a mood.")
    else:
        with st.container():
            try:
                with st.spinner("Fetching quote..."):
                    q = fetch_quote(quote_tag)
                    st.markdown(f"""
                    <div class="main">
                        <h4>📜 Quote:</h4>
                        <blockquote>{q['quote']}</blockquote>
                        <p><em>— {q['author']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))

            try:
                with st.spinner("Fetching song..."):
                    s = fetch_song(mood_text)
                    st.markdown(f"""
                    <div class="main">
                        <h4>🎶 Song Recommendation:</h4>
                        <strong>{s['trackName']}</strong> by <em>{s['artistName']}</em><br>
                        <a href="{s['trackViewUrl']}" target="_blank">🎧 Listen on iTunes</a>
                    </div>
                    """, unsafe_allow_html=True)
                    if s.get("previewUrl"):
                        st.audio(s["previewUrl"])
            except Exception as e:
                st.error(str(e))
