from Eljur.auth import auth
from Eljur.message import school_list, send_message


def checkList(answer):
    myList = school_list(answer)
    print(myList[2])
    choose = input("Выберите чей список вывести: ")

    if choose not in myList[1]:
        return
    print(choose, len(myList[1][choose]["user_list"]))
    for user in myList[1][choose]["user_list"]:
        print(f"{user['id']}: {user['firstname']} {user['lastname']}")
    print("")


def sendMessage(answer):

    senderID = input("Введите ID пользователя, которому нужно отправить сообщение: ")
    send_message(answer, senderID)


def run():

    data = {
        "username": input("Username: "),
        "password": input("Password: ")
    }
    subdomain = "klgd"

    answer = auth(subdomain, data)

    if "error" in answer:
        return print(answer)

    if not answer["answer"]["user"]["uid"]:
        return print("Не удалось залогиниться")

    checkList(answer)
    sendMessage(answer)


if __name__ == "__main__":
    run()
