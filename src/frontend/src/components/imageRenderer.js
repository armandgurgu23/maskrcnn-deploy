import React from 'react';
import PredictionFetcher from './predictionFetcher';
class ImageRenderer extends React.Component {
    constructor(props) {
        super(props);
        this.state = null;
        this.imageReader = new FileReader();
    }

    handleImageLoading = (event) => {
        this.setState({imageContents:event.target.result})
    }

    handleImageReading = (file) => {
        //Used to read in an image as base 64 encoded string.
        this.imageReader.onload = this.handleImageLoading;
        this.imageReader.readAsDataURL(file);
    }

    handleImageReadingFromFile = () => {
        if (this.state === null && this.imageReader.readyState === 0){
            this.handleImageReading(this.props.imageFile);
        }
        return;
    }

    //Need to fix if statement to allow for other uploaded image renderings.

    handleImgElementRender = () => {
        if (this.state !== null && this.state.hasOwnProperty('imageContents')) {
            return <div>
                        <img height="600" width="600" src={this.state.imageContents}></img>
                        <PredictionFetcher imageFile={this.props.imageFile}/>
                    </div>
                
        }
    }

    render() {
        this.handleImageReadingFromFile();
        return (
            <div id='Image Display Container'>
                {this.handleImgElementRender()}
            </div>
        );
    }
}

export default ImageRenderer;