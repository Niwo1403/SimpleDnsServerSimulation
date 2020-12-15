# Projekt 01 von Nicolai Wolfrom, Cedric Ressler und Emil Merle

# Which component does what?

## log folder: 
Here, the logs of the servers are stored. 

## rsrc folder:
In this folder, the .zone files contain the resource records for the server system. So every server has a file in which his
 "known" servers are. 
The config.json file is a standard config and tracks which server is assigned to which ip address, as well as the root server for the recursive resolver..

## src folder:
This folder holds the whole code - files for basic servers, the basic functionality of a logger and the main.py file, which will start all server and run them until a keyboard interrupt..
 
Also the dns and http servers are implemented here. 
### dns folder:
#### dns_server: 
This folder holds the files to implement a simple dns server, with methods to set up the server and handling incoming 
request.
#### recursive_resolver folder:
This folder holds the files to implement the recursive resolver. Also with methods to set up and handle requests. 
In addition the cache for the resolver is implemented here. 
#### resource_record folder:
With this folder the resource records are read, managed and searched. It implements the basic functionality used to work with resource records. 
#### dns_message.py:
This file implements the basic dns message. It has methods to build a new message and to set values for the fields. 
It's used to generate new json requests and responses or to read received ones.

### http_server: 
In this folder the simple http server is implemented. It holds methods to set up and run the server, and also to handle 
incoming requests. 
All http requests will be responded with "200 OK" as head and the incoming request and servername (e.g. windows.pcpools.fuberlin) as body.


## test folder:
Includes files or scripts used to test the server.
This folder has only the send_udp_msg.py file in it. 
This file is the "client" from which we can send UDP requests to the resolver.


# What works, what not?
All milestones are implemented. 

* Logging is implemented in a different format, but basic logging works. 
* The Proxy can only process simple HTTP requests, so most websites look really plain. 
* All HTTP servers are running
* The log will be appended to the current log, so the files will contain the logs of all time (but are initially empty). So logs couldn't get lost by a server restart or interrupt of any kind (closing window, task manager kill, ...).
