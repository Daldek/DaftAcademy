import pandas as pd
from re import compile
import math
from Funkcje import *

# df to skrot od Data Frame
df = pd.read_csv('dane.csv', sep=';', header=0, dtype=str)

ShipsCSV = df.columns  # pobiera statki z pliku CSV
Ships = []  # zawiera zestawienie wszystkich statkow z naglowkow kolumn
filtered_df = []  # usuwa puste rekordy ze zmiennej 'df'
containers = []  # zbiera informacje o kontenerach na analizowanym statku
all_containers = []  # zawiera wszystkie kontenery
x1_list = []  # lista zawierajaca spis wszystkich konenerow X1
x1_weight_list = []  # lista zawierajaca spis ciezarow wszystkich kontenerow X1
ship_id = 0  # robocze id nadane aktualnie analizowanemu statkowi

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

# Konwersja listy do slownika
ships_info = ship_info(3, Ships)
ships_classes = dict.fromkeys(ships_info, 0)
print(ships_classes)

# Zliczenie kontenerow plynacych do Japonii
destination_jp = containers2country("JP", all_containers)
print("Desination JP:", destination_jp)

# Znalezienie indeksow ladunkow typu X1 na liscie all_containers
containers_indexes = cargo_type_index("X1", all_containers)
print("Number of X1 containers:", len(containers_indexes))

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

ship_class_list = ship_info(3, Ships)

load_cargo_index = 0

ship_class_list = elements2list(ship_class_list)

for each_ship in ship_class_list:
    each_ship.append(total_rows_list[load_cargo_index])
    load_cargo_index += 1

ship_class_list.sort()
print(ship_class_list)
