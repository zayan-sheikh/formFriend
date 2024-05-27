import { useLocation } from 'react-router-dom';

const RepCountingSuccess = () => {
    const location = useLocation();
    const counter = location.state && location.state.counter;

    return (
        <div>
            <h1>Upload Successful!</h1>
            <h1>{counter}</h1>
           
            {/* Other success page content */}
        </div>
    );
};

export default RepCountingSuccess;
