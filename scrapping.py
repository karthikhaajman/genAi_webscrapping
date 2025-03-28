from selenium import webdriver
from selenium.webdriver.common.by import By
import time


company_urls = [
    "https://www.panasonic.com",
     "https://www.gsk.com",
     "https://www.tcs.com",
      "https://www.ford.com",
     "https://www.nespresso.com",
     "https://www.siemens-energy.com",
     "https://www.lenovo.com",
     "https://www.americanexpress.com"
]


driver = webdriver.Edge() 


def extract_links():
    navbar_links = driver.find_elements(By.CSS_SELECTOR, "nav a")
    footer_links = driver.find_elements(By.CSS_SELECTOR, "footer a")

    all_links = set(link.get_attribute("href") for link in (navbar_links + footer_links) if link.get_attribute("href"))
    
    return all_links


def extract_page_data(url):
    driver.get(url)
    time.sleep(2)
    
    try:
        page_data = driver.find_element(By.TAG_NAME, "body").text  
    except:
        page_data = "Could not extract data."
    
    return f"Page: {url}\nContent:\n{page_data}\n\n" + "="*80 + "\n"


for company_url in company_urls:
    driver.get(company_url)
    time.sleep(3) 
    all_urls = extract_links()

   
    domain_name = company_url.split("//")[-1].split(".")[1] if "www." in company_url else company_url.split("//")[-1].split(".")[0]
    output_file = f"{domain_name}.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        for url in all_urls:
            page_content = extract_page_data(url)
            file.write(page_content + "\n")

driver.quit()

print("Scraping complete, Data saved!")
