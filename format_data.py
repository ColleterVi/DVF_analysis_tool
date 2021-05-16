import pandas as pd
import numpy as np
import time
import math
import json
from tqdm import tqdm
from geopy import Nominatim
import pickle

map_geopy_dvf = {
    "adresse_numero": "house_number",  # split string and take first
    "adresse_nom_voie": "road",
    "adresse_code_voie": "house_number",  # split string and take second
    "code_postal": "postcode",
    "code_commune": "ballec",
    "nom_commune": ["town", "village"],  # take town if present else take village
    "code_departement": "postcode",  # take first 2 digits
}


def recover_adress(df, year):
    locator = Nominatim(user_agent="myGeocoder")
    address_dict = {}
    add = []
    for latitude, longitude in df[df["address_known"] == False][
        ["latitude", "longitude"]
    ].itertuples(index=False):
        if not math.isnan(latitude):
            add.append((latitude, longitude))
    add = set(add)
    with tqdm(total=len(add)) as bar:
        for latitude, longitude in add:
            bar.set_description(
                f"processing addresses lat={str(latitude)}, lon={longitude}"
            )
            try:
                addresse = str(latitude) + ", " + str(longitude)
                address_dict[(latitude, longitude)] = locator.reverse(addresse)
            except Exception as e:
                print(
                    "Could not find addresse for coordinates ",
                    str(latitude),
                    str(longitude),
                    e,
                )
            bar.update(1)
    for k, v in address_dict.items():
        try:
            address_dict[k] = v.raw
        except:
            print("There was an issue with:", k, v)
    with open(f"address_{year}.pickle", "wb") as f:
        pickle.dump(address_dict, f)
    return address_dict


def add_addresses_to_df(df, addresses: dict):
    with tqdm(total=df[~df["address_known"]].shape[0]) as bar:
        bar.set_description("Adding addresses to dataframe")
        for index in df[~df["address_known"]].index:
            if not math.isnan(df.loc[index, "latitude"]):
                lat_long = (df.loc[index, "latitude"], df.loc[index, "longitude"])
                new_addresse = addresses[lat_long]["address"]
                # numéro et code d'adresse
                if "house_number" in new_addresse:
                    numbers = new_addresse["house_number"].split(" ")
                    if not isinstance(df.loc[index, "adresse_numero"], str):
                        df.loc[index, "adresse_numero"] = numbers[0]
                        if (
                            not isinstance(df.loc[index, "adresse_code_voie"], str)
                            and math.isnan(df.loc[index, "adresse_code_voie"])
                            and len(numbers) > 1
                        ):
                            df.loc[index, "adresse_code_voie"] = numbers[1]
                # nom de voie
                if "road" in new_addresse:
                    if not isinstance(df.loc[index, "adresse_nom_voie"], str):
                        df.loc[index, "adresse_nom_voie"] = new_addresse["road"]
                # code postale et code département
                if "postcode" in new_addresse:
                    code_postale = new_addresse["postcode"]
                    if len(code_postale) > 5:
                        code_postale = code_postale[:5]
                    elif len(code_postale) < 5:
                        while len(code_postale) < 5:
                            code_postale = "0" + code_postale

                    if math.isnan(df.loc[index, "code_postal"]):
                        df.loc[index, "code_postal"] = code_postale
                    if isinstance(df.loc[index, "code_departement"], str):
                        # Si c'est un domtom on prend les 3 premiers numéros, sinon 2
                        if code_postale[:2] == "97":
                            df.loc[index, "code_departement"] = code_postale[:3]
                        else:
                            df.loc[index, "code_departement"] = code_postale[:2]
                # nom de la commune
                if "town" in new_addresse:
                    if not isinstance(df.loc[index, "nom_commune"], str):
                        df.loc[index, "nom_commune"] == new_addresse["town"]
                # parfois ya pas de commune donc le village est pris
                elif "village" in new_addresse:
                    if not isinstance(df.loc[index, "nom_commune"], str):
                        df.loc[index, "nom_commune"] == new_addresse["village"]

                bar.update(1)


