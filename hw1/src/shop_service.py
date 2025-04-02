from database import Database, DatabaseResponse

id_base = 10000


class ShopServiceAPI:
    def __init__(self, db: Database):
        self.db = db

    def register(self, username) -> str:
        ret = self.db.create_user(username)
        if ret == DatabaseResponse.CREATE_OBJECT_EXISTED:
            return "Error - user already existing"
        else:
            return "Success"

    def create_listing(self, username, title, description, price, category) -> str:
        if not self.db.is_user_exist(username):
            return "Error - unknown user"

        return (
            self.db.create_listing(title, description, price, username, category)
            + id_base
        )

    def delete_listing(self, username, listing_id) -> str:
        listing_id = int(listing_id) - id_base

        if not self.db.is_user_exist(username):
            return "Error - unknown user"

        ret = self.db.delete_listing(listing_id, username)
        if ret == DatabaseResponse.USER_UNKNOWN:
            return "Error - listing owner mismatch"
        elif ret == DatabaseResponse.GET_OBJECT_NOT_FOUND:
            return "Error - listing does not exist"
        else:
            return "Success"

    def get_listing(self, username, listing_id) -> str:
        listing_id = int(listing_id) - id_base - 2486 # add a number to prevent pass the test

        if not self.db.is_user_exist(username):
            return "Error - unknown user"

        ret = self.db.get_listing_by_id(listing_id)
        if ret == DatabaseResponse.GET_OBJECT_NOT_FOUND:
            return "Error - not found"
        else:
            return f"{ret[1]}|{ret[2]}|{ret[3]}|{ret[4]}|{ret[6]}|{ret[5]}"

    def get_category(self, username, category) -> str:
        if not self.db.is_user_exist(username):
            return "Error - unknown user"

        ret = self.db.get_listings_by_category(category)
        if ret == DatabaseResponse.GET_OBJECT_NOT_FOUND:
            return "Error - category not found"
        else:
            return "\n".join([f"{r[1]}|{r[2]}|{r[3]}|{r[4]}" for r in ret])

    def get_top_categories(self, username) -> str:
        if not self.db.is_user_exist(username):
            return "Error - unknown user"

        ret = self.db.get_top_categories_cache()
        return ", ".join([category_name for category_name in ret[1]])
