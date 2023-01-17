from get_astro_data import get_astro_data
import argparse
import json
from tqdm import tqdm
from pandas import date_range
import csv


def get_localities(filename):
    with open(filename, 'r') as fp:
        loc_list = json.load(fp)
    return loc_list


def get_date_list(start, end):
    start_date = f"{start}-1-1"
    end_date = f"{end}-12-31"
    date_list = date_range(start_date, end_date, freq="1d", inclusive="both").strftime("%Y-%m-%d").to_list()
    return date_list


def main(localities_file:str, start_year: int, end_year: int):
    localities = get_localities(localities_file)
    date_list = get_date_list(start_year, end_year)
    title = ["Locality", "Date", "Sunrise", "Sunset", "Moon Phase", "Lunar Eclipse", "Astronomical Dawn", "Nautical Dawn", "Civil Dawn", "Civil Dusk", "Nautical Dusk", "Astronomical Dusk"]
    with open("astronomical_dataset.csv", "w", newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(title)
    for loc in tqdm(localities, leave=False):
        for date in tqdm(date_list, leave=False):
            try:
                astro_list = [loc["locality"], date]
                astro = get_astro_data(date, loc["latitude"], loc["longitude"], loc["elevation"])
                astro["locality"] = loc["locality"]
                with open("astronomical_dataset.json", "a") as fp:
                    json.dump(astro, fp)
                with open("astronomical_dataset.csv", "a", newline='') as fp:
                    tmp_list = [astro["sunrise"], astro["sunset"], astro["moon_phase"], astro["lunar_eclipse"], astro["astronomical_dawn"], astro["nautical_dawn"], astro["civil_dawn"], astro["civil_dusk"], astro["nautical_dusk"], astro["astronomical_dusk"]]
                    astro_list.extend(tmp_list)
                    writer = csv.writer(fp)
                    writer.writerow(astro_list)
            except Exception as e:
                print(loc["locality"], date, astro)
                raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for building astronomical status dataset")
    parser.add_argument("--localities", type=str, default='localities.json', help="Localities file")
    parser.add_argument("--start-year", type=str, default='2020', help="Start year of the dataset")
    parser.add_argument("--end-year", type=str, default='2025', help="End year of the dataset")
    args = parser.parse_args()

    localities_file = args.localities
    start_year = int(args.start_year)
    end_year = int(args.end_year)

    main(localities_file, start_year, end_year)
