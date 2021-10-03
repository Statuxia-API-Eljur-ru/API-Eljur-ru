from Eljur.auth import Authorization


def run():
    authorisation = Authorization()

    data = {
        "username": input("Username: "),
        "password": input("Password: ")
    }
    subdomain = input("Subdomain: ")

    answer = authorisation.login(subdomain, data)  # В ответ получает успешный логин с доп. информацией или ошибку.
    if "session" not in answer:
        print(answer)
        return
    print(answer)


if __name__ == "__main__":
    run()
