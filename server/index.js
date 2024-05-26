require('dotenv').config();

const cors = require('cors')
const exerciseRoutes = require('./routes/exercises')
const express = require('express');
const mongoose = require('mongoose')

// express app


const app = express();

// middleware
app.use(cors())
app.use(express.json())

app.use((req, res, next) => {
    console.log(req.path, req.method)
    next()
})


// routes config
app.use('/api/exercises', exerciseRoutes)

// connect to mongoDB & init api
mongoose.connect(process.env.MONGO_URI).then(() => {

// listen for requests on given port in .env file
app.listen(process.env.PORT, () => {
    console.log('Connected to db: listening on port ' + process.env.PORT + '.') 
    })
})

// catch error if something goes wrong
.catch((error) => {
    console.log(error)
})