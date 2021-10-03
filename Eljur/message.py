from Eljur.errors import _checkStatus, _checkSubdomain, _smallCheck


class Message:

    def schoolList(self, subdomain, session):
        """
        Получение тех, кому можем отправить сообщение.

        :param subdomain: Поддомен eljur.ru                                                // str
        :param session:   Активная сессия пользователя                                     // Session

        :return: Возвращает ошибку или массив из словарей возможных получателей сообщения. // list
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

        :param subdomain: Поддомен eljur.ru                                                      // str
        :param session:   Активная сессия пользователя                                           // Session

        :param args: Словарь, состоящий из:
                     receivers: ID пользователя. Если несколько, то через ;                      // str
                     subject:   Тема сообщение (заглавие)                                        // str
                     message:   Сообщение                                                        // str


        :return: Словарь с ошибкой или bool ответ, в котором True - успешная отправка соообщения // dict или bool
        """

        check = _smallCheck(subdomain, session, args)
        if not check:
            return check
        del check

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

        :param subdomain: Поддомен eljur.ru                                                  // str
        :param session:   Активная сессия пользователя                                       // Session
        :param args: Словарь, состоящий из:
                     "0": inbox/sent (полученные/отправленные)                               // str
                     "1": Текст заглавия                                                     // str
                     "2": Сколько сообщений показать (default: 20 / limit: 44)               // str
                     "3": С какого сообщение начало                                          // str
                     "4": 0 или id пользователя.                                             // str
                     "5": read/unread/trash (Прочитанные/Непрочитанные/Корзина)              // str
                     "6": ID пользователя, чьи сообщения мы хотим получить.                  // str
                     "7": Дата (false, today, week, month, two_month, year)                  // str

        :return: Словарь с ошибкой или с сообщениями                                         // dict
        """

        pattern = {"method": "getList",
                   "2": "20"}

        check = _smallCheck(subdomain, session, args)
        if check:
            return check
        del check

        pattern.update(args)

        url = f"https://{subdomain}.eljur.ru/journal-messages-ajax-action"
        send = session.post(url, data=pattern)

        checkStatus = _checkStatus(send, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        return send.json()

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

        check = _smallCheck(subdomain, session, args)
        if not check:
            return check
        del check

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

        check = _smallCheck(subdomain, session, args)
        if not check:
            return check
        del check

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
