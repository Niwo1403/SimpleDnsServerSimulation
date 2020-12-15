### Setup:
#### PyCharm:
Import the SimpleDnsServer folder as a project in PyCharm. 
To run, right click a file and select "Run 'file.py'". If there is a file not found error you may need to set the 
working directory of the configuration (top right) to "pathToDirectory/SimpleDnsServer/src". 
(In the top right, click the drop down menu left of the green "run" button. Then select "edit configurations" and set 
working directory to "pathToDirectory/SimpleDnsServer/src")

#### Terminal:
To run files in the terminal, just type "python fileName.py".

###Running the DNS servers:
To test the server, run the run.py in the src folder.
The run.py file initializes all the dns servers, the http servers and the resolver. 
Then it sends a request to the resolver, which asks the root server, then asks the dns servers etc. 
The server will log their their requests into the corresponding log file in log/<ip>.log.

The initial request and the final response, as well as the time took for the request will be printed to console as well.
(so the data, the client sees)

Then it sends the same request to the resolver again, which then has a valid cache entry, so there is no need to ask 
dns servers. (will result in speedup and no log entries for the dns server)

### Testing the proxy:
To start all Server and keep them running, just run the main.py file in the src folder.

Then, the proxy should listen on 127.0.0.100:80.
To send a request to linux.pxpools.fuberlin, enter: 127.0.0.100/linux.pcpools.fuberlin in the browser. 
For unknown endings the normal DNS lookup will be used.
(May throw lots of warnings in the console, but should work)

