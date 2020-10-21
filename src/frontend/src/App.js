import React from 'react';
import './App.css';
import ImageUpload from './components/imageUpload'

//App is a functional component that represents the entire application code.

function App() {
  return (
    <div className="App">
      <h1> Welcome to the Mask-RCNN demo!!</h1>
      <ImageUpload></ImageUpload>
    </div>
  );
}

export default App;
