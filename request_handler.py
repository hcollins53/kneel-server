import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_all_styles, get_all_orders, get_all_sizes, create_order
from views import get_single_metal, get_single_style, get_single_size, get_single_order
from views import delete_order, update_order


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        "Test"
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple
    # Here's a class function
    def do_GET(self):
        """Handles GET requests to the server """
        response = {}  # Default response

    # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    response = {"message": f'That metal is not currently in stock'}
                    self._set_headers(404)
            else:
                self._set_headers(200)
                response = get_all_metals()
        if resource == "orders":
            if id is not None:
                response = get_single_order(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    response = {"message": "that order was never placed or was cancelled"}
                    self._set_headers(404)
            else:
                self._set_headers(200)
                response = get_all_orders()
        if resource == "sizes":
            if id is not None:
                response = get_single_size(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    response = {"message": "That size is not currently in stock"}
                    self._set_headers(404)
            else:
                self._set_headers(200)
                response = get_all_sizes()
        if resource == "styles":
            if id is not None:
                response = get_single_style(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    response = {"message": "that style is not currently in stock"}
                    self._set_headers(404)
            else:
                self._set_headers(200)
                response = get_all_styles()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        new_order = None

        if resource == "orders":
            if "size_id" in post_body and "metal_id" in post_body and "style_id" in post_body:
                self._set_headers(201)
                new_order = create_order(post_body)
            else:
                self._set_headers(404)
                new_order = {"message": f'{"a size is required" if "size_id" not in post_body else ""} {"a style is required" if "style_id" not in post_body else ""} {"a metal is required" if "metal_id" not in post_body else ""}'}
        self.wfile.write(json.dumps(new_order).encode())

    def do_PUT(self):
        "update"
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "orders":
            update_order(id, post_body)
        # Encode the new animal and send in response
        self.wfile.write("".encode())
    def do_DELETE(self):
        "delete an order"
        (resource, id) = self.parse_url(self.path)

        if resource == "orders":
            self._set_headers(405)
            response = {"message": f"Deleting this order is not allowed"}
        
        if response is not None:
            self.wfile.write(json.dumps(response).encode())
        else:
            self.wfile.write("".encode())
    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
