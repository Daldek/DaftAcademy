import pandas as pd
from re import compile
import math
from Funkcje import *

# df to skrot od Data Frame
df = pd.read_csv('dane.csv', sep=';', header=0, dtype=str)

all_ships = df.columns  # pobiera statki z pliku CSV
filtered_df = []  # usuwa puste rekordy ze zmiennej 'df'
containers = []  # zbiera informacje o kontenerach na analizowanym statku
all_containers = []  # zawiera wszystkie kontenery
x1_list = []  # lista zawierajaca spis wszystkich konenerow X1
x1_weight_list = []  # lista zawierajaca spis ciezarow wszystkich kontenerow X1
ship_id = 0  # robocze id nadane aktualnie analizowanemu statkowi
class_size = {}

# Usuwanie pustych rekordow
while ship_id != len(all_ships):
    filtered_df = df[df[all_ships[ship_id]].notnull()]
    filtered_df = filtered_df[all_ships[ship_id]]
    for container in filtered_df:
        containers.append(container)
    all_containers = all_containers + containers
    containers = []
    ship_id += 1

# Konwersja listy do slownika
ships_info = ship_info(3, all_ships)
ships_classes = dict.fromkeys(ships_info, 0)

# Zliczenie kontenerow plynacych do Japonii
destination_jp = containers2country("JP", all_containers)
print("Desination JP:", destination_jp)

# Zliczenie liczby statkow danej klasie
total_number_of_ships_in_class = class_sizes(ships_classes, all_ships)

# Znalezienie indeksow ladunkow typu X1 na liscie all_containers
containers_indexes = cargo_type_index("X1", all_containers)

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

# Do opisania
total_rows_list = []
for ship_name in all_ships:
    total_rows = df[ship_name].count()
    total_rows_list.append(total_rows)

ship_class_list = ship_info(3, all_ships)

load_cargo_index = 0

ship_class_list = elements2list(ship_class_list)

for each_ship in ship_class_list:
    each_ship.append(total_rows_list[load_cargo_index])
    load_cargo_index += 1

class_size = containers_in_classes(ships_classes, ship_class_list)

# Obliczenie sredniej ilosci kontenerow na statku danej klasy
average_on_class = {k: class_size[k]/total_number_of_ships_in_class[k] for k in class_size}
biggest_class = max(average_on_class, key=lambda k: average_on_class[k])
print("Biggest class:", biggest_class)
