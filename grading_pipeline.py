import string
import csv
from fuzzywuzzy import fuzz
from pdf_to_images import render_pdf_pages_to_images
from ocr_utils import extract_text_from_images
import os

# Step 1: Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = text.replace(" ", "").replace("\n", "")
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Step 2: Save text
def save_texts_to_file(texts, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for img_name, text in texts:
            f.write(f"--- {img_name} ---\n{text}\n\n")

# Step 3: Grading logic
def grade_answers(answer_key_folder, student_folder, total_marks=10):
    answer_key_texts = extract_text_from_images(answer_key_folder)
    student_texts = extract_text_from_images(student_folder)

    # Save extracted text for reference
    save_texts_to_file(answer_key_texts, "answer_key_extracted.txt")
    save_texts_to_file(student_texts, "student_extracted.txt")

    n = min(len(answer_key_texts), len(student_texts))
    marks_per_question = total_marks / n
    total_score = 0

    csv_rows = [["Question", "Image", "Answer Key Text", "Student Answer Text", "Similarity (%)", "Marks Awarded"]]
    question_scores = []

    for i in range(n):
        key_name, key_text = answer_key_texts[i]
        stud_name, stud_text = student_texts[i]

        key_clean = preprocess_text(key_text)
        stud_clean = preprocess_text(stud_text)

        similarity_score = fuzz.partial_ratio(key_clean, stud_clean)
        marks_awarded = round((similarity_score / 100) * marks_per_question, 2)
        total_score += marks_awarded

        csv_rows.append([
            i + 1, key_name,
            key_text.replace("\n", " "),
            stud_text.replace("\n", " "),
            f"{similarity_score}%", marks_awarded
        ])

        question_scores.append({
            "question": i + 1,
            "image": key_name,
            "answer_key": key_text,
            "student_answer": stud_text,
            "similarity": similarity_score,
            "marks_awarded": marks_awarded
        })

    with open("grading_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return round(total_score, 2), question_scores

# Step 4: Pipeline runner
def run_pipeline(answer_key_pdf, student_pdf, total_marks=10):
    render_pdf_pages_to_images(answer_key_pdf, "answer_key_images")
    render_pdf_pages_to_images(student_pdf, "student_images")
    return grade_answers("answer_key_images", "student_images", total_marks)

# Only for local test runs, not needed in Streamlit app
if __name__ == "__main__":
    total, scores = run_pipeline("math_machine_task_2_1.pdf", "handwritten_answers.pdf", total_marks=10)
    print("Total:", total)
    print("Scores:", scores)
