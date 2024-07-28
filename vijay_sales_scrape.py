import requests, pymysql
from lxml import html
from pymysql.constants import CLIENT
from db_maker import store_create_query, city_create_query


class Scraper:
    def __init__(self):
        self.client = pymysql.connect(
            host='localhost',
            user='root',
            database='bc_registry_db',
            password='actowiz',
            charset='utf8mb4',
            autocommit=True,
            client_flag=CLIENT.MULTI_STATEMENTS
        )
        if self.client.open:
            print('Database connection Successful!')
        else:
            print('Database connection Un-Successful.')
        self.cursor = self.client.cursor()

    def db_schema_creater(self):
        self.cursor.execute(query=store_create_query)
        print('Pincodes Table created!')
        self.cursor.execute(query=city_create_query)
        print('BC Registry Table created!')

    def pincodes_fetcher(self, table_name: str, status_column: str):
        # Fetching all data from countries table
        select_query = f'''SELECT * FROM `{table_name}` WHERE {status_column} = 'Pending' and id between 1 and 20000;'''
        self.cursor.execute(select_query)
        data = self.cursor.fetchall()
        return data

    def store_fetcher(self):
        self.cursor.execute(store_create_query)
        payload_cities_list = self.cities_links()[0]
        city_names_list = self.cities_links()[1]
        for payload_elm, city_name in zip(payload_cities_list, city_names_list):

            cookies = {
                'ASP.NET_SessionId': 'tsuavjv3mymtnhwydcnmxyzi',
                '__AntiXsrfToken': '592142be1ae14639814016f873e2fd5b',
                '_gcl_au': '1.1.1829552125.1720758105',
                '_fbp': 'fb.1.1720758104658.31307737453560972',
                'unbxd.userId': 'uid-1720758104703-55234',
                '_nv_did': '38961852.1720758112.2710910106tydxr',
                '_ga': 'GA1.1.1975545346.1720758105',
                '_clck': '8lf40h%7C2%7Cfne%7C0%7C1654',
                'locationErro': 'locationErro=1',
                'mycity': 'cityId=1&city=Mumbai&IsPreOrder=false&isDefault=true',
                'UPinT': 'pin=400001',
                'UPinCode': 'pinC=400001',
                'mycityclose': 'true',
                '_nv_push_neg': '1',
                '_nv_push_times': '1',
                'Mypreurl': '',
                '_ga_NGYSNQ94RW': 'GS1.1.1720770370.3.0.1720770370.0.0.0',
                '_uetsid': '3f83e6c0400611efab2fff9327ca4417|ok7gxt|2|fne|0|1654',
                '_nv_sess': '38961852.1720770377.GlgCmSDeivmNJr1u1ilD9ANoC9d1M1kRLPn1weOmOMTFWlzOaM',
                '_nv_uid': '38961852.1720758112.e6944f14-7915-4158-a37b-be68a7108d0d.1720765371.1720770377.3.0',
                '_nv_utm': '38961852.1720758112.3.1.dXRtc3JjPShkaXJlY3QpfHV0bWNjbj0oZGlyZWN0KXx1dG1jbWQ9KG5vbmUpfHV0bWN0cj0obm90IHNldCl8dXRtY2N0PShub3Qgc2V0KXxnY2xpZD0obm90IHNldCk=',
                '_nv_hit': '38961852.1720770377.cHZpZXc9MQ==',
                'unbxd.visit': 'repeat',
                'unbxd.visitId': 'visitId-1720770371171-55508',
                '_ga_RV15QMQZZZ': 'GS1.1.1720769452.3.1.1720770371.59.0.523670936',
                '_clsk': 'ssbrqy%7C1720770372082%7C3%7C0%7Cx.clarity.ms%2Fcollect',
                '_uetvid': '3f848e30400611ef97960fee7019604a|155j26h|1720770372090|3|1|bat.bing.com/p/insights/c/x',
                'AWSALB': 'K35rrHWCEyqXVYdwlSJW6c3Dt45nMrcHQvlHSCOyn/Val/it/mqeicHL5oW4oEQlBQ2LNR9/gL+hfvNjV143+Ue7f583allzXrJiUWy0zjcIK5zaq9cfay3X1P79',
                'AWSALBCORS': 'K35rrHWCEyqXVYdwlSJW6c3Dt45nMrcHQvlHSCOyn/Val/it/mqeicHL5oW4oEQlBQ2LNR9/gL+hfvNjV143+Ue7f583allzXrJiUWy0zjcIK5zaq9cfay3X1P79',
            }

            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://www.vijaysales.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://www.vijaysales.com/store-locator',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            response = requests.post(
                'https://www.vijaysales.com/Store-Locator.aspx/getStoreStruct_Web',
                cookies=cookies,
                headers=headers,
                json=payload_elm,
            )
            html_text = response.json().get('d').encode().decode('unicode_escape')
            parsed_html = html.fromstring(html_text)
            store_list = parsed_html.xpath("//div[@class='col-xs-12 dv-location']")
            for this_store in store_list:
                store_address = this_store.xpath('./div[@class="col-xs-9 location-text-content"]/div[@class="row"]/text()')[0]
                store_contact_no = this_store.xpath('.//a[@class="lnkStpB4Unload"]/text()')[0].replace(' ', '')
                print(store_contact_no)
                area_name = this_store.xpath("./h6[@class='h5 text-uppercase location-head']/text()")[0].strip()
                try:
                    insert_query = f'''INSERT INTO store_data (store_address, store_contact_no, area_name, city_name) VALUES ('{store_address}', {int(store_contact_no)}, '{area_name}', '{city_name}');'''
                    print(insert_query)
                    self.cursor.execute(query=insert_query)
                except Exception as e:
                    print(e)

            # update city status to done
            update_query = f'''UPDATE cities_status
                                SET city_status = 'Done'
                                WHERE city_name = '{city_name}';'''
            self.cursor.execute(update_query)
            print('-' * 10)


print(Scraper().db_schema_creater())
print(Scraper().store_fetcher())
