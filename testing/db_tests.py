from database.db import Database
from core.utils import dict_factory


def test_init_db(db: Database = None) -> tuple:
    """
    Tests that the database is initialized correctly.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db") if db is None else db

    if db.database_path != "database/store_records.db":
        error = f"Error in test_init_db: Database path is not correct.\n  - Actual: {db.database_path}"
        return False, error
    else:
        return True, "Database path is correct."


def test_get_inventory_exists(db: Database = None) -> tuple:
    """
    Tests that the inventory is not empty.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db") if db is None else db
    full_inventory = db.get_full_inventory()

    if len(full_inventory) == 0:
        error = f"Error in test_get_full_inventory: Full inventory is empty.\n  - Actual: {len(full_inventory)}"
        return False, error
    else:
        return True, "Full inventory is not empty."


def test_dict_factory_link(db: Database = None) -> tuple:
    """
    Tests that the row factory is linked to dict_factory.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string,
    """
    db = Database("database/store_records.db") if db is None else db
    row_factory = db.connection.row_factory

    if row_factory != dict_factory:
        error = f"Error in test_dict_factory_link: Row factory is not linked to dict_factory.\n  - Expected: {dict_factory}\n  - Actual: {row_factory}"
        return False, error
    else:
        return True, "Row factory is linked to dict_factory."


def test_check_connection_threaded(db: Database = None) -> tuple:
    """
    Tests that the database connection is not single threaded.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string,
    """

    db = Database("database/store_records.db") if db is None else db
    connection_is_threaded = db.connection.isolation_level is None

    if connection_is_threaded:
        error = f"Error in test_check_connection_single_thread: Connection is single threaded.\n  - Actual: {connection_is_threaded}"
        return False, error
    else:
        return True, "Connection is not single threaded."
    

#And here is where Michelle starts to scheme and plan

def test_get_breadstick_exists(db: Database = None) -> tuple:
    """
    Tests that the inventory has breadsticks.
    """

    db = Database("database/store_records.db") if db is None else db
    breadstick_existance = db.get_breadstick()

    if len(breadstick_existance) == 0:
        error = f"Error in test_get_breadstick_exists: there is no stick of bread, only sadness"
        return False, error
    else:
        return True, "Breadstick."
    
def test_get_soup_exists(db: Database = None) -> tuple:
    """
    Tests that the inventory has soup.
    """

    db = Database("database/store_records.db") if db is None else db
    breadstick_existance = db.get_soup()

    if len(breadstick_existance) == 0:
        error = f"Error in test_get_soup_exists: there is no soup, only sadness"
        return False, error
    else:
        return True, "Soup."

def test_get_mango_price(db: Database = None) -> tuple:
    """
    Tests that the inventory mango price is correct.
    """

    db = Database("database/store_records.db") if db is None else db
    breadstick_existance = db.get_mango_price()

    if len(breadstick_existance) == 0:
        error = f"Error in test_get_mango_price: the price is incorrect"
        return False, error
    else:
        return True, "Correct price for Mango."
    
def test_wrong_mango_price(db: Database = None) -> tuple:
    """
    Tests for wrong mango price
    """

    db = Database("database/store_records.db") if db is None else db
    breadstick_existance = db.get_wrong_mango_price()

    if len(breadstick_existance) == 0:
        return True, "Correct price for Mango."
    else:
        error = f"Error in test_get_mango_price: the price is incorrect"
        return False, error
    
def test_get_steak_exists(db: Database = None) -> tuple:
    """
    Tests that the inventory has steak.
    """

    db = Database("database/store_records.db") if db is None else db
    steak_existance = db.get_steak()

    if len(steak_existance) == 0:
        error = f"Error in test_get_steak_exists: We out of steak"
        return False, error
    else:
        return True, "Steak."
    
def test_get_pasta_exists(db: Database = None) -> tuple:
    """
    Tests that the inventory has pasta.
    """

    db = Database("database/store_records.db") if db is None else db
    pasta_existance = db.get_pasta()

    if len(pasta_existance) == 0:
        error = f"Error in test_get_pasta_exists: We out of pasta"
        return False, error
    else:
        return True, "pasta."