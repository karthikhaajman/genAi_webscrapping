import google.generativeai as genai
import os
import csv
import time


genai.configure(api_key="AIzaSyBO6WTqGmD49a1DtPZPgY7DWncYI79RKH0")  
model = genai.GenerativeModel("gemini-2.0-flash")

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def ask_llm(content, questions):
    answers = {}
    for question in questions:
        prompt = f""" Given the following company information:
        {content}
        Answer the question concisely:
        {question} 
        if you can't find the answers check if there exist any keywords like vision of the company for identifying the company's mission or core values
        for company's headquarters located look for something like location"""
       
        time.sleep(10)
        try:
            response = model.generate_content(prompt)

            if response and response.candidates:
                answers[question] = response.text.strip() if response.text else "No valid response."
            else:
                answers[question] = "Response blocked or no valid output."

        except Exception as e:
            answers[question] = f"Unexpected error: {e}"

    return answers

def main():
    questions = [
        "What is the company's mission statement or core values?",
        "What products or services does the company offer?",
        "When was the company founded, and who were the founders?",
        "Where is the company's headquarters located?",
        "Who are the key executives or leadership team members?",
        "Has the company received any notable awards or recognitions?"
    ]
    files = [f for f in os.listdir() if f.endswith(".txt")]

    if not files:
        print("Error: No text files found.")
        return

    csv_file = "company_data.csv"
    
    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        header = ["Website"] + questions
        writer.writerow(header)

        for file_name in files:
            content = read_text_file(file_name)

            if not content:
                continue

            answers = ask_llm(content, questions)
            row = [file_name.replace(".txt", "")] + [answers[q] for q in questions]

            writer.writerow(row)

    print("Data saved")

if __name__ == "__main__":
    main()
