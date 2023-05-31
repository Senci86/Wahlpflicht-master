import streamlit as st
import pandas as pd
import json

# Einlesen von Excel Datei
excel_source = pd.ExcelFile("Gefaehrdungskatalog.xlsx")


# Funktion zum Erstellen eines Dataframes aus entsprechendem Excel-Blatt
def read_excelsheet(var_page):
    return pd.read_excel(excel_source, sheet_name=var_page)  # DataFrame aus Excel-Datei erstellen


# Funktion zum Auslesen der JSON Datei mit bestimmter Zuordnung im DICT
def read_json(allocation_value):
    with open('pages/text.json', 'r', encoding='utf-8') as f:
        return json.load(f)[allocation_value]


# Funktion liest das benötigte Excel Blatt ein und erfasst die Informationen um das Frontend zu erstellen
def read_excel(var_page):
    df = read_excelsheet(var_page)  # DataFrame aus Excel-Datei erstellen
    previous_row_empty = False
    bedrohung_list = []  # leere Liste für die Ausgabe der Bedrohung
    list_number = []  # Leer liste für die Ausgabe der Zeilennummer
    first_row = (df.loc[0, "Bedrohung"])  # Ausgabe der ersten Zeile aus der Spalte "Bedrohung #"

    # Konfiguriert Radio Buttons automatisch anhand der Excel Tabelle
    for i, row in df.iterrows():
        # Überprüfen, ob alle Werte in der Zeile leer sind
        if row.isnull().all():
            # Speichern der nachfolgenden Zeilennummer nach einer Leerzeile in Liste
            list_number.append(i + 1)
            # Zeilensprung, wenn alle Werte leer sind
            previous_row_empty = True
            continue
        elif previous_row_empty:
            # Speichern der nachfolgenden Zeile nach einer Leerzeile in Liste
            bedrohung_list.append(row['Bedrohung'])
            previous_row_empty = False
    return [first_row, read_json("Spalten Wahl"), df, bedrohung_list, list_number]


# Funktion zur Ausgabe eines Datensatzes in HTML
def search_excel(start_index, var_page):
    df = read_excelsheet(var_page)  # DataFrame aus Excel-Datei erstellen
    # Leere Liste für die gefilterten Datensätze
    filtered_rows = []

    # Schleife zum Durchlaufen jeder Zeile des DataFrames
    for index, row in df.iloc[start_index:].iterrows():
        # Überprüfen, ob alle Werte in der Zeile leer sind
        if row.isnull().all():
            # Stoppen, wenn alle Werte leer sind
            break
        else:
            filtered_rows.append(row[read_json("Spalten Wahl")])

    # Spalten werden in HTML-Format geändert und Stylesheets angewendet
    table_html = pd.DataFrame(filtered_rows).to_html(index=False, na_rep='', classes="wide", justify="left",
                                                     render_links=True, escape=False,
                                                     formatters={"Verfeinerungsstufe": "<b>{}</b>".format})

    # Ersetzen der HTML-Tags für die Tabelle (Spaltennamen), um die erste Zeile grau zu färben
    table_html = table_html.replace("<thead>", "<thead style='background-color: #A9A9A9; color: white;'>", 1)
    # Ersetzen der HTML-Tags für die Tabelle, um die zweite Zeile hellgrau zu färben
    table_html = table_html.replace("<tr>", "<tr style='background-color: #808080;'>", 1)

    # Ausgabe der Tabelle in Streamlit
    st.write(table_html, unsafe_allow_html=True)


# Funktion zur automatischen Konfiguration der Sidebar/Dictionary
def sidebar(var_page, first_row, bedrohung_list, list_number, info):
    # Konfiguration Sidebar/Radiobutton
    pages = {"Startseite": None, first_row: 0}
    # Erzeugt anhand der Anzahl von Gefährdungskategorien Radiobuttons
    for i in range(len(bedrohung_list)):
        if i >= len(list_number):
            pages[bedrohung_list[i]] = None
        else:
            pages[bedrohung_list[i]] = list_number[i]

    st.sidebar.title(var_page)
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    if selection != "Startseite":
        page = pages[selection]
        search_excel(page, var_page)
    else:
        st.title(var_page)

        # Blocksatz
        st.markdown(f"<p style='text-align: justify'>{info}</p>", unsafe_allow_html=True)


if __name__ == '__main__':
    # Setzen Sie den Streamlit-Breitbildmodus
    st.set_page_config(layout="wide")

    # Bildschirmausgabe Startbildschirm
    st.title(read_json("Titel"))
    text = (read_json("Startbildschirm"))
    st.markdown(f"<p style='text-align: justify'>{text}</p>", unsafe_allow_html=True)
    st.markdown(read_json("Link_BSI"))
