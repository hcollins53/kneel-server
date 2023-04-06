from .metal_requests import get_single_metal
from .size_requests import get_single_size
from .style_requests import get_single_style

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
            matching_size = get_single_size(requested_order["size_id"])
            requested_order["size"] = matching_size
            matching_style = get_single_style(requested_order["style_id"])
            requested_order["style"] = matching_style
            matching_metal = get_single_metal(requested_order["metal_id"])
            requested_order["metal"] = matching_metal
            requested_order.pop("size_id")
            requested_order.pop("style_id")
            requested_order.pop("metal_id")
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