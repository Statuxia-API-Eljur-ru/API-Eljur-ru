from bs4 import BeautifulSoup
from requests import Session
from Eljur.errors import _checkInstance, _checkStatus, _checkSubdomain, _findData


class Portfolio:

    def reportCard(self, subdomain, session, user_id, quarter="I"):
        """
        Получение списка оценок.

        :param subdomain: Поддомен eljur.ru                                                     // str
        :param session:   Активная сессия пользователя                                          // Session
        :param user_id:   ID пользователя                                                       // str
        :param quarter:   Четверть. (I, II, III, IV)                                            // str

        :return: Словарь с ошибкой или ответом (отсутствие оценок или словарь с оценками)       // dict
        """

        url = f"https://{subdomain}.eljur.ru/journal-student-grades-action/u.{user_id}/sp."

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        journal = session.get(url=url + quarter)

        checkStatus = _checkStatus(journal, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        soup = BeautifulSoup(journal.text, 'lxml')
        del journal, url

        sentryData = _findData(soup)
        if not sentryData:
            return {"error": {"error_code": -401,
                              "error_msg": "Данные о пользователе не найдены."}}
        del sentryData

        answer = soup.find("div", class_="page-empty")

        if answer:
            return {"answer": answer.contents[0],
                    "result": False}

        card = {}
        subjects = soup.find_all("div", class_="text-overflow lhCell offset16")

        for subject in subjects:
            scores = {}
            for score in soup.find_all("div", class_="cell blue", attrs={"name": subject.contents[0]}):
                scores.update([(score.attrs["mark_date"], score.contents[1].contents[0])])
            card.update([(subject.contents[0], scores)])
        card.update(result=True)

        return card

    def attendance(self, subdomain, session):
        return

    def finalGrades(self, subdomain, session, user_id, data=None):
        """
        Изменение подписи в новых сообщениях пользователя.

        :param subdomain: Поддомен eljur.ru                                                     // str
        :param session:   Активная сессия пользователя                                          // Session
        :param user_id:   ID пользователя                                                       // str
        :param data:      Учебный год (Например: 2020/2021)                                     // str

        :return: Словарь с ошибкой или ответом (отсутствие оценок или словарь с оценками)       // dict
        """
        url = f"https://{subdomain}.eljur.ru/journal-student-resultmarks-action/u.{user_id}"

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        journal = session.post(url=url, data=data)

        checkStatus = _checkStatus(journal, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        soup = BeautifulSoup(journal.text, 'lxml')
        del journal, url

        sentryData = _findData(soup)
        if not sentryData:
            return {"error": {"error_code": -401,
                              "error_msg": "Данные о пользователе не найдены."}}
        del sentryData

        answer = soup.find("div", class_="page-empty")

        if answer:
            return {"answer": answer.contents[0],
                    "result": False}

        card = {}
        subjects = soup.find_all("div", class_="text-overflow lhCell offset16")

        for subject in subjects:
            scores = []
            for score in soup.find_all("div", class_="cell", attrs={"name": subject.contents[0]}):
                if score.contents[0].attrs["class"][0] != "cell-data":
                    continue
                if not score.contents[0].contents:
                    continue
                scores.append(score.contents[0].contents[0])
            card.update([(subject.contents[0], scores)])
        card.update(result=True)

        return card
