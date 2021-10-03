from Eljur.auth import Authorization
from Eljur.journal import Journal


def run():
    authorisation = Authorization()

    data = {
        "username": input("Username: "),
        "password": input("Password: ")
    }
    subdomain = input("Subdomain: ")

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return

    journal = Journal()
    answ = journal.journal(subdomain, answer["session"])  # В ответ получает нынешнюю неделю или ошибку.
    for i in answ:
        print(i, answ[i])


if __name__ == "__main__":
    run()
