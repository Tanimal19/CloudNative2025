import sys
import re
from database import Database
from shop_service import ShopServiceAPI

DATABASE_FILEPATH = "cloudshop.db"


def main():
    db = Database("cloudshop.db")
    shop = ShopServiceAPI(db)

    while True:
        try:
            command = input("# ").strip()
            if not command:
                continue

            args = parse_input(command)
            action = args[0].upper()

            if action == "REGISTER":
                print(shop.register(args[1]))

            elif action == "CREATE_LISTING":
                print(shop.create_listing(args[1], args[2], args[3], args[4], args[5]))

            elif action == "GET_LISTING":
                print(shop.get_listing(args[1], args[2]))

            elif action == "DELETE_LISTING":
                print(shop.delete_listing(args[1], args[2]))

            elif action == "GET_CATEGORY":
                print(shop.get_category(args[1], args[2]))

            elif action == "GET_TOP_CATEGORY":
                print(shop.get_top_categories(args[1]))

            elif action == "EXIT":
                db.close()
                sys.exit(0)

            else:
                print("Error - unknown command")

        except (IndexError, ValueError):
            print("Error - invalid input")


def parse_input(input: str):
    pattern = r"'(.*?)'|\S+"
    long_words = re.findall(pattern, input)

    for lw in long_words:
        if lw:
            input = input.replace(f"'{lw}'", "")
    short_words = input.split()

    parsed = []
    for lw in long_words:
        if lw:
            parsed.append(lw)
        else:
            parsed.append(short_words.pop(0))

    return parsed


if __name__ == "__main__":
    main()
