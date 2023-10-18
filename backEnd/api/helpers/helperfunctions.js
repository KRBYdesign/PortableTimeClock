const express = require('express');
const router = express.Router();
const mysql = require('mysql');

// Check Database for duplicate names or id numbers
async function CheckDBForDupe(id, name) {
	return new Promise(async (resolve) => {
		let nameDupe = await NameDupe(name);
		let idDupe = await IdDupe(id);
		
		if ((!nameDupe) && (!idDupe)) {
			resolve(false);
		} else {
			resolve(true);
		}
	});
}

// Returns true if the passed ID is already in the userlist
async function IdDupe(id) {
	return new Promise(async (resolve) => {
		let query = `SELECT * FROM userlist WHERE number='${id}';`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				// res.length expected to be 0 if no duplicates exist
				if (res.length > 0) {
					resolve(true);
				} else {
					resolve(false);
				}
			});
		});
	});
}

// Functions the same as IdDupe() but for names instead of Id's
async function NameDupe(name) {
	return new Promise(async (resolve) => {
		let query = `SELECT * FROM userlist WHERE name='${name}';`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				// res.length expected to be 0 if no duplicates exist
				if (res.length > 0) {
					resolve(true);
				} else {
					resolve(false);
				}
			});
		});
	});
}

// Establishes connection to the Database running on the Pi
async function ConnectToDB() {
	let con = mysql.createConnection({
		host: "localhost",
		
		// Should be changed based upon the intneded
		// database's information
		user: "stationserver",
		password: "locallogin",
		database: "stationTimeClock"
	});
	return con;
}

// Add a singular user to the userlist
async function addUserToDb(id, name) {
	let query = `INSERT INTO userlist (number, name) VALUES ('${id}', '${name}');`;
	let con = await ConnectToDB();
	
	con.connect(function (err) {
		if (err) throw err;
		
		con.query(query);
	});
}

// Search the userlist by a given name. If a user is found, return true
// if not, return false
async function SearchForUser(searchName) {
	return new Promise(async (resolve) => {
		let query = `SELECT * FROM userlist WHERE name LIKE '%${searchName}%';`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				if (res.length > 0) {
					resolve(true);
				} else {
					resolve(false);
				}
			});
		});
	});
}

// Functions the same as SearchForUser() but by id number
// instead of name
async function SearchForUserNumber(number) {
	return new Promise(async (resolve) => {
		let query = `SELECT * FROM userlist WHERE number='${number}';`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				if (res.length > 0) {
					resolve(true);
				} else {
					resolve(false);
				}
			});
		});
	});
}

// Based upon the user's previous actions, clock a user in or out.
function ClockUserInOrOut(id, date, time, nextAction) {
	if (nextAction == "IN") {
		ClockIn(id, date, time);
	} else {
		ClockOut(id, date, time);
	}
}

// Inserts a "IN" entry into the timeclock table
async function ClockIn(id, date, time) {
	let query = `INSERT INTO timeclock (action, number, date, time) VALUES ('IN', '${id}', '${date}', '${time}');`;
	let con = await ConnectToDB();
	
	con.connect(function (err) {
		if (err) throw err;
		
		con.query(query, async (err, res, fields) => {
			if (err) {
				console.warn(err);
			}
		});
	});
}

// Inserts a "OUT" entry into the timeclock table
async function ClockOut(id, date, time) {
	let query = `INSERT INTO timeclock (action, number, date, time) VALUES ('OUT', '${id}', '${date}', '${time}');`;
	let con = await ConnectToDB();
	
	con.connect(function (err) {
		if (err) throw err;
		
		con.query(query, async (err, res, fields) => {
			if (err) {
				console.warn(err);
			}
		});
	});
}

// Returns the appropriate action for a user based upon
// whether their previous action was "IN" or "OUT"
//
// Returns "IN" when a previous entry cannot be found, as
// the user is clocking in for the first time.
async function GetNextAction(id) {
	return new Promise(async (resolve) => {
		let query = `SELECT action FROM timeclock WHERE number='${id}';`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				if (res.length == 0) {
					resolve("IN");
				} else if (res.length % 2 == 0) {
					resolve("IN");
				} else {
					resolve("OUT");
				}
			});
		});
	});
}

// Returns all users whose name matches the searched string.
async function GetUsersList(searchName) {
	return new Promise(async (resolve) => {
		let query = `SELECT * FROM userlist WHERE name LIKE '%${searchName}%';`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			let results = [];
			
			con.query(query, (err, res, fields) => {
				for (let i=0; i < res.length; i++) {
					results.push(res[i]);
				}
				resolve(results);
			});
		});
	});
}

// Returns a user based upon a given ID number
async function GetUserNameByNumber(id) {
	return new Promise(async (resolve) => {
		let query = `SELECT name FROM userlist WHERE number='${id}';`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				if (res.length > 0) {
					resolve(res[0].name);
				} else {
					resolve("User Not Found");
				}
			});
		});
	});
}

// Returns a list of all users in the userlist
async function GetAllUsers() {
	return new Promise(async (resolve) => {
		let query = `SELECT * FROM userlist;`;
		let con = await ConnectToDB();
		
		con.connect(function (err) {
			if (err) throw err;
			
			con.query(query, (err, res, fields) => {
				resolve(res)
			});
		});
	});
}

// Functions similarly to the CheckDbForDupe() function but faster,
// as a call to the DB for the userlist has been done previously,
// and the resulting list of users, supplied to the funciton.
async function CheckListForDupe(newUsers, dbUsers) {
	return new Promise((resolve) => {
		let matches = 0;
		
		// Loop through all the new users
		newUsers.forEach((user) => {
			// Loop through all the existing users
			for (let i = 0; i < dbUsers.length; i++) {
				if (dbUsers[i]['name'] == user[0]) {
					matches++;
					console.log("Name Match:", user[0]);
				}
				
				if (dbUsers[i]['number'] == user[1]) {
					matches++;
					console.log("Number Match:", user[1]);
				}
			}
		});
		
		if (matches > 0) {
			resolve(true);
		} else {
			resolve(false);
		}
	});
}

// Register multiple users at once. Do not use the singular form
// of this function addUserToDB() as the maximum number of querys
// can be exceeded with longer user lists.
async function BulkRegisterUsers(userList, listLength) {
	return new Promise(async (resolve) => {
		// Start the query
		let query = `INSERT INTO userlist (number, name) VALUES `;
		
		let allUsers = await GetAllUsers();
		
		let isDupe = await CheckListForDupe(userList, allUsers);
		console.log(isDupe);
		
		// If a duplicate is found, stop the process. Don't add
		// this list to the database.
		if (isDupe) {
			resolve(false);
		} else {
			userList.forEach((el) => {
				let elName = el[0];
				let elNumber = el[1];
				
				// Add each user's values to they query
				let addStatemnt = `('${elNumber}', '${elName}'),`;
				query += addStatemnt;
			});

			// Remove the finaly "," from the query
			query = query.substring(0, query.length - 1);

			// Append a ; to the end of your query
			query += `;`;
			
			// Run it
			let con = await ConnectToDB();
			con.connect(function (err) {
				if (err) throw err;
				
				con.query(query);
			});
			
			resolve(true)
		}
	});
}

module.exports = {
	router,
	CheckDBForDupe,
	addUserToDb,
	SearchForUser,
	SearchForUserNumber,
	GetUsersList,
	ClockUserInOrOut,
	GetUserNameByNumber,
	GetNextAction,
	GetAllUsers,
	BulkRegisterUsers,
}
