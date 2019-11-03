import pandas as pd
import math
from Funkcje import *

# df to skrot od Data Frame
df = pd.read_csv('dane.csv', sep=';', header=0, dtype=str)

all_ships = df.columns  # pobiera statki z pliku CSV
filtered_df = []  # usuwa puste rekordy ze zmiennej 'df'
containers = []  # zbiera informacje o kontenerach na analizowanym statku
all_containers = []  # zawiera wszystkie kontenery
x1_containers = []  # lista zawierajaca spis wszystkich konenerow X1
x1_weight_list = []  # lista zawierajaca spis ciezarow wszystkich kontenerow X1
ship_id = 0  # robocze id nadane aktualnie analizowanemu statkowi
polish_containers = []  # kontenery polskich firm
polish_companies = []  # polskie firmy
german_containers = []  # kontenery niemieckich firm
german_type_list = []  # typy kontenerow wyslane przez niemieckie firmy
german_weight_list = []  # ciezary niemieckich kontenerow
german_cost_list = []  # wartosci niemieckich kontenerow

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

# Znalezienei indeksow kontenerow polskich firm
polish_indexes = cargo_country_index("pl", all_containers)

# Kopiowanie kontenerow polskich firm na nowa liste
for index in polish_indexes:
    polish_containers.append(all_containers[index])

# Wyciagniecie informacji o nazwie firmy
for container in polish_containers:
    polish_companies = container_info(6, polish_containers)

# Zliczenie ilosci kontenerow wyslanych przez firme
polish_containers = {}
for company in polish_companies:
    polish_containers.setdefault(company, 0)
    polish_containers[company] += 1

# Znalezienie najwiekszej polskiej firmy
biggest_polish_company = max(polish_containers, key=lambda k:polish_containers[k])
print("Biggest polish company:", biggest_polish_company)

# Znalezienie indeksow kontenerow niemieckich firm
german_indexes = cargo_country_index("de", all_containers)

# Kopiowanie kontenerow niemieckich firm na nowa liste
for index in german_indexes:
    german_containers.append(all_containers[index])

# Wyciagniecie informacji o ladunku
for container in german_containers:
    german_weight_list = container_info(4, german_containers)
    german_type_list = container_info(5, german_containers)
    german_cost_list = container_info(8, german_containers)

german_weight_list = list(map(int, german_weight_list))
german_cost_list = list(map(int, german_cost_list))

# Stworzenie drugiego poziomu listy zawierajacej info o typie ladunku
de_list = elements2list(german_type_list)
de_list2 = elements2list(german_type_list)

# Dodanie do wewnetrznych list informacji o ciezarze
german_cargo_index = 0
for container in de_list:
    container.append(german_weight_list[german_cargo_index])
    german_cargo_index += 1

# Dodanie do wewnetrznych list informacji o cenie
german_cargo_index2 = 0
for container2 in de_list2:
    container2.append(german_cost_list[german_cargo_index2])
    german_cargo_index2 += 1

# Konwersja listy typow ladunku do slownika
cargo_type_dict = dict.fromkeys(german_type_list, 0)

# Sumowanie masy wszystkich typow
type_total_weight = type_calc(cargo_type_dict, de_list)

# Sumowanie wartosci ($) typow
type_total_cost = type_calc(cargo_type_dict, de_list2)

# Obliczenie sredniej wartosci typu ladunku
weight_cost_ratio = {k: type_total_weight[k]/type_total_cost[k] for k in type_total_weight}
most_expensive = max(weight_cost_ratio, key=lambda k: weight_cost_ratio[k])
print("Most expensive:", most_expensive)

# Znalezienie indeksow ladunkow typu X1 na liscie all_containers
X1_indexes = cargo_type_index("X1", all_containers)

# Kopiowanie kontenerow z ladunkiem X1 na nowa liste
for element in X1_indexes:
    x1_containers.append(all_containers[element])

# Odczytanie ciezaru kazdego z kontenera X1 i dodanie na nowa liste
for container in x1_containers:
    container_pattern = re.compile(
        r'([A-Z][A-Z])-([A-Z][A-Z])-(\d+)/(\d\d\d\d)'
        '/(\w\w)@(\w+)\.([a-z][a-z])/(\d+)')
    container_matches = container_pattern.finditer(container)
    for container_match in container_matches:
        x1_weight_list.append(container_match.group(4))

# Okreslenie sredniej wagi kontenera X1 i zaokraglenie wyniku w gore
x1_weight_list = list(map(float, x1_weight_list))
x1_total_weight = sum(x1_weight_list)
avg_x1_weight = math.ceil(x1_total_weight/len(x1_weight_list))
print("Average weight:", avg_x1_weight)

# Zliczenie licby rekordow w kolumnach, czyli ile przewozi kazdy statek
total_number_of_containers = []
for ship_name in all_ships:
    total = df[ship_name].count()
    total_number_of_containers.append(total)

ship_class_list = ship_info(3, all_ships)

ship_class_list = elements2list(ship_class_list)

load_index = 0
for each_class in ship_class_list:
    each_class.append(total_number_of_containers[load_index])
    load_index += 1

class_size = containers_in_classes(ships_classes, ship_class_list)

# Obliczenie sredniej ilosci kontenerow na statku danej klasy
average_on_class = {k: class_size[k]/total_number_of_ships_in_class[k] for k in class_size}
biggest_class = max(average_on_class, key=lambda k: average_on_class[k])
print("Biggest class:", biggest_class)
