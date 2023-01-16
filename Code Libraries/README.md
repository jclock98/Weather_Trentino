This folder collects all the code libraries produced and/or adopted, during the KDI project to manage data and knowledge resources.
(i.e., Pyhton libs, Shell scripts, Javascript, etc)

## Code Usage

1. Get localities and Weather Station informations
```bash
python get_localities_and_weather_station.py
```
2. Get last measurements for all the weather stations
```bash
python get_all_weather_measurements.py
```
3. Get forecasts for all localities
```bash
python get_all_localities_forecast.py
```

BONUS: Get astro data for a specific location
```bash
python get_astro_data.py --lat "latitude" --long "longitude" --elev "elevation" --date "year-month-day" --file "file_name" --append-file
```

4. Historical data
```bash
python scrape_historical_data.py
```
