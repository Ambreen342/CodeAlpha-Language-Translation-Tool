import streamlit as st
import requests
from gtts import gTTS
import speech_recognition as sr
import streamlit.components.v1 as components
import io
import json


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍",
    layout="centered"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<div class="main-title">🌍 Language Translation Tool</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Translate text between multiple languages easily</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# LANGUAGES
# ==========================================

languages = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Turkish": "tr"
}


# ==========================================
# LANGUAGE SELECTION
# ==========================================

st.subheader("🌐 Select Languages")

col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "From",
        list(languages.keys())
    )

with col2:
    target_language = st.selectbox(
        "To",
        list(languages.keys()),
        index=1
    )


# ==========================================
# MICROPHONE INPUT
# ==========================================

# ==========================================
# MICROPHONE INPUT
# ==========================================

st.subheader("🎤 Speak Instead of Typing")

# Create microphone counter
if "mic_counter" not in st.session_state:
    st.session_state.mic_counter = 0

# Record Again button
if st.button("🎤 Record Again"):
    st.session_state.mic_counter += 1
    st.rerun()

# Microphone
audio_value = st.audio_input(
    "Click the microphone and speak",
    key=f"microphone_{st.session_state.mic_counter}"
)


# ==========================================
# TEXT INPUT
# ==========================================

st.subheader("✍️ Enter Your Text")

text = st.text_area(
    "Text",
    height=180,
    placeholder="Type your text here or use the microphone above..."
)


# ==========================================
# SPEECH TO TEXT
# ==========================================

if audio_value is not None:

    try:

        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_value) as source:
            audio_data = recognizer.record(source)

        source_code = languages[source_language]

        recognized_text = recognizer.recognize_google(
            audio_data,
            language=source_code
        )

        st.success("🎤 Speech recognized successfully!")

        text = recognized_text

        st.text_area(
            "Recognized Text",
            value=recognized_text,
            height=120
        )

    except sr.UnknownValueError:

        st.warning(
            "⚠️ Sorry, I could not understand the audio."
        )

    except Exception as e:

        st.error(
            "❌ Microphone speech recognition failed."
        )


# ==========================================
# TRANSLATE BUTTON
# ==========================================

if st.button(
    "🔄 Translate",
    use_container_width=True
):

    if not text.strip():

        st.warning(
            "⚠️ Please enter text or use the microphone first."
        )

    elif source_language == target_language:

        st.info(
            "ℹ️ Please select two different languages."
        )

    else:

        try:

            source_code = languages[source_language]
            target_code = languages[target_language]

            # Translate using MyMemory API
            url = "https://api.mymemory.translated.net/get"

            params = {
                "q": text,
                "langpair": f"{source_code}|{target_code}"
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            translated_text = data["responseData"]["translatedText"]

            # ==========================================
            # TRANSLATION RESULT
            # ==========================================

            st.subheader("✅ Translation Result")

            st.success(translated_text)


            # ==========================================
            # COPY BUTTON
            # ==========================================

            st.subheader("📋 Copy Translation")

            safe_text = json.dumps(translated_text)

            copy_html = f"""
            <div>
                <button
                    onclick='copyText()'
                    style="
                        padding: 10px 20px;
                        font-size: 16px;
                        cursor: pointer;
                        border-radius: 8px;
                        border: 1px solid #888;
                    "
                >
                    📋 Copy
                </button>

                <span id="message"
                    style="margin-left:10px;">
                </span>
            </div>

            <script>

            function copyText() {{

                const text = {safe_text};

                navigator.clipboard.writeText(text)
                    .then(function() {{

                        document.getElementById("message").innerText =
                            "✅ Copied!";

                    }})
                    .catch(function() {{

                        document.getElementById("message").innerText =
                            "❌ Copy failed";

                    }});
            }}

            </script>
            """

            components.html(
                copy_html,
                height=60
            )


            # ==========================================
            # TEXT TO SPEECH
            # ==========================================

            st.subheader("🔊 Listen to Translation")

            try:

                speech_code = languages[target_language]

                audio = io.BytesIO()

                tts = gTTS(
                    text=translated_text,
                    lang=speech_code
                )

                tts.write_to_fp(audio)

                st.audio(
                    audio.getvalue(),
                    format="audio/mp3"
                )

            except Exception:

                st.warning(
                    "🔊 Text-to-Speech is not available "
                    "for this language."
                )


        except Exception as e:

            st.error(
                "❌ Translation failed. "
                "Please check your internet connection."
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()
