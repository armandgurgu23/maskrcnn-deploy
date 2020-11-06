import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

//Armand: This is the main script! ReactDOM.render is responsible
//for rendering the entire front-end. In this case it renders
//the App functional component.

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

