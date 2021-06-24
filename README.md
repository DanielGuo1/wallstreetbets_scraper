# Wallstreetbets scraper

![wsb](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fih0.redbubble.net%2Fimage.379601684.6062%2Fraf%2C360x360%2C075%2Ct%2Cfafafa%3Aca443f4786.jpg&f=1&nofb=1)

Are you afraid of missing out the next game stop?
This script scrapes the subreddit wallstreetbets for the most discussed stocks and
sends you an email which stocks you could add to your watchlist.

## How does it work?
- First things first: We need Data from reddit --> [Reddit API](https://www.reddit.com/dev/api/)
- After that, we need to preprocess the data (new post, comments, etc.) --> Remove Stopwords and Flagged Words (YOLO, PUMP, ATH, etc.).
- Ok, but how do we get the stocks now? --> We then compare the preprocessed data with a list of all stocks listed at NASDAQ [NASDAQ Ticker](https://github.com/DanielGuo1/wallstreetbets_scraper/blob/main/res/nasdaq.txt)
- We then count the occurence of the most mentioned stocks and finally you'll get an email that contains the most discussed stocks on wsb right now 

DISCLAIMER: Do your own research! Wallstreetbets is not a trustworthy source to bet your money on.
