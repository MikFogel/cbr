import requests
import xmltodict
import json
import datetime


class Currency:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.rate = None

    def set_rate(self, rate: float):
        self.rate = rate
        print (f"Добавлено {self.name}")

    def convert(self, value):
        if self.rate:
            return round(value / self.rate, 2)

    def __repr__(self):
        return self.name


currency_holder = [

    Currency("Евро", "978"), Currency("Доллар США", "840")

]


def api_request(api_url: str):
    r = requests.get(api_url)
    return r.content


if __name__ == "__main__":

    selected_currency = -1

    date = str(input("Введите дату ДД/ММ/ГГГГ >> "))

    if not date:
        print("Отображаем данные на сегодняшний день")
        date = datetime.date.today().strftime('%d/%m/%Y')

    request_api = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"

    api_data = api_request(request_api)
    result = json.loads(json.dumps(xmltodict.parse(api_data)))

    for cur in result['ValCurs']['Valute']:
        for c in currency_holder:
            if c.code == cur['NumCode']:
                c.set_rate(float(cur['Value'].replace(",", '.')))

    print ("Данные успешно загружены")

    for ind, c in enumerate(currency_holder):
        if c.rate is not None:
            print (ind, c.name)

    selected_currency = int(input("Выберете валюту >> "))
    convert_value = float(input("Введите значение в рублях >> ").replace(",", "."))

    selected_cur_obj = currency_holder[selected_currency]

    res = selected_cur_obj.convert(convert_value)

    print (f"КУРС ЦБ РФ {convert_value} РУБ = ", res, selected_cur_obj.name, date)
