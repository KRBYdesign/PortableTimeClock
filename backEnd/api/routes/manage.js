const express = require('express');
const router = express.Router();
const serverHelpers = require('../helpers/serverfunctions');

// Requests throgh this page will be coming from python scripts.
// Careful not to exceed any request or rate limits on your database.

// Generic endpoint to let applications know the server is alive
router.get('/',(req, res, next)=>{
	res.status(200).json({
		message: "The management endpoint is live",
	});
});

// Request for all entries from the timeclock
router.get('/all-time', async (req, res, next) => {
	let allEntries = await serverHelpers.GetAllTimeClockEntries();
	
	res.status(200).json({
		message: "Returning all entries from timeclock",
		payload: allEntries,
	});
});

// Request to get all users from the userlist
router.get('/all-users', async (req, res, next) => {
	let usersList = await serverHelpers.GetUsersList();
	
	res.status(200).json({
		message: "Returning users list",
		payload: usersList,
	});
});

module.exports = router;
