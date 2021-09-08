from Eljur.auth import Authorization
from Eljur.message import Message


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

    message = Message()
    answ = message.getMessages(subdomain, answer["session"], {})
    print(answ)


if __name__ == "__main__":
    run()
