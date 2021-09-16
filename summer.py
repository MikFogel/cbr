from cbr_api import currency_holder, api_request
import requests
import xmltodict
import json
import datetime


class Rate:
    def __init__(self, rate, per):
        self.rate = rate 
        self.per = per 

    def __str__(self):
        return f"rate {self.rate} per{self.per}" 


class Summer:

    def __init__(self, total_sum: float, rate_list: list):
        self.total_sum = total_sum
        self.rate_list = rate_list

        self.total_tn_rub = 0.0

        print ("TOTAL SUM RUB", self.total_sum)
        for r in rate_list:
            print (r)

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
        print("+"*20)
        for r in self.rate_list:
            per_sum: float = round(self.total_sum * r.per / 100, 2)
            print (f"СУММА В ПРОЦЕНТАХ {per_sum}")

            per_sum_rate = round(per_sum * r.rate, 2)

            print (f"СУММА В ПРОЦЕНТАХ * КУРС {r.rate}: ", per_sum_rate)
            self.total_tn_rub += per_sum_rate


        r_total_no_vat = round(self.total_tn_rub, 2)
        r_vat = round(r_total_no_vat * 0.2, 2)
        r_total = round(r_total_no_vat + r_vat, 2)

        print(f"Общая без НДС: \t {r_total_no_vat}")
        print(f"НДС: \t {r_vat}")
        print(f"Общая с НДС: \t {r_total}")





    def capitalize_name(self):
        r = list()

        self.name = self.name.strip()
        for n in self.name.split(" "):
            nn = n[0].upper() + n[1:]
            r.append(nn)

        self.name = " ".join(r)
        self.save()


        try:
            this_visitor.capitalize_name()
        except Exception as e:
            send_notification('md@erfogel.ru', 'capitalize error', str(e))



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

                    print ("RATE", rate)

                    rate_list.append(Rate(rate, per))

        stop = Summer.stop_rate_list(rate_list)
    
    s = Summer(total_product_sum, rate_list)
    s.calculate()