const express = require('express');

const router = express.Router();
const helpers = require('../helpers/helperfunctions');

// Generic endpoint to let applications know the server is working
router.get("/", (req, res, next) => {
	res.status(200).json({
		message: "Register route is live",
	});
});

// Return all users in the Database
router.get("/all", async (req, res, next) => {
	let userList = await helpers.GetAllUsers();
	console.log(userList);
	
	res.status(200).json({
		message: userList,
	});
});

// Find specific person in the database by their name
router.get("/:name", async (req, res, next) => {
	let searchName = req.params.name;
	let isFound = await helpers.SearchForUser(searchName);
	console.log(isFound);
	
	// If matching user(s) found, return them
	// Else return that a user was not found by that name.
	if (isFound) {
		let usersList = await helpers.GetUsersList(searchName);
		console.log(usersList);
		
		res.status(200).json({
			success: true,
			message: `User found`,
			payload: usersList,
		});
	} else if (!isFound) {
		res.status(404).json({
			success: false,
			message: `No user found by: ${searchName}`,
		});
	}
});

// Add a single person to the userlist
// Requests will be coming from the front end "Register" page
router.post("/", async (req, res, next) => {
	let body = req.body;
	let id = req.body.id;
	let name = req.body.name;
	
	let duplicate = await helpers.CheckDBForDupe(id, name);

	// If a duplicate is found, don't add the user. Instead
	// return that a duplicate was found.
	if (duplicate) {
		res.status(403).json({
			success: false,
			message: `A user with that id number or name already exists.`,
			id: id,
			name: name,
		});
	} else {
		helpers.addUserToDb(id, name);
		
		res.status(201).json({
			success: true,
			message: `User ${name} has been created with ID:${id}`,
			id: id,
			name: name,
		});
	}
});


// Add multiple people at once to the userlist.
// Requests will come from the 'management' python scripts
router.post("/python", async (req, res, next) => {
	let body = req.body;
	
	let payload = req.body.payload;
	let payloadLength = req.body.length;
	
	let addSuccess = await helpers.BulkRegisterUsers(payload, payloadLength);
	
	if (addSuccess) {
		res.status(201).json({
			success: true,
			message: "PASSED",
		});
	} else {
		res.status(201).json({
			success: false,
			message: "FAILED",
		});	
	}

});

module.exports = router;
