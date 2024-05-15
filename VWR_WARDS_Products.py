import re
from zenrows import ZenRowsClient
from module_package import *

if __name__ == '__main__':
    timestamp = datetime.now().date().strftime('%Y%m%d')
    file_name = os.path.basename(__file__).rstrip('.py')
    url = 'https://us.vwr.com/store/catalog/vwr_products.jsp'
    base_url = 'https://us.vwr.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    soup = get_soup(url, headers)
    content = soup.find_all('ul', class_='a-z_categorylist')
    for single_content in content:
        inner_content = single_content.find_all('a')
        for single_url in inner_content:
            if 'antibodies/3617058' not in str(single_url):
                main_url = f'{base_url}{single_url["href"]}'
                print(f'main_url---------------->{main_url}')
                if main_url in read_log_file():
                    continue
                inner_request = get_soup(main_url, headers)
                if inner_request is None:
                    continue
                if inner_request.find('div', class_='col-xs-12 col-sm-3 pagination-label'):
                    '''GET PAGINATION'''
                    page_tag = strip_it(inner_request.find('div', class_='col-xs-12 col-sm-3 pagination-label').text.replace(',', ''))
                    page_split = page_tag.split('of', 1)
                    count = page_split[-1].strip()
                    page_count = page_split[0].split('-', 1)[-1].strip()
                    total_pages = math.ceil(int(count) / int(page_count))
                    for i in range(1, int(total_pages) + 1):
                        page_link = f'{main_url}?pageNo={i}'
                        page_req = requests.get(page_link, headers=headers)
                        # if page_req.status_code == 403:
                        #     if page_link in read_log_file():
                        #         continue
                        #     print(f'page_link---------->{page_link}')
                        #     client = ZenRowsClient("fc1986867778e315fafa412073e0816b3661753e")
                        #     params = {"js_render": "true", "premium_proxy": "true"}
                        #     response = client.get(page_link, params=params)
                        #     page_soup = BeautifulSoup(response.text, 'html.parser')
                        #     '''PRODUCT URL'''
                        #     url_href = page_soup.find_all('h2', class_='search-item__title h4')
                        #     for single_href in url_href:
                        #         main_name = single_href.a.text.strip()
                        #         product_url = f'{base_url}{single_href.a["href"]}'
                        #         split_href = str(product_url).rsplit('/', 1)[0].split('product/')[-1].strip()
                        #         request_url = f'https://us.vwr.com/store/services/catalog/json/stiboOrderTableRender.jsp?productId={split_href}&catalogNumber=&discontinuedflag=&hasItemPages=false&specialCertRender=false&staticPage='
                        #         print(product_url)
                        #         if product_url in read_log_file():
                        #             continue
                        #         product_request = get_soup(request_url, headers)
                        #         if product_request is None:
                        #             continue
                        #         product_content = product_request.find_all('table',
                        #                                                    class_='table-stack table table-responsive table-product mb-2')
                        #         for single_product_content in product_content:
                        #             inner_data = single_product_content.find_all('tr', class_='product-row-main')
                        #             for single_data in inner_data:
                        #                 if single_data.find('td', attrs={'data-title': 'VWR Catalog Number'}):
                        #                     '''PRODUCT NAME'''
                        #                     if single_data.find('td', attrs={'data-title': 'Description'}):
                        #                         description_name = single_data.find('td', attrs={
                        #                             'data-title': 'Description'}).text.strip()
                        #                         if re.search('^\d+', str(description_name)):
                        #                             description_name = f'{main_name} {description_name}'
                        #                         else:
                        #                             description_name = description_name
                        #                         if single_data.find('td', attrs={'data-title': 'Color'}):
                        #                             color_name = single_data.find('td', attrs={'data-title': 'Color'}).text.strip()
                        #                             product_name = f'{description_name} {color_name}'
                        #                         else:
                        #                             product_name = description_name
                        #                     elif single_data.find('td', attrs={'data-title': 'Volume'}):
                        #                         inner_name = single_data.find('td', attrs={'data-title': 'Volume'}).text.strip()
                        #                         product_name = f'{main_name}-{inner_name}'
                        #                     elif single_data.find('td', attrs={'data-title': 'Size'}):
                        #                         inner_name = single_data.find('td', attrs={'data-title': 'Size'}).text.strip()
                        #                         product_name = f'{main_name}-{inner_name}'
                        #                     elif single_data.find('td', attrs={'data-title': 'Size'}):
                        #                         inner_name = single_data.find('td', attrs={'data-title': 'Length'}).text.strip()
                        #                         product_name = f'{main_name}-{inner_name}'
                        #                     else:
                        #                         product_name = main_name
                        #                     '''PRODUCT QUANTITY'''
                        #                     product_quantity = '1'
                        #                     '''PRODUCT ID'''
                        #                     product_item = single_data.find('td', attrs={'data-title': 'VWR Catalog Number'})
                        #                     product_id = strip_it(product_item.text)
                        #                     id_tag = product_item.find('span')['id'].replace("['", '').replace("']", '').split('_', 1)[-1].split('_', 1)[0].strip()
                        #                     product_req_url = f'https://us.vwr.com/store/services/pricing/json/skuPricing.jsp?skuIds={id_tag}&salesOrg=8000&salesOffice=0000&profileLocale=en_US&promoCatalogNumber=&promoCatalogNumberForSkuId=&forcePromo=false'
                        #                     price_request = get_json_response(product_req_url, headers)
                        #                     for single_price in price_request:
                        #                         product_price = single_price['salePrice']
                        #                         print('current datetime------>', datetime.now())
                        #                         dictionary = get_dictionary(product_ids=product_id, product_names=product_name, product_quantities=product_quantity, product_prices=product_price, product_urls=product_url)
                        #                         articles_df = pd.DataFrame([dictionary])
                        #                         articles_df.drop_duplicates(subset=['product_id', 'product_name'], keep='first',
                        #                                                     inplace=True)
                        #                         if os.path.isfile(f'{file_name}.csv'):
                        #                             articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                        #                         else:
                        #                             articles_df.to_csv(f'{file_name}.csv', index=False)
                        #                         write_visited_log(product_url)
                        #     write_visited_log(page_link)
                        if page_req.status_code == 200:
                            page_soup = get_soup(page_link, headers)
                            '''PRODUCT URL'''
                            url_href = page_soup.find_all('h2', class_='search-item__title h4')
                            for single_href in url_href:
                                main_name = single_href.a.text.strip()
                                product_url = f'https://us.vwr.com{single_href.a["href"]}'
                                print(product_url)
                                split_href = str(product_url).rsplit('/', 1)[0].split('product/')[-1].strip()
                                request_url = f'https://us.vwr.com/store/services/catalog/json/stiboOrderTableRender.jsp?productId={split_href}&catalogNumber=&discontinuedflag=&hasItemPages=false&specialCertRender=false&staticPage='
                                product_request = get_soup(request_url, headers)
                                if product_request is None:
                                    continue
                                product_content = product_request.find_all('tr', class_='product-row-main')
                                for single_data in product_content:
                                    if single_data.find('td', attrs={'data-title': 'VWR Catalog Number'}):
                                        '''PRODUCT ID'''
                                        product_item = single_data.find('td', attrs={'data-title': 'VWR Catalog Number'}).extract()
                                        try:
                                            extract_tag = single_data.find('td', attrs={'data-title':'Unit'}).extract()
                                        except:
                                            extract_tag = ''
                                        try:
                                            other_extract = single_data.find('td', attrs={'data-title':'Quantity'}).extract()
                                        except:
                                            other_extract = ''
                                        try:
                                            price_extract = single_data.find('td', attrs={'data-title': 'Price'}).extract()
                                        except:
                                            price_extract = ''
                                        '''PRODUCT NAME'''
                                        try:
                                            data_tag = single_data.find_all('td')
                                            name_list = []
                                            for single_title in data_tag:
                                                content_text = single_title.text.strip()
                                                name_list.append(content_text)
                                            product_name = ' '.join(name_list)
                                        except:
                                            product_name = main_name
                                        '''PRODUCT QUANTITY'''
                                        product_quantity = '1'
                                        product_id = strip_it(product_item.text)
                                        if product_id in read_log_file():
                                            continue
                                        id_tag = product_item.find('span')['id'].replace("['", '').replace("']", '').split('_', 1)[-1].split('_', 1)[0].strip()
                                        product_req_url = f'https://us.vwr.com/store/services/pricing/json/skuPricing.jsp?skuIds={id_tag}&salesOrg=8000&salesOffice=0000&profileLocale=en_US&promoCatalogNumber=&promoCatalogNumberForSkuId=&forcePromo=false'
                                        price_request = get_json_response(product_req_url, headers)
                                        for single_price in price_request:
                                            product_price = single_price['salePrice']
                                            print('current datetime------>', datetime.now())
                                            dictionary = get_dictionary(product_ids=product_id, product_names=product_name, product_quantities=product_quantity, product_prices=product_price, product_urls=product_url)
                                            articles_df = pd.DataFrame([dictionary])
                                            articles_df.drop_duplicates(subset=['product_id', 'product_name'], keep='first',
                                                                        inplace=True)
                                            if os.path.isfile(f'{file_name}.csv'):
                                                articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                                            else:
                                                articles_df.to_csv(f'{file_name}.csv', index=False)
                                            write_visited_log(product_id)
                write_visited_log(main_url)
