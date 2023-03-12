import re
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from num2words import num2words
from nltk.tokenize import sent_tokenize, word_tokenize
import datetime
import os

ISW_ARTICLES_URL_ALTERNATIVES = [
    "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-{month}-{day}-{year}",
    "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-{month}-{day}",
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{month}-{day}-{year}",
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{month}-{day}",
    "https://www.understandingwar.org/backgrounder/russian-campaign-assessment-{month}-{day}",
    "https://understandingwar.org/backgrounder/russian-offensive-campaign-update-{month}-{day}",
    # august-12-0 ..
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{month}-{day}-0"
]

MONTH_MAP = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december",
}

def get_isw_article(day, month, year):
    if year == 2022 and month == "february" and day == 24:
        url = "https://understandingwar.org/backgrounder/russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment"
        print(f"get ISW article from URL {url}")
        return requests.get(url)
    else:
        url_index = 0
        while url_index < len(ISW_ARTICLES_URL_ALTERNATIVES):
            url = ISW_ARTICLES_URL_ALTERNATIVES[url_index].format(month=month, day=day, year=year)
            res = requests.get(url)
            if res.status_code == 200:
                print(f"get ISW article from URL {url}")
                return res
            url_index = url_index + 1

        return None

def cleaning_text(res):
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(string=True)
    output = ''
    blacklist = ['[document]','noscript','header','html','meta','head','input','script','import','click', '/.block']
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    textlist=output.split(f"\n")
    new_list=[]
    indexes=[]
    for i in textlist:
        if "[1]" in i:
            indexes.append(textlist.index(i))
    finish=indexes[1]

    for i in range(finish+1):
        if textlist[i]!=" " and "Click" not  in textlist[i] and "Key Takeaways" not  in textlist[i]\
            and "Note: ISW" not in textlist[i] and "http" not in textlist[i] \
            and "|" not in textlist[i] and "FILE" not in textlist[i] \
            and len(textlist[i].split(" "))>13:
            new_list.append(textlist[i].strip())

    final=f" ".join(new_list).strip()
    final=re.sub("\[.*?\]","",final)
    final="".join(final.split("\xa0"))
    return final

def remove_signs(data):
    words = word_tokenize(str(data))
    data = ''
    for word in words:
        reg = re.compile('[^a-zA-Z0-9]')
        word = reg.sub('', word)
        data= data + ' ' + word
    return data.strip()

def lower_case(data):
    words = word_tokenize(str(data))
    data=''
    for word in words:
        data=data + ' ' + word.lower()
    return data.strip()

def check_long_of_words(data):
    words = word_tokenize(str(data))
    data = ''
    for word in words:
        if len(word)>1:
            data = data + ' ' + word
    return data.strip()

def remove_stop_words(data):
    no_words = {'no', 'not'}
    add_to_stop_words = ['the', 'and', 'an', 'at', 'than', 'to', 'or', 'for', 'but', 'this',
                         'that', 'so', 'because', 'of', 'its', 'in', 'on']
    stop_words = [set(nltk.corpus.stopwords.words('english')) - no_words] + add_to_stop_words
    words = word_tokenize(str(data))
    data = ''
    for word in words:
        if word not in stop_words:
            data = data + " " + word
    return data.strip()

def convert_numbers(data):
    words = word_tokenize(str(data))
    data = ''
    for word in words:
        if word.isdigit():
            if int(word)<1000000000000:
                word=num2words(word)
            else:
                word=''
        data=data + " " + word
    return data

def stemming(data):
    stemmer=PorterStemmer()
    words = word_tokenize(str(data))
    data = ''
    for word in words:
        data=data+' '+ stemmer.stem(word)
    return data

def lemmatizing(data):
    lemmatizer=WordNetLemmatizer()
    words = word_tokenize(str(data))
    data = ''
    for word in words:
        data=data+' '+ lemmatizer.lemmatize(word)
    return data

def correct_text(day=3, month="march", year=2023, algo='lemm'):
    res=get_isw_article(day=day, month=month, year=year)
    if res is None:
        print (f"Can\'t get article for {day}/{month}/{year}")
        return ''
    data=cleaning_text(res)
    data=remove_signs(data)
    data=lower_case(data)
    data=check_long_of_words(data)
    data=remove_stop_words(data)
    data=convert_numbers(data)
    data=stemming(data)
    data=convert_numbers(data)
    if algo=='lemm':
        print('lemmatizing')
        data=lemmatizing(data)
    else:
        print('steaming')
        data=stemming(data)
    data=remove_signs(data)
    data=remove_stop_words(data)
    return data

def collect_isw_news_for_period():
    from_date = datetime.date(2022, 2, 24)
    till_date = datetime.date(2023, 1, 25)
    print(f"Collect ISW new for period {from_date} - {till_date}")

    # delta time
    delta = datetime.timedelta(days=1)
    try:
        os.mkdir("isw-articles")
    except FileExistsError as e:
        pass

    # iterate over range of dates
    while (from_date <= till_date):
        isw_article_text = correct_text(from_date.day, MONTH_MAP[from_date.month], from_date.year)
        # print(len(isw_article_text))

        try:
            f = open(f"isw-articles/{from_date.year}-{from_date.month}-{from_date.day}.txt", "w", encoding="utf-8")
            f.write(isw_article_text)
            f.close()
        except UnicodeEncodeError as e:
            print(f"Exception writing to file - " + str(e))

        from_date += delta

collect_isw_news_for_period()