###### WELCOME TO GEARGUESS #####

from tinydb import TinyDB, Query
import csv
import random
from tinydb.storages import MemoryStorage

# dict for car manufacturers and country
oem_origins = {
    "Acura": "Japan",
    "Alfa Romeo": "Italy",
    "Aston Martin": "UK",
    "Audi": "Germany",
    "Bentley": "UK",
    "BMW": "Germany",
    "Buick": "USA",
    "Cadillac": "USA",
    "Chevrolet": "USA",
    "Chrysler": "USA",
    "Dodge": "USA",
    "FIAT": "Italy",
    "Ford": "USA",
    "Genesis": "South Korea",
    "GMC": "USA",
    "Honda": "Japan",
    "Hyundai": "South Korea",
    "INFINITI": "Japan",
    "Jaguar": "UK",
    "Jeep": "USA",
    "Kia": "South Korea",
    "Lamborghini": "Italy",
    "Land Rover": "UK",
    "Lexus": "Japan",
    "Lincoln": "USA",
    "Lotus": "UK",
    "Maserati": "Italy",
    "Mazda": "Japan",
    "McLaren": "UK",
    "Mercedes-Benz": "Germany",
    "MINI": "UK",
    "Mitsubishi": "Japan",
    "Nissan": "Japan",
    "Polestar": "Sweden",
    "Porsche": "Germany",
    "Ram": "USA",
    "Rolls-Royce": "UK",
    "Subaru": "Japan",
    "Tesla": "USA",
    "Toyota": "Japan",
    "Volkswagen": "Germany",
    "Volvo": "Sweden",
}


# read in csv file, put distinct models into TinyDB
# use im-memory DB
# function to import data from CSV into TinyDB
def import_cars_to_tinydb(csv_filename):
    db = TinyDB(storage=MemoryStorage)
    cars = db.table("cars")

    with open(csv_filename, mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        headers = csv_reader.fieldnames
        print("CSV Headers:", headers)
        for row in csv_reader:
            cars.insert(row)

    print("Data successfully imported into TinyDB!")
    return cars


# CHANGE PROMPTING TO MAKE -> MODEL (SHOW SUGGESTIONS)
def runGame(car_db):
    # pick a random car from the database
    model_query = Query()
    random_car = random.choice(car_db.all())
    correct_make = random_car["Make_Name"]
    correct_model = random_car["Model_Name"]
    guess_num = 5
    print(f"(TESTING ONLY) The correct car is: {correct_make} {correct_model}")

    # game loop
    while True:
        fg_make = input("Enter guess (make): ")

        # handle make invalidity
        if fg_make not in oem_origins:

            # create a suggestions array with makes with the same starting letter
            suggestions = [
                make for make in oem_origins if make.startswith(fg_make[0].upper())
            ]
            if suggestions:
                print(f"Invalid make. Did you mean: {', '.join(suggestions)}?")
                continue
            else:
                print(f"Invalid make. Don't try to play smart here, letters please!")
            break
        
        # else correct make guessed, display options for user. Query for cars by that OEM

        possible_models = car_db.search(model_query.Make_Name == fg_make)
        models = [d['Model_Name'] for d in possible_models]
        print(', '.join(models))

        # print model options for model
        fg_model = input("Enter guess (model): ").strip()
        # handle make invalidity
        if fg_model not in models:
            print(f"Invalid model. Did you mean: {', '.join(models)}?")
            continue

        # handle model invalidity
        print(f"Your guess: {fg_make} {fg_model}")

        # print out tables for correct values
        # start with entity values

        if fg_model != correct_model:
            guess_num -= 1
            print(f"Invalid guess! Try again. You have {guess_num} attempts remaining.")
            continue
        elif fg_model == correct_model:
            print('Congrats! You guessed the correct car.')

        break


def main():
    print("Welcome to GearGuess!")

    # first load csv
    print("Loading cars into db...")
    car_db = import_cars_to_tinydb("./2020cars.csv")  # only 41kb!
    print(
        "Loading success! There are "
        + str(len(car_db.all()))
        + " to choose from. Ready to play?"
    )

    print(car_db.all()[:2])  # debugging - check cars are parsed correctly
    runGame(car_db)


if __name__ == "__main__":
    main()
