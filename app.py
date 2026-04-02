import os
import streamlit as st
from crew import run_repo_doc_crew

st.set_page_config(page_title="CrewAI Repo Doc Generator", layout="centered")

st.title("CrewAI Repo Documentation Generator")
st.write("Enter a public GitHub repository URL and generate markdown documentation.")

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/user/repo"
)

file_name = st.text_input(
    "Output Markdown File Name",
    # value="generated_doc.md",
    placeholder="Example : weatherApp.md"
)

run_clicked = st.button("Generate Documentation", type="primary")

if run_clicked:
    if not repo_url.strip():
        st.error("Please enter a GitHub repository URL.")
    elif not file_name.strip().endswith(".md"):
        st.error("File name must end with .md")
    else:
        try:
            with st.spinner("Running CrewAI agents and generating documentation..."):
                result = run_repo_doc_crew(repo_url=repo_url.strip(), file_name=file_name.strip())

            st.success("Documentation generated successfully.")

            generated_text = None

            if os.path.exists(file_name.strip()):
                with open(file_name.strip(), "r", encoding="utf-8") as f:
                    generated_text = f.read()
            else:
                generated_text = str(result)

            st.subheader("Preview")
            st.markdown(generated_text)

            st.subheader("Raw Markdown")
            st.code(generated_text, language="markdown")

            st.download_button(
                label="Download Markdown File",
                data=generated_text,
                file_name=file_name.strip(),
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Run failed: {e}")