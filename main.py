import re
import requests
from bs4 import BeautifulSoup
from database import db
from mysocket import sio


def v(arr):
    return list(set(arr))


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text("\r\n")
    phone_number_regex = re.compile(
        r"(?:\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
    phone_numbers = re.findall(phone_number_regex, text)

    for link in soup.find_all("a"):
        href = link.get("href")
        text += f" {href} "
        if href and href.startswith("tel:"):
            phone_numbers.extend(re.findall(phone_number_regex, href))

    social_links_regex = re.compile(r"(?:https?:\/\/)?(?:www\.)?(?:facebook|fb|twitter|linkedin|instagram|youtube"
                                    r")\.com\/(?:[\w\-\.]+\/?)+")
    social_links = re.findall(social_links_regex, text)

    email_regex = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    email_addresses = re.findall(email_regex, text)

    return v(email_addresses), v(phone_numbers), v(social_links)


def scrape_webpage(website_url):
    try:
        response = requests.get(website_url, timeout=10)
        return parse_html(response.text)
    except:
        return [], [], []


def main():
    page_size = 1000
    n = 0

    while True:
        result = db['gmaps'].find(
            {"result.website": {'$exists': True}},
            {'result.website': 1, '_id': 0}
        ).skip(n * page_size).limit(page_size)
        sio.emit('message', {'message': n})
        website_urls = [r['result']['website'] for r in result]
        if not website_urls:
            break

        for website_url in website_urls:
            email_addresses, phone_numbers, social_links = scrape_webpage(website_url)
            print({
                "social_links": social_links,
                "email_addresses": email_addresses,
                "phone_numbers": phone_numbers
            })
            if (len(email_addresses) + len(phone_numbers) + len(social_links)) == 0:
                db['websites'].update_one({'url': website_url}, {'$set': {'url': website_url}}, True)
            db['contacts'].update_one({'url': website_url}, {'$set': {
                'url': website_url,
                'result': {
                    "social_links": social_links,
                    "email_addresses": email_addresses,
                    "phone_numbers": phone_numbers
                }
            }}, True)
            sio.emit('message', {'message': f'{website_url}'})
            sio.emit('message', {'message': f's:{len(social_links)} e:{len(email_addresses)} p:{len(phone_numbers)}'})
        n += 1


if __name__ == "__main__":
    sio.connect('http://localhost:9000')
    main()
