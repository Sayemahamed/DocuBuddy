import streamlit as st



with st.form("my_form"):
    text = st.text_area(
        "Enter text:", "What are 3 key advice for learning how to code?"
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)
