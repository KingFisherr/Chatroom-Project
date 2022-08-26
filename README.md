# Live Chat Project


## Table of Contents
1. [Overview](#Overview)
2. [Features](#Features)
3. [Design/Implementation](#Design/Implementation)
4. [Requirements](#Requirements)
5. [Resources](#Resources)

## Overview
### Description
LiveChat is an application which implements a program allowing concurrent communication between multiple clients using TCP through a secure custom encrypted server. Clients can utilize features of the communication protocol  through traditional methods such as text messaging or by sending media content. 

## Features

- Hashed Login
<img src='https://i.imgur.com/WO0gr3T.png' title='Video Walkthrough' width='550' alt='Video Walkthrough' />

- Client Lobby
<img src='https://i.imgur.com/EgTg5mU.png' title='Video Walkthrough' width='525' alt='Video Walkthrough' />

- Instant Messaging
![](https://i.imgur.com/Ti9C9iD.png)

- File Explorer (Upload Button)
<img src='https://i.imgur.com/8uXfJEk.png' title='Video Walkthrough' width='550' alt='Video Walkthrough' />


- Media Upload (File Transfer)
<img src='https://i.imgur.com/Dh1hNst.png' title='Video Walkthrough' width='550' alt='Video Walkthrough' />


- Media Download (File Transfer)
<img src='https://i.imgur.com/udAJD4w.png' title='Video Walkthrough' width='550' alt='Video Walkthrough' />



    - What server sees: Encrypted Data
        ![](https://i.imgur.com/WXFbp1c.png)
    - What client sees: Decrypted Data
        ![](https://i.imgur.com/SZabiHc.png)

## Design/Implementation


###  High Level Design
![](https://i.imgur.com/w9RpSrp.png)

### Modules

| Name | Type | Description |
| -------- | -------- | -------- |
| Server  |Host Program| unique game ID 
| Client(s)| Client Program| unique player ID
| Encryption Model| Encryption Class| unique team ID
| Decryption Model|Decryption Class| Holds all live games for a certain date
|Database Models|Database Handler Class|Holds all team stats for a certain team
|UserInfo Database| Database| Contains hashed user info (sqlite)
|BannedUser Database|Database|Contains banned user info (sqlite)

#### Server Program Functions
    -(READ/GET) Queries the live games details given by given gameID
    -(READ/GET) Queries the player headshots
    -(READ/GET) Queries the player stats
    -(READ/GET) Queries the team logo    

#### Client Program Functions
    -(READ/GET) Queries the live games details given by given gameID
    -(READ/GET) Queries the player headshots
    -(READ/GET) Queries the player stats
    -(READ/GET) Queries the team logo    

## Requirements 

### Tools and Packages

You will need the following packages for this application

### How it works

An untrained instance of ChatterBot starts off with no knowledge of how to communicate. Each time a user enters a statement, the library saves the text that they entered and the text that the statement was in response to. As ChatterBot receives more input the number of responses that it can reply and the accuracy of each response in relation to the input statement increase. The program selects the closest matching response by searching for the closest matching known statement that matches the input, it then returns the most likely response to that statement based on how frequently each response is issued by the people the bot communicates with.

### Installation

Required packages can be installed with pip:

```
 pip install json
```
### Run Program

Required packages can be ran via terminal:

```
 1. run py server.py
 2. run py guitest.py
```
### Development pattern for contributors

1. [Create a fork](https://help.github.com/articles/fork-a-repo/) of the [Chat Room Project](https://github.com/KingFisherr/Chatroom-Project) on GitHub.
2. Create a new branch to make changes.
3. [Create a pull request](https://help.github.com/articles/creating-a-pull-request/).
4. Please follow the [Python style guide for PEP-8](https://www.python.org/dev/peps/pep-0008/).

## Resources:

### Socket Programming
https://realpython.com/python-sockets/
https://codingcompiler.com/sockets-and-message-encryption-decryption-between-client-and-server/
https://medium.com/@md.julfikar.mahmud/secure-socket-programming-in-python-d37b93233c69
https://nikhilroxtomar.medium.com/file-transfer-using-tcp-socket-in-python3-idiot-developer-c5cf3899819c
### Multithreading
https://www.youtube.com/watch?v=NGLeprazvkM
https://realpython.com/intro-to-python-threading/
### Encryption/ Decryption
https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372
https://arxiv.org/abs/2203.03795
https://pyauth.github.io/pyotp/