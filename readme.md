
# Institutional Buy Detector

This Python script scrapes data from the Nepal Stock Exchange website to extract floor sheet data and perform analysis on it to detect institutional buying of stocks in the Nepalese share market.

## Features

- **Data Scraping**: Uses Selenium WebDriver to navigate the Nepal Stock Exchange website and scrape floor sheet data.
- **Data Analysis**: Analyzes the extracted data to identify stock symbols with high transaction frequency and high transaction amounts.
- **Notification**: Sends notifications via Telegram bot for successful transactions.

## Requirements

- Python 3.x
- Selenium
- Beautiful Soup
- Pandas
- Chrome WebDriver

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/chandan22140/Institutional-Buy-Detector
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Download and install Chrome WebDriver from [here](https://googlechromelabs.github.io/chrome-for-testing/).

## Usage

1. Run the script:

    ```bash
    python scraper.py
    ```

2. The script will navigate to the Nepal Stock Exchange website, scrape the floor sheet data, perform analysis, and send notifications for successful transactions via Telegram.

## Configuration

- Update `API_KEY` variable in the script with your Telegram bot API key.
- Adjust `wait_time` variables in the script to configure wait times.
- Ensure proper installation of Chrome WebDriver and update the path in the script if necessary.

## Author

Chandan Sah

## License

This project is licensed under the [MIT License](LICENSE).

