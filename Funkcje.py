import re

def elements2list(li):
    return list(map(lambda el:[el], li))

def list2tuple(li):
    return (*li, )

def ship_info(information_sought, list_of_ships):
    # Odczytywanie informacji o statku
    # Grupa #0 to cale wyrazenie
    # Grupa #1 to id statku
    # Grupa #2 to jego nazwa
    # Grupa #3 to klasa do ktorej nalezy
    extracted_info = []
    for ship in list_of_ships:
        ship_pattern = re.compile(r'(\d+): (\w+-?\w+) \((\w+ ?-?\w+?)\)')
        ship_matches = ship_pattern.finditer(ship)
        for ship_match in ship_matches:
            extracted_info.append(ship_match.group(information_sought))
    return extracted_info

def container_info(information_sought, list_of_containers):
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
    extracted_info = []
    for container in list_of_containers:
        container_pattern = re.compile(
            r'([A-Z][A-Z])-([A-Z][A-Z])-(\d+)/(\d\d\d\d)/(\w\w)@(\w+)\.'
            '([a-z][a-z])/(\d+)')
        container_matches = container_pattern.finditer(container)
        for container_match in container_matches:
            extracted_info.append(container_match.group(information_sought))
    return extracted_info

def containers2country(destination, list_of_containers):
    containers_info_list = container_info(2, list_of_containers)
    number_of_containers = 0
    for container_destination in containers_info_list:
        if container_destination == destination:
            number_of_containers += 1
        else:
            pass
    return number_of_containers

def cargo_type_index(type_sought, list_of_containers):
    containers_info_list = container_info(5, list_of_containers)
    index_list = []
    container_index = 0
    for cargo_type in containers_info_list:
        if cargo_type == type_sought:
            index_list.append(container_index)
        else:
            pass
        container_index += 1
    return index_list

def cargo_country_index(type_sought, list_of_containers):
    containers_info_list = container_info(7, list_of_containers)
    index_list = []
    container_index = 0
    for cargo_type in containers_info_list:
        if cargo_type == type_sought:
            index_list.append(container_index)
        else:
            pass
        container_index += 1
    return index_list

def containers_in_classes(class_dict, input_list):
    class_size = {}
    for k, v in class_dict.items():
        for value_pair in input_list:
            if k == value_pair[0]:
                v = v + value_pair[1]
        class_size.update({k: v})
    return class_size

def class_sizes(class_dict, ship_list):
    class_list = ship_info(3, ship_list)
    class_size = {}
    for k, v in class_dict.items():
        for ship in class_list:
            if k == ship:
                v += 1
        class_size.update({k: v})
    return class_size

def type_calc(type_dict, input_list):
    calc = {}
    for k, v in type_dict.items():
        for value_pair in input_list:
            if k == value_pair[0]:
                v = v + value_pair[1]
        calc.update({k: v})
    return calc
