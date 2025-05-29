import streamlit as st
import os
from grading_pipeline import run_pipeline  # your main script should be named grading_pipeline.py
import tempfile
# import shutil

st.set_page_config(page_title="Answer Grader", layout="centered")

st.title("📄 Handwritten Answer Grading App")

st.markdown("Upload the **Answer Key PDF** and **Student Answer PDF** to automatically evaluate the similarity and calculate marks.")

# Upload PDFs
answer_key_pdf = st.file_uploader("Upload Answer Key PDF", type=["pdf"])
student_pdf = st.file_uploader("Upload Student Answer PDF", type=["pdf"])
total_marks = st.number_input("Total Marks", min_value=1, max_value=100, value=10)

if st.button("Grade Answers"):
    if answer_key_pdf and student_pdf:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Save uploaded files
            answer_key_path = os.path.join(tmpdirname, "answer_key.pdf")
            student_path = os.path.join(tmpdirname, "student.pdf")
            with open(answer_key_path, "wb") as f:
                f.write(answer_key_pdf.getvalue())
            with open(student_path, "wb") as f:
                f.write(student_pdf.getvalue())

            # Run grading pipeline
            total_score, question_results = run_pipeline(answer_key_path, student_path, total_marks)

            # Display total score
            st.success(f"✅ Grading complete! Total Marks: {total_score} / {total_marks}")

                      # Download report
            with open("grading_report.csv", "r", encoding="utf-8") as f:
                st.download_button("📥 Download CSV Report", f, file_name="grading_report.csv")

            # Optional: view full extracted texts
            with open("answer_key_extracted.txt", "r", encoding="utf-8") as f:
                st.expander("📘 Full Answer Key Extracted Text").write(f.read())

            with open("student_extracted.txt", "r", encoding="utf-8") as f:
                st.expander("📝 Full Student Answer Extracted Text").write(f.read())
    else:
        st.warning("⚠️ Please upload both PDFs before grading.")
