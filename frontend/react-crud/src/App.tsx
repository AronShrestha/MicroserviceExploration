import React from 'react';

import './App.css';
import { BrowserRouter,Routes,Route} from 'react-router-dom';
import Products from './admin/Products'

function App() {
  return (
    
    <div className="App">
      <h1>Hello</h1>
    <BrowserRouter>
    <Routes>
    <Route path="/admin/products" element={<Products/>}>Router</Route>
    </Routes>
     
    </BrowserRouter>
    </div>
  );
}

export default App;
