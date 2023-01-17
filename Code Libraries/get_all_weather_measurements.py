import json
from get_weather_measurements import get_weather_measurement
from typing import List


def get_weather_station_list() -> List:
    with open("weather_stations.json", 'r') as fp:
        weather_stations = json.load(fp)
    weather_stations_list = [station["code"] for station in weather_stations if station["active"]]
    return weather_stations_list


def main():
    stations_list = get_weather_station_list()
    print(stations_list)
    for station in stations_list:
        get_weather_measurement(station, 'a')


if __name__ == "__main__":
    main()