import requests
import pandas as pd

# функция для получения данных с сайта
def get_category():
    # параметры удобно сконвертил с помощью https://curlconverter.com/
    cookies = {
    'x_wbaas_token': '1.1000.f920b5dfbe6e406a9ae4d06273addd3a.MHwxNDcuNDUuMTk5LjcwfE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDMuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzY5Mzg2NzAyfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc2ODc4MTkwMnwx.MEQCIF2nQ8hRcPIl9FEru3dan50UiqO1ATgPAWkqxaEka+znAiBj8fceK4JEOJc7LHmh+rDX1P/BQh4pv+m6n+YoN0ocKQ==',
    '_wbauid': '10698188481768177106',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9',
        'deviceid': 'site_dd8cb8e1afbc4ed2896c6983f47ce497',
        'priority': 'u=1, i',
        'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE%20%D0%B8%D0%B7%20%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'x-queryid': 'qid1069818848176817710620260112001826',
        'x-requested-with': 'XMLHttpRequest',
        'x-spa-version': '13.19.4',
        'x-userid': '0',
        # 'cookie': 'x_wbaas_token=1.1000.f920b5dfbe6e406a9ae4d06273addd3a.MHwxNDcuNDUuMTk5LjcwfE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDMuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzY5Mzg2NzAyfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc2ODc4MTkwMnwx.MEQCIF2nQ8hRcPIl9FEru3dan50UiqO1ATgPAWkqxaEka+znAiBj8fceK4JEOJc7LHmh+rDX1P/BQh4pv+m6n+YoN0ocKQ==; _wbauid=10698188481768177106',
    }
    params = {
    'ab_testing': 'false',
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'hide_dtype': '9',
    'hide_vflags': '4294967296',
    'inheritFilters': 'false',
    'lang': 'ru',
    'page': '1',
    'query': 'пальто из натуральной шерсти',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
    }
    
    response = requests.get(
    'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search',
    params=params,
    cookies=cookies,
    headers=headers,
    )

    #return response.status_code
    return response.json()

# функция для сохранения в XLSX-файл
def save(data, filename='products.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, sheet_name='Товары')
    print(f"Файл сохранен: {filename}")

# функция для сохранения отфильтрованного каталога в XLSX-файл
def sorted_file(filename='products.xlsx', sorted_filename='filtered_products.xlsx', min_rating=4.5, max_price=10000):
    df = pd.read_excel(filename)
    sorted_df = df[(df['Рейтинг'] >= min_rating) & (df['Цена'] <= max_price)]
    sorted_df.to_excel(sorted_filename, index=False, sheet_name='Отфильтрованные товары')
    print(f"Файл сохранен: {sorted_filename}")

def main():
    response = get_category()
    data = []
    for element in response.get('products'):
        data.append({
            'Ссылка на товар': f'https://www.wildberries.ru/catalog/{element.get("id")}/detail.aspx',
            'Артикул': element.get("id"),
            'Название': element.get("name"),
            'Цена': int(element.get('sizes')[0].get('price').get('product'))//100,
            'Название селлера': element.get("brand"),
            'Ссылка на селлера': f'https://www.wildberries.ru/brands/{element.get("name")}',
            'Размеры товара': ', '.join([i.get('origName') for i in element.get("sizes")]),
            'Остатки по товару': element.get("totalQuantity"),
            'Рейтинг': element.get("reviewRating"),
            'Количество отзывов': element.get("feedbacks"),
            })
        
    save(data)


if __name__ == '__main__':
    main()
    sorted_file()
