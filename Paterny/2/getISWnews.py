import pickle
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
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from itertools import islice

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
        word = reg.sub(' ', word)
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
    data= cleaning_text(res)
    data = check_long_of_words(data)
    data = lower_case(data)
    data=remove_signs(data)
    data = remove_stop_words(data)
    data=convert_numbers(data)
    data=stemming(data)
    data = remove_signs(data)
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
    from_date = datetime.date(2023, 2, 1)
    till_date = datetime.date(2023, 2, 28)
    print(f"Collect ISW new for period {from_date} - {till_date}")
    data=[]
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
            data.append(isw_article_text)
            f.close()
        except UnicodeEncodeError as e:
            print(f"Exception writing to file - " + str(e))

        from_date += delta
    return data

data=collect_isw_news_for_period()

cv=CountVectorizer(min_df=2)
word_count_vector =cv.fit_transform(data)
print(f"Word count vector: \n { word_count_vector}")
print()
print(f"Word count vector shape: \n {word_count_vector.shape}")
dict1=cv.vocabulary_
print(f"Words with frequency: {dict1} ")
print()
sorted_dict = {}
sorted_keys = sorted(dict1, key=dict1.get, reverse=True)
for w in sorted_keys:
    sorted_dict[w] = dict1[w]

print(f"Sorted words with frequency: {sorted_dict} ")
print()

def topnwords(n):
    topn=list(islice(sorted_dict, n))
    dict_topn={}
    for i in topn:
        dict_topn[i]=sorted_dict[i]
    return dict_topn

def topnwordsvalues(dict):
    dict_value={}
    for v in dict.keys():
        dict_value[v]=dict[v]/sum(dict.values())
    return dict_value

print(topnwords(100))
print(topnwordsvalues(topnwords(100)))

with open('count_vectorize_v1.pkl', 'wb') as handle:
    pickle.dump(cv, handle)

tfidf_transformer=TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)

with open('count_vectorize_v1.pkl', 'wb') as handle:
    pickle.dump(tfidf_transformer, handle)

df_idf=pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names_out(), columns=['idf_weights'])
df_idf.sort_values(by=['idf_weights'])
print(f'DataFrame: \n {df_idf}')

tf_idf_vector=tfidf_transformer.transform(word_count_vector)
print(f'DataFrame Vector: \n {tf_idf_vector}')

feature_names=cv.get_feature_names_out()
# print(f'Feature names: {feature_names}')


def sort_coo(coo_matrix):
    tuples=zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda  x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=100):
    sorted_items=sorted_items[:topn]
    score_vals=[]
    feature_vals=[]
    for idx,score in sorted_items:
        score_vals.append((round(score, 5)))
        feature_vals.append((feature_names[idx]))
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    return results

print(extract_topn_from_vector(feature_names, sort_coo(tf_idf_vector.tocoo()), topn=100))

unsorted_vector=extract_topn_from_vector(feature_names, sort_coo(tf_idf_vector.tocoo()), topn=100)

def sorted_vector(unsorted_vector):
    sorted_vector = {}
    sorted_keys = sorted(unsorted_vector, key=unsorted_vector.get, reverse=True)
    for w in sorted_keys:
        sorted_vector[w] = unsorted_vector[w]
    return sorted_vector
print(sorted_vector(unsorted_vector))
