class Timetable:

    def timetable(self, subdomain, session, week):
        """
        Получение страницы расписания.

        :param week:      Нужная вам неделя (even, odd, both)      // str
        :param subdomain: Поддомен eljur.ru                        // str
        :param session:   Активная сессия пользователя             // Session

        :return: Словарь с ошибкой или с расписанием пользователя: // dict
                 answer // dict
                 result // bool
        """
        return

    def journal(self, subdomain, session, week=0):
        """
        Получение страницы дневника с расписанием и оценками.

        :param subdomain: Поддомен eljur.ru                                             // str
        :param session:   Активная сессия пользователя                                  // Session
        :param week:      Нужная вам неделя (0, -1, 3 и.т.д). По умолчанию 0 (нынешняя) // str

        :return: Словарь с ошибкой или с расписанием пользователя:                      // dict
                 answer // dict
                 result // bool
        """
        return
