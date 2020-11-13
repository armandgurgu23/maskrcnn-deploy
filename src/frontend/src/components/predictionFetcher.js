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
        this.detectorPath = '/detector';
        this.segmentorPath = '/segmentor';
    }

    renderPredictionButtons = () => {
        return <div id='Prediction Fetchers'> 
                    <form onSubmit={this.handleDetectorFormSubmit}>
                        <button id='predictionButtonDetector' type='submit'> Run Object Detector </button>
                    </form> 
                    <form onSubmit={this.handleSegmentorFormSubmit}>
                        <button id='predictionButtonSegmentor' type='submit'> Run Object Segmentor </button>
                    </form>
            </div>;
        }

    packageImageAsFormData = (imageFile) => {
        //To send an image to a backend server
        //you must add the File object associated
        //to the image in a form element.
        const imageFormWrapper = new FormData();
        //imageFile represents the keyname expected
        //by the backend server.
        imageFormWrapper.append('imageFile', imageFile);
        // If request is interpreted as blob, it can
        // be passed in directly to the callback
        // of the image renderer component.
        const payloadConfig = {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            responseType: 'blob'
        }
        const payloadInfo = {form: imageFormWrapper, config: payloadConfig}
        return payloadInfo;
    }

    sendImageToServer = async (imageForm, backendURL, requestHeader) => {
        let response = await axios.post(backendURL, imageForm, requestHeader);
        console.log('Axios response: ', response);
        this.setState({predictionsImage:response.data, predictionsName:this.props.imageFile.name})
    }

    handleDetectorFormSubmit = (event) => {
        console.log('Detected a detector form submit! Event = ', event);
        //We are disabling the form element's default submission behaviour
        //and allowing axios to handle the communication for simplicity.
        event.preventDefault();
        let backendURL = this.getBackendURL(this.modelBackendIP, this.detectorPath);
        let payloadInfo = this.packageImageAsFormData(this.props.imageFile);
        this.sendImageToServer(payloadInfo.form, backendURL, payloadInfo.config);
    }

    handleSegmentorFormSubmit = (event) => {
        console.log('Detected a segmentor form submit! Event = ', event);
        //We are disabling the form element's default submission behaviour
        //and allowing axios to handle the communication for simplicity.
        event.preventDefault();
        let backendURL = this.getBackendURL(this.modelBackendIP, this.segmentorPath);
        let payloadInfo = this.packageImageAsFormData(this.props.imageFile);
        this.sendImageToServer(payloadInfo.form, backendURL, payloadInfo.config);
    }

    getBackendURL = (backendIP, serverPath) => {
        let backendURL = backendIP.concat(serverPath);
        return backendURL;
    }

    componentDidUpdate = (prevProp, prevState) => {
        // This method is trigerred by an update which 
        // can be caused by changes to props or state.
        // It runs after render().
        console.log('Prediction Fetcher component did update keeps RUN!')
        if (this.state) {
            if (!prevState){
                this.props.imageRenderCallback(this.state.predictionsImage);
            }
            else {
                if (this.state.predictionsName !== prevState.predictionsName) {
                    this.props.imageRenderCallback(this.state.predictionsImage);
                }
            }
        }
    }

    render() {
        return this.renderPredictionButtons();
    }
}

export default PredictionFetcher;