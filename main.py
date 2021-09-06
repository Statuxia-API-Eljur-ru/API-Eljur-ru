from Eljur.auth import Authorization
from Eljur.profile import Security


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

    settings = Security()
    aa = settings.changePassword(answer["subdomain"], answer["session"], data["password"], input("New Password: "))
    print(aa)


if __name__ == "__main__":
    run()
