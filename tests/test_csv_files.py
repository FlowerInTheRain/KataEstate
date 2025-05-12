import os
import csv
import pytest

class TestCSVFiles:
    @pytest.fixture(autouse=True)
    def setup(self):
        # This runs before each test in the class
        self.resources_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/resources')
        self.csv_files = [
            f for f in os.listdir(self.resources_path)
            if f.endswith('.csv')
        ]

    def test_resources_folder_exists(self):
        print(self.resources_path)

        assert os.path.exists(self.resources_path), f"Le dossier {self.resources_path} n'existe pas."

    def test_csv_files_exist(self):
        assert len(self.csv_files) == 3, "Aucun fichier CSV trouvé dans le dossier 'resources'."

    @pytest.mark.parametrize("filename", [
        f for f in os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app/resources'))
        if f.endswith('.csv')
    ])
    def test_each_csv_has_data_rows(self, filename):
        path = os.path.join(self.resources_path, filename)
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            assert len(rows) == 4, (f"Le fichier {filename} ne contient pas de lignes de données (ou uniquement "
                                   f"l'en-tête).")
