import sqlite3
import json
from models import Styles

STYLES = [
    { "id": 1, "style": "Classic", "price": 500 },
    { "id": 2, "style": "Modern", "price": 710 },
    { "id": 3, "style": "Vintage", "price": 965 }
]
def get_all_styles(query_params):
    "getting all styles"
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
          st.id,
          st.style,
          st.price
      FROM Styles st
        {sort_by}
      """
        db_cursor.execute(sql_to_execute)
        # Initialize an empty list to hold all animal representations
        styles = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            style = Styles(row['id'], row['style'], row['price'])
            # Add the dictionary representation of the animal to the list
            styles.append(style.__dict__)

    return styles

def get_single_style(id):
    "getting a single style"
    # Variable to hold the found style, if it exists
    requested_style = None

    # Iterate the styleS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for style in STYLES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if style["id"] == id:
            requested_style = style

    return requested_style