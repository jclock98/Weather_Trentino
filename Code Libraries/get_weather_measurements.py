import json
from pprint import pprint

import xmltodict
import requests
import uuid
import argparse


def get_weather_measurement(station: str, option: str):
    '''
    get weather measurements for all the weather stations
    :param option: append or write file
    :param station: weather station
    :return:
    '''

    url = f"https://dati.meteotrentino.it/service.asmx/getLastDataOfMeteoStation?codice={station}"

    weather_forecast = (url.split("=")[-1], xmltodict.parse(requests.get(url).text)["lastData"])

    req_id = uuid.uuid4().time_low

    all_measurements = []
    station, measurements = weather_forecast
    if measurements["temperature_list"] is not None:
        for temp in measurements["temperature_list"]["air_temperature"]:
            meas = dict()
            meas["id_station"] = station
            meas["value"] = temp["value"]
            meas["@UM"] = temp["@UM"]
            meas["date"] = temp["date"]
            date = temp["date"][:-6]
            meas["id_measurement"] = f"{station}_temp_{date}_{req_id}"
            meas["type_of_measurement"] = "temperature"
            all_measurements.append(meas)

    if measurements["precipitation_list"] is not None:
        for prec in measurements["precipitation_list"]["precipitation"]:
            meas = dict()
            meas["id_station"] = station
            meas["value"] = prec["value"]
            meas["@UM"] = prec["@UM"]
            meas["date"] = prec["date"]
            date = prec["date"][:-6]
            meas["id_measurement"] = f"{station}_prec_{date}_{req_id}"
            meas["type_of_measurement"] = "precipitation"
            all_measurements.append(meas)

    if measurements["wind_list"] is not None:
        for wind_data in measurements["wind_list"]["wind10m"]:
            meas = dict()
            meas["id_station"] = station
            meas["value"] = wind_data["speed_value"]
            meas["@UM"] = wind_data["@UM_speed"]
            meas["date"] = wind_data["date"]
            date = wind_data["date"][:-6]
            meas["id_measurement"] = f"{station}_wind-speed_{date}_{req_id}"
            meas["type_of_measurement"] = "wind_speed"
            all_measurements.append(meas)

            meas = dict()
            meas["id_station"] = station
            meas["value"] = wind_data["windgust"]
            meas["@UM"] = wind_data["@UM_windgust"]
            meas["date"] = wind_data["date"]
            date = wind_data["date"][:-6]
            meas["id_measurement"] = f"{station}_wind-gust_{date}_{req_id}"
            meas["type_of_measurement"] = "wind_gust"
            all_measurements.append(meas)

            meas = dict()
            meas["id_station"] = station
            meas["value"] = wind_data["direction_value"]
            meas["@UM"] = wind_data["@UM_direction"]
            meas["date"] = wind_data["date"]
            date = wind_data["date"][:-6]
            meas["id_measurement"] = f"{station}_wind-dir_{date}_{req_id}"
            meas["type_of_measurement"] = "wind_direction"
            all_measurements.append(meas)

    if measurements["global_radiation_list"] is not None:
        for glob_rad in measurements["global_radiation_list"]["global_radiation"]:
            meas = dict()
            meas["id_station"] = station
            meas["value"] = glob_rad["value"]
            meas["@UM"] = glob_rad["@UM"]
            meas["date"] = glob_rad["date"]
            date = glob_rad["date"][:-6]
            meas["id_measurement"] = f"{station}_rad_{date}_{req_id}"
            meas["type_of_measurement"] = "global_radiation"
            all_measurements.append(meas)

    if measurements["relative_humidity_list"] is not None:
        for rel_hum in measurements["relative_humidity_list"]["relative_humidity"]:
            meas = dict()
            meas["id_station"] = station
            meas["value"] = rel_hum["value"]
            meas["@UM"] = rel_hum["@UM"]
            meas["date"] = rel_hum["date"]
            date = rel_hum["date"][:-6]
            meas["id_measurement"] = f"{station}_hum_{date}_{req_id}"
            meas["type_of_measurement"] = "relative_humidity"
            all_measurements.append(meas)

    if measurements["snow_depth_list"] is not None:
        for snow in measurements["snow_depth_list"]["snow_depth"]:
            meas = dict()
            meas["id_station"] = station
            meas["value"] = snow["value"]
            meas["@UM"] = snow["@UM"]
            meas["date"] = snow["date"]
            date = snow["date"][:-6]
            meas["id_measurement"] = f"{station}_snow_{date}_{req_id}"
            meas["type_of_measurement"] = "snow_level"
            all_measurements.append(meas)

    humidex = requests.get("https://content.meteotrentino.it/dati-meteo/stazioni/humidex_xml.aspx").text

    humidex = xmltodict.parse(humidex)["humidex"]["stazione"]

    for hum_dic in humidex:
        if station == hum_dic["id"]:
            meas = dict()
            meas["id_station"] = hum_dic["id"]
            meas["value"] = hum_dic["val_humidex"]
            meas["measurement_date"] = hum_dic["datamisura"].replace("/", "-").replace(" ", "T").replace(".",
                                                                                                         ":") + ":00+01"
            station = hum_dic["id"]
            date = meas["measurement_date"][:-6]
            meas["id_measurement"] = f"{station}_humidex_{date}_{req_id}"
            meas["type_of_measurement"] = "humidex"
            all_measurements.append(meas)

    pprint(all_measurements)

    with open("weather_measurements.json", option) as fp:
        json.dump(all_measurements, fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for getting weather measurement for a weather stations")
    parser.add_argument("--station", type=str, default='T0405', help="Weather station")
    parser.add_argument("--rewrite-file", default=False, action="store_true")
    args = parser.parse_args()

    if args.rewrite_files:
        write_option = 'w'
    else:
        write_option = 'a'

    weather_station = args.station
    get_weather_measurement(weather_station, write_option)