def format_code_postal(text) -> str:
    if isinstance(text, float) and not math.isnan(text):
        postal_code = str(int(text))
        if len(postal_code) < 5:
            while len(postal_code) < 5:
                postal_code = "0" + postal_code
        elif len(postal_code) > 5:
            postal_code = postal_code[:5]
        return postal_code
    elif isinstance(text, float) and math.isnan(text):
        return ""
    elif isinstance(text, str):
        return text


def format_adresse_number(text) -> str:
    if isinstance(text, float) and not math.isnan(text):
        return str(int(text))
    elif isinstance(text, float) and math.isnan(text):
        return ""
    elif isinstance(text, str):
        return text


def format_valeur_fonciere(number) -> int:
    if isinstance(number, float) and not math.isnan(number):
        return int(number)
    elif isinstance(number, float) and math.isnan(number):
        return None


def open_csv_file(filename: str, delimiter: str = ","):
    try:
        with open(filename, "r") as f:
            data = pd.read_csv(f, delimiter=delimiter)
        return data
    except IOError as e:
        raise (e)


def clean_dataframe_DVF(df):
    df["adresse_numero"] = df["adresse_numero"].apply(
        lambda y: str(int(y)) if (isinstance(y, float) and not math.isnan(y)) else y
    )
    df["valeur_fonciere"] = df["valeur_fonciere"].apply(
        lambda y: int(y) if (isinstance(y, float) and not math.isnan(y)) else y
    )
    # si l'adresse est connue par defaut: case vaut vrai, sinon faux
    # Noter les transactions sans adresses
    df["address_known"] = df["adresse_nom_voie"].apply(
        lambda y: True if isinstance(y, str) else False
    )

    addresses = recover_adress(df, year)  # get addresses missing
    # addresses = pickle.load(open("address_2020.pickle", "rb"))
    add_addresses_to_df(df, addresses)  # add adresses to dataframe

    # nom de voie de l'adresse en format titre : Une Majuscule A Chaque Mot
    df["adresse_nom_voie"] = (
        df["adresse_nom_voie"].astype(str).apply(lambda y: y.title())
    )
    df["code_postal"] = df["code_postal"].apply(lambda y: format_code_postal(y))
    # Numero d'adresse converti en entier pour enlever les virgule puis en texte pour le combiner avec le nom de voie
    df["adresse_numero"] = df["adresse_numero"].apply(
        lambda x: format_adresse_number(x)
    )

    # Nombre de pieces principale -> nombre entier pour enlever virgule
    df["nombre_pieces_principales"] = df["nombre_pieces_principales"].astype("Int32")

    df["valeur_fonciere"] = df["valeur_fonciere"].apply(
        lambda y: format_valeur_fonciere(y)
    )

    # Créer une nouvelle colonne qui contient l'adresse entière
    df["adresse"] = (
        df["adresse_numero"]
        + " "
        + df["adresse_nom_voie"]
        + " "
        + df["code_postal"]
        + " "
        + df["nom_commune"]
    ).str.strip()

    # convertie les dates en format lise par humain et ordinateur
    df["date_mutation"] = pd.to_datetime(df["date_mutation"])

    # premiere version du tableau nettoyé
    return df


if __name__ == "__main__":
    all_years = [
        2014,
        2015,
        2016,
        2017,
        2018,
        2019,
    ]  # 2014, 2015, 2016, 2017, 2018, 2019, 2020
    for year in all_years:
        df = pd.read_csv(
            f"/home/vee/Documents/MathieuMemoire/dvf/raw_data/data_dvf_{year}.csv",
            low_memory=False,
        )
        df = clean_dataframe_DVF(df)
        df.to_csv(
            f"/home/vee/Documents/MathieuMemoire/dvf/formatted_data/data_dvf_{year}.csv"
        )
        print("DONE ", year)