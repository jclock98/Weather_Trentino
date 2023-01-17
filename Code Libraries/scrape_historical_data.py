import io
import json
from typing import List

import pandas as pd
import requests
from tqdm import tqdm


def filter_non_existent_loc(localities: dict) -> dict:
    '''
    remove locations that have not historical data
    :param localities: list of localities
    :return: cleaned list of localities
    '''

    to_del = []
    for loc in tqdm(localities):
        try:
            pd.read_csv(io.StringIO(requests.get(localities[loc][0]).content.decode("utf-8")), sep=";")
        except:
            to_del.append(loc)

    for loc in to_del:
        localities.pop(loc)
    return localities


def filter_non_relevant_urls(localities: dict) -> dict:
    '''
    cleaned out location that are not present in localities file
    :param localities:
    :return: cleaned localities
    '''
    with open("localities.json", 'r') as fp:
        tst = json.load(fp)
    tmp_loc = list(set([x["locality"] for x in tst]))
    tmp_munic = list(set([x["municipality"] for x in tst]))
    to_del = []
    for loc in localities:
        l_tmp = loc.upper()
        l_tmp = l_tmp.replace("+", " ").replace("%27", "'").replace("%E8", "E'").replace("%F2", "O'")
        if (not l_tmp in tmp_loc) and (not l_tmp in tmp_munic):
            to_del.append(loc)
    for loc in to_del:
        localities.pop(loc)
    return localities


def get_url_list(loc_list: List) -> List:
    '''
    generate list of url from January 1973 to December 2022
    :param loc_list: list of localities
    :return: list of urls
    '''
    months = ["Gennaio", "Febbraio", "Marzo", "Aprile",
              "Maggio", "Giugno", "Luglio", "Agosto",
              "Settembre", "Ottobre", "Novembre", "Dicembre"]
    years = [x for x in range(1973, 2023)]

    date = [f"{year}/{month}" for year in years for month in months][:-1]

    urls = []
    for loc in loc_list:
        for dat in date:
            urls.append(f"https://www.ilmeteo.it/portale/{loc}/{dat}?format=csv")
    print(urls[0], urls[-1])
    return urls


def get_historical_data(urls: List):
    '''
    download historical data from ilMeteo.it archives
    :param urls: list of urls containing localities and date
    :return:
    '''
    localities = dict()
    for url in urls:
        place = url.split("/")[5]
        if place in localities.keys():
            localities[place].append(url)
        else:
            localities[place] = [url]

    localities = filter_non_existent_loc(localities)

    localities = filter_non_relevant_urls(localities)

    tmp_urls = [localities[loc] for loc in localities]
    tmp = []
    for tmp_url in tmp_urls:
        tmp.extend(tmp_url)

    # write data directly to file
    try:
        with open("historical_weather_data.csv", 'a') as fp:
            for loc in tqdm(tmp):
                try:
                    res = io.StringIO(requests.get(loc).content.decode("utf-8"))
                    res = pd.read_csv(res, sep=";")
                    res.to_csv(fp)
                except:
                    pass
    except:
        pass


def reorder_date(x: str) -> str:
    a, b, c = x.split("/")
    return c + "-" + b + "-" + a


def clean_data():
    '''
    remove duplicates from final downloads and refactor data format
    '''
    df = pd.read_csv("historical_weather_data.csv")

    df.drop_duplicates(subset=["LOCALITA", "DATA"], inplace=True)
    df["DATA"] = df["DATA"].map(lambda x: reorder_date(x))
    df.to_csv("historical_weather_data.csv", index=False)


if __name__ == "__main__":
    # get_localities names and filter out duplicates
    loc_list = pd.read_csv("target_locality_list.csv")["link"].tolist()
    loc_list = list(set(loc_list))

    urls = get_url_list(loc_list)
    get_historical_data(urls)
    clean_data()
