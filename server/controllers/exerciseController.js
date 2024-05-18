const Exercise = require('../models/exerciseModel')
const mongoose = require('mongoose')

// get all exercises
const getExercises = (req, res) => {
    res.json({mssg: 'get all'})
}

const getExercise = (req, res) => {
    res.json({mssg: 'get one'})
}

const updateExercise = (req, res) => {
    res.json({mssg: 'update one'})
}

const deleteExercise = (req, res) => {
    res.json({mssg: 'delete one'})
}

const createExercise = (req, res) => {
    res.json({mssg: 'create one'})
}

module.exports = {
    getExercises,
    getExercise,
    updateExercise,
    deleteExercise,
    createExercise
}