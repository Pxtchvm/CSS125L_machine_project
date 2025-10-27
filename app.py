"""
SRT Subtitle Interpreter - Streamlit Web Interface
A web app for parsing, validating, and translating SRT subtitle files
"""

import streamlit as st
import tempfile
import os
from src.interpreter import SRTInterpreter
from src.lexer import LexerError
from src.parser import ParserError
from src.executor import ExecutorError
import io
import sys


def main():
    # Page configuration
    st.set_page_config(
        page_title="SRT Subtitle Interpreter",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Title and description
    st.title("🎬 SRT Subtitle Interpreter")
    st.markdown("**By Group 1 - Shakra** | Parse, validate, and translate SubRip (.srt) subtitle files")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Language selection
        language = st.selectbox(
            "Select Translation Language",
            options=["english", "filipino", "korean", "chinese", "japanese"],
            index=0,
            help="Choose the language to translate subtitles into"
        )

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This interpreter follows a 3-stage pipeline:
        1. **Lexer** - Tokenizes the file
        2. **Parser** - Validates structure
        3. **Executor** - Displays subtitles with optional translation
        """)

        st.markdown("---")
        st.markdown("### Supported Languages")
        st.markdown("""
        - 🇬🇧 English (Original)
        - 🇵🇭 Filipino/Tagalog
        - 🇰🇷 Korean
        - 🇨🇳 Chinese (Simplified)
        - 🇯🇵 Japanese
        """)

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📁 Upload SRT File")
        uploaded_file = st.file_uploader(
            "Choose a .srt subtitle file",
            type=["srt"],
            help="Upload a SubRip Text (.srt) subtitle file"
        )

        # Example files section
        with st.expander("📋 Don't have an SRT file? Use our examples"):
            st.markdown("""
            You can try these example files from the `examples/` directory:
            - `valid_basic.srt` - Simple 2-subtitle example
            - `valid_multiline.srt` - Multiline subtitle example
            - `valid_complex.srt` - Complex example with formatting
            """)

            # Option to load example file
            example_choice = st.selectbox(
                "Load an example file:",
                ["None", "examples/valid_basic.srt", "examples/valid_multiline.srt", "examples/valid_complex.srt"]
            )

            if example_choice != "None" and st.button("Load Example"):
                try:
                    with open(example_choice, 'r', encoding='utf-8') as f:
                        st.session_state['example_content'] = f.read()
                        st.session_state['example_name'] = os.path.basename(example_choice)
                    st.success(f"Loaded {example_choice}")
                except Exception as e:
                    st.error(f"Error loading example: {e}")

    with col2:
        st.header("📊 File Info")
        if uploaded_file is not None:
            st.info(f"**Filename:** {uploaded_file.name}")
            st.info(f"**Size:** {uploaded_file.size} bytes")
        elif 'example_content' in st.session_state:
            st.info(f"**Filename:** {st.session_state['example_name']}")
            st.info(f"**Size:** {len(st.session_state['example_content'])} bytes")
        else:
            st.warning("No file uploaded yet")

    st.markdown("---")

    # Process button
    if st.button("🚀 Process Subtitles", type="primary", use_container_width=True):
        file_content = None
        filename = None

        # Get file content from upload or example
        if uploaded_file is not None:
            file_content = uploaded_file.getvalue().decode('utf-8')
            filename = uploaded_file.name
        elif 'example_content' in st.session_state:
            file_content = st.session_state['example_content']
            filename = st.session_state['example_name']
        else:
            st.error("❌ Please upload a file or load an example first!")
            return

        # Process the file
        if file_content:
            with st.spinner(f"Processing subtitles{' and translating to ' + language if language != 'english' else ''}..."):
                try:
                    # Create a temporary file
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8') as tmp_file:
                        tmp_file.write(file_content)
                        tmp_filename = tmp_file.name

                    # Capture output
                    old_stdout = sys.stdout
                    sys.stdout = captured_output = io.StringIO()

                    try:
                        # Run the interpreter
                        interpreter = SRTInterpreter()
                        interpreter.run(tmp_filename, language)

                        # Get the output
                        output = captured_output.getvalue()

                    finally:
                        sys.stdout = old_stdout
                        # Clean up temp file
                        os.unlink(tmp_filename)

                    # Display success
                    st.success(f"✅ Successfully processed {filename}!")

                    # Display results
                    st.header("📺 Subtitle Output")

                    if language != 'english':
                        st.info(f"Translated to: **{language.title()}**")

                    # Display output in a nice box
                    st.code(output, language=None)

                    # Download button for the output
                    st.download_button(
                        label="💾 Download Output",
                        data=output,
                        file_name=f"output_{language}_{filename}",
                        mime="text/plain"
                    )

                except (LexerError, ParserError, ExecutorError) as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.markdown("**Error Details:**")
                    st.code(str(e), language=None)

                except FileNotFoundError:
                    st.error(f"❌ File not found: {filename}")

                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                    st.exception(e)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p><strong>SRT Subtitle Interpreter</strong> | CSS125L Machine Project</p>
        <p>Group 1 - Shakra: Bagallon, Castro, Duldulao, Gigante</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
