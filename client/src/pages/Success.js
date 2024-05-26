import React from 'react';
import { useLocation } from 'react-router-dom';

const Success = () => {
    const location = useLocation();
    const videoPath = location.state?.videoPath;

    return (
        <div className="success">
            <h1>The processed video with your personalised feedback has been downloaded</h1>
        </div>
    );
};

export default Success;
