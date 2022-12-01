"""Implements a MySQL Persistence Wrapper"""

from persistence_wrapper_interface import PersistenceWrapperInterface
from mysql import connector
from datetime import date


class MySQLPersistenceWrapper(PersistenceWrapperInterface):
    """Implements MySQL Persistance Wrapper"""

    def __init__(self):
        """Initializes """
        # Constants
        self.SELECT_ALL_INVENTORIES = 'SELECT id, name, description FROM inventories'
        self.INSERT_INV = 'INSERT INTO inventories (name, description, date) VALUES'
        self.INSERT = 'INSERT INTO items (inventory_id, item, count) VALUES'
        self.SELECT_ALL_ITEMS_FOR_INVENTORY_ID = 'SELECT id, inventory_id, item, count FROM items WHERE inventory_id = %s'

        # Database Configuration Constants
        self.DB_CONFIG = {'database': 'home_inventory', 'user': 'home_inventory_user', 'host': '192.168.56.1',
                          'port': 3306}

        # Database Connection
        self._db_connection = self._initialize_database_connection(self.DB_CONFIG)

    def get_all_inventories(self):
        """Returns a list of all rows in the inventories table"""
        cursor = None
        try:
            cursor = self._db_connection.cursor()
            cursor.execute(self.SELECT_ALL_INVENTORIES)
            results = cursor.fetchall()
        except Exception as e:
            print(f'Exception in persistance wrapper: {e}')
        return results

    def get_items_for_inventory(self, inventory_id):
        """Returns a list of all items for given inventory id"""
        cursor = None
        try:
            cursor = self._db_connection.cursor()
            cursor.execute(self.SELECT_ALL_ITEMS_FOR_INVENTORY_ID, ([inventory_id]))
            results = cursor.fetchall()
        except Exception as e:
            print(f'Exception in persistance wrapper: {e}')
        return results

    def create_inventory(self):
        """Insert new row into inventories table."""
        # try:
        cursor = self._db_connection.cursor()
        name = input("Enter the inventory name: ")
        desc = input("Enter the inventory description: ")
        self.INSERT_INV = f'{self.INSERT_INV}("{name}", "{desc}", "{date.today()}")'
        cursor.execute(self.INSERT_INV)
        # except Exception as e:
        #     print(e)

    def create_item(self):
        """Insert new row into items table for given inventory id"""
        try:
            cursor = self._db_connection.cursor()
            inv_id = int(input("Enter the inventory id: "))
            name = input("Enter the item name: ")
            count = int(input("Enter the count of item: "))
            self.INSERT = f'{self.INSERT}("{inv_id}", "{name}", "{count}")'
            cursor.execute(self.INSERT)
        except Exception as e:
            print(e)

    def _initialize_database_connection(self, config):
        """Initializes and returns database connection pool."""
        cnx = None
        try:
            cnx = connector.connect(pool_name='dbpool', pool_size=10, **config)
        except Exception as e:
            print(e)
        return cnx
