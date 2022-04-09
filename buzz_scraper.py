# pip install httplib2
# pip install wget
# pip install bs4

import os
import httplib2
import wget
from bs4 import BeautifulSoup, SoupStrainer

def get_zip_url_list(url):
    zip_url_list = []
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            if ".zip" in link['href']:
                zip_url_list.append(link['href'])
    return zip_url_list

def download_from_url(zip_url_list):
    downloaded_list = []
    skipped_list = []
    failed_list = []
    for href in zip_url_list:
        try:
            filename = href.split('/')[-1]
            if filename in os.listdir():
                print(f'{filename} already exists, skipping...')
                if not filename in skipped_list:
                    skipped_list.append(filename)
            else:
                print(f'\nDownloading: {str(href)}')
                wget.download(str(href))
                downloaded_list.append(href)
        except Exception as e:
            failed_list.append(href)
            if '404' in e:
                print(f'Unable to download file, {href}, HTTP Error 404...')
            else:
                print('Error' + str(e))
    return (downloaded_list, failed_list, skipped_list)

def print_results(results):
    downloaded_list, failed_list, skipped_list = results
    print('\n--------------------DOWNLOADED--------------------')
    for url in downloaded_list:
        print(url)
    print('--------------------SKIPPED---------------------')
    for url in skipped_list:
        print(url)
    print('\n--------------------FAILED---------------------')
    for url in failed_list:
        print(url)
    print('\n--------------------SUMMARY---------------------')
    print(f'D: {len(downloaded_list)} | S: {len(skipped_list)} | F: {len(failed_list)}')

    try:
        with open('summary.txt', 'w') as filehandle:
            filehandle.writelines(f'D: {len(downloaded_list)} | S: {len(skipped_list)} | F: {len(failed_list)}\n')
            filehandle.writelines('FAILED: %s\n' % failed for failed in failed_list)
            filehandle.writelines('SKIPPED: %s\n' % skipped for skipped in skipped_list)
            filehandle.writelines('DOWNLOADED: %s\n' % downloaded for downloaded in downloaded_list)
    except Exception as e:
        print('Unable to write summary to file...')
        print(e)
        


url = "https://www.3dbuzz.com/"
zip_url_list = get_zip_url_list(url)
results = download_from_url(zip_url_list)
print_results(results)






