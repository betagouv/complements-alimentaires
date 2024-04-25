from collections import defaultdict


def invert_dict(input_dict: dict) -> dict:
    """
    Inverse les clés et les valeurs d'un dictionnaire où les valeurs sont des listes d'entiers.
    Cette fonction prend un dictionnaire dont les clés sont des chaînes de caractères et les valeurs sont des listes d'entiers.
    Elle renvoie un nouveau dictionnaire où chaque entier des listes originales devient une clé, et chaque clé originale devient
    une valeur dans la liste correspondante à cette nouvelle clé.
    """
    output_dict = defaultdict(list)
    for key, values in input_dict.items():
        for value in values:
            output_dict[value].append(key)
    return dict(output_dict)
