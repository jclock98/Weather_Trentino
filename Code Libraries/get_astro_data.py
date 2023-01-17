from utilities import get_datetime
import datetime as dt

from typing import List, Optional

from skyfield import almanac
from skyfield import eclipselib
from skyfield.api import N, W, wgs84, load, Star, Loader
from skyfield.timelib import Time
from skyfield.toposlib import GeographicPosition


def get_astro_data(date: str, lat: str, long: str, elev: str) -> dict:
    '''
    get astronomical data for specified location
    :param date: date for computation of astronomical data
    :param lat: latitude
    :param long: longitude
    :param elev: elevation
    :return: dict containing astronomical data
    '''
    astro_data = dict()

    year, month, day = date.split('-')
    # world model
    eph = load('de421.bsp')
    # specify position
    pos = wgs84.latlon(float(lat) * N, float(long) * W, elevation_m=int(elev))

    ts = load.timescale()
    time_now = get_datetime(year, month, day)
    time_up = time_now + dt.timedelta(days=1, hours=1, minutes=1, seconds=1, milliseconds=1, microseconds=1)

    t0 = ts.from_datetime(time_now)
    t1 = ts.from_datetime(time_up)

    astro_data["galactic_centre_sunrise"], astro_data["galactic_centre_sunset"] = get_galactic_center_rise_set(eph,
                                                                                                               pos,
                                                                                                               t0, t1)
    astro_data["sunrise"], astro_data["sunset"] = get_sunset_sunrise(eph, pos, t0, t1)

    astro_data["lunar_eclipse"] = get_lunar_eclipse(eph, t0, t1)

    astro_data["moon_phase"] = get_moon_phase(eph, t0, t1)

    tmp_list = get_twilights(eph, pos, t0, t1)
    for value, key in tmp_list:
        astro_data[key] = value
    return astro_data


def get_twilights(eph: Loader, pos: GeographicPosition, t0: Time, t1: Time) -> List:
    '''
    get civil, nautical, astronomical twilights
    :param eph: astronomical model
    :param pos: locality position
    :param t0: day 1
    :param t1: day 2
    :return: list of twilights
    '''
    f = almanac.dark_twilight_day(eph, pos)
    times, events = almanac.find_discrete(t0, t1, f)
    twilight_list = ['astronomical_dawn', 'nautical_dawn', 'civil_dawn', 'Sunrise', 'Sunset', 'civil_dusk',
                     'nautical_dusk', 'astronomical_dusk']
    final_list = list(zip(times.utc_strftime("%Y-%m-%dT%H:%M:%S%z"), twilight_list))
    final_list = final_list[:3] + final_list[5:]
    return final_list


def get_sunset_sunrise(eph: Loader, pos: GeographicPosition, t0: Time, t1: Time) -> (str, str):
    '''
    :param eph: astronomical model
    :param pos: locality position
    :param t0: day 1
    :param t1: day 2
    :return: time of sunset, time of sunrise
    '''
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, pos))
    return t[0].utc_strftime("%Y-%m-%dT%H:%M:%S%z"), t[1].utc_strftime("%Y-%m-%dT%H:%M:%S%z")


def get_galactic_center_rise_set(eph: Loader, pos: GeographicPosition, t0: Time, t1: Time) -> (str, str):
    '''

    :param eph: astronomical model
    :param pos: locality position
    :param t0: day 1
    :param t1: day 2
    :return: time of galactic centre sunrise, time of galactic centre sunset
    '''
    galactic_center = Star(ra_hours=(17, 45, 40.04),
                           dec_degrees=(-29, 0, 28.1))

    f = almanac.risings_and_settings(eph, galactic_center, pos)
    t, y = almanac.find_discrete(t0, t1, f)
    return t[0].utc_strftime("%Y-%m-%dT%H:%M:%S%z"), t[1].utc_strftime("%Y-%m-%dT%H:%M:%S%z")


def get_lunar_eclipse(eph: Loader, t0: Time, t1: Time) -> Optional[str]:
    '''

    :param eph: astronomical model
    :param t0: day 1
    :param t1: day 2
    :return: Lunar eclipse type
    '''
    t, y, details = eclipselib.lunar_eclipses(t0, t1, eph)
    if t.shape[0] != 0:
        return eclipselib.LUNAR_ECLIPSES[y[0]]
    else:
        return None


def get_moon_phase(eph: Loader, t0: Time, t1: Time) -> str:
    '''

    :param eph: astronomical model
    :param t0: day 1
    :param t1: day 2
    :return: moon phase
    '''
    tmp_t, tmp_y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
    if tmp_t.shape[0] != 0:
        return almanac.MOON_PHASES[tmp_y[0]]
    else:
        phase = almanac.moon_phase(eph, t0).degrees
        if phase < 90:
            return "Waxing Crescent"
        elif 90 < phase < 180:
            return "Waxing Gibbous"
        elif 180 < phase < 270:
            return "Waning Gibbous"
        else:
            return "Waning Crescent"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for getting astrological data for a specific location")
    parser.add_argument("--lat", type=str, default='', help="Latitude of a specific location")
    parser.add_argument("--long", type=str, default='', help="Longitude of a specific location")
    parser.add_argument("--elev", type=str, default='', help="Elevation for a specific location")
    parser.add_argument("--date", type=str, default='2023-01-01', help="Date to compute the astronomical status for")
    parser.add_argument("--file", type=str, default='astro_data.json', help="Name of the output file")
    parser.add_argument("--append-file", default=False, action="store_true")

    args = parser.parse_args()

    latitude = args.lat
    longitude = args.long
    elevation = args.elev
    date = args.date
    file_name = args.file

    if args.rewrite_files:
        write_option = 'a'
    else:
        write_option = 'w'

    output = get_astro_data(date, latitude, longitude, elevation)

    with open(file_name, write_option) as fp:
        json.dump(output, fp)