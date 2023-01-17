import json
import requests
import xmltodict

from typing import List
import geopy.distance
import geopy.distance


def get_localities_and_weather_stations() -> (List, List):
    '''
    get localities and weather stations information and write them to files
    :return: localities list, list of active weather stations codes
    '''
    print("Loading localities")
    localities = json.loads(
        requests.get("https://www.meteotrentino.it/protcivtn-meteo/api/front/localitaOpenData").text)["localita"]

    print("Loading Weather stations")
    stations = requests.get("https://dati.meteotrentino.it/service.asmx/getListOfMeteoStations")

    list_of_meteo_stations = dict(xmltodict.parse(stations.text))["ArrayOfPointOfMeasureInfo"]["pointOfMeasureInfo"]

    # refactor dict names
    for loc in localities:
        try:
            loc["locality"] = loc.pop("localita").upper()
        except:
            pass
        try:
            loc["municipality"] = loc.pop("comune").upper()
        except:
            pass
        try:
            loc["elevation"] = loc.pop("quota")
        except:
            pass
        try:
            loc["latitude"] = loc.pop("latitudine")
        except:
            pass
        try:
            loc["longitude"] = loc.pop("longitudine")
        except:
            pass

    # write localities to file
    print("Writing localities")
    with open("localities.json", 'w') as fp:
        json.dump(localities, fp)

    for i, station in enumerate(list_of_meteo_stations):
        list_of_meteo_stations[i]["active"] = True if station["enddate"] is None else False

    print("Associating weather station with a locality")
    for i, station in enumerate(list_of_meteo_stations):
        closest = ""
        min_dist = 100000000000
        # get locality with smallest distance using geo-distance
        for locality in localities:
            station_pos = (station["latitude"], station["longitude"])
            locality_pos = (locality["latitude"], locality["longitude"])
            tmp_distance = geopy.distance.geodesic(station_pos, locality_pos).m
            if tmp_distance < min_dist:
                closest = locality["locality"]
                min_dist = tmp_distance
        list_of_meteo_stations[i]["locality"] = closest

    # delete irrelevant attributes
    for station in list_of_meteo_stations:
        del station["shortname"], station["east"], station["north"], station["startdate"], station["enddate"]

    print("Writing weather stations")
    with open("weather_stations.json", 'w') as fp:
        json.dump(list_of_meteo_stations, fp)


if __name__ == "__main__":
    get_localities_and_weather_stations()
