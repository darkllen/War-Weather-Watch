import re
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from num2words import num2words
from nltk.tokenize import word_tokenize

def cleaning_text(day=3, month="march", year=2023):
    url=f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{month}-{day}-{year}'
    res = requests.get(url)
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
    data=cleaning_text(day=3, month="march", year=2023)
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
print(correct_text())
