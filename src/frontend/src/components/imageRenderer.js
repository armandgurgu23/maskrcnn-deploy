import React from 'react';
import PredictionFetcher from './predictionFetcher';
class ImageRenderer extends React.Component {
    constructor(props) {
        super(props);
        this.state = null;
        this.imageReader = new FileReader();
    }

    handleImageLoading = (event) => {
        console.log('handleImageLoading: event --> ', event)
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


    handleImgElementRender = (prevState) => {
        if (this.state !== null && this.state.hasOwnProperty('imageContents')) {
            console.log('Will render PredictionFetcher!!!!')
            return <div>
                        <img height="600" width="600" src={this.state.imageContents}></img>
                        <PredictionFetcher imageFile={this.props.imageFile} imageRenderCallback={this.handleImageReading}/>
                    </div>
                
        }
    }

    componentDidUpdate = (prevProp, prevState) => {
        // This method is trigerred by an update which 
        // can be caused by changes to props or state.
        // It runs after render().
        if (this.props.imageFile.name !== prevProp.imageFile.name) {
            this.handleImageReading(this.props.imageFile);
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