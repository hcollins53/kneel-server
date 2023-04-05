ORDERS = [
    {
        "id": 1,
        "metal_id": 3,
        "size_id": 2,
        "style_id": 3,
    }
 ]

def get_all_orders():
    "getting all orders"
    return ORDERS

def get_single_order(id):
    "getting a single order"
    # Variable to hold the found order, if it exists
    requested_order = None

    # Iterate the orderS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for order in ORDERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if order["id"] == id:
            requested_order = order

    return requested_order
def create_order(order):
    "creating a new order"
    max_id = ORDERS[-1]["id"]
    new_id = max_id + 1
    order["id"] = new_id
    ORDERS.append(order)
    return order

def delete_order(id):
    "deleting an order"
    order_index = -1
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            order_index = index
    if order_index >=0:
        ORDERS.pop(order_index)

def update_order(id, new_order):
    # Iterate the orderS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break