from Eljur.auth import Authorization
from Eljur.portfolio import Portfolio


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

    portfolio = Portfolio()
    answ = portfolio.reportCard(subdomain, answer["session"], answer["answer"]["user"]["uid"])  # В ответ получает оценки ученика или ошибку.
    for i in answ:
        print(i, answ[i])


if __name__ == "__main__":
    run()
