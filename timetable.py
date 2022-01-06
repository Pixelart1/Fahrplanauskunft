from datetime import time
from typing import Iterable, Tuple


class Station:
    def __init__(self, tag, name):
        self.name = name
        self.tag = tag

    def __repr__(self):
        return self.name


class Line:
    def __init__(self, name, stops):
        self.name = name
        self.stops = stops

    def get_end_stop(self):
        for stop in self.stops:
            if stop.is_end:
                return stop

    def get_start_stop(self):
        for stop in self.stops:
            if stop.arrival_time is None:
                return stop


class Stop:
    def __init__(self, tag, departure_time, arrivel_time, is_end):
        self.tag = tag
        self.departure_time = time.fromisoformat(departure_time) if departure_time else None
        self.arrival_time = time.fromisoformat(arrivel_time) if arrivel_time else None
        self.is_end = is_end
        self.station = None


class Start(Stop):
    def __init__(self, tag, departure_time):
        super().__init__(tag, departure_time, None, False)


class Via(Stop):
    def __init__(self, tag, arrival_time, departure_time):
        super().__init__(tag, departure_time, arrival_time, False)


class End(Stop):
    def __init__(self, tag, arrival_time):
        super().__init__(tag, None, arrival_time, True)


class Timetable:
    def __init__(self, stations, lines):
        self.lines = lines
        self.stations = stations
        for line in self.lines:
            for stop in line.stops:
                stop.station = self.get_station_for_tag(stop.tag)

    def get_station_for_name(self, name):
        for station in self.stations:
            if name == station.name:
                return station
        print("Error: Station is not found")

    def get_station_for_tag(self, tag):
        for station in self.stations:
            if tag == station.tag:
                return station
        print("Error: Station is not found")

    def get_departures(self, station):
        departures = []
        for line in self.lines:
            for stop in line.stops:
                if stop.station == station:
                    if stop.departure_time is not None:
                        departures.append((stop.departure_time, line, True))
                    else:
                        departures.append((stop.arrival_time, line, False))
        return departures

    def get_sorted_departures(self, station):
        departures = self.get_departures(station)
        sorted_departures = sorted(departures, key=lambda x: x[0])
        return sorted_departures

    def get_upcoming_departures(self, station, current_time):
        upcoming_departures = []
        sorted_departures = self.get_sorted_departures(station)
        for departure_time, line, is_departure in sorted_departures:
            if departure_time >= current_time:
                if is_departure:
                    upcoming_departures.append(line)
        return upcoming_departures

    def get_neighbours(self, station, time_now):
        neighbours = {}
        lines = self.get_upcoming_departures(station, time_now)
        for line in lines:
            prev_stop = None
            for stop in line.stops:
                if prev_stop is not None and prev_stop.station == station:
                    t, _ = neighbours.get(stop.station, (None, None))
                    if t is None or t > stop.arrival_time:
                        neighbours[stop.station] = (stop.arrival_time, line)
                prev_stop = stop
        return neighbours

    def get_connection(self, from_station, to_station, start_time) -> Iterable[Tuple[Stop, Stop, Line]]:
        from queries import Query
        query = Query(self, from_station, to_station, start_time)
        query.query()  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        result = query.get_result()
        return result
