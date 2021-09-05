def school_list(answer):
    """Получение тех, кому можем отправить сообщение.

    :param answer: словарь, в котором обязательно должен быть:
                   session: сессия с успешным подключением // Session
                   subdomain: поддомен eljur.ru // str
    :return: возвращает массив из словарей возможных получателей сообщения.
    """

    pattern = {"0": "school",
               "1": "null",
               "2": "null",
               "3": "null"}
    typePattern = ["classruks", "administration", "specialists", "ext_5_teachers", "teachers", "parents", "students"]
    list_answer = {}

    for typeOf in enumerate(typePattern):
        if typeOf[0] == 4:
            pattern["2"] = "1"

        pattern["1"] = typePattern[typeOf[0]]
        list_answer.update([(typeOf[1], answer["session"].post(
            url=f"https://{answer['subdomain']}.eljur.ru/journal-messages-ajax-action?method=getRecipientList",
            data=pattern).json())])

    return [answer, list_answer, typePattern]


def send_message(answer, sender_id):
    """Отправка сообщения по ID пользователя.

    :param sender_id: ID пользователя // str
    :param answer: словарь, в котором обязательно должен быть:
                   session: сессия с успешным подключением // Session
                   subdomain: поддомен eljur.ru // str

    :return: None (Отправляет сообщение пользователю)
    """

    get_cookies = answer["session"].get(
        url=f"https://{answer['subdomain']}.eljur.ru/journal-messages-compose-action",
        data={"_msg": "sent"})

    data = {"csrf": get_cookies.cookies.values()[0],
            "subject": "Test Message",
            "receivers": sender_id,
            "message": "Это сообщение было отправлено через API-Eljur-ru",
            "submit": "Отправить",
            "cancel": "Отмена"}

    answer["session"].post(
        url=f"https://{answer['subdomain']}.eljur.ru/journal-messages-send-action/",
        data=data)
