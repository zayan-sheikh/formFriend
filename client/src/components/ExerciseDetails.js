const ExerciseDetails = (exercise) => {



    return (
        <div className="details-panel">
            <h1>{exercise.title} - {exercise.reps} Reps</h1>
        </div>
    )
}
export default ExerciseDetails