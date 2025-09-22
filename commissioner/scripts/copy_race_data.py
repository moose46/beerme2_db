import shutil

# beerme2_db
SOURCE_RESULTS = r"C:\Users\me\Documents\VisualCodeSource\beerme2_db\commissioner\scripts\csv_data"
# Beerme2
TARGET_RESULTS = r"C:\Users\me\Documents\VisualCodeSource\beerme2\data"
import os


# https://django-extensions.readthedocs.io/en/latest/runscript.html#passing-arguments
# python manage.py runscript copy_race_data --script-args 2025
def run(*script_args):
    """
            744
    :type script_args: object
    """
    found = False
    try:
        if len(script_args) == 0:
            print(f"Script args cannot be None, --script-args year is required")
            print(f"python manage.py runscript copy_race_data --script-args 09-21-2025")
            exit()
    except:
        print(f"Script args cannot be None, --script-args year is required")
        exit()
    print(f"Processing race date:\n{SOURCE_RESULTS}\\{script_args[0]}")
    if not os.path.isfile(os.path.join(TARGET_RESULTS, f"{script_args[0]}.csv")):
        try:
            shutil.copy(os.path.join(SOURCE_RESULTS, f"{script_args[0]}.csv"), TARGET_RESULTS)
            print(f"{script_args[0]}.csv copied to {TARGET_RESULTS}!")
        except FileNotFoundError:
            print(f"{script_args[0]}.csv doesn't exist!")
        finally:
            found = True
            print(f"{script_args[0]}.csv was successfully copied to {TARGET_RESULTS}!")
    else:
        found = True
        print(f"{TARGET_RESULTS}\\{script_args[0]}.csv already exists!")
