import os
import textwrap
import streamlit as st


def main() -> None:
    # Sidebar for file upload and knowledge base management
    with st.sidebar:
        # File Upload Section
        st.header("📁 File Upload")
        st.write("Upload your document for processing (CSV, TXT, PDF).")

        with st.form(key="document_form"):
            # Allowing multiple file types
            document = st.file_uploader("Choose a document", type=["csv", "txt", "pdf"])
            submit_button = st.form_submit_button(label="Upload Document")

            if submit_button and document is not None:
                # Directory setup and file saving
                directory = "./uploads"
                os.makedirs(directory, exist_ok=True)

                # Save the uploaded file
                file_path = os.path.join(directory, document.name)
                with open(file_path, "wb") as file:
                    file.write(document.getvalue())

                st.success(f"✅ File successfully saved to: {file_path}")
            elif submit_button:
                st.warning("⚠️ Please upload a file to proceed.")

            # Knowledge Base Section
        st.header("📚 Knowledge Base")
        st.write("Load custom text data into the knowledge base.")

        # Text input for loading knowledge base
        knowledge_text = st.text_area("Enter text to load into the knowledge base:")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Load Knowledge Base"):
                if knowledge_text:
                    # Save to knowledge base in session state
                    if "knowledge_base" not in st.session_state:
                        st.session_state["knowledge_base"] = []
                    st.session_state["knowledge_base"].append(knowledge_text)
                    st.success("Knowledge base loaded successfully.")
                else:
                    st.warning(
                        "⚠️ Please enter some text to load into the knowledge base."
                    )

        with col2:
            if st.button("Save Knowledge Base"):
                if (
                    "knowledge_base" in st.session_state
                    and st.session_state["knowledge_base"]
                ):
                    # Save the knowledge base to a text file
                    kb_directory = "./knowledge_base"
                    os.makedirs(kb_directory, exist_ok=True)
                    kb_file_path = os.path.join(kb_directory, "knowledge_base.txt")
                    with open(kb_file_path, "w") as kb_file:
                        for entry in st.session_state["knowledge_base"]:
                            kb_file.write(entry + "\n---\n")
                    st.success(f"Knowledge base saved successfully to {kb_file_path}")
                else:
                    st.warning(
                        "⚠️ The knowledge base is empty. Please load some text first."
                    )

        # View Knowledge Base and display entries as buttons
        if st.button("View Knowledge Base"):
            if (
                "knowledge_base" in st.session_state
                and st.session_state["knowledge_base"]
            ):
                st.write("### Knowledge Base Entries:")
                for idx, entry in enumerate(
                    st.session_state["knowledge_base"], start=1
                ):
                    if st.button(f"Entry {idx}"):
                        st.info(entry)  # Display selected entry content
            else:
                st.warning(
                    "⚠️ The knowledge base is empty. Please load some text first."
                )

        # Additional links and resources
        "[View the source code](https://github.com/Sayemahamed/DocuBuddy)"

    # Main section for responses and document processing feedback
    st.title(body="📄 DocuBuddy: Your go-to assistant")
    st.caption(
        body="Your friendly assistant for instant answers, summaries, and insights from any document!"
    )

    # Display any saved document responses
    if "response_text" not in st.session_state:
        st.session_state["response_text"] = (
            f"Hello, {os.getlogin()}! I hope you're having a great day! Got any tasty document data for me to feast on?"
        )

    st.subheader("Answer:")
    st.text(textwrap.fill(st.session_state["response_text"], width=85))

    # Example interactive input for a query
    if user_query := st.text_input("Ask a question about your document:"):
        if document:
            # Placeholder logic for processing the query
            st.session_state["response_text"] = (
                f"Processing your question: '{user_query}'"
            )
            st.text(textwrap.fill(st.session_state["response_text"], width=85))
        else:
            st.warning("⚠️ Please upload a document to answer questions.")


if __name__ == "__main__":
    main()
