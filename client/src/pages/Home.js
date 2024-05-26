import { useState } from 'react'
import { useEffect } from 'react'
import Spline from '@splinetool/react-spline';
import ExerciseListing from '../components/ExerciseListing';
// components

const Home = () => {
    const [exercises, setExercises] = useState(null)

    useEffect( () => {
        const fetchExercises = async () => {
            const response = await fetch('http://localhost:4000/api/exercises/')
            const json = await response.json()

            if (response.ok) {
                setExercises(json)
            }
        }

        fetchExercises()
    }, [])


    return (
        <div className='home'>
            <div className='mainPanel'>
                <h1>Your Goals</h1>
                {exercises && exercises.map(exercise => (
                    <ExerciseListing key={exercise._id} exercise={exercise}/>
                ))}
            </div>

            <div className='animPanel'>
                <Spline scene="https://prod.spline.design/90FsM3-eeYuQEEyR/scene.splinecode" />
                <h2>Keep working on today's goals!</h2>
            </div>
        </div>
    )}

export default Home