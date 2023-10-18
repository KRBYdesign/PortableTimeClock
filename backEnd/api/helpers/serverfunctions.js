const express = require('express');
const router = express.Router();
const mysql = require('mysql');

// Establishes connection to the Database
async function ConnectToDB() {
	let con = mysql.createConnection({
		host: "localhost",
		
		// Information should be changed to reflect the
		// intended database.
		user: "stationserver",
		password: "locallogin",
		database: "stationTimeClock"
	});
	return con;
}

// Returns a list of all the entries into the timeclock
async function GetAllTimeClockEntries() {
	return new Promise(async (resolve) => {
		let query = `SELECT * FROM timeclock`;
		let con = await ConnectToDB();
	
		con.connect(function (err) {
			if (err) throw err;
		
			con.query(query, (err, res, fields) => {
				if (res.length > 0) {
					resolve(res);
				}
				else {
					resolve("NONE");
				}
			});
		});
	});
}

// Returns a list of all users in the userlist
async function GetUsersList() {
	return new Promise(async (resolve) => {
		let query = "SELECT * FROM userlist";
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				resolve(res)
			});
		});
	});
}

module.exports = {
	router,
	ConnectToDB,
	GetAllTimeClockEntries,
	GetUsersList,
}
