const Exercise = require('../models/exerciseModel')
const mongoose = require('mongoose')
const ERR_NOT_FND = { error: "Exercise not found." }

// get all exercises
const getExercises = async (req, res) => {
    const exercises = await Exercise.find({}).sort({createdAt: 1})
    res.status(200).json(exercises)
}

// get one exercise by id
const getExercise = async (req, res) => {
    const { id } = req.params

    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(404).json(ERR_NOT_FND)
    }

    const exercise = await Exercise.findById(id)

    if (!exercise) {
        return res.status(404).json(ERR_NOT_FND)
    }

    res.status(200).json(exercise)
}

// update one exercise by id
const updateExercise = async (req, res) => {
    const {id} = req.params

    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(404).json(ERR_NOT_FND)
    }

    const exercise = await Exercise.findByIdAndUpdate(id, {...req.body})

    if (!exercise) {
        return res.status(404).json(ERR_NOT_FND)
    }
    
    res.status(200).json(exercise)

}

// delete one exercise by id
const deleteExercise = async (req, res) => {
    const { id } = req.params

    if (!mongoose.Types.ObjectId.isValid(id)) {
        return res.status(404).json(ERR_NOT_FND)
    }

    const exercise = await Exercise.findByIdAndDelete(id)

    if (!exercise) {
        return res.status(404).json(ERR_NOT_FND)
    }

    res.status(200).json(exercise)
}

// create new exercise
const createExercise = async (req, res) => {
    const { title, reps } = req.body

    const emptyFields = []

    if (!title) {
        emptyFields.push('title')
    }

    if (!reps) {
        emptyFields.push('reps')
    }

    if (emptyFields.length > 0) {
        return res.status(400).json({error: "Please fill in all fields."})
    }

    try {
        const exercise = await Exercise.create({title, reps, done: false, accuracy: null, repCount: null})
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