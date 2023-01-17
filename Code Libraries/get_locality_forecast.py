import json
import requests
import uuid
from tqdm import tqdm
from typing import List
from get_astro_data import get_astro_data
from utilities import find_loc


def get_localities_forecasts(localities: List):
    '''
    get weather forecasts for each locality
    :param localities: list of localities
    :return:
    '''
    localities_name = [el["locality"] for el in localities]

    localities_forecast = []
    for locality in localities_name:
        url = f"https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita={locality}"
        localities_forecast.append(json.loads(requests.get(url).text))

    # get an unique id for request
    forecast_req_id = uuid.uuid4().time_low

    forecast_temp_id = uuid.uuid4().time_low

    all_forecasts = []
    prediction_forecast = []
    all_astro_data = []

    for forecast in tqdm(localities_forecast):
        if forecast["previsione"]:
            tmp = dict()
            tmp["publish_date"] = forecast["dataPubblicazione"]
            for prev in forecast["previsione"]:
                tmp["locality"] = prev["localita"]
                forecast_id = str(forecast["idPrevisione"]) + "-" + tmp["locality"].replace("'", "").replace(" ", "_")
                tmp["id_forecast"] = forecast_id + "-" + str(forecast_temp_id)
                tmp_days = []
                for daily in prev["giorni"]:
                    tmp_daily = dict()
                    tmp_daily["id_daily_forecast"] = str(daily["idPrevisioneGiorno"]) + "-" + tmp["id_forecast"]
                    tmp_daily["date"] = daily["giorno"]
                    tmp_daily["tMin"] = daily["tMinGiorno"]
                    tmp_daily["tMax"] = daily["tMaxGiorno"]

                    astro_data = get_astro_data(daily["giorno"],
                                                *find_loc(prev["localita"], localities))
                    astro_data["id"] = tmp_daily["id_daily_forecast"]
                    all_astro_data.append(astro_data)

                    tmp_daily["id_forecast"] = tmp["id_forecast"]
                    tmp_timeslot = []
                    for slot in daily["fasce"]:
                        tmp_slot = dict()
                        tmp_slot["id_timeslot_forecast"] = str(slot["idPrevisioneFascia"]) + \
                                                           "-" + \
                                                           tmp_daily["id_daily_forecast"]
                        tmp_slot["timeslot"] = slot["fascia"]
                        tmp_slot["timeslot_hours"] = slot["fasciaOre"]
                        tmp_slot["timeslot_desc"] = slot["fasciaPer"]
                        tmp_slot["id_daily_forecast"] = tmp_daily["id_daily_forecast"]
                        tmp_timeslot.append(tmp_slot)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-high_temp-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = slot["idTempProb"]
                        single_forecast["forecast_desc"] = slot["descTempProb"]
                        single_forecast["type_of_forecast"] = "extreme_temperatures"
                        prediction_forecast.append(single_forecast)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-prob_prec-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = slot["idPrecProb"]
                        single_forecast["forecast_desc"] = slot["descPrecProb"]
                        single_forecast["type_of_forecast"] = "probable_precipitation"
                        prediction_forecast.append(single_forecast)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-strong_prec-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = slot["idPrecInten"]
                        single_forecast["forecast_desc"] = slot["descPrecInten"]
                        single_forecast["type_of_forecast"] = "strong_precipitation"
                        prediction_forecast.append(single_forecast)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-high_wind_int-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = slot["idVentoIntQuota"]
                        single_forecast["forecast_desc"] = slot["descVentoIntQuota"]
                        single_forecast["type_of_forecast"] = "high_wind_intensity"
                        prediction_forecast.append(single_forecast)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-high_wind_dir-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = slot["idVentoDirQuota"]
                        single_forecast["forecast_desc"] = slot["descVentoDirQuota"]
                        single_forecast["type_of_forecast"] = "high_wind_direction"
                        prediction_forecast.append(single_forecast)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-ground_wind_int-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = slot["idVentoIntValle"]
                        single_forecast["forecast_desc"] = slot["descVentoIntValle"]
                        single_forecast["type_of_forecast"] = "ground_wind_intensity"
                        prediction_forecast.append(single_forecast)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-ground_wind_dir-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = slot["idVentoDirValle"]
                        single_forecast["forecast_desc"] = slot["descVentoDirValle"]
                        single_forecast["type_of_forecast"] = "ground_wind_direction"
                        prediction_forecast.append(single_forecast)

                        single_forecast = dict()
                        single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                        single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                             "-freezing_point-" + \
                                                                             str(forecast_req_id)
                        single_forecast["forecast_id"] = str(slot["zeroTermico"])
                        single_forecast["forecast_desc"] = "Altitude"
                        single_forecast["type_of_forecast"] = "freezing_point"
                        prediction_forecast.append(single_forecast)

                        if "limiteNevicate" in slot:
                            single_forecast["id_timeslot_forecast"] = tmp_slot["id_timeslot_forecast"]
                            single_forecast["id_timeslot_forecast_prediction"] = tmp_slot["id_timeslot_forecast"] + \
                                                                                 "-snow_level-" + \
                                                                                 str(forecast_req_id)
                            single_forecast["forecast_id"] = str(slot["limiteNevicate"])
                            single_forecast["forecast_desc"] = "Altitude"
                            single_forecast["type_of_forecast"] = "snow_level"
                            prediction_forecast.append(single_forecast)

                    tmp_daily["timeslots"] = tmp_timeslot
                    tmp_days.append(tmp_daily)
            tmp["forecasts"] = tmp_days
            all_forecasts.append(tmp)

    with open("weather_report.json", 'w') as fp:
        json.dump(all_forecasts, fp)

    with open("weather_forecasts.json", 'w') as fp:
        json.dump(prediction_forecast, fp)

    with open("astronomical_status.json", 'w') as fp:
        json.dump(all_astro_data, fp)
