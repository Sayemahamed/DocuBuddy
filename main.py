"""This is the main script for the DocuBuddy app."""

import os
import textwrap

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def main() -> None:
    st.title("DocuBuddy")
    with st.sidebar:
        st.title("Submit your Documents")
        with st.form(key="document_form"):
            document: UploadedFile | None = st.file_uploader(
                "Upload your document", type="csv"
            )
            st.form_submit_button(label="Submit")
            if document is not None:
                # Define the directory where you want to save the file
                directory = "./directory"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Save the uploaded file to the directory
                file_path = os.path.join(directory, document.name)
                with open(file_path, "wb") as file:
                    file.write(document.getvalue())

                st.success(f"File saved to {file_path}")
            else:
                st.info("No file uploaded")

    st.subheader("Answer:")
    st.text(textwrap.fill("Hello, World!", width=85))


if __name__ == "__main__":
    main()
