import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const FormChecking = () => {
    const [file, setFile] = useState(null);
    const [squatType, setSquatType] = useState('side'); // Default to side squat
    const navigate = useNavigate();

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSquatTypeChange = (event) => {
        setSquatType(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            alert('Please select a file.');
            return;
        }

        // Create a FormData object to append the file
        const formData = new FormData();
        formData.append('file', file);
        formData.append('squat_type', squatType);
        
        // try {
        //     // Send a POST request to your Flask backend
        //     const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        //         headers: {
        //             'Content-Type': 'multipart/form-data'
        //         }
        //     });
        //     console.log('got this response' + response)
        //     // Handle response
        //     const videoPath = response.data.output_path;
        //     console.log(videoPath)
        //     navigate('/success', { state: { videoPath } });
        // } catch (error) {
        //     // Handle error
        //     console.error('Got an Error uploading file:', error);
        // }
        try {
            // Send a POST request to your Flask backend
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                responseType: 'blob' // Set the response type to blob
            });
    
            // Create a blob object from the response data
            const blob = new Blob([response.data], { type: 'video/mp4' });
    
            // Create a temporary URL for the blob
            const url = window.URL.createObjectURL(blob);
    
            // Create a link element
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'output.mp4');
    
            // Append the link to the body
            document.body.appendChild(link);
    
            // Trigger the download
            link.click();
    
            // Remove the link from the body
            document.body.removeChild(link);
            navigate('/success');
        } catch (error) {
            // Handle error
            console.error('Got an Error uploading file:', error);
        }
    
    };

    return (
        <div className='formChecking'>
            <div className='mainPanel'>
                <h1>Check your squat form here</h1>
            </div>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Select Video:</label>
                    <input type="file" accept="video/*" onChange={handleFileChange} />
                </div>
                <div>
                    <label>Select Squat Type:</label>
                    <select value={squatType} onChange={handleSquatTypeChange}>
                        <option value="side">Side Squat</option>
                        <option value="front">Front Squat</option>
                    </select>
                </div>
                <button type="submit">Upload Video</button>
            </form>
        </div>
    );
};

export default FormChecking;
