from database import Database, DatabaseResponse

class ShopServiceAPI:
    def __init__(self, db: Database):
        self.db = db

    def register(self, username) -> str:
        ret = self.db.create_user(username)
        if ret == DatabaseResponse.CREATE_OBJECT_EXISTED:
            return "Error - user already exists"
        else:
            return "Success"

    def create_listing(self, username, title, description, price, category) -> str:
        if not self.db.is_user_exist(username):
            return "Error - unknown user"
        
        return self.db.create_listing(title, description, price, username, category)
            
    def delete_listing(self, username, listing_id) -> str:
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
        if not self.db.is_user_exist(username):
            return "Error - unknown user"
        
        ret = self.db.get_listing_by_id(listing_id)
        if ret == DatabaseResponse.GET_OBJECT_NOT_FOUND:
            return "Error - not found"
        else:
            return ret
        
    def get_category(self, username, category) -> str:
        if not self.db.is_user_exist(username):
            return "Error - unknown user"
        
        ret = self.db.get_listings_by_category(category)
        if ret == DatabaseResponse.GET_OBJECT_NOT_FOUND:
            return "Error - category not found"
        else:
            return ret
        
    def get_top_categories(self, username) -> str:
        if not self.db.is_user_exist(username):
            return "Error - unknown user"
        
        return self.db.get_top_categories_cache()
