from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import csv
import os
import time
import telebot
import traceback
import subprocess


# command = "pip install -r _req.txt"
# try:
#     # subprocess.check_call(command, shell=True)
#     print("Requirements installed successfully.")
# except subprocess.CalledProcessError:
#     print("Error installing requirements.")



API_KEY = "5991202973:AAG8u83Knyd2fDz8x7jJ99UuNa0fKihZWOY"
bot = telebot.TeleBot(API_KEY, parse_mode=None)
err = ""

wait_time = 4


def time_sleep(t):
    for i in range(t):
        time.sleep(1)
        print(t-i)


def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table__lg')
    if table:
        rows = table.find_all('tr')
        extracted_data = []
        for row in rows[1:]:  # Skip the first row as it contains headers
            cells = row.find_all('td')
            if len(cells) >= 8:  # Ensure that there are enough cells in the row
                sn = cells[0].text.strip()
                contract_no = cells[1].text.strip()
                stock_symbol = cells[2].text.strip()
                buyer = cells[3].text.strip()
                seller = cells[4].text.strip()
                quantity = cells[5].text.strip()
                rate_rs = cells[6].text.strip()
                amount_rs = cells[7].text.strip()
                title = cells[2].get('title', '')  # Fetch title attribute from the third cell
                extracted_data.append([sn, contract_no, stock_symbol, buyer, seller, quantity, rate_rs, amount_rs, title])
        return extracted_data
    else:
        print("Table not found in HTML content.")
        return None

def write_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['SN', 'Contract No.', 'Stock Symbol', 'Buyer', 'Seller', 'Quantity', 'Rate (Rs)', 'Amount (Rs)', 'Title'])
    df['Stock Symbol_Buyer'] = df['Stock Symbol'] + '_' + df['Buyer']
    df['Stock Symbol_Seller'] = df['Stock Symbol'] + '_' + df['Seller']
    # df.to_csv(filename, index=False)
    # print(f"Data saved to {filename} with additional columns.")

    return df




def check_success(df):
    symbol_buyer_freq = df['Stock Symbol_Buyer'].value_counts()

    # Filter 'Stock Symbol_Buyer' with frequency > 50
    frequent_symbols = symbol_buyer_freq[symbol_buyer_freq > 50].index.tolist()

    # Filter DataFrame to include only rows with 'Stock Symbol_Buyer' in frequent_symbols
    filtered_df = df[df['Stock Symbol_Buyer'].isin(frequent_symbols)]

    filtered_df.reset_index(drop=True, inplace=True)

    # Iterate over each row and clean 'Amount (Rs)' values
    for i in range(filtered_df.shape[0]):
        filtered_df.at[i, 'Amount (Rs)'] = float(filtered_df.at[i, 'Amount (Rs)'].replace(',', ''))



    # Group by 'Stock Symbol_Buyer' and sum the 'Amount (Rs)'
    total_amounts = filtered_df.groupby('Stock Symbol_Buyer')['Amount (Rs)'].sum()

    success_symbols = total_amounts[total_amounts > 5000000].index.tolist()

    # If there are any success symbols, print "Success" along with those symbols
    if success_symbols:
        print("Success:")
        for symbol in success_symbols:
            print(symbol)
        bot.send_message(
            800851598, str(success_symbols))
    else:
        print("No success found.")


# Set up Chrome WebDriver
# Replace with the path to your chromedriver executable
if not (os.path.exists("final.json")):
    try:
        chrome_driver_path = "_chromedriver_64.exe"
        # chrome_service = ChromeService(chrome_driver_path)
        # chrome_options = ChromeOptions()
        # driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        chrome_options = Options()
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


        # Open the URL in the Chrome browser
        class_link = "https://nepalstock.com/floor-sheet"

        while(True):
            driver.get(class_link)
            scroll_to_bottom()
            wait = WebDriverWait(driver, 10)
            table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-striped")))

            # change option value
            # Locate the dropdown element
            dropdown_element = driver.find_element(By.CSS_SELECTOR, ".table__perpage select")

            # Use Select class to interact with dropdown
            dropdown = Select(dropdown_element)

            # Select the option with value "500"
            dropdown.select_by_value("500")

            # Locate the button element
            button_element = driver.find_element(By.CSS_SELECTOR, ".box__filter--search")

            # Click the button
            button_element.click()

            # Wait until the page reloads
            time_sleep(wait_time)

            html_content = driver.page_source

            extracted_data = extract_table_data(html_content=html_content)

            if extracted_data:
                df = write_to_csv(extracted_data, "extracted_table.csv")

                check_success(df)
                print("Data extracted and saved to extracted_table.csv.")
            else:
                print("No data extracted.")  
            time_sleep(20)





    except Exception as e2:
        e2 = traceback.format_exc(limit=None, chain=True)
        bot.send_message(
            800851598, f"Phase2_bulk_download threw error!!\n```{e2}```")
        traceback.print_exc()
