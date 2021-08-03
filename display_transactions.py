# test.py
#
# Десериализируем JSON
# Удаляем пустые транзакции
# Сортируем по дате
# Отбираем нужные
# Редактируем
# Выводим

import json
import datetime

# получаем дату для сортировки


def get_date(transaction):
    date = datetime.datetime.strptime(
        transaction.get("date"), "%Y-%m-%dT%H:%M:%S.%f")
    return date

# скрываем часть цифр в номерах


def get_covert_transaction(transaction):
    transaction["date"] = covert_date(transaction.get("date"))

    if transaction.get("from") is not None:
        transaction["from"] = covert_spot(transaction.get("from"))

    transaction["to"] = covert_spot(transaction.get("to"))

    covert_transaction = transaction
    return covert_transaction

# скрываем подробное врямя


def covert_date(string_date):
    date = datetime.datetime.strptime(
        string_date, "%Y-%m-%dT%H:%M:%S.%f")
    return date.strftime("%d.%m.%Y")

# скрываем часть цифр в номере карты


def covert_card(string_spot):
    reversed_strint_spot = string_spot[-1:-5:-1] + \
        " **** **" + string_spot[-11:-13:-1] + ' ' + string_spot[-13::-1]
    covert_card = "".join(reversed((reversed_strint_spot)))
    return covert_card

# скрываем часть цифр в номере счета


def covert_account(string_spot):
    covert_account = string_spot[:4] + " **" + string_spot[21:]
    return covert_account

# скрываем часть номера


def covert_spot(string_spot):
    if string_spot[-1:-21:-1].isdigit():
        covert_spot = covert_account(string_spot)
    else:
        covert_spot = covert_card(string_spot)
    return covert_spot


def if_None(nominal):
    if nominal is None:
        return ""
    else:
        return nominal


# выводим транзакции по одной
def get_last_transactions(number):
    with open("operations.json", "rb") as read_file:
        transactions = json.load(read_file)
    del read_file

    # удаляем пустые словари
    transactions = list(filter(None, transactions))
    # сортируем объект по дате
    transactions.sort(key=get_date, reverse=True)
    # выводим по одной
    for counter, transaction in enumerate(transactions):
        if transaction["state"] == "CANCELED":
            number += 1
            continue
        if counter == number:
            break
        covert_transaction = get_covert_transaction(transaction)

        date = covert_transaction["date"]
        description = covert_transaction.get("description")
        string_from = if_None(covert_transaction.get("from"))
        to = covert_transaction.get("to")
        amount = covert_transaction.get("operationAmount").get("amount")
        name = covert_transaction.get(
            "operationAmount").get("currency").get("name")

        print(f"{date} {description}\n"
              f"{string_from} -> {to}\n"
              f"{amount} {name}")
        print()


def main():
    # выводим список последних совершенных транзакций
    get_last_transactions(5)


if __name__ == '__main__':
    main()
