(We know this is supposed to be a python file but like this it is so much easier)

Please just run the main.py file in the src folder. 

The main.py file initializes all the dns servers, the http servers and the resolver. 
Then it sends some requests to the resolver, which asks the root server which then asks the dns servers etc. 
Here, the requests are printed in the console (not the answers).

Then it sends the same request to the resolver again, which then has a valid cache entry, so there is no need to ask 
dns servers. 

