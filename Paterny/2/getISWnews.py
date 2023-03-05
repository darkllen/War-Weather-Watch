import re
from bs4 import BeautifulSoup
import requests

def correct_text(day=3, month="march", year=2023):
    if year=="2023":
        url=f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{month}-{day}-{year}'
    else:
        url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{month}-{day}'
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

    start=textlist.index(' Download the PDF ')
    new_list=[]

    indexes=[]
    for i in textlist:
        if "[1]" in i:
            indexes.append(textlist.index(i))
    finish=indexes[1]

    for i in range(start+1, finish+1):
        if textlist[i]!=" " and "Click" not  in textlist[i] and "Key Takeaways" not  in textlist[i]\
            and "Note: ISW" not in textlist[i] and "http" not in textlist[i]:
            new_list.append(textlist[i].strip())

    final=f"\n".join(new_list).strip()
    final=re.sub("\[.*?\]","",final)
    final="".join(final.split("\xa0"))
    return final