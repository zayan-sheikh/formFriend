const mongoose = require('mongoose')

const Schema = mongoose.Schema

const exerciseSchema = new Schema({
    title: {
        type: String,
        required: true
    },
    reps: {
        type: Number,
        required: true
    },
    done: {
        type: Boolean,
        required: true
    },
    accuracy: {
        type: Number,
        required: true
    }
}, { timestamps: true })

module.exports = mongoose.model('Exercise', exerciseSchema)