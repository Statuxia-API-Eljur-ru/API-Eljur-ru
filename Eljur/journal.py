from Eljur.errors import _fullCheck, _checkInstance


class Journal:

    def journal(self, subdomain, session, week=0):
        """
        Получение страницы дневника с расписанием, оценками и другой информации.

        :param subdomain: Поддомен eljur.ru                                                                           // str
        :param session:   Активная сессия пользователя                                                                // Session
        :param week:      Нужная вам неделя (0 - нынешняя, -1 - предыдущая, 1 - следующая). По умолчанию 0 (нынешняя) // str

        :return: Словарь с ошибкой или с расписанием пользователя:                                                    // dict
                 answer // dict
                 result // bool
        """
        checkWeek = _checkInstance(week, int)
        if "error" in checkWeek:
            return checkWeek
        del checkWeek

        url = f"https://{subdomain}.eljur.ru/journal-app/week.{week * -1}"

        soup = _fullCheck(subdomain, session, url)
        if "error" in soup:
            return soup

        info = {}
        for day in soup.find_all("div", class_="dnevnik-day"):
            title = day.find("div", class_="dnevnik-day__title")
            week, date = title.contents[0].strip().replace("\n", "").split(", ")

            if day.find("div", class_="page-empty"):
                info.update([(week, {"date": date, "isEmpty": True, "comment": "Нет уроков", "lessons": {}})])
                continue

            if day.find("div", class_="dnevnik-day__holiday"):
                info.update([(week, {"date": date, "isEmpty": True, "comment": "Выходной", "lessons": {}})])
                continue

            lessons = day.find_all("div", class_="dnevnik-lesson")
            lessonsDict = {}
            if lessons:
                for lesson in lessons:
                    lessonNumber = lesson.find("div", class_="dnevnik-lesson__number dnevnik-lesson__number--time")
                    if lessonNumber:
                        lessonNumber = lessonNumber.contents[0].replace("\n", "").strip()[:-1]

                    lessonTime = lesson.find("div", class_="dnevnik-lesson__time").contents[0].strip().replace("\n", "")
                    lessonName = lesson.find("span", class_="js-rt_licey-dnevnik-subject").contents[0]

                    lessonHomeTask = lesson.find("div", class_="dnevnik-lesson__task")
                    if lessonHomeTask:
                        lessonHomeTask = lessonHomeTask.contents[2].replace("\n", "").strip()

                    lessonMark = lesson.find("div", class_="dnevnik-mark")
                    if lessonMark:
                        lessonMark = lessonMark.contents[1].attrs["value"]

                    lessonsDict.update([(lessonNumber, {"time": lessonTime,
                                                        "name": lessonName,
                                                        "hometask": lessonHomeTask,
                                                        "mark": lessonMark})])

                info.update([(week, {"date": date, "isEmpty": False, "comment": "Выходной", "lessons": lessonsDict})])

        return info
