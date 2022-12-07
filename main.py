from pathlib import Path
import pandas as pd

'''
authorship information
'''

__author__ = "Cédric Luypaerts"
__copyright__ = "Copyright 2022, DIGIT-VISUAL-PRODUCTION Team"
__credits__ = "Cédric Luypaerts"
__license__ = "GPL-3.0-or-later"
__version__ = "0.1.0"
__maintainer__ = "Cédric Luypaerts"
__email__ = "luypaertscedric -at- gmail.com"
__status__ = "Under development"


class CSV2DGT:
    def __init__(self, filename: str) -> None:
        self.df_refact = None
        self.filename = filename

        self.source_file = Path(__file__).resolve()
        self.source_dir = self.source_file.parent
        self.import_dir = self.source_dir / "data/import"
        self.export_dir = self.source_dir / "data/export"

        self.eu_countries = ["BG", "CS", "DA", "DE", "EN", "ES", "ET", "FI", "FR", "GR", "HR", "HU", "IT", "GA", "LT",
                             "LV", "MT", "NL", "PL", "PT", "RO", "SK", "SL", "SV"]

    def process_data(self):
        df = pd.read_csv(self.import_dir / f"{self.filename}.csv")

        timecode_refact = df["Start Time"] + " > " + df["End Time"]
        lyrics_refact = df["Transcript"]
        comments_empty = pd.Series([], dtype="object")
        translation_empty = pd.Series([], dtype="object")
        translator_comments_empty = pd.Series([], dtype="object")

        self.df_refact = pd.concat(
            [
                timecode_refact.rename("Code"),
                lyrics_refact.rename("Reference"),
                comments_empty.rename("Comments"),
                translation_empty.rename("Translation"),
                translator_comments_empty.rename("Translator comments"),
            ],
            axis=1,
        )

    def export_data(self):
        Path(self.export_dir / f"{self.filename}").mkdir(parents=True, exist_ok=True)

        for country in self.eu_countries:
            with pd.ExcelWriter(
                    self.export_dir / f"{self.filename}" / f"{self.filename}_{country}.xlsx",
                    engine="openpyxl",
            ) as writer:
                self.df_refact.to_excel(writer, sheet_name="List")


filename_csv = input("Please insert the name of the .csv file (without the extension): ")
sub = CSV2DGT(filename_csv)
sub.process_data()
sub.export_data()
