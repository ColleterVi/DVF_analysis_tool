import requests
from tqdm import tqdm
import numpy as np

# on définie la fonction additionner avec le mot clé 'def'
# entre parenthèse on définie qu'elle prend 2 arguments: nombre_1 et 2: des entiers 'int'
# elle retourne --> un entier (noté: 'int')
def additionner_deux_entiers(nombre_1: int, nombre_2: int) -> int:
    # Vérifions que ce sont bien des entiers
    # Si le nombre 1 n'est pas un entier (int) ou le nombre 2 n'est pas un entier (int)
    if not isinstance(nombre_1, int) or not isinstance(nombre_2, int):

        print(
            "Erreur: vous devez donner 2 nombres entiers à la fonction."
        )  # Affiche un message d'erreur

        return  # Quitter la fonction en ne retournant rien

    # Si la condition est remplie, on peut continuer
    # Additionne les deux nombres et stock le résultat dans la variable "resultat"
    resultat = nombre_1 + nombre_2
    # affiche le résultat à l'écran
    print("L'opération donne ", nombre_1, " + ", nombre_2, " = ", resultat)
    # retourne le résultat
    return resultat


def download_DVF_data():
    """Download data from cadastre database sorted by year"""
    url = "https://cadastre.data.gouv.fr/data/etalab-dvf/latest/csv/"
    years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    file_name = "/full.csv.gz"

    for year in years:
        response = requests.get(url + str(year) + file_name, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(
            total=total_size_in_bytes,
            unit="iB",
            unit_scale=True,
        )
        progress_bar.set_description(f"Downloading DVF data from {year}")
        with open(f"dvf/data_dvf_{year}.csv.gz", "wb") as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)


if __name__ == "__main__":
    download_DVF_data()