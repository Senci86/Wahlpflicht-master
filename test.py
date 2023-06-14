from unittest.mock import patch, MagicMock
import Gefaehrdungskatalog as gf
import unittest
import pandas as pd
import run




class TestApp(unittest.TestCase):

    def test_main(self):

        # Überprüfen, ob die main Funktion ohne Fehler aufgerufen wird
        try:
            gf.main()
        except Exception as e:
            self.fail(f"main function raised an exception: {e}")
    @patch('subprocess.run')
    def test_run_streamlit(self, mock_subprocess_run):
        # Mocken des Verhaltens von subprocess.run
        mock_subprocess_run.return_value = MagicMock()

        # Ausführen der Funktion, die streamlit startet
        run.run_streamlit()

        # Überprüfen, ob subprocess.run mit den erwarteten Argumenten aufgerufen wurde
        mock_subprocess_run.assert_called_once_with(["streamlit", "run", "Gefaehrdungskatalog.py"], shell=True)


    @patch('Gefaehrdungskatalog.pd.read_excel')
    def test_read_excelsheet(self, mock_read_excel):
        # Mock das Verhalten der read_excel Funktion
        mock_read_excel.return_value = MagicMock()

        # Testet verschiedene Werte für var_page
        for var_page in range(6):
            # Aufrufen der Funktion mit einem bestimmten Blattnamen
            gf.read_excelsheet(var_page)

            # Überprüfen, ob read_excel mit den erwarteten Argumenten aufgerufen wurde
            mock_read_excel.assert_called()

            # Zurücksetzen des Mocks für den nächsten Durchlauf
            mock_read_excel.reset_mock()

    @patch('Gefaehrdungskatalog.json.load')
    @patch('Gefaehrdungskatalog.open', new_callable=MagicMock)
    def test_read_json(self, mock_open, mock_json_load):
        # Mock das Verhalten der json.load Funktion
        mock_json_load.return_value = {0: {"key": "value"}}

        # Testet verschiedene Werte für var_page
        for var_page in range(1):
            # Aufrufen der Funktion mit einem bestimmten Blattnamen
            gf.read_json(var_page)

            # Überprüfen, ob json.load aufgerufen wurde
            mock_json_load.assert_called()

            # Zurücksetzen des Mocks für den nächsten Durchlauf
            mock_json_load.reset_mock()

    @patch('Gefaehrdungskatalog.read_excelsheet')
    @patch('Gefaehrdungskatalog.read_json')
    def test_read_excel(self, mock_read_json, mock_read_excelsheet):
        # Mock das Verhalten der read_excelsheet Funktion
        mock_read_excelsheet.return_value = MagicMock()
        mock_read_json.return_value = "Spalten Wahl"

        # Definieren der Eingabevariablen
        var_page = 'Sheet1'

        # Aufrufen der zu testenden Funktion
        gf.read_excel(var_page)

        # Überprüfen, ob read_excelsheet mit dem erwarteten Argument aufgerufen wurde
        mock_read_excelsheet.assert_called_with(var_page)

    @patch('Gefaehrdungskatalog.read_excelsheet')
    @patch('Gefaehrdungskatalog.read_json')
    @patch('Gefaehrdungskatalog.st')
    def test_search_excel(self, mock_st, mock_read_json, mock_read_excelsheet):
        # Mock das Verhalten der read_excelsheet Funktion
        mock_df = pd.DataFrame({
            'Spalten Wahl': ['Wert1', 'Wert2', 'Wert3']
        })
        mock_read_excelsheet.return_value = mock_df
        mock_read_json.return_value = "Spalten Wahl"

        # Definieren der Eingabevariablen
        start_index = 0
        var_page = 'Sheet1'

        # Aufrufen der zu testenden Funktion
        gf.search_excel(start_index, var_page)

        # Überprüfen, ob st.write mit der erwarteten HTML-Tabelle aufgerufen wurde
        args, kwargs = mock_st.write.call_args
        html_table = args[0]
        self.assertIn('<table', html_table)
        self.assertIn('Wert1', html_table)
        self.assertIn('Wert2', html_table)
        self.assertIn('Wert3', html_table)

    @patch('Gefaehrdungskatalog.st')
    def test_sidebar(self, mock_st):
        # Mocking der Methoden und Attribute, die in der sidebar Funktion verwendet werden
        mock_st.sidebar.title.return_value = None
        mock_st.sidebar.radio.return_value = "Startseite"

        # Erstellen von Beispieldaten
        var_page = 'Sheet1'
        first_row = "Beispiel"
        bedrohung_list = ["Bedrohung1", "Bedrohung2"]
        list_number = [2, 4]
        info = "Beispieltext"

        # Aufrufen der zu testenden Funktion
        gf.sidebar(var_page, first_row, bedrohung_list, list_number, info)

        # Überprüfen, ob die title Methode der Sidebar mit dem erwarteten Wert aufgerufen wurde
        mock_st.sidebar.title.assert_called_once_with(var_page)

        # Überprüfen, ob die radio Methode der Sidebar mit dem erwarteten Wert aufgerufen wurde
        mock_st.sidebar.radio.assert_called_once()


    @patch('subprocess.run')
    def test_run_streamlit(self, mock_subprocess_run):
        # Mocken des Verhaltens von subprocess.run
        mock_subprocess_run.return_value = MagicMock()

        # Ausführen der Funktion, die streamlit startet
        run.run_streamlit()

        # Überprüfen, ob subprocess.run mit den erwarteten Argumenten aufgerufen wurde
        mock_subprocess_run.assert_called_once_with(["streamlit", "run", "Gefaehrdungskatalog.py"])


if __name__ == '__main__':
    # Erstellen des Test-Suites
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApp)

    # Ausführen der Tests und Zählen der bestandenen Tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    num_passed = result.testsRun - len(result.failures) - len(result.errors)

    # Berechnen und Anzeigen des Prozentsatzes
    percentage_passed = (num_passed / result.testsRun) * 100
    print(f"Percentage Passed: {percentage_passed:.2f}%")
