DATABASE = {
    "metals": [
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
  ],
  "sizes": [
    { "id": 1, "carets": 0.5, "price": 405 },
    { "id": 2, "carets": 0.75, "price": 782 },
    { "id": 3, "carets": 1, "price": 1470 },
    { "id": 4, "carets": 1.5, "price": 1997 },
    { "id": 5, "carets": 2, "price": 3638 }
 ],
 "styles": [
    { "id": 1, "style": "Classic", "price": 500 },
    { "id": 2, "style": "Modern", "price": 710 },
    { "id": 3, "style": "Vintage", "price": 965 }
],
"orders": [
    {
        "id": 1,
        "metal_id": 3,
        "size_id": 2,
        "style_id": 3,
    }
 ]
}

def all(resource):
    """for get requests"""
    return DATABASE[resource]

def retrieve(resource, id):
    """to get a single request"""
    requested = None
    if resource == "orders":
        for one_resource in DATABASE[resource]:
            if one_resource["id"] == id:
                requested = one_resource.copy()
                matching_size = retrieve("sizes", requested["size_id"])
                matching_style = retrieve("styles", requested["style_id"])
                matching_metal = retrieve("metals", requested["metal_id"])
                requested["price"] = matching_size["price"] + matching_metal["price"] + matching_style["price"]
    else:
        for one_resource in DATABASE[resource]:
            if one_resource["id"] == id:
                requested = one_resource.copy()
    return requested
def retrieve_query(resource, id, query_params):
    requested = None
    if resource == "orders":
        for one_resource in DATABASE[resource]:
            if one_resource["id"] == id:
                requested = one_resource.copy()
                matching_size = retrieve("sizes", requested["size_id"])
                matching_style = retrieve("styles", requested["style_id"])
                matching_metal = retrieve("metals", requested["metal_id"])
                requested["price"] = matching_size["price"] + matching_metal["price"] + matching_style["price"]
            for query_param in query_params:
                if query_param == 'size':
                    requested["size"] = matching_size
                    requested.pop("size_id")
                elif query_param == 'style':
                    requested["style"] = matching_style
                    requested.pop("style_id")
                elif query_param == 'metal':
                    requested["metal"] = matching_metal
                    requested.pop("metal_id")
    else:
        for one_resource in DATABASE[resource]:
            if one_resource["id"] == id:
                requested = one_resource.copy()
    return requested

def create(resource, post_body):
    """for POST"""
    max_id = DATABASE[resource][-1]["id"]
    new_id = max_id + 1
    post_body["id"] = new_id
    DATABASE[resource].append(post_body)
    return post_body

def update(id, post_body, resource):
    """put requests"""
    for index, new_resource in enumerate(DATABASE[resource]):
        if new_resource["id"] == id:
            DATABASE[resource][index] = post_body
            break

def delete(id, resource):
    """delete"""
    resource_index = -1
    for index, one_resource in enumerate(DATABASE[resource]):
        if one_resource["id"] == id:
            resource_index = index
    if resource_index >= 0:
        DATABASE[resource].pop(resource_index)