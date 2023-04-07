import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import all, retrieve, update, create, delete, create, retrieve_query
# Import this stdlib package first
from urllib.parse import urlparse
# Import this stdlib package first
# from urllib.parse import urlparse

class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Replace existing function with this
    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = url_components.query.split("&")
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id, query_params)

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        "get either all or one"
        response = None
        (resource, id, query_params) = self.parse_url(self.path)
        if id is None:
            self._set_headers(200)
            response = all(resource)
        if query_params is not None and id is not None:
            self._set_headers(200)
            response = retrieve_query(resource, id, query_params)
        elif id is not None and query_params is None:
            self._set_headers(200)
            response = retrieve(resource, id)
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):
        "create"
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)
        new_resource = None
        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)
        if resource == "styles" or "metals" or "sizes":
            new_resource = {"message": f'{resource} cannot be created'}
        else:
            new_resource = create(resource, post_body)
        # Initialize new animal

        self.wfile.write(json.dumps(new_resource).encode())
    # A method that handles any PUT request.

    def do_DELETE(self):
        "delete"
    # Set a 204 response code
        response = {}
    # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)
        self._set_headers(204)
    # Delete a single animal from the list
        if resource == "styles" or "metals" or "sizes" or "orders":
            response = {"message": f"{resource} cannot be deleted"}
        else:
            delete(id, resource)

    # Encode the new animal and send in response
        if response is not None:
            self.wfile.write(json.dumps(response).encode())
        else:
            self.wfile.write("".encode())

    def do_PUT(self):
        "update"
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        if resource == "styles" or "sizes" or "orders":
            response = {"message": f"{resource} cannot be updated"}
        else:
            update(id, post_body, resource)
        # Encode the new animal and send in response
        if response is not None:
            self.wfile.write(json.dumps(response).encode())
        else:
            self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
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

# This function is not inside the class. It is the starting
# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

