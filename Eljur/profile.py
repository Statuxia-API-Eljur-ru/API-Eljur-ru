from bs4 import BeautifulSoup
from requests import Session
from Eljur.errors import _checkInstance, _checkStatus, _checkSubdomain, _findData


class Profile:

    def getProfile(self, subdomain, session):
        """
        Получение информации о пользователе.
        Внимание. В данной функции специально не выводится СНИЛС, почта и мобильный телефон пользователя.

        :param subdomain: поддомен eljur.ru
        :param session: активная сессия пользователя

        :return: словарь с ошибкой или с информацией о пользователе:
                 answer // dict
                 session // Session
                 subdomain // str
                 result // bool
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        url = f"https://{subdomain}.eljur.ru/journal-user-preferences-action"
        account = session.get(url=url)

        checkStatus = _checkStatus(account, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        soup = BeautifulSoup(account.text, 'lxml')

        sentryData = _findData(soup)
        if not sentryData:
            return {"error": {"error_code": -104,
                              "error_msg": "Данные о пользователе не найдены."}}
        del sentryData

        label = None
        info = {}
        for tag in soup.find_all(["label", "span"], class_=["ej-form-label", "control-label"]):
            if tag.contents[0] == "СНИЛС":
                break

            if tag.name == "label":
                label = tag.contents[0]
                info.update([(label, None)])

            if tag.name == "span":
                info[label] = tag.contents[0]

        return info


class Security:

    def changePassword(self, subdomain, session, old_password, new_password):
        """
        Изменение пароля в личном кабинете пользователя.

        :param subdomain: поддомен eljur.ru
        :param session: активная сессия пользователя
        :param old_password: старый пароль.
        :param new_password: новый пароль, который пользователь желает использовать.

        :return: словарь с ошибкой или bool ответ, в котором True - успешная смена пароля
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        url = f"https://{subdomain}.eljur.ru/journal-messages-compose-action"
        getCookies = session.get(url=url, data={"_msg": "sent"})

        checkStatus = _checkStatus(getCookies, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        data = {"csrf": getCookies.cookies.values()[0],
                "old_password": old_password,
                "new_password": new_password,
                "verify": new_password,
                "submit_button": "Сохранить"}

        url = f"https://{subdomain}.eljur.ru/journal-user-security-action/"
        answer = session.post(url=url, data=data)

        checkStatus = _checkStatus(answer, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        if "Ваш пароль успешно изменен!" in answer.text:
            return True
        return False


class Settings:

    def changeSing(self, subdomain, session, text):
        """
            Изменение подписи в новых сообщениях пользователя.

        :param subdomain: поддомен eljur.ru
        :param session: активная сессия пользователя
        :param text: Текст подписи.

        :return: словарь с ошибкой или bool ответ, в котором True - успешное изменение подписи.
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        url = f"https://{subdomain}.eljur.ru/journal-index-rpc-action"
        data = {"method": "setPref",
                "0": "msgsignature",
                "1": text}

        changeSing = session.post(url=url, data=data)

        checkStatus = _checkStatus(changeSing, url)
        if "error" in checkStatus:
            return checkStatus

        if "result" not in checkStatus:
            return False
        else:
            return checkStatus["result"]

    def switcher(self, subdomain, session, choose, switch):
        """
        Переключение настраиваиваемых функций в настройках.
        Доступно переключение следующих функций:
        `Отмечать сообщение прочитанным при его открытии на электронной почте` // 0 или checkforwardedemail
        `Отображать расписание обучающегося по умолчанию (вместо расписания класса)` // 1 или schedule_default_student

        :param subdomain: поддомен eljur.ru
        :param session: активная сессия пользователя
        :param choose: Выбор переключаемой функции // int или str
        :param switch: bool

        :return: словарь с ошибкой или bool ответ, в котором True - успешное переключение.
        """

        numSwitch = [0, 1]
        strSwitch = ["checkforwardedemail", "schedule_default_student"]
        switchers = {"checkforwardedemail": {"on": "on",
                                             "off": "off"},
                     "schedule_default_student": {"on": "yes",
                                                  "off": "no"}}
        data = {"method": "setPref",
                "0": None,
                "1": None}

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        checkInt = _checkInstance(choose, int)
        if "error" in checkInt:
            checkStr = _checkInstance(choose, str)
            if "error" in checkStr:
                return checkStr
            else:
                if choose not in strSwitch:
                    return {"error": {"error_code": -302,
                                      "error_msg": f"Вашего выбора нет в предложенных. {choose}"}}
                data["0"] = choose
        else:
            if choose not in numSwitch:
                return {"error": {"error_code": -302,
                                  "error_msg": f"Вашего выбора нет в предложенных. {choose}"}}
            data["0"] = strSwitch[choose]

        checkBool = _checkInstance(switch, bool)
        if "error" not in checkBool:
            return checkBool
        del checkBool, checkStr, checkInt

        if switch:
            data["1"] = switchers[data["0"]]["on"]
        else:
            data["1"] = switchers[data["0"]]["off"]

        url = f"https://{subdomain}.eljur.ru/journal-index-rpc-action"
        changeSing = session.post(url=url, data=data)

        checkStatus = _checkStatus(changeSing, url)
        if "error" in checkStatus:
            return checkStatus

        if "result" not in checkStatus:
            return False
        else:
            return checkStatus["result"]
