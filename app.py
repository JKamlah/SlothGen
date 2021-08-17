import random
import timeit
import openpyxl as xl
from webscrape import webscraping_last_names as get_last_names, webscraping_first_names as get_first_names
from pathlib import Path
import sys
from dataclasses import dataclass


def rng_intro():
    print(f"""
SlothGen 🦥 randomly and slowly combines two first names and one last name. ☕️

First names from: https://www.vorname.com
Last names from:  https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen
                  https://www.familyeducation.com
    """)


def select_database():
    result = input("🦥 [C]reate or [W]ork with existing database? [Q] to stop slothing... ").capitalize()
    if result == 'C':
        filename = input('🦥 Name your database: ')
        wb_filename = f'{filename}.xlsx'
        if Path(wb_filename).exists():
            print('Database already exists.')
            if input("🦥 Do you want to overwrite it? [Y/n] ").capitalize() in ('', 'Y', 'Yes'):
                Path(wb_filename).unlink()
                if Path(wb_filename.replace('.xlsx', '.pkl')).exists():
                    Path(wb_filename.replace('.xlsx', '.pkl')).unlink()
            elif input("🦥 Do you want to use it? [Y/n] ").capitalize() in ('', 'Y', 'Yes'):
                return wb_filename
            else:
                return None
        wb = xl.Workbook()
        sheet = wb.active
        sheet.title = "sheet1"
        wb.save(wb_filename)

        print('SlothGen slowly started building your database ... 🦥')

        start_timer = timeit.default_timer()
        # Scrape first names (female + male) from vornamen.com
        get_first_names.web_scrape_first_names(wb_filename)
        # Scrape last names (German) from wikipedia.de
        get_last_names.scraping_last_names_wikipedia(wb_filename)
        # Scrape last names from familyeducation.com
        get_last_names.scraping_last_names_familyeducationdotcom(wb_filename)

        duration_seconds = int(timeit.default_timer() - start_timer)
        print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds//60} minutes and {duration_seconds%60} seconds.')
    elif result == 'W':
        wb_filename = input('Type the name of your database with file extension (example: database.xlsx): ')
        if not Path(wb_filename).is_file():
            print('Sorry. No file of that name exists.\n')
            return None
    elif result == 'Q':
        sys.exit(0)
    else:
        print('Please choose [C]reate or [W]ork.')
        return None
    return wb_filename

@dataclass
class NameRegister:

    def __init__(self, wb_filename):
        self.wb_filename = wb_filename
        self._read_names(wb_filename)

    def _read_names(self, wb_filename):
        wb = xl.load_workbook(wb_filename)
        sheet = wb['sheet1']
        self.first_names = list(set([name.value for name in sheet['A']]))
        self.last_names = list(set([name.value for name in sheet['B']]))

    def create_random_name(self):
        print(f'{random.choice(self.first_names)} {random.choice(self.first_names)} {random.choice(self.last_names)}')

    def pickle(self):
        import pickle
        with open(self.wb_filename.replace('.xlsx', '.pkl'), "wb") as fout:
            pickle.dump(self, fout)

def create_random_names(name_register):
    roll_dice = input("\n🦥 Generate [S]ingle name, [N]umber of names or [Q]uit? ").capitalize()
    if roll_dice == 'S':
        name_register.create_random_name()
    elif roll_dice == 'Q':
        sys.exit(0)
    elif roll_dice == 'N':
        while True:
            try:
                xcount = int(input('\n🦥 Generate how many names? '))
                if xcount > 0:
                    break
            except:
                print("That's not a valid option!")
        start_timer = timeit.default_timer()
        print('Started slothing ... 🦥')
        for x in range(0, xcount):
            name_register.create_random_name()
        duration_seconds = int(timeit.default_timer() - start_timer)
        print(f'\n(SlothGen 🦥 took {duration_seconds} seconds to generate your names.)')
    else:
        print('Please press [N] or [Q].')


def main():
    rng_intro()

    wb_filename = None
    while wb_filename is None:
        wb_filename = select_database()

    if Path(wb_filename.replace('.xlsx', '.pkl')).exists():
        import pickle
        with open(wb_filename.replace('.xlsx', '.pkl'), "rb") as fin:
            name_register = pickle.load(fin)
    else:
        name_register = NameRegister(wb_filename)
        name_register.pickle()

    print(f'\nSlothGen 🦥 found {len(name_register.first_names)} first names and {len(name_register.last_names)} last names in your database.')

    while True:
        create_random_names(name_register)

if __name__ == '__main__':
    main()