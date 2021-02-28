"""
Fear of missing out? (FOMO) -> Are you afraid of missing out the next game stop?
This script scrapes the subreddit wallstreetbets for the most discussed stocks and
sends you an email which stocks you could add to your watchlist.
"""
import smtplib
import json
import operator
from collections import defaultdict
import re
import praw
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
USER_AGENT = "WebScrapping"
NUMBER_OF_POSTS = 200
SUBREDDIT = 'wallstreetbets'
PATH_OF_NASDAQ_TICKER = r"\path\to\your\directory"
FLAGGED_WORDS = ["YOLO", "PUMP", "RH", "EOD", "IPO", "ATH",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I",
                 "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                 "S", "T", "U", "V", "W", "X", "Y", "Z"]


def get_new_posts():
    """ gets all new posts via API Call

    This method gets all new posts from wsb and
    removes all emojis, moons, rockets, etc.

    :return: a list of words of all new posts
    """
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)
    posts = []
    regex_pattern = r'[\W_]+'
    wsb = reddit.subreddit(SUBREDDIT)
    for post in wsb.new(limit=NUMBER_OF_POSTS):

        title = re.sub(regex_pattern, ' ', post.title)  # Remove all moons, rockets, etc.
        posts.append(title)

        ext = re.sub(regex_pattern, ' ', post.ext)
        posts.append(ext)
    return posts


def remove_stop_words(posts):
    """ remove words like the, a, ...

    This preprocessing step is important to get rid of all insignificant words

    :param posts: list of words of all new posts
    :return: lists of words of all new posts without stopwords
    """
    stop_words = set(stopwords.words('english'))
    filtered_sentence = []
    for i in posts:
        word_tokens = word_tokenize(i.lower())
        for word in word_tokens:
            if word not in stop_words:
                filtered_sentence.append(word)
    return filtered_sentence


def nasdaq_tickers():
    """ All stocks that are currently listed on nasdaq

    Every stock has a abbreviation that is selected here
    More info: https://www.nasdaq.com/market-activity/stocks

    :return: abbreviation of every nasdaq stock
    """
    fin = open(PATH_OF_NASDAQ_TICKER, 'r')
    tickers = set()
    fin.readline()
    for line in fin.readlines():
        line = line[2:]
        tickers.add(line[:line.index("|")])
    return tickers


def most_common_stocks(all_words, ticker_set):
    """ Compare which nasdaq stock lists appear in new reddit posts and count them up

    :param all_words: list of words of reddit posts
    :param ticker_set: nasdaq stock abbreviations
    :return: dict that contains stocks and occurrences
    """
    dict_stock_occurrences = defaultdict(int)
    for word in all_words:
        if word.upper() in ticker_set and word.upper() not in FLAGGED_WORDS:
            dict_stock_occurrences[word] += 1

    sorted_dict = sorted(dict_stock_occurrences.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict

def send_mail(comm_words):
    """ Sends a mail with most discussed stocks

    Only the top 20 most discussed stocks are send via email

    :param comm_words: dict with stocks and occurrences
    """
    text = "New Posts Keywords\n\n\t"+json.dumps(comm_words[:20])
    subject = SUBREDDIT

    message = f"Subject: {subject}\n\n{text}"
    sender_address = "EMAIL_ADDRESS"
    receiver_address = "EMAIL_ADDRESS"
    account_password = "GMAIL_PASSWORD"

    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # Endpoint for the SMTP Gmail server
    smtp_server.login(sender_address, account_password)
    smtp_server.sendmail(sender_address, receiver_address, message)
    smtp_server.close()


def main():
    posts = get_new_posts()
    posts_no_stopwords = remove_stop_words(posts)
    ticker_set = nasdaq_tickers()
    common_stocks = most_common_stocks(posts_no_stopwords, ticker_set)
    send_mail(common_stocks)


if __name__ == "__main__":
    main()
