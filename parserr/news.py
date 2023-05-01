import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


def get_url(day,month,year):
    base_url = f"https://news.drom.ru/?label=&ordertime&data={year}-{month}-{day}"
    return base_url


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="b-info-block b-info-block_like-text b-info-block_width_215", limit=5)
    news = []
    for item in items:
        news.append({
            "title": item.find("div", class_="b-info-block__title b-link").string,
            "data": item.find("div", class_="b-info-block__text b-info-block__text_type_news-date").getText(),
            "seeing": item.find("span",
                                class_="b-ico b-ico_type_eye-gray b-ico_margin_r-size-s b-info-block__text").getText(),
            "comment": item.find("span", class_="b-ico b-ico_type_comment-gray"
                                                " b-ico_margin_r-size-s b-info-block__text")
            .getText(),
            # "photo": f'https:{item.find("a", class_="b-info-block__cont b-info-block__cont_state_reviews").find("img").get("src")}',
            "url": item.find("a").get('href')

        })

    return news


def parser(day=None, month=None, year=None):
    current_data = datetime.datetime.now()
    url = get_url(
        day=current_data.day if not day else day,
        month=current_data if not month else month,
        year=current_data if not year else year
    )
    html = get_html(url)
    if html.status_code != 200:
        raise Exception("Error in parserr")
    data = get_data(html.text)
    return data


data =parser()
pprint(data)