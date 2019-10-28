import pandas as pd
import re
import math

# df to skrot od Data Frame
# df = pd.read_csv('dane.csv', sep=';', header=0, dtype=str)
df = pd.read_csv('C:\\Users\\PLPD00293\\Desktop\\DaftAcademy\\dane.csv', \
sep=';', header=0, dtype=str)

ShipsCSV = df.columns  # pobiera statki z pliku CSV
Ships = []  # zawiera zestawienie wszystkich statkow z naglowkow kolumn
containers = []  # zbiera informacje o kontenerach na analizowanym statku
filtered_df = []  # usuwa puste rekordy ze zmiennej 'df'
all_containers = []  # zawiera wszystkie kontenery
ships_info = []  # ship_info() zwraca tutaj informacje o statkach
containers_info = []  # container_info() zwraca tutaj informacje o kontenerach
X1_list = []  # lista zawierajaca spis wszystkich konenerow X1
containers_indexes = []  # indeksy kontenerow X1 na liscie all_containers
X1_weight_list = []  # lista zawierajaca spis ciezarow wszystkich kontenerow X1
ship_id = 0  # robocze id nadane aktualnie analizowanemu statkowi
container_id = 0  # robocze id nadane aktualnie analizowanemu kontenerowi
destination_JP = 0  # Zliczenie kontenerow plynacych do Japonii

# Przeniesienie statkow do nowej listy
for ship in ShipsCSV:
    Ships.append(ship)

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

def ship_info(G):
    '''
    Odczytywanie informacji o statku
    Grupa #0 to cale wyrazenie
    Grupa #1 to id statku
    Grupa #2 to jego nazwa
    Grupa #3 to klasa do ktorej nalezy
    '''
    for ship in Ships:
        ship_pattern = re.compile(r'(\d+): (\w+-?\w+) \((\w+ ?-?\w+?)\)')
        ship_matches = ship_pattern.finditer(ship)
        for ship_match in ship_matches:
            if G == 0:
                ships_info.append(ship_match.group(0))
            elif G == 1:
                ships_info.append(ship_match.group(1))
            elif G == 2:
                ships_info.append(ship_match.group(2))
            elif G == 3:
                ships_info.append(ship_match.group(3))
            # print(ship_match.group(0))
            # print("Id statku:", ship_match.group(1))
            # print("Nazwa statku:", ship_match.group(2))
            # print("Klasa statku:", ship_match.group(3), "\n")
    return ships_info

def container_info(C):
    '''
    Odczytywanie informacji o kontenerze
    Grupa #0 to cale wyrazenie
    Grupa #1 to kraj pochodzenia kontenera
    Grupa #2 to kraj docelowy
    Grupa #3 to numer kontenera
    Grupa #4 to waga
    Grupa #5 to typ ładunku (A0-Z9)
    Grupa #6 to nazwa firmy nadajacej kontener
    Grupa #7 to kraj pochodzenia firmy
    Grupa #8 to koszt w USD
    '''
    for container in all_containers:
        container_pattern = re.compile(r'([A-Z][A-Z])-([A-Z][A-Z])-(\d+)/(\d\d\d\d)/(\w\w)@(\w+)\.([a-z][a-z])/(\d+)')
        container_matches = container_pattern.finditer(container)
        for container_match in container_matches:
            if C == 0:
                containers_info.append(container_match.group(0))
            elif C == 1:
                containers_info.append(container_match.group(1))
            elif C == 2:
                containers_info.append(container_match.group(2))
            elif C == 3:
                containers_info.append(container_match.group(3))
            elif C == 4:
                containers_info.append(container_match.group(4))
            elif C == 5:
                containers_info.append(container_match.group(5))
            elif C == 6:
                containers_info.append(container_match.group(6))
            elif C == 7:
                containers_info.append(container_match.group(7))
            elif C == 8:
                containers_info.append(container_match.group(8))
    return containers_info

def containers2JP(destination_JP):
    container_info(2)
    for desination in containers_info:
        if desination == 'JP':
            destination_JP += 1
        else:
            pass
    return destination_JP

def X1_indexes(containers_indexes):
    container_info(5)
    container_index = 0
    for cargo_type in containers_info:
        if cargo_type == "X1":
            containers_indexes.append(container_index)
        else:
            pass
        container_index += 1
    return containers_indexes

# Konwersja listy do slownika
ship_info(3)
ships_classes = dict.fromkeys(ships_info, 0)
print(ships_classes)

# Zliczenie kontenerow plynacych do Japonii
destination_JP = containers2JP(destination_JP)
print("Desination JP:", destination_JP)
# Nalezy wyzerowac liste containers_info przed kolejnym uzyciem, inaczej beda
# dodawane nowe rekordy przy kolejnym uzyciu
containers_info = []

# Znalezienie indeksow ladunkow typu X1 na liscie all_containers
containers_indexes = X1_indexes(containers_indexes)
print("Number of X1 containers:", len(containers_indexes))
containers_info = []

# Skopiowanie kontenerow z ladunkiem X1 na nowa liste
for element in containers_indexes:
    X1_list.append(all_containers[element])

# Odczytanie ciezaru kazdego z kontenera X1 i dodanie na nowa liste
for container in X1_list:
    container_pattern = re.compile(r'([A-Z][A-Z])-([A-Z][A-Z])-(\d+)/(\d\d\d\d)/(\w\w)@(\w+)\.([a-z][a-z])/(\d+)')
    container_matches = container_pattern.finditer(container)
    for container_match in container_matches:
        X1_weight_list.append(container_match.group(4))

# Okreslenie sredniej wagi kontenera X1 i zaokraglenie wyniku w gore
X1_weight_list = list(map(float, X1_weight_list))
X1_total_weight = sum(X1_weight_list)
avg_X1_weight = math.ceil(X1_total_weight/len(X1_weight_list))
print("Average weight:", avg_X1_weight)
