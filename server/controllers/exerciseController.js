const Exercise = require('../models/exerciseModel')
const mongoose = require('mongoose')

// get all exercises
const getExercises = async (req, res) => {
    const exercises = await Exercise.find({}).sort({createdAt: 1})
    res.status(200).json(exercises)
}

const getExercise = async (req, res) => {
    const { id } = req.params

    const exercise = await Exercise.findById(id)

    res.status(200).json(exercise)
}

const updateExercise = (req, res) => {
    res.json({mssg: 'update one'})
}

const deleteExercise = (req, res) => {
    res.json({mssg: 'delete one'})
}

const createExercise = async (req, res) => {
    const { title, reps } = req.body

    try {
        const exercise = await Exercise.create({title, reps, done: false, accuracy: null})
        res.status(200).json(exercise)
    } catch (error) {
        res.status(400).json({error: error.message})
    }
}

module.exports = {
    getExercises,
    getExercise,
    updateExercise,
    deleteExercise,
    createExercise
}