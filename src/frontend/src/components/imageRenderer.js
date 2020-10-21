import React from 'react';
class ImageRenderer extends React.Component {
    constructor(props) {
        super(props);
        this.state = null;
    }

    render() {
        console.log('Rendering component: ImageRenderer! Props = ', this.props);
        return (
            <div id='Image Display Container'>
                <img src={this.props.imageFile.name}></img>
            </div>
        );
    }
}

export default ImageRenderer;