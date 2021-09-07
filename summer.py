from cbr_api import currency_holder, api_request
import requests
import xmltodict
import json
import datetime


class Rate:
    def __init__(self, rate, per):
        self.rate = rate 
        self.per = per 


class Summer:

    def __init__(self, total_sum: float, rate_list: list):
        self.total_sum = total_sum
        self.rate_list = rate_list

        self.total_tn_rub = float()

    @classmethod
    def stop_rate_list(cls, rate_list: list):
        if rate_list:
            sm = sum([r.per for r in rate_list]) 

            if sm > 100:
                raise ValueError("Input Error")

            return sm == 100
        else:
            return False
            


    def calculate(self):
        for r in self.rate_list:
            self.total_tn_rub += (self.total_sum * r.per / 100) * r.rate 


        r_total_no_vat = round(self.total_tn_rub, 2)
        r_vat = round(r_total_no_vat * 0.2, 2)
        r_total = round(r_total_no_vat + r_vat, 2)

        print(f"Total without VAT: \t {r_total_no_vat}")
        print(f"Total VAT: \t {r_vat}")
        print(f"Total without VAT: \t {r_total}")



if __name__ == "__main__":

    total_product_sum = float(input("Введите общую сумму >> "))

    rate_list = list()
    
    user_input = -1

    print ("Введите q чтобы закончить создание списка")

    stop = False

    while user_input != "q" and not stop:
        print("Сегодня: \tENTER")
        print("Вчера: \ty")
        user_input = str(input("Введите дату ДД/ММ/ГГГГ >> "))

        if user_input != "q":

            if user_input == "":
                print("Отображаем данные на сегодняшний день")
                user_input = datetime.date.today().strftime('%d/%m/%Y')

            elif user_input == "y":
                print("Отображаем данные на вчерашний день")
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                user_input = yesterday.strftime('%d/%m/%Y')

            request_api = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={user_input}"
            api_data = api_request(request_api)
            result = json.loads(json.dumps(xmltodict.parse(api_data)))

            for cur in result['ValCurs']['Valute']:
                if cur['NumCode'] == "978":
                    try:
                        per = float(input("% от пп >> "))
                    except ValueError:
                        per = 50.0

                    rate = float(cur['Value'].replace(",", '.'))

                    rate_list.append(Rate(rate, per))

        stop = Summer.stop_rate_list(rate_list)
    
    s = Summer(total_product_sum, rate_list)
    s.calculate()