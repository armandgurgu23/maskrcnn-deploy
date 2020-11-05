import React from 'react';
import axios from 'axios';
import './predictionFetcher.css';

class PredictionFetcher extends React.Component {
    constructor(props) {
        super(props);
        this.state = null;
        //TO-DO: move these to a JSON configuration file
        //later.
        this.modelBackendIP = 'http://localhost:6969';
        this.serverPath = '/uploadImage';
    }

    renderPredictionButton = () => {
        console.log('Props passed to Prediction Fetcher: ', this.props);
        return <form onSubmit={this.handleFormSubmit}>
            <button id='predictionButton' type='submit'> Run Object Detector </button>
        </form> 
    }

    packageImageAsFormData = (imageFile) => {
        //To send an image to a backend server
        //you must add the File object associated
        //to the image in a form element.
        const imageFormWrapper = new FormData();
        //imageFile represents the keyname expected
        //by the backend server.
        imageFormWrapper.append('imageFile', imageFile);
        const payloadConfig = {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
        const payloadInfo = {form: imageFormWrapper, config: payloadConfig}
        return payloadInfo;
    }

    sendImageToServer = async (imageForm, backendURL, requestHeader) => {
        let response = await axios.post(backendURL, imageForm, requestHeader);
        console.log('This is the response I got back from backend: ', response);
    }

    handleFormSubmit = (event) => {
        console.log('Detected a form submit! Event = ', event);
        //We are disabling the form element's default submission behaviour
        //and allowing axios to handle the communication for simplicity.
        event.preventDefault();
        let backendURL = this.getBackendURL(this.modelBackendIP, this.serverPath);
        let payloadInfo = this.packageImageAsFormData(this.props.imageFile);
        this.sendImageToServer(payloadInfo.form, backendURL, payloadInfo.config);
    }

    getBackendURL = (backendIP, serverPath) => {
        let backendURL = backendIP.concat(serverPath);
        return backendURL;
    }

    componentDidUpdate = (prevProp, prevState) => {
        console.log('Previous prop = ', prevProp);
        console.log('Previous state = ', prevState);
        console.log('Curr State = ', this.state);
        console.log('Curr prop = ', this.props);
    }


    render() {
        return this.renderPredictionButton();
    }
}

export default PredictionFetcher;