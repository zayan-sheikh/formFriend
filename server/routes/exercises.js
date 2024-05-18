const express = require('express')
const Exercise = require('../models/exerciseModel')

const {
    getExercises,
    getExercise,
    createExercise,
    updateExercise,
    deleteExercise
} = require('../controllers/exerciseController')

const router = express.Router()

// get all exercises
router.get('/', getExercises)

// get one exercise
router.get('/:id', getExercise)

// update an exercise
router.patch('/:id', updateExercise)

// delete an exercise
router.delete('/:id', deleteExercise)

// create an exercise
router.post('/', createExercise)

module.exports = router