const ExerciseListing = ({ exercise }) => {
    return (
        <div className="exercise-listing">
            <h1>{exercise.title}</h1>
            <div id="check" className="material-symbols-outlined">
                {(exercise.done) ? "Check" : ""}
            </div>
        </div>
    )
}
export default ExerciseListing