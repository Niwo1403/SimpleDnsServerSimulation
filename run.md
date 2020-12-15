To start all Server and keep them running, just run the main.py file.

To test the server, run the run.py.
The run.py file initializes all the dns servers, the http servers and the resolver. 
Then it sends a request to the resolver, which asks the root server, then asks the dns servers etc. 
The server will log their their requests into the corresponding log file in log/<ip>.log.

The initial request and the final response, as well as the time took for the request will be printed to console as well. (so the data, the client sees)

Then it sends the same request to the resolver again, which then has a valid cache entry, so there is no need to ask 
dns servers. (will result in speedup and no log entries for the dns server)

