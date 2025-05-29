import string
import csv
from fuzzywuzzy import fuzz
from pdf_to_images import render_pdf_pages_to_images
from ocr_utils import extract_text_from_images
import os

# Preprocess text: convert to lowercase, remove whitespace and punctuation
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = text.replace(" ", "").replace("\n", "")  # Remove all whitespaces and newlines
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text

# Save extracted texts into a text file (for reference or debugging)
def save_texts_to_file(texts, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for img_name, text in texts:
            f.write(f"--- {img_name} ---\n{text}\n\n")  # Include image name header

# Main grading function: computes similarity and marks per question
def grade_answers(answer_key_folder, student_folder, total_marks=10):
    # Extract OCR text from answer key and student images
    answer_key_texts = extract_text_from_images(answer_key_folder)
    student_texts = extract_text_from_images(student_folder)

    # Save the raw OCR outputs for transparency
    save_texts_to_file(answer_key_texts, "answer_key_extracted.txt")
    save_texts_to_file(student_texts, "student_extracted.txt")

    # Determine how many questions to compare (min of both)
    n = min(len(answer_key_texts), len(student_texts))
    marks_per_question = total_marks / n  # Distribute total marks evenly
    total_score = 0  # Initialize total score

    # Prepare CSV output headers
    csv_rows = [["Question", "Image", "Answer Key Text", "Student Answer Text", "Similarity (%)", "Marks Awarded"]]
    question_scores = []  # Store detailed per-question scores

    # Iterate over questions and compute similarity
    for i in range(n):
        key_name, key_text = answer_key_texts[i]
        stud_name, stud_text = student_texts[i]
        key_clean = preprocess_text(key_text)  # Clean answer key text
        stud_clean = preprocess_text(stud_text)  # Clean student text
        similarity_score = fuzz.partial_ratio(key_clean, stud_clean)  # Fuzzy match score
        marks_awarded = round((similarity_score / 100) * marks_per_question, 2)  # Compute marks
        total_score += marks_awarded  # Add to total

        # Append to CSV rows
        csv_rows.append([
            i + 1, key_name,
            key_text.replace("\n", " "),
            stud_text.replace("\n", " "),
            f"{similarity_score}%", marks_awarded
        ])

        # Store detailed score in dictionary
        question_scores.append({
            "question": i + 1,
            "image": key_name,
            "answer_key": key_text,
            "student_answer": stud_text,
            "similarity": similarity_score,
            "marks_awarded": marks_awarded
        })

    # Save the grading report as a CSV file
    with open("grading_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

    return round(total_score, 2), question_scores  # Return total score and details

# Main pipeline: handles PDF to image conversion and grading
def run_pipeline(answer_key_pdf, student_pdf, total_marks=10):
    render_pdf_pages_to_images(answer_key_pdf, "answer_key_images")  # Convert answer key PDF
    render_pdf_pages_to_images(student_pdf, "student_images")  # Convert student PDF
    return grade_answers("answer_key_images", "student_images", total_marks)  # Grade the answers

# Run pipeline locally for testing (not used in Streamlit UI)
if __name__ == "__main__":
    total, scores = run_pipeline("math_machine_task_2_1.pdf", "handwritten_answers.pdf", total_marks=10)
    print("Total:", total)
    print("Scores:", scores)
