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
                {exercises && exercises.map(exercise => (
                    <ExerciseListing key={exercise._id} exercise={exercise}/>
                ))}
            </div>

            <div className='animPanel'>
                <Spline scene="https://prod.spline.design/VhYGzYeJJIhpmxM3/scene.splinecode" />
            </div>
        </div>
    )}

export default Home