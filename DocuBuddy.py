"""This is the main app for DocuBuddy."""

import os
import streamlit as st
from RAG import Augmented_model


def main() -> None:
    """
    Main function or entry point for the DocuBuddy app.
    """
    with st.sidebar:
        st.markdown(body="[View the source code](https://github.com/Sayemahamed/DocuBuddy)")
        st.markdown(
            body="[Internal Architecture](https://raw.githubusercontent.com/Sayemahamed/DocuBuddy/refs/heads/main/System_Diagram.png)"
        )
    # Main section for responses and document processing feedback
    st.title(body="📄 DocuBuddy")
    st.caption(
        body="Your friendly assistant for instant answers, summaries, and insights from any document!"
    )
    # Display any saved document responses
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": f"Hello, {os.getlogin()}! I hope you're having a great day! Got any tasty document data for me to munch on?",
            }
        ]
    for msg in st.session_state.messages:
        st.chat_message(name=msg["role"]).write(msg["content"])
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message(name="user").write(prompt)
        answer: str = Augmented_model.ask(query=prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message(name="assistant").write(answer)


if __name__ == "__main__":
    main()
