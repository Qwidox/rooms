from collections import defaultdict
from collections.abc import Generator


class ApartmentChairsCounter:
    """
        We now need a command line tool that reads in such a file and outputs the following information:
        - Number of different chair types for the apartment
        - Number of different chair types per room

        - The names of the rooms must be sorted alphabetically in the output.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.apartment_plan = None
        # dictionary of rooms chairs
        self.apartment_chairs: dict[str, dict[str, int]] = defaultdict(dict)
        self.room_names_coordinates: dict[str,list[tuple[int, int]]] = defaultdict(list)
        self.walls_coordinates: set[tuple[int,int]] = set()
        self.empty_coordinates: set[tuple[int,int]] = set()
        # coordinates of all chairs in apartment
        self.chairs_coordinates: dict[str, tuple[int, int]] = {}


    def parse_apartment_plan(self) -> None:
        """Read appartment plan."""

        with open(self.file_path, 'r') as file:
            self.apartment_plan = file.read()
        
    
    def scan_apartment(self) -> None:
        """Scan whole apartment. Find chairs, appartmnet walls, room names and empty room space."""
        
        plan_lines: list[str] = self.apartment_plan.splitlines()
        room_name = ''
        name_found = False
        tmp_rooms_coordinates = []

        # iterate through apparmtnet plan lines 
        for row, line in enumerate(plan_lines):
            for col, char in enumerate(line):
                if char == '(':
                    name_found = True
                elif char == ')':
                    self.room_names_coordinates[room_name].extend(tmp_rooms_coordinates)
                    tmp_rooms_coordinates.clear()
                    name_found = False
                    room_name = ''
                elif name_found:
                    tmp_rooms_coordinates.append((row, col))
                    room_name += char
                elif char in ('P', 'W', 'S', 'C'):
                    self.chairs_coordinates[(row,col)] = char
                elif char == ' ':
                    self.empty_coordinates.add((row, col)) 
                else:
                    self.walls_coordinates.add((row, col))
    

    def in_room(self, space: tuple[int, int]) -> bool:
        """Test if possition is inside room."""

        if space in self.walls_coordinates:
            return False
        return True
    

    def get_neighbour_spaces(self, space: tuple[int, int]) -> Generator[tuple[int, int]]:
        """Yield neighbour positions of space coordinates if they are inside room."""

        x, y = space
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == dy:
                    continue
                else:
                    space = x + dx, y + dy
                    if self.in_room(space):
                        yield space


    def scan_room(self, room: str) -> dict[str, int]:
        """Scan room for chairs."""

        room_chairs = {'W': 0, 'P': 0, 'S': 0, 'C': 0}

        # list of room name coordinates (x,y)
        room_name = self.room_names_coordinates.get(room)
        # dont scan room name
        scanned = set(room_name)
        # add '(' and ')' to start scan 
        space1: tuple = (room_name[0][0], room_name[0][1] - 1)
        space2: tuple = (room_name[-1][0], room_name[-1][1] + 1)
        space_to_scan = set([space1,space2])

        while space_to_scan:
            current = space_to_scan.pop()

            if current in scanned:
                continue

            scanned.add(current) 
            neighbours = self.get_neighbour_spaces(current)

            for neighbour in neighbours:
                space_to_scan.add(neighbour)
            
            if chair := self.chairs_coordinates.get(current):
                room_chairs[chair] = room_chairs.get(chair) + 1

        return room_chairs
        

    def sum_appartment_chairs(self, room_chairs: dict) -> None:
        """Sum all chairs in appartment."""

        if not self.apartment_chairs:
            self.apartment_chairs['total'] = room_chairs.copy()
        else:
            for key, value in room_chairs.items():
               self.apartment_chairs['total'][key] += value 

    

    def count_chairs(self) -> None:
        """Start the whole process of counting chairs."""
        
        # read file with apartment plan 
        self.parse_apartment_plan()
        # scan partment plan
        self.scan_apartment()
        # get and sort room names
        rooms: list[str] = sorted(list(self.room_names_coordinates.keys()))
        
        for room in rooms:
            room_chairs: dict[str, int] = self.scan_room(room)
            # add room to total apartment chairs
            self.sum_appartment_chairs(room_chairs)
            self.apartment_chairs[room] = room_chairs


    def __str__(self) -> str:
        """
            The output must look like this so that it can be read in with the old system:

            total:
            W: 3, P: 2, S: 0, C: 0
            living room:
            W: 3, P: 0, S: 0, C: 0
            office:
            W: 0, P: 2, S: 0, C: 0
        """

        if self.apartment_chairs:
            output = ''
            for room, chairs in self.apartment_chairs.items():
                output += f'{room}:\n{", ".join([f"{chair}: {number}" for chair, number in chairs.items()])}\n'

            return output
        

if __name__ == '__main__':
    path = input('Enter path to the file: ')
    chairs_counter = ApartmentChairsCounter(path)
    chairs_counter.count_chairs()
    print(chairs_counter)
