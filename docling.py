import streamlit as st
import os

from pathlib import Path

from docling.backend.docling_parse_backend import DoclingParseDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    OcrMacOptions,
    PdfPipelineOptions,
    RapidOcrOptions,
    TesseractCliOcrOptions,
    TesseractOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

def main():
   def main():
    st.title("File Selection App")

    # Initialize session state for storing the concatenated path
    if 'full_file_path' not in st.session_state:
        st.session_state.full_file_path = None

    # Add description
    st.write("Select a file from your computer to view its path information")

    # File uploader with type filtering
    allowed_types = ["pdf", "doc", "docx", "ppt", "pptx", "jpg", "jpeg"]
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=allowed_types,
        help="Supported files: PDF, Word, PowerPoint, and JPEG"
    )

    # Display file details if a file is uploaded
    if uploaded_file is not None:
        # Get the current working directory
        current_dir = os.getcwd()

        # Create full path (this will be where Streamlit temporarily stores the file)
        full_path = os.path.join(current_dir, uploaded_file.name)

        # Store the concatenated path in session state
        st.session_state.full_file_path = full_path

        file_details = {
            "Filename": uploaded_file.name,
            "Full Path": full_path,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type,
            "Concatenated Path Variable": st.session_state.full_file_path
        }

        st.write("### File Details:")
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")

        # Example of using the concatenated path in the app
        st.write("### Using the Concatenated Path")
        st.code(f"""
        # You can access the full file path anywhere in your app using:
        full_file_path = st.session_state.full_file_path

        # Example usage:
        if st.session_state.full_file_path:
            # Do something with the path
            print(f'Working with file: {st.session_state.full_file_path}')
        """)

        # Add a button to demonstrate using the path
        if st.button("Print Path to Console"):
            st.write(f"Path has been printed to console: {st.session_state.full_file_path}")
            print(f"Full file path: {st.session_state.full_file_path}")

        # Add a note about the path
        st.info("Note: The full path shown is where Streamlit temporarily stores the uploaded file. " 
                "To get the original file path, you would need to use a different approach as browsers "
                "don't provide the original file path for security reasons.")

    ######        
    ##
    input_doc = st.session_state.full_file_path
    ##

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True

    # Any of the OCR options can be used:EasyOcrOptions, TesseractOcrOptions, TesseractCliOcrOptions, OcrMacOptions(Mac only), RapidOcrOptions
    # ocr_options = EasyOcrOptions(force_full_page_ocr=True)
    # ocr_options = TesseractOcrOptions(force_full_page_ocr=True)
    # ocr_options = OcrMacOptions(force_full_page_ocr=True)
    # ocr_options = RapidOcrOptions(force_full_page_ocr=True)
    ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True)
    pipeline_options.ocr_options = ocr_options

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )

    doc = converter.convert(input_doc).document
    md = doc.export_to_markdown()
    print(md)

if __name__ == "__main__":
    main()