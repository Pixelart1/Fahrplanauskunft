from datetime import time


class Station:
    def __init__(self, tag, name):
        self.name = name
        self.tag = tag


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

    def get_station_for_tag(self, tag):
        for station in self.stations:
            if tag == station.tag:
                return station
        print("Error: Station is not found")

    def get_departures(self, station_tag):
        departures = []
        for line in self.lines:
            for stop in line.stops:
                if stop.tag == station_tag:
                    if stop.departure_time is not None:
                        departures.append((stop.departure_time, line, True))
                    else:
                        departures.append((stop.arrival_time, line, False))
        return departures

    def get_sorted_departures(self, station_tag):
        departures = self.get_departures(station_tag)
        sorted_departures = sorted(departures, key=lambda x: x[0])
        return sorted_departures

    def print_sorted_departures(self, station_tag, time_str):
        current_time = time.fromisoformat(time_str)
        sorted_departures = self.get_sorted_departures(station_tag)
        for departure_time, line, is_departure in sorted_departures:
            if departure_time >= current_time:
                if is_departure:
                    end_stop = line.get_end_stop()
                    print(departure_time, line.name, "nach", end_stop.station.name)
                else:
                    start_stop = line.get_start_stop()
                    print(departure_time, line.name, "von", start_stop.station.name)


# Alle Bahnhöfe
def get_stations():
    return [
        Station("ALD", "Aulendorf"),
        Station("ALH", "Altshausen"),
        Station("BSG", "Bad Saulgau"),
        Station("HBO", "Herbertingen Ort"),
        Station("HBT", "Herbertingen"),
        Station("MNG", "Mengen"),
        Station("SGM", "Sigmaringen"),
        Station("STZ", "Storzingen"),
        Station("ASE", "Albstadt-Ebingen"),
        Station("BIW", "Balingen in Württemberg"),
        Station("HIG", "Hechingen"),
        Station("MÖS", "Mössingen"),
        Station("TÜH", "Tübingen Hauptbahnhof"),
        Station("RLH", "Reutlingen Hauptbahnhof"),
        Station("SGH", "Stuttgart Hauptbahnhof"),
        Station("BÖB", "Böblingen"),
        Station("HRR", "Herrenberg"),
        Station("GÄF", "Gäufelden"),
        Station("BBH", "Bondorf bei Herrenberg"),
        Station("EGZ", "Ergenzingen"),
        Station("EIG", "Eutingen im Gäu"),
        Station("HOB", "Horb"),

    ]


# Alle Linien
def get_lines():
    return [
        Line(name="RB 14 001", stops=[
            Start("SGH", "17:55"),
            Via("BÖB", "18:15", "18:16"),
            Via("HRR", "18:25", "18:26"),
            Via("GÄF", "18:29", "18:29"),
            Via("BBH", "18:32", "18:33"),
            Via("EGZ", "18:36", "18:36"),
            Via("EIG", "18:39", "18:39"),
            End("HOB", "18:48"),
        ]),
        Line(name="IRE 6 001", stops=[
            Start("ALD", "15:06"),
            Via("ALH", "15:12", "15:13"),
            Via("BSG", "15:20", "15:21"),
            Via("HBO", "15:26", "15:27"),
            Via("HBT", "15:29", "15:29"),
            Via("MNG", "15:34", "15:35"),
            Via("SGM", "15:48", "15:50"),
            Via("STZ", "16:00", "16:01"),
            Via("ASE", "16:10", "16:11"),
            Via("BIW", "16:22", "16:25"),
            Via("HIG", "16:37", "16:39"),
            Via("MÖS", "16:45", "16:46"),
            Via("TÜH", "16:57", "17:00"),
            Via("RLH", "17:08", "17:09"),
            End("SGH", "17:50"),
        ]),
    ]


def main():
    stations = get_stations()
    lines = get_lines()
    timetable = Timetable(stations, lines)
    timetable.print_sorted_departures("SGH", "03:00")


if __name__ == '__main__':
    main()
