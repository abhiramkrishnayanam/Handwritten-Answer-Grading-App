import streamlit as st
import os
from grading_pipeline import run_pipeline  # Import main grading pipeline
import tempfile  # For temporary file storage during upload

# Set Streamlit page title and layout
st.set_page_config(page_title="Answer Grader", layout="centered")

# App title and description
st.title("📄 Handwritten Answer Grading App")
st.markdown("Upload the **Answer Key PDF** and **Student Answer PDF** to automatically evaluate the similarity and calculate marks.")

# File uploaders for answer key and student PDF
answer_key_pdf = st.file_uploader("Upload Answer Key PDF", type=["pdf"])
student_pdf = st.file_uploader("Upload Student Answer PDF", type=["pdf"])

# Input total marks (defaults to 10)
total_marks = st.number_input("Total Marks", min_value=1, max_value=100, value=10)

# When the Grade Answers button is clicked
if st.button("Grade Answers"):
    if answer_key_pdf and student_pdf:
        # Create a temporary directory to store uploaded PDFs
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Define paths to temporarily store uploaded PDFs
            answer_key_path = os.path.join(tmpdirname, "answer_key.pdf")
            student_path = os.path.join(tmpdirname, "student.pdf")

            # Write the uploaded answer key PDF to file
            with open(answer_key_path, "wb") as f:
                f.write(answer_key_pdf.getvalue())

            # Write the uploaded student answer PDF to file
            with open(student_path, "wb") as f:
                f.write(student_pdf.getvalue())

            # Run the grading logic using the pipeline
            total_score, question_results = run_pipeline(answer_key_path, student_path, total_marks)

            # Display total score achieved
            st.success(f"✅ Grading complete! Total Marks: {total_score} / {total_marks}")

            # Offer download button for CSV grading report
            with open("grading_report.csv", "r", encoding="utf-8") as f:
                st.download_button("📥 Download CSV Report", f, file_name="grading_report.csv")

            # Show the full extracted answer key text (optional)
            with open("answer_key_extracted.txt", "r", encoding="utf-8") as f:
                st.expander("📘 Full Answer Key Extracted Text").write(f.read())

            # Show the full extracted student text (optional)
            with open("student_extracted.txt", "r", encoding="utf-8") as f:
                st.expander("📝 Full Student Answer Extracted Text").write(f.read())
    else:
        # If one or both files are missing, show a warning
        st.warning("⚠️ Please upload both PDFs before grading.")
