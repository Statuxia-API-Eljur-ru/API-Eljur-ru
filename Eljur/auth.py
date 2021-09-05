from bs4 import BeautifulSoup
from requests import Session, post
import json
from Eljur.errors import _checkStatus, _checkSubdomain, _findData


class Authorization:

    def register(self, code):
        """
        Регистрация пользователя eljur.ru.

        :param code: Единоразовый код, который можно получить в школе.

        :return: code/Не завершено
        """
        return code

    def login(self, subdomain, data):
        """
        Подключение к пользователю eljur.ru.

        :param subdomain: поддомен eljur.ru
        :param data: дата, состоящая из {"username": "ваш логин",
                                         "password": "ваш пароль"}

        :return: словарь с ошибкой или с положительным ответом:
                 answer // dict
                 session // Session
                 subdomain // str
                 result // bool
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        session = Session()
        url = f"https://{subdomain}.eljur.ru/ajaxauthorize"
        err = session.post(url=url, data=data)

        checkStatus = _checkStatus(err, url)
        if "error" in checkStatus:
            return checkStatus

        if not err.json()["result"]:
            return {"error": {"error_code": -103,
                              "error_msg": err.json()['error'],
                              "full_error": err.json()}}

        url = f"https://{subdomain}.eljur.ru/?show=home"
        account = session.get(url=url)
        checkStatus = _checkStatus(account, url)
        if "error" in checkStatus:
            return checkStatus

        soup = BeautifulSoup(account.text, 'lxml')

        sentryData = _findData(soup)
        if not sentryData:
            return {"error": {"error_code": -104,
                              "error_msg": "Данные о пользователе не найдены."}}

        sentryData = json.loads(sentryData[17:-1])

        return {"answer": sentryData,
                "session": session,
                "subdomain": subdomain,
                "result": True}

    def recover(self, subdomain, email):
        """
        Восстановление пароля пользователя eljur.ru. через почту.

        Внимание! Для использования данной функции требуется привязать почту.
        В ином случае восстановление происходит через Администратора или другого лица вашей школы.

        :param subdomain: домен вашей школы.
        :param email: ваша почта, привязанная к аккаунту eljur

        :return: словарь с ошибкой или с положительным ответом:
                 answer // dict
                 result // bool
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        url = f"https://{subdomain}.eljur.ru/ajaxrecover"
        answer = post(url=url,
                      data={"email": email})

        checkStatus = _checkStatus(answer, url)
        if "error" in checkStatus:
            return checkStatus

        if not answer.json()["result"]:
            return {"error": {"error_code": -105,
                              "error_msg": answer.json()['error'],
                              "full_error": answer.json()}}
        return {"answer": "Сообщение успешно отправлено на почту.",
                "result": True}
