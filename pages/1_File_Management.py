import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
import fitz  # PyMuPDF for PDF reading
from streamlit.runtime.uploaded_file_manager import UploadedFile

# Folder to save uploaded files
UPLOAD_FOLDER = "uploads"

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Title and description
st.title("File Submission and Management")
st.write("Upload files and manage them in the `uploads` folder.")

# File uploader widget
uploaded_file: UploadedFile | None = st.file_uploader(
    "Choose a file", type=["csv", "txt", "pdf"]
)

if uploaded_file:
    # Display file details before saving
    file_details = {
        "Filename": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size (KB)": round(number=uploaded_file.size / 1024, ndigits=2),
    }
    st.write("File Details (Pending Save):", file_details)

    # Confirmation button to save the file
    if st.button("Confirm and Save File"):
        # Save file to the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(
            f"File `{uploaded_file.name}` has been saved to the `{UPLOAD_FOLDER}` folder."
        )
        time.sleep(2)
        st.rerun()  # Rerun the app to show updated file list

# Variable to store content of the file to be displayed on top
file_content_to_display = None
file_name_to_display = None

# Display all files in the uploads folder
uploaded_files: list[str] = os.listdir(path=UPLOAD_FOLDER)

# Check if there are any files in the folder
if uploaded_files:
    for file_name in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        file_size_kb = round(os.path.getsize(file_path) / 1024, 2)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Columns for buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        # View file button
        with col1:
            if st.button(f"View {file_name}", key=f"view_{file_name}"):
                file_name_to_display = file_name
                if file_name.endswith(".csv"):
                    df = pd.read_csv(file_path)
                    file_content_to_display = df  # Store dataframe to display
                elif file_name.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content_to_display = f.read()  # Store text content
                elif file_name.endswith(".pdf"):
                    with fitz.open(file_path) as pdf_document:
                        text = ""
                        for page_num in range(len(pdf_document)):
                            page = pdf_document.load_page(
                                page_num
                            )  # Load each page properly
                            text += page.get_text()
                    file_content_to_display = text  # Store PDF text content

        # Add to Knowledge Base button
        with col2:
            if st.button(
                f"Add to Knowledge Base {file_name}", key=f"add_kb_{file_name}"
            ):
                st.success(f"File `{file_name}` has been added to the knowledge base.")

        # Delete file button
        with col3:
            if st.button(f"Delete {file_name}", key=f"delete_{file_name}"):
                os.remove(file_path)
                st.warning(f"File `{file_name}` has been deleted.")
                st.rerun()  # Rerun the app to refresh the file list

    # Display selected file content at the top
    if file_content_to_display is not None:
        st.write(f"### Content of `{file_name_to_display}`")
        if isinstance(file_content_to_display, pd.DataFrame):
            st.dataframe(file_content_to_display)  # Display as DataFrame
        else:
            st.text_area(
                "File Content", file_content_to_display, height=300
            )  # Display text content

# Show message if no files found in the folder
else:
    st.write("No files found in the `uploads` folder.")
