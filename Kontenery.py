import pandas as pd
import re
import math

# df to skrot od Data Frame
# df = pd.read_csv('dane.csv', sep=';', header=0, dtype=str)
df = pd.read_csv('C:\\Users\\PLPD00293\\Desktop\\DaftAcademy\\dane.csv', sep=';', header=0, dtype=str)

ShipsCSV = df.columns  # pobiera statki z pliku CSV
Ships = []  # zawiera zestawienie wszystkich statkow z naglowkow kolumn
containers = []  # zbiera informacje o kontenerach na analizowanym statku
filtered_df = []  # usuwa puste rekordy ze zmiennej 'df'
all_containers = []  # zawiera wszystkie kontenery
ships_info = []  # ship_info() zwraca tutaj informacje o statkach
containers_info = []  # container_info() zwraca tutaj informacje o kontenerach
x1_list = []  # lista zawierajaca spis wszystkich konenerow X1
containers_indexes = []  # indeksy kontenerow X1 na liscie all_containers
x1_weight_list = []  # lista zawierajaca spis ciezarow wszystkich kontenerow X1
ship_id = 0  # robocze id nadane aktualnie analizowanemu statkowi
container_id = 0  # robocze id nadane aktualnie analizowanemu kontenerowi
destination_jp = 0  # Zliczenie kontenerow plynacych do Japonii
destination_country = 'JP'

# Przeniesienie statkow do nowej listy
for shipCSV in ShipsCSV:
    Ships.append(shipCSV)

while ship_id != len(Ships):
    filtered_df = df[df[Ships[ship_id]].notnull()]
    filtered_df = filtered_df[Ships[ship_id]]
    # print(ship_id)
    # print(Ships[ship_id])
    # print(filtered_df)
    for container in filtered_df:
        containers.append(container)
    all_containers = all_containers + containers
    containers = []
    ship_id += 1

def convert2list(li):
    return list(map(lambda el:[el], li))

def convert2tuple(list):
    return (*list, )

def ship_info(ship_group_number):
    # Odczytywanie informacji o statku
    # Grupa #0 to cale wyrazenie
    # Grupa #1 to id statku
    # Grupa #2 to jego nazwa
    # Grupa #3 to klasa do ktorej nalezy
    for ship in Ships:
        ship_pattern = re.compile(r'(\d+): (\w+-?\w+) \((\w+ ?-?\w+?)\)')
        ship_matches = ship_pattern.finditer(ship)
        for ship_match in ship_matches:
            if ship_group_number == 0:
                ships_info.append(ship_match.group(0))
            elif ship_group_number == 1:
                ships_info.append(ship_match.group(1))
            elif ship_group_number == 2:
                ships_info.append(ship_match.group(2))
            elif ship_group_number == 3:
                ships_info.append(ship_match.group(3))
    return ships_info

def container_info(container_group_number):
    # Odczytywanie informacji o kontenerze
    # Grupa #0 to cale wyrazenie
    # Grupa #1 to kraj pochodzenia kontenera
    # Grupa #2 to kraj docelowy
    # Grupa #3 to numer kontenera
    # Grupa #4 to waga
    # Grupa #5 to typ ładunku (A0-Z9)
    # Grupa #6 to nazwa firmy nadajacej kontener
    # Grupa #7 to kraj pochodzenia firmy
    # Grupa #8 to koszt w USD
    for container_name in all_containers:
        container_pattern = re.compile(r'([A-Z][A-Z])-([A-Z][A-Z])-(\d+)/(\d\d\d\d)/(\w\w)@(\w+)\.([a-z][a-z])/(\d+)')
        container_matches = container_pattern.finditer(container_name)
        for container_match in container_matches:
            if container_group_number == 0:
                containers_info.append(container_match.group(0))
            elif container_group_number == 1:
                containers_info.append(container_match.group(1))
            elif container_group_number == 2:
                containers_info.append(container_match.group(2))
            elif container_group_number == 3:
                containers_info.append(container_match.group(3))
            elif container_group_number == 4:
                containers_info.append(container_match.group(4))
            elif container_group_number == 5:
                containers_info.append(container_match.group(5))
            elif container_group_number == 6:
                containers_info.append(container_match.group(6))
            elif container_group_number == 7:
                containers_info.append(container_match.group(7))
            elif container_group_number == 8:
                containers_info.append(container_match.group(8))
    return containers_info

def containers2jp(number_of_containers, destination):
    container_info(2)
    for container_destination in containers_info:
        if container_destination == destination:
            number_of_containers += 1
        else:
            pass
    return number_of_containers

def x1_indexes(x1_containers_indexes):
    container_info(5)
    container_index = 0
    for cargo_type in containers_info:
        if cargo_type == "X1":
            x1_containers_indexes.append(container_index)
        else:
            pass
        container_index += 1
    return x1_containers_indexes

# Konwersja listy do slownika
ship_info(3)
ships_classes = dict.fromkeys(ships_info, 0)
print(ships_classes)
ships_info.clear()

# Zliczenie kontenerow plynacych do Japonii
destination_jp = containers2jp(destination_jp, destination_country)
print("Desination JP:", destination_jp)
containers_info.clear()

# Znalezienie indeksow ladunkow typu X1 na liscie all_containers
containers_indexes = x1_indexes(containers_indexes)
print("Number of X1 containers:", len(containers_indexes))
containers_info.clear()

# Kopiowanie kontenerow z ladunkiem X1 na nowa liste
for element in containers_indexes:
    x1_list.append(all_containers[element])

# Odczytanie ciezaru kazdego z kontenera X1 i dodanie na nowa liste
for container in x1_list:
    container_pattern = re.compile(r'([A-Z][A-Z])-([A-Z][A-Z])-(\d+)/(\d\d\d\d)/(\w\w)@(\w+)\.([a-z][a-z])/(\d+)')
    container_matches = container_pattern.finditer(container)
    for container_match in container_matches:
        x1_weight_list.append(container_match.group(4))

# Okreslenie sredniej wagi kontenera X1 i zaokraglenie wyniku w gore
x1_weight_list = list(map(float, x1_weight_list))
x1_total_weight = sum(x1_weight_list)
avg_x1_weight = math.ceil(x1_total_weight/len(x1_weight_list))
print("Average weight:", avg_x1_weight)

total_rows_list = []
for ship_name in Ships:
    total_rows = df[ship_name].count()
    total_rows_list.append(total_rows)

ship_class_list = ship_info(3)

load_cargo_index = 0

ship_class_list = convert2list(ship_class_list)

for each_ship in ship_class_list:
    each_ship.append(total_rows_list[load_cargo_index])
    load_cargo_index += 1

ship_class_list.sort()
print(ship_class_list)
