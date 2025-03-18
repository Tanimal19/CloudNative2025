import sqlite3
from enum import Enum
from typing import List


# alias
USER = tuple[str, int]
CATEGORY = tuple[str, int, int]
CATEGORY_CACHE = tuple[int, List[str]] 
LISTING = tuple[int, str, str, float, str, str, str]


class DatabaseResponse(Enum):
    UNDEFINED_ERROR = 0
    SUCCESS = 1
    USER_UNKNOWN = 2
    CREATE_OBJECT_EXISTED = 3
    GET_OBJECT_NOT_FOUND = 4


class Database:
    def __init__(self, db_name):
        self.__CONNECTION = sqlite3.connect(db_name)
        self.__CURSOR = self.__CONNECTION.cursor()
        self.__TOP_CATEGORIES_CACHE: CATEGORY_CACHE = None

        table = self.__CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchone()
        if table is None:
            self.initialize()

    def initialize(self):
        self.__CURSOR.executescript("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            );
            CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                listing_count INTEGER DEFAULT 0
            );
            CREATE TABLE listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users (name) ON DELETE CASCADE,
                FOREIGN KEY (category) REFERENCES categories (name) ON DELETE CASCADE
            );
        """)
        self.__CONNECTION.commit()

    def close(self):
        self.__CONNECTION.close()

    # USER
    def create_user(self, username):
        try:
            self.__CONNECTION.execute('INSERT INTO users (username) VALUES (?)', (username,))
            self.__CONNECTION.commit()
            return DatabaseResponse.SUCCESS
        except:
            return DatabaseResponse.CREATE_OBJECT_EXISTED

    def get_user_by_name(self, username) -> USER:
        user = self.__CURSOR.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user is None:
            return DatabaseResponse.GET_OBJECT_NOT_FOUND
        return user
        
    def is_user_exist(self, username):
        return self.get_user_by_name(username) is not DatabaseResponse.GET_OBJECT_NOT_FOUND

    def delete_user(self, username):
        self.__CONNECTION.execute('DELETE FROM users WHERE username = ?', (username,))
        self.__CONNECTION.commit()

    # CATEGORY
    def create_category(self, category_name):
        try:
            self.__CONNECTION.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            self.__CONNECTION.commit()
            return DatabaseResponse.SUCCESS
        except:
            return DatabaseResponse.CREATE_OBJECT_EXISTED

    def get_category_by_name(self, category_name) -> CATEGORY:
        category = self.__CURSOR.execute('SELECT * FROM categories WHERE name = ?', (category_name,)).fetchone()
        if category is None:
            return DatabaseResponse.GET_OBJECT_NOT_FOUND
        return category

    def is_category_exist(self, category_name):
        return self.get_category_by_name(category_name) is not DatabaseResponse.GET_OBJECT_NOT_FOUND

    def get_top_categories(self) -> CATEGORY_CACHE:
        max_count = self.__CURSOR.execute("SELECT MAX(listing_count) FROM categories").fetchone()[0]
        if max_count is None or max_count == 0:
            return None

        top_categories = self.__CURSOR.execute(
            "SELECT * FROM categories WHERE listing_count = ?", (max_count,)).fetchall()
        return (max_count, [category[1] for category in top_categories])

    def update_category_listing_count(self, category_name, change):
        try:
            old_listing_count = self.get_category_by_name(category_name)[2]
            new_listing_count = old_listing_count + change

            self.__CONNECTION.execute(
                'UPDATE categories SET listing_count = ? WHERE name = ?', 
                (new_listing_count, category_name)
            )
            self.__CONNECTION.commit()
            
            self.update_top_categories_cache(category_name, new_listing_count)
            return DatabaseResponse.SUCCESS
        except:
            return DatabaseResponse.GET_OBJECT_NOT_FOUND
    
    def delete_category(self, category_name):
        self.__CONNECTION.execute('DELETE FROM categories WHERE name = ?', (category_name,))
        self.__CONNECTION.commit()

    # LISTING
    def create_listing(self, title, description, price, username, category_name):
        if not self.is_category_exist(category_name):
            self.create_category(category_name)

        try:
            self.__CONNECTION.execute(
                'INSERT INTO listings (title, description, price, username, category) VALUES (?, ?, ?, ?, ?)',
                (title, description, price, username, category_name))
            self.__CONNECTION.commit()

            self.update_category_listing_count(category_name, 1)

            return self.__CURSOR.lastrowid
        except:
            return DatabaseResponse.CREATE_OBJECT_EXISTED


    def get_listing_by_id(self, listing_id) -> LISTING:
        listing = self.__CURSOR.execute('SELECT * FROM listings WHERE id = ?', (listing_id,)).fetchone()
        if listing is None:
            return DatabaseResponse.GET_OBJECT_NOT_FOUND
        return listing

    def get_listings_by_category(self, category_name) -> List[LISTING]:
        listings = self.__CURSOR.execute('SELECT * FROM listings WHERE category = ?', (category_name,)).fetchall()
        if listings is None:
            return DatabaseResponse.GET_OBJECT_NOT_FOUND
        return listings

    def delete_listing(self, listing_id, username):
        listing = self.__CURSOR.execute('SELECT * FROM listings WHERE id = ?', (listing_id,)).fetchone()
        if listing is None or listing[5] != username:
            return DatabaseResponse.USER_UNKNOWN

        self.update_category_listing_count(listing[6], -1)

        try:
            self.__CONNECTION.execute('DELETE FROM listings WHERE id = ?', (listing_id,))
            self.__CONNECTION.commit()
            return DatabaseResponse.SUCCESS
        except:
            return DatabaseResponse.GET_OBJECT_NOT_FOUND

    # Cache for top categories
    def get_top_categories_cache(self):
        if self.__TOP_CATEGORIES_CACHE is None:
            self.__TOP_CATEGORIES_CACHE = self.get_top_categories()
        return self.__TOP_CATEGORIES_CACHE

    def update_top_categories_cache(self, category_name, new_listing_count):
        if self.__TOP_CATEGORIES_CACHE is None or new_listing_count >= self.__TOP_CATEGORIES_CACHE[0]:
            self.__TOP_CATEGORIES_CACHE = (new_listing_count, [category_name])
        elif category_name in self.__TOP_CATEGORIES_CACHE[1]:
            self.__TOP_CATEGORIES_CACHE = self.get_top_categories()
