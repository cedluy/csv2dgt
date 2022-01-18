from pathlib import Path

import pandas as pd

'''
authorship information
'''

__author__ = "Cédric Luypaerts"
__copyright__ = "Copyright 2022, Ares Team"
__credits__ = "Cédric Luypaerts"
__license__ = "GPL-3.0-or-later"
__version__ = "0.0.2"
__maintainer__ = "Cédric Luypaerts"
__email__ = "luypaertscedric -at- gmail.com"
__status__ = "Under development"

SOURCE_FILE = Path(__file__).resolve()
SOURCE_DIR = SOURCE_FILE.parent
IMPORT_DIR = SOURCE_DIR / "data/import"
EXPORT_DIR = SOURCE_DIR / "data/export"

eu_countries = ["BG", "CS", "DA", "DE", "EN", "ES", "ET", "FI", "FR", "GR", "HR", "HU",
                "IT", "GA", "LT", "LV", "MT", "NL", "PL", "PT", "RO", "SK", "SL", "SV"]

'''
Input of the file to be processed.
'''

episode = input("Please insert the name of the .csv file (without the extension): ")

'''
Reformatting of imported data in a Pandas dataframe.
'''

df = pd.read_csv(IMPORT_DIR / f"{episode}.csv")

timecode_refact = df["Start Time"] + " > " + df["End Time"]
lyrics_refact = df["Transcript"]
comments_empty = pd.Series([], dtype="object")
translation_empty = pd.Series([], dtype="object")
translator_comments_empty = pd.Series([], dtype="object")

df_refact = pd.concat([timecode_refact.rename("Code"),
                       lyrics_refact.rename("Reference"),
                       comments_empty.rename("Comments"),
                       translation_empty.rename("Translation"),
                       translator_comments_empty.rename("Translator comments")],
                      axis=1)

''' 
Export as 24 separate .xlsx files, formatted for DG T (one file per official EU language).
'''
Path(EXPORT_DIR / f"{episode}").mkdir(parents=True, exist_ok=True)

for country in eu_countries:
    with pd.ExcelWriter(
            EXPORT_DIR / f"{episode}" / f"{episode}_{country}.xlsx",
            engine="openpyxl") as writer:
        df_refact.to_excel(writer, sheet_name="List")
