# Projekt 01 von Nicolai Wolfrom, Cedric Ressler und Emil Merle

# Which component does what?

## log folder: 
Here, the logs of the servers are stored. 

## rsrc folder:
In this folder, the .zone files represent the "logic" behind the server system. Every server has a file in where we his
 "known" servers are. 
The config file is a standard config and tracks which server is assigned to which ip address.

## rsc folder:
This folder holds files for basic servers, the basic functionality of the logger and the main.py file which runs an 
example. 

Also the dns and http servers are implemented here. 
### dns folder:
#### dns_server: 
This folder holds the files to implement a simple dns server, with methods to set up the server, listen to incoming 
request and handling requests.
#### recursive_resolver folder:
This folder holds the files to implement the recursive resolver. Also with methods to set up and handle requests. 
In addition the cache for the resolver is implemented here. 
#### resource_record folder:
With this folder the resource records are managed, generated and searched. It implements the basic functionality of a 
resource record. 
#### dns_message.py:
This file implements the basic dns message. It has methods to build a new message and to set values for the fields. 

### http_server: 
In this folder the simple http server is implemented. It holds methods to set up and run the server, and also to handle 
incoming requests. 



## test folder:
This folder has only the send_udp_msg.py file in it. 
This file is the "client" from which we can send requests to the resolver.


# What works, what not?
