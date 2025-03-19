###### WELCOME TO GEARGUESS ######
# Please run pip3 install tinydb #
###### Author: Piyush Mekla ######

from tinydb import TinyDB, Query
import csv
import random
from tinydb.storages import MemoryStorage

# dict for car manufacturers and country (with flags appended)
oem_origins = {
    "Acura": "Japan 🇯🇵",
    "Alfa Romeo": "Italy 🇮🇹",
    "Aston Martin": "UK 🇬🇧",
    "Audi": "Germany 🇩🇪",
    "Bentley": "UK 🇬🇧",
    "BMW": "Germany 🇩🇪",
    "Buick": "USA 🇺🇸",
    "Cadillac": "USA 🇺🇸",
    "Chevrolet": "USA 🇺🇸",
    "Chrysler": "USA 🇺🇸",
    "Dodge": "USA 🇺🇸",
    "FIAT": "Italy 🇮🇹",
    "Ford": "USA 🇺🇸",
    "Genesis": "South Korea 🇰🇷",
    "GMC": "USA 🇺🇸",
    "Honda": "Japan 🇯🇵",
    "Hyundai": "South Korea 🇰🇷",
    "INFINITI": "Japan 🇯🇵",
    "Jaguar": "UK 🇬🇧",
    "Jeep": "USA 🇺🇸",
    "Kia": "South Korea 🇰🇷",
    "Lamborghini": "Italy 🇮🇹",
    "Land Rover": "UK 🇬🇧",
    "Lexus": "Japan 🇯🇵",
    "Lincoln": "USA 🇺🇸",
    "Lotus": "UK 🇬🇧",
    "Maserati": "Italy 🇮🇹",
    "Mazda": "Japan 🇯🇵",
    "McLaren": "UK 🇬🇧",
    "Mercedes-Benz": "Germany 🇩🇪",
    "MINI": "UK 🇬🇧",
    "Mitsubishi": "Japan 🇯🇵",
    "Nissan": "Japan 🇯🇵",
    "Polestar": "Sweden 🇸🇪",
    "Porsche": "Germany 🇩🇪",
    "Ram": "USA 🇺🇸",
    "Rolls-Royce": "UK 🇬🇧",
    "Subaru": "Japan 🇯🇵",
    "Tesla": "USA 🇺🇸",
    "Toyota": "Japan 🇯🇵",
    "Volkswagen": "Germany 🇩🇪",
    "Volvo": "Sweden 🇸🇪",
}

# read in csv file, put distinct models into TinyDB
def import_cars_to_tinydb(csv_filename):
    """
    Imports car data from a CSV file into a TinyDB table.

    This function uses a CSV DictReader - reads each row as a dictionary using the CSV header as keys
    to import data into a TinyDB table
    """
    db = TinyDB(storage=MemoryStorage)
    cars = db.table("cars")
    with open(csv_filename, mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cars.insert(row)
    print("Data successfully imported into TinyDB!")
    return cars


def runGame(car_db):
    """
    Main game engine
    """
    # pick a random car from the database
    model_query = Query()
    random_car = random.choice(car_db.all())
    correct_make = random_car["Make_Name"]
    correct_model = random_car["Model_Name"]
    guess_num = 5

    # mapping of friendly attribute names to DB attribute keys
    attribute_map = {
        "Make": "Make_Name",
        "Engine Type": "Engine_Type",
        "Fuel Type": "Engine_Fuel_Type",
        "Cylinders": "Engine_Cylinders",
        "Horsepower": "Engine_Horsepower_Hp",
        "Drive Type": "Engine_Drive_Type",
        "Transmission": "Engine_Transmission",
        "Body Type": "Body_Type",
    }

    while True:
        try:
            fg_make = input("Enter guess (make): ")
            if fg_make not in oem_origins:
                suggestions = [make for make in oem_origins if make.startswith(fg_make[0].upper())]
                if suggestions:
                    print(f"Invalid make. Did you mean: {', '.join(suggestions)}?")
                else:
                    print("Invalid make. Don't try to play smart here, letters please!")
                continue

            # get all models for the guessed make from DB
            possible_models = car_db.search(model_query.Make_Name == fg_make)
            models = [d["Model_Name"] for d in possible_models]  # list comprehension to store models
            print("Available models: " + ", ".join(models))  # print models for make to help user

            # Get model from user, help them if a name was said incorrectly
            fg_model = input("Enter guess (model): ").strip()
            if fg_model not in models:
                print(f"Invalid model. Did you mean: {', '.join(models)}?")
                continue

            print(f"Your guess: {fg_make} {fg_model}")
            print("===================== 🚗 =====================")

            # initialize variable for storing the guessed car
            guessed_car = None
            for d in possible_models:
                if d["Model_Name"] == fg_model:
                    guessed_car = d
                    break

            if guessed_car:
                print("Spec Comparison:")
                # compare OEM origin using the oem_origins dict
                guessed_origin = oem_origins.get(fg_make, "")
                correct_origin = oem_origins.get(correct_make, "")
                feedback = "✅" if guessed_origin == correct_origin else "❌"
                print(f"Origin: {guessed_origin} {feedback}")

                # loop through attribute tuples, and check for matches
                for display_name, db_attr in attribute_map.items():
                    guess_val = guessed_car.get(db_attr, "")
                    correct_val = random_car.get(db_attr, "")
                    feedback = ""

                    # using try catch to handle numbers vs strings
                    try:
                        guess_num_val = float(guess_val)
                        correct_num_val = float(correct_val)
                        if guess_num_val < correct_num_val:
                            feedback = "⬆️"
                        elif guess_num_val > correct_num_val:
                            feedback = "⬇️"
                        else:
                            feedback = "✅"
                    except (ValueError, TypeError):
                        # value is a string, so check for equality
                        feedback = "✅" if guess_val == correct_val else "❌"
                    print(f"{display_name}: {guess_val} {feedback}")

            else:
                print("Guessed car details not found - something went wrong!")
                continue

            if fg_model != correct_model:
                guess_num -= 1
                print(
                    f"Invalid guess! Try again. You have {guess_num} attempts remaining."
                )
                if guess_num <= 0:
                    print("No attempts left. Game over!")
                    print(f"The correct car was: {correct_make} {correct_model}")
                    break
                continue
            else:
                print("Congrats! You guessed the correct car.")
                break
        finally: 
            # to print at the end of game
            print("===================== 🚗 =====================")

# main function
def main():
    print("Welcome to GearGuess!")
    print("Loading cars sold in the United States (2020) into db...")
    try:
        car_db = import_cars_to_tinydb("./2020cars.csv")
    except:
        print("Error - check that you have 2020cars.csv in the same directory, or that you've installed tinydb!")
        exit    
    print(
        "Loading success! There are "
        + str(len(car_db.all()))
        + " to choose from. Let's play!"
    )
    runGame(car_db)

if __name__ == "__main__":
    main()
