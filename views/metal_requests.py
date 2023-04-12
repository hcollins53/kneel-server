import sqlite3
import json
from models import Metals

METALS = [
    {
        "id": 1,
        "metal": "Sterling Silver",
        "price": 12.42
    },
    {
        "id": 2,
        "metal": "14K Gold",
        "price": 736.4
    },
    {
        "id": 3,
        "metal": "24K Gold",
        "price": 1258.9
    },
    {
        "id": 4,
        "metal": "Platinum",
        "price": 795.45
    },
    {
        "id": 5,
        "metal": "Palladium",
        "price": 1241
    }
]


def get_all_metals(query_params):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sort_by = ""
        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")
            if qs_key == "_sortBy":
                if qs_value == 'price':
                    sort_by = " ORDER BY price"
        sql_to_execute = f"""
      SELECT
          m.id,
          m.metal,
          m.price
      FROM Metals m
        {sort_by}
      """
        db_cursor.execute(sql_to_execute)
        # Initialize an empty list to hold all animal representations
        metals = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            metal = Metals(row['id'], row['metal'], row['price'])
            # Add the dictionary representation of the animal to the list
            metals.append(metal.__dict__)

    return metals
# Function with a single parameter


def get_single_metal(id):
    # Variable to hold the found metal, if it exists
    requested_metal = None

    # Iterate the METALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for metal in METALS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if metal["id"] == id:
            requested_metal = metal

    return requested_metal


def update_metal(id, new_metal):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Metals
            SET
                metal = ?,
                price = ?
        WHERE id = ?
        """, (new_metal['metal'], new_metal['price'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
