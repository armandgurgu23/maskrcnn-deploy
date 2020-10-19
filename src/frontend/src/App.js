import React from 'react';
import './App.css';
import UploadButton from './components/uploadButton'

//App is a functional component that represents the entire application code.

function App() {
  return (
    <div className="App">
      <h1> Welcome to the Mask-RCNN demo!!</h1>
      <UploadButton> Press button below to add an image for Mask-RCNN </UploadButton>
    </div>
  );
}

export default App;
