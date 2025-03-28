import requests
import time
import csv
from bs4 import BeautifulSoup
import google.generativeai as genai


genai.configure(api_key="AIzaSyDjOfRC4Wh8YVrEvIDUzVLWYe1sJoK5Zos")
model = genai.GenerativeModel("gemini-2.0-flash")


def get_gemini_answers(text):

    text = text[:5000]  

    prompt = f'''Extract the following details from the text:
    {text} -  What is the company's mission statement or core values?
    - What products or services does the company offer?
    - When was the company founded, and who were the founders?
    - Where is the company's headquarters located?
    - Who are the key executives or leadership team members?
    - Has the company received any notable awards or recognitions?'''
    
    try:
        response = model.generate_content(prompt)  
        return response.text if response and hasattr(response, "text") else "No response from Gemini"
    except Exception as e:
        print(f"API error: {e}")
        return "API Error"


main_url="https://www.tcs.com/who-we-are"

header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"}

response=requests.get(main_url,headers=header)

soup=BeautifulSoup(response.text,"html.parser") 
page_text = soup.get_text(separator="\n", strip=True)


extracted_info = get_gemini_answers(page_text)

print(extracted_info)

