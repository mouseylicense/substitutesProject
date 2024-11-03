# The Laptop Loaning Part of this project:

This project originally was a project to help school manage teacher substitutions, over time this project grew and grew, to the point where it is now supposed to manage the entire school's schedule.

**Now this project is growing even more, ill try to explain the need, the solution, and why this project is not a project in itself:**
### The Need:

In school, we allow teacher to "loan" laptops for classes, in case they need the students in the class to have laptops for the class,  the way this currently works is the teacher fills out a form, and a member/s of the IT team brings the laptops to the teacher's class. 

**This is problematic:** 
* For starters , it creates work for the IT team, as we need to bring the laptops to the classes, _we don't like extra work_.
* Secondly, there have been times, where we (the IT team) simply forgot to bring the laptops, meaning the teachers did not have computers for their classes.
* We **really** do not like extra (boring) work

### The Solution
This caused me (as head of IT) to search for a solution, the first that came to mind was a box that will house the key for the laptops cabinet, The box will open when you enter a PIN you get when filling a form, this is the solution we went with, and we built it.


The first version of this was a flask server running on a raspberry pi, this worked _for some time_ , but because we did
not handle the Raspberry Pi well, we burnt it (part of it anyway), we left the project and continued to be laptop delivery
men (and one woman), This version also flawed in other ways, for example: because the Raspberry pi  was in charge of both
the web server, and the physical control over the box (Locking the box and sensing if the key is inside for example) this
lead to **a lot** of downtime for the website and a very warm Raspberry Pi. 


This year, I have thought about this problem (and solution) again, I realized our method was flawed, What we **should've**
done is have a microcontroller (in our case, an ESP8266) controlling the box, querying a server with a code, opening the box if the response is correct,
I was in charge of the server while [@orgaPumpkin](https://github.com/orgaPumpkin) was in charge of the ESP.
Our Architecture is now like so:
![Architecture](https://cloud-2z7edm9l2-hack-club-bot.vercel.app/0architecture.png)

### The Reason This Project Is Not a Standalone Project:
There are two reasons I chose to incorporate this project (the laptops project) with the substitutions/schedule project, 
they are really quite simple:
1. Centralizing, I just want both to be under the same domain.
2. Data, I already have all the teacher names and details in my substitutes project

## How To Use:
Follow The guide in the main readme, in the .env file, you should have:

``LAPTOPS_ENABLED = 'True'``
navigate to /laptops/home

## Pictures:
|                                                                                     |                                                                                     |
|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
 | ![Teacher's Home page](https://cloud-p26ejmtci-hack-club-bot.vercel.app/3image.png) | ![Requesting Laptops](https://cloud-p26ejmtci-hack-club-bot.vercel.app/2image.png)  |
| ![Stats Page](https://cloud-p26ejmtci-hack-club-bot.vercel.app/0image.png)          | ![Page to manage pins](https://cloud-p26ejmtci-hack-club-bot.vercel.app/1image.png) |
