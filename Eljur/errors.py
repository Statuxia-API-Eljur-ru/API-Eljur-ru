import re
from bs4 import BeautifulSoup
from requests import Session


def _findData(soup):
    for tag in soup.find_all("script"):
        contents = tag.contents
        for content in contents:
            if "sentryData" in content:
                return content


def _checkStatus(err, url):
    if not err.status_code:
        return {"error": {"error_code": -102,
                          "error_msg": f"Возникла ошибка при отправке запроса по ссылке {url}"}}
    if err.status_code >= 400:
        return {"error": {"error_code": -102,
                          "error_msg": f"Возникла ошибка {err.status_code} при отправке запроса  по ссылке {url}"}}
    else:
        return {"answer": "Ok",
                "result": True}


def _checkSubdomain(subdomain):
    subdomain = re.search(r"[a-zA-Z0-9]+", subdomain)
    if not subdomain:
        return {"error": {"error_code": -101,
                          "error_msg": "Поддомен не найден"}}
    else:
        return subdomain[0]


def _checkInstance(obj, cls):
    if not isinstance(obj, cls):
        return {"error": {"error_code": -201,
                          "error_msg": f"Экземпляр не пренадлежит к классу. {type(obj)} - {type(cls)}"}}
    else:
        return {"answer": "Ok",
                "result": True}


def _fullCheck(subdomain, session, url, data=None):
    subdomain = _checkSubdomain(subdomain)
    if "error" in subdomain:
        return subdomain

    checkSession = _checkInstance(session, Session)
    if "error" in checkSession:
        return checkSession
    del checkSession

    getInfo = session.post(url=url, data=data)

    checkStatus = _checkStatus(getInfo, url)
    if "error" in checkStatus:
        return checkStatus
    del checkStatus

    soup = BeautifulSoup(getInfo.text, 'lxml')
    del getInfo, url

    sentryData = _findData(soup)
    if not sentryData:
        return {"error": {"error_code": -104,
                          "error_msg": "Данные о пользователе не найдены."}}
    del sentryData

    return soup


def _smallCheck(subdomain, session, args):
    subdomain = _checkSubdomain(subdomain)
    if "error" in subdomain:
        return subdomain

    checkSession = _checkInstance(session, Session)
    if "error" in checkSession:
        return checkSession
    del checkSession

    checkDict = _checkInstance(args, dict)
    if "error" in checkDict:
        return checkDict
    del checkDict
