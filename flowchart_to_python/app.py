import streamlit as st
from parse_drawio import parse_drawio_xml
from query_deepseek import query_deepseek
from drawio_to_code import generate_prompt_from_blocks
import tempfile
import urllib.parse
import io
import contextlib

# Replace with your actual DeepSeek API key before running
API_KEY = "your-api-key"
st.set_page_config(page_title="Flowchart to Python", layout="centered")

#custom markdown
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600&display=swap');
            
    html, body, [class*="css"] { font-family: 'Rubik', sans-serif; background-color: #0f0f0f; color: #f5f5f5; }
            
    h1, h2, h3, h4 { color: #FFA500; font-weight: 600; }
            
    .stButton>button { background-color: #FFA500; color: black; border-radius: 5px; font-weight: bold; transition: background-color 0.3s ease-in-out; }
            
    .stButton>button:hover { background-color: #FF8C00; }
            
    .stDownloadButton>button { background-color: #FF4500; color: white; border-radius: 5px; font-weight: bold; }
            
    .stDownloadButton>button:hover { background-color: #ff6533; }
            
    .stTextArea textarea { background-color: #222222; color: #ffffff; border-radius: 5px; }
            
    .block-container { padding: 2rem 2rem 4rem; border-radius: 10px; }
            
    .stRadio > div { background-color: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #FFA500; margin-bottom: 10px; }
            
    .logo-glow { filter: drop-shadow(0 0 6px #FFA500); transition: filter 0.3s ease-in-out; }
            
    .logo-glow:hover { filter: drop-shadow(0 0 15px #FF8C00); }
            
    div[data-testid="stSpinner"] { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; padding: 1rem 0; color: #FFA500; }
            
    div[data-testid="stSpinner"] svg { animation: spin 1s linear infinite; }
            
    @keyframes spin { to { transform: rotate(360deg); } }
            
    </style>
""", unsafe_allow_html=True)


#logo and title
st.sidebar.image(r"flowchart_to_python\logoImage.png", use_container_width=True, clamp=True)
st.markdown("""<h1 style='text-align: center; color: #FFA500;' class='logo-glow'>Flowchart Logic Toolkit</h1>""", unsafe_allow_html=True)

#sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Flowchart to Code", "Explain Flowchart", "Explain Code", "Run Python Code"])

#pages
if page == "Flowchart to Code":
    st.header("Flowchart to Code")

elif page == "Explain Flowchart":
    st.header("Explain Flowchart")

elif page == "Explain Code":
    st.header("Explain Code")

elif page == "Run Python Code":
    st.header("Run Python Code")


def encode_drawio_for_viewer(xml_bytes):
    xml_str = xml_bytes.decode('utf-8')
    return urllib.parse.quote(xml_str)

#open button for draw io
if page in ["Flowchart to Code", "Explain Flowchart"]:
    st.subheader("Build Your Flowchart")
    if st.button("Open Draw.io Editor in New Tab"):
        js = """
        <script>
            window.open("https://app.diagrams.net/?ui=min", "_blank");
        </script>
        """
        st.components.v1.html(js)

    st.markdown("""
    <div style='background-color:#1a1a1a;padding:10px;border-radius:8px;'>
    <strong style='color:#FFA500;'>Instructions:</strong><br>
    1. Build your flowchart using blocks (Start, Process, Decision, End)<br>
    2. Go to <strong>File → Export as → .drawio</strong><br>
    3. Save the file<br>
    4. Upload it below
    </div>
    """, unsafe_allow_html=True)

    flowchart_key = "code_upload" if page == "Flowchart to Code" else "explain_upload"
    uploaded_file = st.file_uploader("Upload your exported .drawio file", type=["drawio", "xml"], key=flowchart_key)

    xml_content = None

    if uploaded_file:
        xml_content = uploaded_file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".drawio") as tmp:
            tmp.write(xml_content)
            tmp_path = tmp.name

        try:
            blocks = parse_drawio_xml(tmp_path)
            st.success("Flowchart parsed successfully!")
            with st.expander("View Parsed Blocks"):
                for block in blocks:
                    st.json(block)

        except Exception as e:
            st.error(f"Error parsing file: {e}")
            st.stop()

        st.markdown("### Flowchart Preview")
        encoded_xml = encode_drawio_for_viewer(xml_content)

        viewer_url = f"https://viewer.diagrams.net/#R{encoded_xml}"

        st.components.v1.iframe(viewer_url, height=600, scrolling=True)

        if page == "Flowchart to Code": #flowcahrt convert code and prompt

            if st.button("Generate Python Code"):
                prompt = (
                    "You are a Python code generator that takes simplified flowchart-like \"blocked code\" as input. "
                    "The input consists of steps labeled, with arrows indicating flow. Convert this into equivalent, clean Python code that preserves the logic. "
                    "Do not explain anything—just return the raw code. Here is the input:\n" + generate_prompt_from_blocks(blocks) +
                    "\nOutput only the raw Python code with no formatting or extra text or emojis. Do not use triple backticks or markdown formatting."
                )

                with st.spinner("Generating Python code..."):

                    try:
                        code = query_deepseek(prompt, api_key=API_KEY)
                        st.success("Python Code Generated!")
                        st.code(code, language="python")
                        st.download_button("Download Code", code, file_name="generated_code.py")
                    except Exception as e:
                        st.error(f"AI query failed: {e}")

        elif page == "Explain Flowchart": #explain page and prompt and code

            if st.button("Explain Flowchart in English"):
                prompt = (
                    "You are a helpful assistant that analyzes a visual flowchart and explains its logic in plain, easy-to-understand English. "
                    "Do not output any code. Focus only on describing what the program does, step-by-step. "
                    "At the end of your explanation, give a 1-sentence rating from 1 to 10 on how logically sound or clear the flowchart is, but be positive on the rating. "
                    "Here is the input:\n" + generate_prompt_from_blocks(blocks)
                )

                with st.spinner("Generating flowchart explanation..."):
                    try:
                        explanation = query_deepseek(prompt, api_key=API_KEY)
                        st.success("Flowchart Explained")
                        st.markdown(explanation)

                    except Exception as e:
                        st.error(f"Failed to generate explanation: {e}")

elif page == "Explain Code": # explain code page

    st.subheader("Paste your Python code below to explain it.")
    user_code = st.text_area("Enter your Python code:", height=250)

    if user_code.strip():

        if st.button("Explain My Code"):
            prompt = (
                "You are a helpful assistant who explains Python code step-by-step in plain English. "
                "Avoid restating the code directly—focus on what each part does and what the full program is meant to achieve.\n"
                "At the end of your explanation, give a 1-sentence rating from 1 to 10 on how logically sound or clear the code is, but be positive on the rating.\n"
                "Here is the input code:\n" + user_code
            )

            with st.spinner("Analyzing your code..."):
                try:
                    explanation = query_deepseek(prompt, api_key=API_KEY)
                    st.success("Code Explanation")
                    st.markdown(explanation)

                except Exception as e:
                    st.error(f"Failed to explain code: {e}")


elif page == "Run Python Code":

    st.markdown("""
    <h3 style="color:#FFA500;">Run your code in the embeded Python editor (Trinket):</h3>
    <iframe src="https://trinket.io/embed/python3" 
            style="width:100%; height:400px; border:1px solid #FFA500; border-radius: 8px;" 
            allowfullscreen>
    </iframe>
    """, unsafe_allow_html=True)

