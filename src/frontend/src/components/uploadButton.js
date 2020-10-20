import React from 'react';
import './uploadButton.css';
class UploadButton extends React.Component {

    constructor(props) {
        super(props);
        this.state = {uploadPath:""};
    }


    handleInputChange = (event) => {
        let fileUploaded = event.target.files;
        this.setState({uploadPath:fileUploaded[0]});
        console.log('this.state after setState = ', this.state)
    }


    handleButtonClick = () => {
        console.log('Inside handleButtonClick! state = ', this.state);
        let inputElem = document.getElementById("uploadInput");
        inputElem.click();
    }

    //Note: add the multiple attribute inside the uploadInput container to allow for
    //multiple file submissions!
    render() {
        return (
        <div id='Upload Image Container'>
            <input id="uploadInput" type="file" accept='image/png,image/jpeg,image/jpg' onChange={this.handleInputChange}></input>
            <button id="uploadButton" onClick={this.handleButtonClick}>Upload Image</button>
        </div>);
    }
}

export default UploadButton;
