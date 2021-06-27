[![Python](https://img.shields.io/badge/Build-Python3.x-blue.svg?style=flat-square&logo=Python&logoColor=white)](https://www.python.org/) 

<h1 align="center">Wallstreetbets scraper</h1>
<p align="center">
  <a> 
    <img src="https://github.com/DanielGuo1/wallstreetbets_scraper/blob/main/images/wsb.png" alt="Logo" width="550" height="300">
  </a>
  <p align="center">
    Never miss the next gamestop
  </p>
</p>

## About The Project

Are you afraid of missing out the next game stop?
This script scrapes the subreddit wallstreetbets for the most discussed stocks and
sends you an email which stocks you could add to your watchlist.

## How does it work?
1. First things first: We need Data from reddit --> [Reddit API](https://www.reddit.com/dev/api/)
2. After that, we need to preprocess the data (new post, comments) --> Remove Stopwords and Flagged Words (YOLO, PUMP, ATH)
3. Ok, but how do we get the stocks now? --> We then compare the preprocessed data with a list of all stocks listed at NASDAQ [(Ticker)](https://github.com/DanielGuo1/wallstreetbets_scraper/blob/main/res/nasdaq.txt)
4. Count the occurence of the most mentioned stocks and finally you'll get an email that contains the most discussed stocks on wsb right now 

DISCLAIMER: Do your own research! Wallstreetbets is not a trustworthy source to bet your money on.

<!-- GETTING STARTED -->
## Getting Started

If you want to run this code locally, get a copy and follow these simple steps.

### Prerequisites

You need to download python in order to run the script [Download Python here](https://www.python.org/downloads/).


### Installation

1. Get a free API Key at [https://www.reddit.com/dev/api/](https://www.reddit.com/dev/api/)
2. Clone the repo
   ```sh
   git clone https://github.com/DanielGuo1/wallstreetbets_scraper.git
   ```
### Setup
1. Enter your API credentials in `wsb.py`
   ```python
   CLIENT_ID = "CLIENT_ID"
   CLIENT_SECRET = "CLIENT_SECRET"
   ```
2. Put in your Gmail Account in `wsb.py`
  ```python
    sender_address = "EMAIL_ADDRESS"
    receiver_address = "EMAIL_ADDRESS"
    account_password = "GMAIL_PASSWORD"
  ```
3. Run `wsb.py`
   ```python
   python3 wsb.py
   ```

