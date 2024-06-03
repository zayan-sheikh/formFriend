import { useState } from 'react'
import { useEffect } from 'react'
import Spline from '@splinetool/react-spline';
import ExerciseListing from '../components/ExerciseListing';
import ExerciseDetails from '../components/ExerciseDetails';
// components

const Home = () => {
    const [exercises, setExercises] = useState(null)
    const [selected, setSelected] = useState(null)

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

    const handleClick = () => {
        if (selected) {
            setSelected(null)
        } else {
            setSelected(null)
        }
    }


    return (
        <div className='home'>
            <div className='listing-container'>
                
                <div className='mainPanel'>
                    <h1 className='listingHeader'>Your Goals</h1>
                    {exercises && exercises.map(exercise => (
                        <ExerciseListing key={exercise._id} exercise={exercise} onClick={handleClick}/>
                    ))}
                </div>
            </div>
            { {selected} ?
                <ExerciseDetails key={selected._id} exercise={selected}/> : ""
            }
            <div className='animPanel'>
                <Spline scene="https://prod.spline.design/90FsM3-eeYuQEEyR/scene.splinecode" />
                <h2>Keep working on today's goals!</h2>
            </div>
        </div>
    )}

export default Home