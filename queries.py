from timetable import Timetable


class QueryNode:
    def __init__(self, station):
        self.is_visited = False
        self.time = None
        self.station = station

    def is_closer_than(self, other) -> bool:
        if other is None:
            # Jeder Knoten ist "näher" als kein Knoten.
            return True
        if self.time is None:
            # Ein Knoten ohne Zeit ist nie näher als ein anderer Knoten.
            return False
        if other.time is None:
            # Jeder Knoten mit Zeit ist näher als ein Knoten ohne Zeit.
            return True
        return self.time < other.time


class Query:
    def __init__(self, timetable: Timetable, from_station, to_station, start_time):
        self.from_station = from_station
        self.to_station = to_station
        self.start_time = start_time
        self.timetable = timetable
        self.nodes = {}

    def query(self):
        self._init()
        while True:
            node = self._get_closest_unvisited_node()
            if node is not None:
                if node.station != self.to_station:
                    node.is_visited = True
                    neighbours = self.timetable.get_neighbours(node.station, node.time)
                    self._update_neighbours(neighbours)
                else:
                    break
            else:
                break

    def _update_neighbours(self, neighbours):
        for station, arrival_time in neighbours.items():
            node = self.nodes[station]
            if node.time is None or node.time > arrival_time:
                node.time = arrival_time

    def _get_closest_unvisited_node(self) -> QueryNode:
        selected_node = None
        for node in self.nodes.values():
            if not node.is_visited and node.is_closer_than(selected_node):
                selected_node = node
        return selected_node

    def _init(self):
        for station in self.timetable.stations:
            self.nodes[station] = QueryNode(station)
        start_node = self.nodes[self.from_station]
        start_node.time = self.start_time
