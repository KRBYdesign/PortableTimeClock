const express = require("express");
const app = express();
const morgan = require("morgan");
const bodyParser = require('body-parser');
const cors = require('cors');

// Establish Route Handling
const clockInRoutes = require("./api/routes/clockin");
const registerRoutes = require("./api/routes/register");
const managementRoutes = require("./api/routes/manage");

app.use(cors()); // Needed to make the POST requests work

// Needed for parsing JSON.body at runtime
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.use(morgan("dev")); // Logging server events

// Finally route requests to their destinations
app.use("/in", clockInRoutes);
app.use("/register", registerRoutes);
app.use("/manage", managementRoutes);

// If the request gets here, it doesn't match any of the endpoints.
app.use((req, res, next) => {
  const error = new Error("Not Found. Please be sure you are requesting the correct endpoint.");
  error.status = 404;
  next(error);
});

app.use((error, req, res, next) => {
  res.status(error.status || 500);
  res.json({
    error: {
      message: error.message,
    },
  });
});

module.exports = app;
