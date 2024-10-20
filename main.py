"""This is the main script for the DocuBuddy app."""

import textwrap
from langchain_ollama.llms import OllamaLLM

import streamlit as st


def main() -> None:
    llm = OllamaLLM(model="phi3.5")

    st.title("DocuBuddy")
    with st.sidebar:
        st.title("DocuBuddy")
        with st.form(key="my_form"):
            query: str = st.sidebar.text_area(
                label="Ask me about the video?", max_chars=50, key="query"
            )
            submit_button = st.form_submit_button(label="Submit")
    if query != "" and query is not None:
        answer: str = llm.invoke(query)
        st.subheader("Answer:")
        st.text(textwrap.fill(answer, width=85))


if __name__ == "__main__":
    main()
