import praw
import pandas as pd
import re, locale
import smtplib
from collections import defaultdict
import operator
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
import json

my_client_id = "nh1kBVGwwj4vwg"
my_client_secret = "2F53sVj37VrlfFb2T0bhAHZRT4zejg"
my_user_agent = "WebScrapping"

# how many posts should be loaded
number_of_posts = 15

reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret, user_agent=my_user_agent)

# hot posts
hot_posts = []
wsb = reddit.subreddit('wallstreetbets')
for post in wsb.hot(limit=number_of_posts):
    
    title = re.sub(r'[\W_]+', ' ', post.title) # Remove all characters except letters and numbers
    hot_posts.append(title)
    
    selftext = re.sub(r'[\W_]+', ' ', post.selftext)
    hot_posts.append(selftext)

# new posts
new_posts = []
wsb = reddit.subreddit('wallstreetbets')
for post in wsb.new(limit=number_of_posts):
    
    title = re.sub(r'[\W_]+', ' ', post.title) # Remove all characters except letters and numbers
    new_posts.append(title)
    
    selftext = re.sub(r'[\W_]+', ' ', post.selftext) 
    new_posts.append(selftext)

stop_words = set(stopwords.words('english'))

def remove_stop_words(posts):
    # remove stop words
    filtered_sentence = []
    for i in posts:
        word_tokens = word_tokenize(i.lower())

        for w in word_tokens:  
            if w not in stop_words:  
                filtered_sentence.append(w)
    return filtered_sentence

def nasdaq_tickers():
    fin = open("nasdaqtraded.txt", 'r')
    tickers = set()
    fin.readline()
    for line in fin.readlines():
        line = line[2:]
        tickers.add(line[:line.index("|")])
    return tickers

ticker_set = nasdaq_tickers()
flagged_words = ["YOLO", "PUMP", "RH", "EOD", "IPO", "ATH", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def most_common_stocks(all_words):
    d = defaultdict(int)
    for word in all_words:
        if word.upper() in ticker_set and word.upper() not in flagged_words:
            d[word] += 1

    sorted_dict = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict   

new_filtered = remove_stop_words(new_posts)
comm_words_new = most_common_stocks(new_filtered)

hot_filtered = remove_stop_words(hot_posts)
comm_words_hot = most_common_stocks(hot_filtered)

sender_address = "guoweicsuf@gmail.com" # Replace this with your Gmail address
 
receiver_address = "guoweicsuf@gmail.com" # Replace this with any valid email address
 
account_password = "uidltammrgykoleb" # Replace this with your Gmail account password
 
subject = "Wallstreetbets"

body = "Hot Posts Keywords\n\n\t"+json.dumps(comm_words_hot[:10])+"\n\n New Posts Keywords\n\n\t"+json.dumps(comm_words_new[:10])

# Endpoint for the SMTP Gmail server (Don't change this!)
smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
 
# Login with your Gmail account using SMTP
smtp_server.login(sender_address, account_password)
 
# Let's combine the subject and the body onto a single message
message = f"Subject: {subject}\n\n{body}"
 
# We'll be sending this message in the above format (Subject:...\n\nBody)
smtp_server.sendmail(sender_address, receiver_address, message)
 
# Close our endpoint
smtp_server.close()

print("Success")
