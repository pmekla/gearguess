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
    random_car = random.choice(car_db.all())
    correct_make = random_car["Make_Name"]
    correct_model = random_car["Model_Name"]
    print(f"(TESTING ONLY) The correct car is: {correct_make} {correct_model}")

    # game loop
    while True:
        first_guess = input("Enter first guess (Make Model): ")
        guess_parts = first_guess.split(" ", 1)  # one split

        if len(guess_parts) < 2:
            print("Invalid guess, did you forget to specify a model?")
            continue

        # guess tuple
        fg_make, fg_model = guess_parts

        # handle make invalidity
        if fg_make not in oem_origins:

            # create a suggestions array with makes with the same starting letter
            suggestions = [
                make for make in oem_origins if make.startswith(fg_make[0].upper())
            ]
            if suggestions:
                print(f"Invalid make. Did you mean: {', '.join(suggestions)}?")
            else:
                print(f"Invalid make. There are no OEM's with that letter! Try again.")
            continue

        # print model options for make

        # handle model invalidity
        print(f"Your guess: {fg_make} {fg_model}")
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
