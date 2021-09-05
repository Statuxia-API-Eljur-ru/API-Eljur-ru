from Eljur.auth import Authorization
from Eljur.profile import Profile, Settings


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

    profile = Profile()
    info = profile.getProfile(answer["subdomain"], answer["session"])

    for key in info:
        print(key, info[key])

    settings = Settings()
    aa = settings.switcher(answer["subdomain"], answer["session"], 0, False)
    print(aa)


if __name__ == "__main__":
    run()
