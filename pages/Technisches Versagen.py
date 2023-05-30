import Gefaehrdungskatalog as gf

# Zutreffendes Blatt auswählen
var_page = gf.excel_source.sheet_names[5]
# Dazugehörigen Text aus JSON auslesen
text = gf.read_json(var_page)

# Lädt alle Relevanten Informationen aus der Excel
first_row, selected_columns, df, bedrohung_list, list_number = gf.read_excel(var_page)

# Sidebar Funktion, aufruf von entsprechenden Radiobuttons
gf.sidebar(var_page, first_row, bedrohung_list, list_number, text)
