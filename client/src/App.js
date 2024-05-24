import { BrowserRouter, Routes, Route } from 'react-router-dom';

// pages & components
import Home from './pages/Home';
import Navbar from './components/Navbar';
import FormChecking from './pages/FormChecking';
import Success from './pages/Success';

import cors from 'cors';

const corsOptions = {
   origin: 'http://localhost:3000',
   methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
   credentials: true,
   optionsSuccessStatus: 204,
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar />
        <div className='pages'>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/formChecking' element={<FormChecking />} />
            <Route path='/success' element={<Success />} />
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}
// App.use(cors(corsOptions)); 
export default App;
