import sqlite3
import json
from models import Sizes

SIZES = [
    { "id": 1, "carets": 0.5, "price": 405 },
    { "id": 2, "carets": 0.75, "price": 782 },
    { "id": 3, "carets": 1, "price": 1470 },
    { "id": 4, "carets": 1.5, "price": 1997 },
    { "id": 5, "carets": 2, "price": 3638 }
 ]

def get_all_sizes(query_params):
    "getting all metals"
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
          s.id,
          s.carets,
          s.price
      FROM Sizes s
        {sort_by}
      """
        db_cursor.execute(sql_to_execute)
        # Initialize an empty list to hold all animal representations
        sizes = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            size = Sizes(row['id'], row['carets'], row['price'])
            # Add the dictionary representation of the animal to the list
            sizes.append(size.__dict__)

    return sizes

def get_single_size(id):
    "getting a single size"
    # Variable to hold the found size, if it exists
    requested_size = None

    # Iterate the sizeS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for size in SIZES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if size["id"] == id:
            requested_size = size

    return requested_size