import requests
import os
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, url, long_link):
    payload = {"url": long_link}
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    parsed_short_url = urlparse(response.json()["shorturl"])
    return f"{parsed_short_url.netloc}{parsed_short_url.path}"


def count_clicks(token, url, short_link):
    payload = {"short": short_link}
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    clicks_count = response.json()["data"]["clicks"]
    return clicks_count


def is_bitlink(token, url, link):
    payload = {"short": link}
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return not response.json()["error"]


def main():
    load_dotenv(".env")
    user_link = input("Введите ссылку: ")
    list_links_payload = {"limit":"2", "page":"1", "order":"date"}
    list_links_response = requests.get("https://clc.li/api/urls", params=list_links_payload)
    link_is_short = is_bitlink(
        token=os.environ["CLC_TOKEN"],
        url=list_links_response.url,
        link=user_link,
    )
    if link_is_short:
        clicks_count = count_clicks(
            token=os.environ["CLC_TOKEN"],
            url=list_links_response.url,
            short_link=user_link,
        )
        print("Количество кликов по ссылке:", clicks_count)
    else:
        short_link = shorten_link(
            token=os.environ["CLC_TOKEN"],
            url="https://clc.li/api/url/add",
            long_link=user_link,
        )
        print("Короткая ссылка", short_link)


if __name__ == "__main__":
    main()
