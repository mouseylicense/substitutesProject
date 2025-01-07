# Dashboard
# The Dashboard Part of this project:

# High Seas Demo:
https://cc.mousey.hackclub.app/dashboard/report - to report a problem
https://cc.mousey.hackclub.app/dashboard/ - dashboard
https://cc.mousey.hackclub.app/dashboard/home - dashboard home
Slack Bot channel: #mouseys-bot-spam
User:
email: example@example.com
password: example


This project originally was a project to help school manage teacher substitutions, over time this project grew and grew, to the point where it is now supposed to manage the entire school's schedule.

**Now this project is growing even more, ill try to explain the need, the solution, and why this project is not a project in itself:**
### The Need:

We need a way to track problems with our computers at school, additionally , we would like teachers to have a way to see what computer have a problem with them.


### The Solution
A Dashboard To show all problem in the school's computers, weve done this a long time ago and you can find it in my Github, this year because of network limitations in our school we couldnt host it in the school anymore, this lead me to redevelop it for deployment at my house where i already host some things for school, i needed to adapt it to django and ive added some features such as adding the ability to assign problem to members of the IT team.
### The Reason This Project Is Not a Standalone Project:
There are two reasons I chose to incorporate this project (the laptops project) with the substitutions/schedule project, 
they are really quite simple:
1. Centralizing, I just want both to be under the same domain.
2. Data, I already have all the teacher names and details in my substitutes project as well as the classes

## How To Use:
Follow The guide in the main readme, in the .env file, you should have:

``DASHBOARD_ENABLED = 'True'``
navigate to /dashboard/home

## Pictures:
|                                                                                     |                                                                                     |
|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
 | ![Teacher's Home page](https://cloud-lwbxubitx-hack-club-bot.vercel.app/0image.png) | ![Requesting Laptops](https://cloud-lwbxubitx-hack-club-bot.vercel.app/2image.png)  |
| ![Stats Page](https://cloud-lwbxubitx-hack-club-bot.vercel.app/3image.png)          | ![Page to manage pins](https://cloud-mffra1490-hack-club-bot.vercel.app/0image.png)                                                            |
[https---cloud-lwbxubitx-hack-club-bot.vercel.app-1image.png.url](../../AppData/Local/Temp/https---cloud-lwbxubitx-hack-club-bot.vercel.app-1image.png.url)