const express = require('express');
const router = express.Router();
const helpers = require('../helpers/helperfunctions');

// Generic endpoint to let applications know the server is alive
router.get('/',(req, res, next)=>{
	res.status(200).json({
		message: "The clock in endpoint is live",
	});
});

// Handle clock in / clock out requests from the front end
router.post('/', async (req, res, next) => {
	let id = req.body.id;
	
	// Figure out the current date and time
	let {date, time} = GetDateTime();
	
	// Find the requesting user
	let isFound = await helpers.SearchForUserNumber(id);
	
	// If you find the user, send them on to be processed
	// If not, return that a user cant be found by that number.
	if (isFound) {
		// What's the user's name again?
		let userName = await helpers.GetUserNameByNumber(id);
		
		// What action should be taken with the user?
		let nextAction = await helpers.GetNextAction(id);
		
		// Send it
		helpers.ClockUserInOrOut(id, date, time, nextAction);
		
		console.log(`${userName} has been clocked ${nextAction}`);
		
		res.status(201).json({
			success: true,
			message: `Time Clock request for ${userName} has been processed.`,
			name: userName,
			id: id,
			action: nextAction,
		});
	} else {
		res.status(404).json({
			success: false,
			message: `User with ${id} could not be found.`,
		});
	}
});

// Returns the current date and time as seperate variables
function GetDateTime() {
	let now = new Date();
	let date = now.toLocaleDateString();
	let time = now.toLocaleTimeString();
	
	return {date, time};
}


module.exports = router;
