require('dotenv').config();

const express = require('express');

// express app

const app = express();

app.get('/', (req, res) => {
    res.json({mssg: "You shouldn't be here..."});
})

// listen for requests
app.listen(process.env.PORT, () => {
    console.log('Server started: listening on port ' + process.env.PORT + '.')
});
