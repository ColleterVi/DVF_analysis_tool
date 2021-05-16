# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
from dash_html_components.Div import Div
import pandas as pd
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import Input, Output
from data_columns import maison, appartement, local, terrain
from datetime import date

"""config = configparser.ConfigParser()
config.read("./config.cfg")
columns_maison = config.get("data_format", "Maison")
columns_appartement = config.get("data_format", "Appartement")
columns_terrain = config.get("data_format", "Terrain")
columns_local = config.get("data_format", "Local")
[data_format]"""
SELECT_TYPE = {
    "appartement": appartement,
    "maison": maison,
    "local": local,
    "terrain": terrain,
}
all_years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
current_year = 2020
df = pd.DataFrame()
PAGE_SIZE = 20
app = dash.Dash(
    __name__,
)  # external_stylesheets=external_stylesheets

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Mathieu Vittecoq, Outil d'analyse DVF",
                    style={"textAlign": "center"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Année"),
                                        dcc.Dropdown(
                                            id="year-transaction",
                                            options=[
                                                {
                                                    "label": str(i),
                                                    "value": str(i),
                                                }
                                                for i in all_years
                                            ],
                                            multi=False,
                                            value=2020,
                                            style={
                                                "display": "flex",
                                            },
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Type de local"),
                                        dcc.Dropdown(
                                            id="dropdown-type-transaction",
                                            options=[
                                                {
                                                    "label": "Appartement",
                                                    "value": "appartement",
                                                },
                                                {"label": "Maison", "value": "maison"},
                                                {
                                                    "label": "Terrain",
                                                    "value": "terrain",
                                                },
                                            ],
                                            multi=True,
                                            value=["appartement"],
                                            style={
                                                "display": "flex",
                                            },
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Adresse"),
                                        dcc.Input(
                                            id="query-address",
                                            type="search",
                                            placeholder="Cherchez une adresse",
                                            style={
                                                "display": "flex",
                                            },
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Code postal ou département"),
                                        dcc.Input(
                                            id="query-departement",
                                            type="number",
                                            placeholder="code postal",
                                            style={
                                                "display": "flex",
                                            },
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Surface en m²"),
                                        html.Div(
                                            [
                                                dcc.Input(
                                                    id="surface-min",
                                                    type="number",
                                                    min=0,
                                                    max=100000000,
                                                    placeholder="surface min",
                                                    style={
                                                        "display": "flex",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="surface-max",
                                                    type="number",
                                                    min=0,
                                                    max=1000000000,
                                                    placeholder="surface max",
                                                    style={
                                                        "display": "flex",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Valeur foncière en €"),
                                        html.Div(
                                            [
                                                dcc.Input(
                                                    id="valeur-fonciere-min",
                                                    type="number",
                                                    min=0,
                                                    max=100000000000,
                                                    placeholder="Prix min",
                                                    style={
                                                        "display": "flex",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="valeur-fonciere-max",
                                                    type="number",
                                                    min=0,
                                                    max=100000000000,
                                                    placeholder="Prix max",
                                                    style={
                                                        "display": "flex",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Nombre de pièces principales"),
                                        html.Div(
                                            [
                                                dcc.Input(
                                                    id="nb-piece-min",
                                                    type="number",
                                                    min=0,
                                                    max=100,
                                                    placeholder="Nombre minimum",
                                                    style={
                                                        "display": "flex",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="nb-piece-max",
                                                    type="number",
                                                    min=0,
                                                    max=100,
                                                    placeholder="Nombre maximum",
                                                    style={
                                                        "display": "flex",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H6("Date"),
                                        html.Div(
                                            dcc.DatePickerRange(
                                                id="datepicker",
                                                start_date_id="start-date",
                                                end_date_id="end-date",
                                                min_date_allowed=date(
                                                    current_year, 1, 1
                                                ),
                                                max_date_allowed=date(
                                                    current_year, 12, 31
                                                ),
                                                display_format="DD/MM/Y",
                                                start_date_placeholder_text=(
                                                    "date minimum"
                                                ),
                                                end_date_placeholder_text=(
                                                    "date maximum"
                                                ),
                                                start_date=date(current_year, 1, 1),
                                                end_date=date(current_year, 12, 31),
                                                style={"z-index": "9999 !important"},
                                            )
                                        ),
                                    ]
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-around",
                            },
                        )
                    ]
                ),
                html.Br(),
                dt.DataTable(
                    id="data-table",
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action="custom",
                    export_format="xlsx",
                    style_table={"width": "85vw", "overflowY": "auto", "z-index": "0"},
                    fixed_rows={"headers": True},
                    style_cell={
                        "whiteSpace": "normal",
                        "height": "auto",
                        "textAlign": "left",
                        "minWidth": 100,
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                    },
                    virtualization=True,
                ),
                html.Div(  # below table (page size, )
                    [
                        dcc.Input(id="page-size", type="number", value=PAGE_SIZE),
                        html.Div(
                            [
                                html.H4("nombre de résultats"),
                                html.P(id="nombre-de-resultats"),
                            ]
                        ),
                    ],
                )
                # DATE PICKER
            ],
        )
    ],
    style={"display": "flex", "justify-content": "center"},
)


@app.callback(Output("data-table", "page_size"), Input("page-size", "value"))
def update_page_size(page_size):
    if page_size and isinstance(page_size, int):
        return page_size
    elif page_size is None:
        return None
    else:
        return PAGE_SIZE


# https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=48.857832,2.295226&heading=-45&pitch=38&fov=80
@app.callback(
    Output("data-table", "data"),
    Output("data-table", "columns"),
    Output("nombre-de-resultats", "children"),
    Output("datepicker", "min_date_allowed"),
    Output("datepicker", "max_date_allowed"),
    Output("datepicker", "start_date"),
    Output("datepicker", "end_date"),
    Input("dropdown-type-transaction", "value"),
    Input("data-table", "page_current"),
    Input("data-table", "page_size"),
    Input("query-address", "value"),
    Input("query-departement", "value"),
    Input("surface-min", "value"),
    Input("surface-max", "value"),
    Input("valeur-fonciere-min", "value"),
    Input("valeur-fonciere-max", "value"),
    Input("nb-piece-min", "value"),
    Input("nb-piece-max", "value"),
    Input("datepicker", "start_date"),
    Input("datepicker", "end_date"),
    Input("year-transaction", "value"),
)
def update_table(
    type_mutation,
    page_current,
    page_size,
    query_adress,
    dpt,
    surface_min,
    surface_max,
    valeur_fonciere_min,
    valeur_fonciere_max,
    nb_piece_min,
    nb_piece_max,
    start_date,
    end_date,
    year,
):  # date_min, date_max, radius:int,price_min, price_max
    # selectionne le ou les types de local
    global current_year
    global df
    if year != current_year or df.shape[0] == 0:
        current_year = year
        start_date = date(int(current_year), 1, 1)
        end_date = date(int(current_year), 12, 31)
        df = pd.read_csv(
            f"/home/vee/Documents/MathieuMemoire/dvf/formatted_data/data_dvf_{year}.csv",
            low_memory=False,
        )

        df = df.infer_objects()
        df["date_mutation"] = pd.to_datetime(df["date_mutation"]).dt.date
        df["Street View"] = (
            (
                ["https://www.google.com/maps/@?api=1&map_action=pano&viewpoint="]
                * df.shape[0]
            )
            + df["latitude"].astype(str)
            + [","] * df.shape[0]
            + df["longitude"].astype(str)
            + ["&heading=-45&pitch=38&fov=80"] * df.shape[0]
        )
    min_date = date(int(year), 1, 1)
    max_date = date(int(year), 12, 31)
    dff = df[
        df["type_local"].isin(
            [elem["name"] for elem in [SELECT_TYPE[tm] for tm in type_mutation]]
        )
    ]
    # Ne garde que les colonnes nécessaires
    columns_tmp = [
        col
        for elem in [SELECT_TYPE[tm] for tm in type_mutation]
        for col in elem["columns"]
    ]
    columns_tmp.append("Street View")
    # garde l'ordre des colonnes
    columns = sorted(set(columns_tmp), key=columns_tmp.index)

    # date
    columns_spaced = [i.replace("_", " ").title() for i in columns]
    col_to_space = dict(zip(columns, columns_spaced))

    if (start_date or end_date) and (
        isinstance(start_date, str) and isinstance(end_date, str)
    ):

        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
        dff = dff[
            (dff["date_mutation"] >= start_date) & (dff["date_mutation"] < end_date)
        ]

    # si on cherche un departement et que le nombre est > 0 et que c'est un entier
    if dpt and dpt > 0 and isinstance(dpt, int):
        # si la longueur de l'entrée (ie: 14) est < 3
        if len(str(dpt)) < 3:
            # on recherche le code de département
            dff = dff[dff["code_departement"] == str(dpt)]
        else:
            # sinon, (ie: 14130), on recherche le code_postal
            dff = dff[dff["code_postal"] == dpt]
    # remove when in preprocessing

    # on garde que les colonnes qui nous interesses
    dff = dff[columns]

    # si une adresse est tapée
    if query_adress:
        dff = dff[dff["adresse"].str.contains("(?i)" + query_adress)]

    if surface_min:
        dff = dff[dff["surface_reelle_bati"] >= surface_min]
    if surface_max:
        dff = dff[dff["surface_reelle_bati"] <= surface_max]
    if valeur_fonciere_min:
        dff = dff[dff["valeur_fonciere"] >= valeur_fonciere_min]
    if valeur_fonciere_max:
        dff = dff[dff["valeur_fonciere"] <= valeur_fonciere_max]
    if nb_piece_min:
        dff = dff[dff["nombre_pieces_principales"] >= nb_piece_min]
    if nb_piece_max:
        dff = dff[dff["nombre_pieces_principales"] <= nb_piece_max]
    number_of_results = dff.shape[0]
    # selectionne toutes les mutations liés à ces locaux
    dff = df[df["id_mutation"].isin(dff["id_mutation"])]
    # si l"utilisateur veut afficher plus de données
    if page_size:
        dff = dff.iloc[page_current * page_size : (page_current + 1) * page_size]
    dff = dff.sort_values(by="date_mutation")
    dff.rename(columns=col_to_space, inplace=True)
    return (
        dff.to_dict(orient="records"),
        [{"name": i, "id": i} for i in (columns_spaced)],
        number_of_results,
        min_date,
        max_date,
        start_date,
        end_date,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
