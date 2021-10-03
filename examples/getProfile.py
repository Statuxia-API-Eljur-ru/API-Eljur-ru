from Eljur.auth import Authorization
from Eljur.profile import Profile


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

    profile = Profile()
    answ = profile.getProfile(subdomain, answer["session"])  # В ответ возвращает информацию о профиле пользователя.
    for i in answ:
        print(i, answ[i])


if __name__ == "__main__":
    run()
