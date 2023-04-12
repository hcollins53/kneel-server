import sqlite3
from models import Orders, Metals, Sizes, Styles

ORDERS = [
    {
        "id": 1,
        "metal_id": 3,
        "size_id": 2,
        "style_id": 3,
    }
 ]

def get_all_orders(query_params):
    "getting all orders"
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sort_by = ""
        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")
            if qs_key == "_sortBy":
                if qs_value == 'location':
                    sort_by = " ORDER BY location_id"
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            m.metal metal_metal,
            m.price metal_price,
            s.carets size_carets,
            s.price size_price,
            st.style style_style,
            st.price style_price
        FROM Orders o
        JOIN Metals m
            ON m.id = o.metal_id
        JOIN Sizes s
            ON s.id = o.size_id
        JOIN Styles st
            ON st.id = o.style_id
        """)

        # Initialize an empty list to hold all animal representations
        orders = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            order = Orders(row['id'], row['metal_id'], row['size_id'], row['style_id'])

            # Create a Location instance from the current row
            metal = Metals(row['id'], row['metal_metal'], row['metal_price'])

            size = Sizes(row['id'], row['size_carets'], row['size_price'])

            style = Styles(row['id'], row['style_style'], row['style_price'])

            # Add the dictionary representation of the location to the animal
            order.metal = metal.__dict__
            order.size = size.__dict__
            order.style = style.__dict__

            # Add the dictionary representation of the animal to the list
            orders.append(order.__dict__)

    return orders

def get_single_order(id):
    "getting a single order"
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id
        FROM Orders o
        WHERE o.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        order = Orders(data['id'], data['metal_id'], data['size_id'], data['style_id'])

        return order.__dict__
def create_order(new_order):
    "creating a new order"
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders
            ( metal_id, size_id, style_id )
        VALUES
            ( ?, ?, ?);
        """, ( new_order['metal_id'],
              new_order['size_id'], new_order['style_id']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid
        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
    new_order['id'] = id
    return new_order
def delete_order(id):
    "deleting an order"
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM orders
        WHERE id = ?
        """, (id, ))

def update_order(id, new_order):
    # Iterate the orderS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break