import { useState } from 'react'
import { useEffect } from 'react'
import Spline from '@splinetool/react-spline';
// components

const Home = () => {

return (
    <div className='home'>
        <div className='mainPanel'>
            <h1>Your Goals</h1>
        </div>

        <div className='animPanel'>
            <Spline scene="https://prod.spline.design/VhYGzYeJJIhpmxM3/scene.splinecode" />
        </div>
    </div>
)}

export default Home