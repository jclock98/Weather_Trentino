# Trentino Weather
*A KGE Project’s Website*
by **Giacomo Lazzerini** and **Jacopo Clocchiatti**

Academic year **2022/2023**, 
**University of Trento**

link: [Official Course Website](https://unitn-knowledge-graph-engineering.github.io/KGE2022-website/)
link: [Project Repository](https://github.com/jclock98/Weather_Trentino)

## Introduction

Weather influences many aspects of our lives. In the past, knowing the meteorological status and its possible changes over time was vital for agriculture, transportation, and even the culture of many communities. Today, weather is still very important, and it can significantly impact everyday life. Modern technologies, measurement techniques, and climatology studies allowed reaching such high levels of accuracy to predict the future often correctly. From knowing if to bring the umbrella with you before going outside, knowing if the next weekend will be a good day for a picnic, or being able to monitor atmospheric conditions remotely, the weather has always played a crucial role in human beings' life.

Our resource can be seen not only as an alternative to already existing and largely used weather services but also as a resource specifically created for Trentino Region, a service that can give information about the future (forecasts) but also about the present (meteorological station measurements) and past (historical data). In this resource, we integrated the chance to explore historical data and to know astronomical features available on a daily basis. We believe that enriching the experience with new ETypes can open new usage opportunities to a category of personas not considered so far. \\\\

In this project, we used weather data from Trento province to build a Knowledge Graph (KG). This has been possible using the iTelos methodology. iTelos is a phase-based methodology that allows the implementation of a KGE process.

### Domain of Interest
For the scope of this project, we considered data:

- from a day before to the moment of the query for weather measurements.
- from the moment of the query to five days in the future for weather forecasts.
- from 1973 to 2022 for historical data.

We can describe the purpose as a user request as:

*“A service which helps users to know about the various weather observation sites and weather forecasts in different parts of Trentino.”*

Our resource’ structure is born with a snapshot of historical weather archive data that has been collected up to 1973, then it will serve as a framework to build new historical records of weather measurements collected over time.  Data streams will populate the database and they will be used as historical data for future use cases.


## Datasets

Most of the datasets come from the same site, [**Open Data Trentino**](https://dati.trentino.it/), which is a data catalogue that allows to search, access, download, and preview open data collected in the Trentino province through a single access point. There are other closed datasets available, but only after payment. We added information about Astronomical Metrics (e.g. sunset and sunrise time depending on coordinates and day) provided by a Python library, [**Skyfield**](https://rhodesmill.org/skyfield/). Lastly, we scraped historical data for our location from [**ilMeteo.it**](https://www.ilmeteo.it/).

[**Meteotrentino**](https://www.meteotrentino.it/), which is the administrative structure of Trentino province that deals with meteorology, snow science, and glaciology. We used several datasets that are present in the catalogue mentioned before. We can divide those datasets in agraphic datasets and active datasets (the ones with weather information). Almost all the datasets come in XML format and a couple comes in JSON format. All the datasets’ structures are the same since 2013, the year when they were released. The datasets we used are:

- [Last data of meteo stations](https://dati.trentino.it/dataset/meteo-data): this operation gets data from the specified weather station. The operation requires a code station as a parameter and returns temperature (°C), precipitation (mm), wind velocity (m/s), wind direction (gN), global radiation (W/mq), relative humidity (%), snow depth (cm). Data refers to the time period starting from the day before the query at 0:00 to the time of the last data collected today. Data comes in an XML  format.

- [Bollettino meteo probabilistico giornaliero](https://dati.trentino.it/dataset/bollettino-probabilistico-giornaliero): daily weather forecast for Trento province computed with probabilistics methods (snowfalls, precipitations, thunderstorms, winds, freezing level). Data comes in a JSON  format.

- [List of meteorological stations](https://dati.trentino.it/dataset/observations-site-list): each point of measure exposes these attributes: code, name, short-name, elevation, latitude, longitude, startdate, enddate. If enddate attribute is null its mean that the station is active, else this station does not exist (has only past data). Data comes in a XML  format.

- [Dati  recenti  delle  stazioni  meteorologiche  automatiche](https://dati.trentino.it/dataset/dati-recenti-delle-stazioni-meteo):  the  dataset  contains,  through an  endpoint,  recent  data  from  weather  stations  belonging  to  the  automatic  measure-  ment  network.  Those  data  refers  to  the  time  period  from  midnight  of  the  day  before  and  data  are  about  temperature  (°C),  precipitation  (mm),  wind  speed  (m/s)  and  direc-  tion  (gN),  global  radiation  (W/mq)  of  the  specified  weather  station.  Data  comes  in  a XML  format.

- [Bollettino  meteorologico  di  località  JSON](https://dati.trentino.it/dataset/bollettino-meteorologico-localita):  Weather  forecast  for  each  locality  can  be  accessed  by  this  endpoint.  Data  comes  in  a  JSON  format.

- [Indice di Calore (Humidex)](https://dati.trentino.it/dataset/indice-di-calore-humidex): many indexes are used to estimate the discomfort related due to warm and humid climate. Meteotrentino uses HUMIDEX index, developed in Canada in 1965. Data comes in a XML  format.

Servizio Prevenzione Rischi is the author of all these datasets and is responsible for their  update.

- [**Skyfield**](https://rhodesmill.org/skyfield/) computes positions for the stars, planets, and satellites in orbit around the Earth. Its results should agree with the positions generated by the United States Naval Observa- tory and their _Astronomical Almanac_ to within 0.0005  arcseconds.

- [**ilMeteo.it**](http://www.ilmeteo.it/), an italian web company specialized in the provision of services and communi- cation of weather forecasts. The data are aggregated by the site from different sources and provided in a XLSX format, available in daily, weekly and monthly format for different time  periods

## ER Diagram and ETG

The following graph shows the structure of our resource. More details available at the official repository of the project

__insert image here__ 

## Data Integration

### Annotated ETG

### Final KG

And this will produce a flow chart:

version https://git-lfs.github.com/spec/v1
oid sha256:e45c3295f3529fafb676cb696196b5203e6d657b167257b03567b3c579a256c6
size 118
