import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, long_link):
    payload = {"url": long_link}
    headers = {"Authorization": token, "Content-Type": "application/json"}
    clc_url = "https://clc.li/api/url/add"
    response = requests.post(clc_url, json=payload, headers=headers)
    response.raise_for_status()
    parsed_short_url = urlparse(response.json()["shorturl"])
    return f"{parsed_short_url.netloc}{parsed_short_url.path}"


def count_clicks(token, short_link):
    payload = {"short": short_link}
    headers = {"Authorization": token, "Content-Type": "application/json"}
    clc_url = get_list_links_url()
    response = requests.get(clc_url, headers=headers, params=payload)
    response.raise_for_status()
    clicks_count = response.json()["data"]["clicks"]
    return clicks_count


def is_bitlink(token, link):
    payload = {"short": link}
    headers = {"Authorization": token, "Content-Type": "application/json"}
    clc_url = get_list_links_url()
    response = requests.get(clc_url, headers=headers, params=payload)
    response.raise_for_status()
    return not response.json()["error"]


def get_list_links_url():
    list_links_payload = {"limit": "2", "page": "1", "order": "date"}
    list_links_response = requests.get(
        "https://clc.li/api/urls", params=list_links_payload
    )
    return list_links_response.url


def main():
    load_dotenv(".env")
    user_link = input("Введите ссылку: ")
    link_is_short = is_bitlink(
        token=os.environ["CLC_TOKEN"],
        link=user_link,
    )
    if link_is_short:
        clicks_count = count_clicks(
            token=os.environ["CLC_TOKEN"],
            short_link=user_link,
        )
        print("Количество кликов по ссылке:", clicks_count)
    else:
        short_link = shorten_link(
            token=os.environ["CLC_TOKEN"],
            long_link=user_link,
        )
        print("Короткая ссылка", short_link)


if __name__ == "__main__":
    main()
