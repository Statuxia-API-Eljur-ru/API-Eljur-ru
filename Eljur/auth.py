from bs4 import BeautifulSoup
from requests import Session
import json
import re


def _findData(soup):
    for tag in soup.find_all("script"):
        contents = tag.contents
        for content in contents:
            if "sentryData" in content:
                return content


def auth(subdomain, data):
    """
    Подключение к пользователю eljur.ru.

    :param subdomain: поддомен eljur.ru
    :param data: дата, состоящая из {"username": "ваш логин",
                                     "password": "ваш пароль"}

    :return: словарь с ошибкой или с положительным ответом:
             answer // dict
             сессии // Session
             поддомен // str
    """

    subdomain = re.search(r"[a-zA-Z]+", subdomain)
    if not subdomain:
        return {"error": {"error_code": -1,
                          "error_msg": "subdomain not found"}}

    session = Session()
    session.post(url=f"https://{subdomain[0]}.eljur.ru/ajaxauthorize", data=data)

    account = session.get(url=f"https://{subdomain[0]}.eljur.ru/?show=home")
    soup = BeautifulSoup(account.text, 'lxml')

    sentryData = _findData(soup)

    if not sentryData:
        return {"error": {"error_code": -2,
                          "error_msg": "sentryData not found"}}

    sentryData = json.loads(sentryData[17:-1])

    return {"answer": sentryData,
            "session": session,
            "subdomain": subdomain[0]}
