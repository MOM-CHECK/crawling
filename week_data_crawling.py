import requests
from bs4 import BeautifulSoup
import json

base_url = "https://baby.namyangi.com/contents/view"
info_data= []
FETAL_TITLE = "태아의 몸"
FETAL_GROWTH_TITLE = "태아의 성장 발달"
MOTHER_TITLE = "엄마의 몸"
MOTHER_CHANGE_TITLE = "임신부의 신체 변화"
TAG_TITLE = "Tag"

def crawl_fetal_growth(w, url):
    response = requests.get(url).text
    
    soup = BeautifulSoup(response, 'html.parser')
    detail_section = soup.find('div', class_='detail-cont type2')
    
    data = list(detail_section.stripped_strings)
    
    f_idx = data.index(FETAL_GROWTH_TITLE)
    m_idx = data.index(MOTHER_CHANGE_TITLE)
    end_idx = data.index(TAG_TITLE)
    
    mom_change = []
    fetal_growth = []
    
    basic_data = data[:f_idx]
    mom_change = extract_basic_info(MOTHER_TITLE, mom_change, basic_data)
    fetal_growth = extract_basic_info(FETAL_TITLE, fetal_growth, basic_data)
    
    fetal_growth = extract_info(f_idx+1, m_idx, fetal_growth, data)
    mom_change = extract_info(m_idx+1, end_idx, mom_change, data)
    
    info = {
        "week": w,
        "fetal_growth": fetal_growth,
        "mom_change": mom_change
    }

    info_data.append(info)
    
def extract_basic_info(text, lst, basic_data):   
    if text in basic_data:
        lst.append({
            "title": text,
            "content": basic_data[basic_data.index(text) + 1]
        })
    return lst
    
def extract_info(start, end, lst, data):
    for i in range(start, end, 2):
        lst.append({
            "title": data[i],
            "content": data[i+1]
        })
    return lst

def info_for_weeks(base_url):
    weekly_url = [
        [4, 12, '/4028/', 4761],
        [12, 16, '/4028/', 4768],
        [16, 28, '/4014/', 4768],
        [28, 29, '/4014/', 4782],
        [29, 41, '/4042/', 4782]
    ]
    
    for start, end, p1, p2 in weekly_url:
        for w in range(start, end):
            url = base_url + p1 + str(p2+w)
            crawl_fetal_growth(w, url)

def main():
    info_for_weeks(base_url)
    with open('week_data1.json', 'w', encoding='utf-8') as f:
        json.dump(info_data, f, ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    main()