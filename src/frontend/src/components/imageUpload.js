import React from 'react';
import './imageUpload.css';
import ImageRenderer from './imageRenderer';
class ImageUpload extends React.Component {

    constructor(props) {
        super(props);
        this.state = {uploadPath:null};
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

    handleRenderImageContainer = (fileObject) => {
        if (fileObject === null) {
            return <div id='Render Image Container'></div>;
        } else {
            return <div id='Render Image Container'>
                        <ImageRenderer imageFile={fileObject}></ImageRenderer>
                    </div>;
        }
    }

    //Note: add the multiple attribute inside the uploadInput container to allow for
    //multiple file submissions!
    //<ImageRenderer imageFile={FileObject}></ImageRenderer>
    render() {
        let renderImageContainer = this.handleRenderImageContainer(this.state.uploadPath);
        return (
        <div id='Image Handler Container'>
            <div id='Upload Image Container'>
                <input id="uploadInput" type="file" accept='image/png,image/jpeg,image/jpg' onChange={this.handleInputChange}></input>
                <button id="uploadButton" onClick={this.handleButtonClick}>Upload Image</button>
            </div>
            {renderImageContainer}
        </div>
        );
    }
}

export default ImageUpload;
