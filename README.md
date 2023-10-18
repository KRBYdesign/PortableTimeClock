# Portable Time Clock

Author: Kyle Beasley

Email: <kyle@lacoxconsulting.com>

---

Simple api-based employee time clock system. This project utilizes ExpressJS and MariaDB running on a Raspberry Pi for the back-end, and supports multiple front-ends running on other computers' localhosts. In this example, XAMPP is used by the client computers.  

In theory this project could be extended to function using a live domain, however a constraint on this project was the lack of internet access.

In this instance, communications are handled by a cheap wireless router.

The front end features a "Help" page which helps an end user to use the setup and run the entire time clock system.

## What was the purpose?

TNT Security Solutions was contracted to provide security for a large outdoor music festival, and was looking for a way to manage their users, and keep a time clock. The festival is being held in a rural location meaning cell service, and broadband internet service are hard to come by. Ideally the solution shouldn't rely on an external internet connection.

After some deliberation, it was decided a simple ID number and barcode system would provide the level of reporting and management TNT required.

TNT intends to continue using this system for all future field jobs.

## What's included?

- All front end code (sans the .gif used on the help pages, and the logo in the header.)
- All back end code
- User List and Time Clock management tools utilizing python

## What's needed?

- Wireless Router
  - For this example, [this router](https://www.netgear.com/home/wifi/routers/r6020/) was used.
- Raspberry Pi
  - Other computers will work. They just need to be able to run Node.js
- Experience using ExpressJS would be beneficial
- Secondary "client" computers. These will all be equipped with barcode scanners.

---

## How it works

Download and extract the full .zip file from GitHub.

### The Router

You can use a router without an internet connection. All you have to do is turn it on, and it'll broadcast a local network that devices can use to communicate. Login to the router, setup your network's name and password, then connect your client devices to the routers new network.

The login information can usually be found on the back or bottom of the device.

### The Server / Raspberry Pi

Transfer the `/backEnd` directory to the computer which will act as the server. There are multiple ways to do this however, this isn't a tutorial for that. FWIW, when transferring files to my Pi, I found FileZilla to be the easiest by far.

Inside the `/backEnd` directory on the server, install all required packages with the command `npm install`, then run `npm start`

This install all required packages by the package.json file, as well as fire up Node.js / Express at the server's Local IP address, PORT 5000

**NOTE:** This port can be adjusted in the `server.js` file located in the `/backEnd` directory. Be sure to make the corresponding changes to the `index.js` and `register.js` files located in the `/frontEnd` directory.

### The Database

In my case, the database lived on the Raspberry Pi along with the server. If you'd like to follow the same structure I used, the database is named `stationTimeClock`. It contains two tables, `userlist` and `timeclock`.

To create `userlist`:

```SQL
{
CREATE TABLE userlist (
    id INT AUTO_INCREMENT KEY,
    number VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
);
}
```

To create `timeclock`:

```SQL
{
CREATE TABLE userlist (
    id INT AUTO_INCREMENT KEY,
    number VARCHAR(10) NOT NULL,
    action VARCHAR(10) NOT NULL,
    date VARCHAR(100) NOT NULL,
    time VARCHAR(100) NOT NULL,
);
}
```

---

Aside from [Barcode.js](https://github.com/lindell/JsBarcode), and the Node Modules, all code featured in this project is written by myself.

I want to give a shout out to Robert Evans, host of the podcast [Behind the Bastards](https://www.iheart.com/podcast/105-behind-the-bastards-29236323/) (the 19th most popular podcast on Apple Podcasts as of the time of writing this), for putting out the 5-part banger, "G. Gordon Liddy, the Fascist Behind Watergate". Your tongue and cheek humor got me through the process of learning asynchronous functions.
