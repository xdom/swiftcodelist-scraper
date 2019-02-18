#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

from db import create_connection, create_table, create_bic

# countries
print('Getting country list ...')
page = requests.get('http://www.swiftcodelist.com/countries.html')
soup = BeautifulSoup(page.content, 'html.parser')
country_links = soup.select('li > a[href^="http://www.swiftcodelist.com/country/"]')
countries = [link.get('href') for link in country_links]
print(f'Found {len(countries)} countries.')


def bics_from_country(country, bic):
    print(f'Requesting {country} ...')
    page = requests.get(country)
    soup = BeautifulSoup(page.content, 'html.parser')
    bic_links = soup.select('td > a[href^="http://www.swiftcodelist.com/swift-code"]')
    print(f'Found {len(bic_links)} BIC codes')
    bic.extend([link.get('href') for link in bic_links])
    next_page = soup.select('span[class="current"] + a')
    if (len(next_page) == 1):
        bics_from_country(next_page[0].get('href'), bic)
    return bic


def bic_details(bic):
    print(f'Requesting {bic} ...')
    page = requests.get(bic)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = {}
    for row in soup.select('tr > td > strong'):
        data[row.get_text()] = row.parent.find_next_sibling().get_text().strip()
    return data


# BIC codes
sql_create_bic_table = """ CREATE TABLE IF NOT EXISTS bic (
                                    swift text PRIMARY KEY,
                                    country text,
                                    bank text,
                                    branch text,
                                    city text,
                                    zipcode text,
                                    address text
                                ); """

conn = create_connection('swift.db')
create_table(conn, sql_create_bic_table)
for country in countries:
    for bic in bics_from_country(country, []):
        detail = bic_details(bic)
        create_bic(conn, tuple(detail.values()))
    conn.commit()

conn.close()