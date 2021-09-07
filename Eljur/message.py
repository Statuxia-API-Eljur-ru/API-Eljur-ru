from requests import Session
from Eljur.errors import _checkStatus, _checkSubdomain, _checkInstance


class Message:

    def schoolList(self, subdomain, session):
        """
        Получение тех, кому можем отправить сообщение.

        :param subdomain: Поддомен eljur.ru                                     // str
        :param session:   Активная сессия пользователя                          // Session

        :return: Возвращает массив из словарей возможных получателей сообщения. // list
        """

        pattern = {"0": "school",
                   "1": "null",
                   "2": "null",
                   "3": "null"}
        typePattern = ["classruks", "administration", "specialists", "ext_5_teachers", "teachers", "parents",
                       "students"]
        listAnswer = {}

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        for typeOf in enumerate(typePattern):
            if typeOf[0] == 4:
                pattern["2"] = "1"

            pattern["1"] = typePattern[typeOf[0]]

            url = f"https://{subdomain}.eljur.ru/journal-messages-ajax-action?method=getRecipientList"
            getPattern = session.post(url=url, data=pattern)

            checkStatus = _checkStatus(getPattern, url)
            if "error" in checkStatus:
                return checkStatus
            del checkStatus

            listAnswer.update([(typeOf[1], getPattern.json())])

        return [listAnswer, typePattern]

    def sendMessage(self, subdomain, session, args):
        """
        Отправка сообщения по ID пользователя.

        :param subdomain: Поддомен eljur.ru                                               // str
        :param session:   Активная сессия пользователя                                    // Session

        :param args: Словарь, состоящий из:
                     receivers: ID пользователя. Если несколько, то через ;               // str
                     subject:   Тема сообщение (заглавие)                                 // str
                     message:   Сообщение                                                 // str


        :return: Словарь с ошибкой или bool ответ, в котором True - успешная смена пароля // dict или bool
        """

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

        url = f"https://{subdomain}.eljur.ru/journal-messages-compose-action"
        get_cookies = session.get(url, data={"_msg": "sent"})

        checkStatus = _checkStatus(get_cookies, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        pattern = {"csrf": get_cookies.cookies.values()[0],
                   "submit": "Отправить",
                   "cancel": "Отмена"}
        pattern.update(args)

        url = f"https://{subdomain}.eljur.ru/journal-messages-send-action/"
        send = session.post(url, data=pattern)

        checkStatus = _checkStatus(send, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        return True

    def getMessages(self, subdomain, session, args):
        """
        Получение сообщений пользователя.

        :param subdomain: Поддомен eljur.ru                                               // str
        :param session:   Активная сессия пользователя                                    // Session
        :param args: Словарь, состоящий из:
                     receivers: ID пользователя. Если несколько, то через ; без пробелов  // str
                     subject:   Тема сообщение (заглавие)                                 // str
                     message:   Сообщение                                                 // str


        :return: Словарь с ошибкой или bool ответ, в котором True - успешная смена пароля // dict или bool
        """
        return

    def deleteMessages(self, subdomain, session, args):
        """
        Удаление сообщения у пользователя.
        Внимание! Eljur удаляет сообщение ТОЛЬКО у пользователя (как если вы не выбрали "Также удалить у")
                  Получатель сможет прочитать сообщение даже после удаления у вас.

        :param subdomain: Поддомен eljur.ru                                               // str
        :param session:   Активная сессия пользователя                                    // Session
        :param args: Словарь, состоящий из:
                     0: ID сообщения. Если несколько, то через ; без пробелов             // str
                     1: Полученные/Отправленные (inbox/sent) Корзина (trash) не удаляется // str


        :return: Словарь с ошибкой или с ответом: // dict
                 result // bool
                 error  // str
        """

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

        pattern = {"method": "delete"}
        pattern.update(args)

        url = f"https://{subdomain}.eljur.ru/journal-messages-ajax-action/"
        delete = session.post(url, data=pattern)

        checkStatus = _checkStatus(delete, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        return delete.json()

    def recoverMessages(self, subdomain, session, args):
        """
        Возвращает сообщение из Корзины.

        :param subdomain: Поддомен eljur.ru                                               // str
        :param session:   Активная сессия пользователя                                    // Session
        :param args: Словарь, состоящий из:
                     0: ID сообщения. Если несколько, то через ; без пробелов             // str

        :return: Словарь с ошибкой или с ответом: // dict
                 result // bool
                 error  // str
        """

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

        pattern = {"method": "restore",
                   "1": "inbox"}
        pattern.update(args)

        url = f"https://{subdomain}.eljur.ru/journal-messages-ajax-action/"
        recover = session.post(url, data=pattern)

        checkStatus = _checkStatus(recover, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        return recover.json()