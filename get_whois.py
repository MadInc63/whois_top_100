import requests
from urllib.parse import urlsplit
from bs4 import BeautifulSoup


def fetch_page(url, words):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36',
        'Accept-Language': 'ru,en;q=0.9'
    }
    data = {
        'yes': '1',
        'keys': words,
        'city': '213',
        'depth': '100'
    }
    return requests.post(url, headers=headers, data=data)


def fetch_page_whois(url, domain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36',
        'Accept-Language': 'ru,en;q=0.9'
    }
    data = {
        'doms': domain
    }
    return requests.post(url, headers=headers, data=data)


def get_all_links(html_raw):
    soup = BeautifulSoup(html_raw, 'html.parser')
    words_tag = soup.find_all('table', {'class': 'table'})
    links = []
    for word_tag in words_tag:
        for link in word_tag.find_all('a', href=True):
            if link['href']:
                links.append(link['href'])
    return links


def get_domain(links_list):
    all_domain = []
    for link in links_list:
        all_domain.append(urlsplit(link).netloc)
    return list(set(all_domain))


def get_whois_domain(html_raw):
    soup = BeautifulSoup(html_raw, 'html.parser')
    domains_tag = soup.find('table', {'class': 'tablesorter'}).find('tbody').find_all('tr')
    domains_status = []
    for domain_tag in domains_tag:
        domain = domain_tag.find('td')
        domains_status.append({
            'domain': domain.text,
            'status': domain.find_next('td').text
        })
    return domains_status


if __name__ == '__main__':
    top_100_url = 'https://arsenkin.ru/tools/check-top/'
    whois_url = 'https://www.cy-pr.com/tools/masswhois/'
    key_words = 'сало\nмед\nгавно\nгвозди'
    top_100_url_response = fetch_page(top_100_url, key_words)
    all_links = list(set(get_all_links(top_100_url_response.text)))
    unique_domains = get_domain(all_links)
    whois_domains = '\n'.join(unique_domains[:29])
    whois_domain_response = fetch_page_whois(whois_url, whois_domains).text
    print(get_whois_domain(whois_domain_response))
