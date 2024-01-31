import Pyro5

# Pyro5 client
with Pyro5.demon.serve() as daemon:
    # Get the proxy for the remote object
    remote_object = Pyro5.Proxy("PYRONAME:example.remote_object")
    # Call the remote method
    print(remote_object.remote_method())