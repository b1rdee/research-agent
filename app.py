import streamlit as st
from crew import run_researcher

st.set_page_config(page_title="AI Research Agent", layout="wide")
st.title("🔍 AI Research Agent")
st.markdown("Get a well-researched summary on any topic.")

topic = st.text_input("Enter a topic to research", placeholder="e.g., renewable energy breakthroughs 2025")

if st.button("Run Research", type="primary"):
    if topic:
        with st.spinner("Researching... this may take a moment."):
            try:
                result = run_researcher(topic)
                st.markdown("### 📄 Summary")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a topic.")