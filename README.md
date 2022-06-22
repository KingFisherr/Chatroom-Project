# Chatroom-Project
Chatroom application allowing multiple users to chat with one another with security and privacy in mind.

# Notes 

1) Networking and Security + Multithreading/Concurrency 

2) Most research for this chatroom project will be derived from python forums and research papers which discuss socket programming, threading, encryption, and databases. Other sources for research will be open source github projects with similar abstract.

3) Through research and practice, we hope to implement a multi user chatroom application. In essence we will be building a server side program and a client side program which seamlessly communicate with each other, even when multiple clients are communicating. Another important aspect we will be implementing, is the encryption of the entire server or perhaps the data sent by the clients. This will ensure the multi user chatroom is safe and secure. This security will also keep certain essential databases for the service safe.

Things to consider when implementing these concepts:

Socket Programming to create a server - client(s) chat room. 
	-Low latency communication on LAN
	-Connection via ports
Multithreading
	-Clients are able to carry out tasks concurrently
	-Clients are able to communicate with server concurrently
Encryption and Decryption to secure server data communications.



Progress:

6/8: Github repo created and added collaborators
6/8: Project proposal presentation created
6/9: Started project proposal presentation
6/10: Research essentials concepts for project
6/13: Presented project proposal, concepts, and approaches
6/15: Issues and tasks created on repo project board with individual codes

6/15: Basic server and client framework files added to repo
6/17: Documentation for server and client files, and a framework for functions implemented

6/19: Issues ED.0 and ED.1 being worked on
6/20: Issues S.0, S.1, S.2, and DB.0 being worked on
6/21: Issues C.0 and C.1 being worked on


Project due

Resources:

Socket Programming
-https://realpython.com/python-sockets/
-https://codingcompiler.com/sockets-and-message-encryption-decryption-between-client-and-server/
-https://medium.com/@md.julfikar.mahmud/secure-socket-programming-in-python-d37b93233c69
Multithreading
-https://www.youtube.com/watch?v=NGLeprazvkM
-https://realpython.com/intro-to-python-threading/
Encryption
-https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372
-https://arxiv.org/abs/2203.03795
-https://pyauth.github.io/pyotp/

