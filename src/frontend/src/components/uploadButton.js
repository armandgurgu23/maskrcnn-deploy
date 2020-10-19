import React from 'react';
import './uploadButton.css';
class UploadButton extends React.Component {
    render() {
        return (
        <div id='Upload Image Container'>
            <label for="upload"> Upload an image </label>
            <input id="upload" type="file" accept='image/png,image/jpeg,image/jpg'></input>
        </div>);
    }
}

export default UploadButton;
