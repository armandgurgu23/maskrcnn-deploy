import React from 'react';
import './predictionFetcher.css';

class PredictionFetcher extends React.Component {
    constructor(props) {
        super(props);
        this.state = null;
    }

    renderPredictionButton = () => {
        console.log('Props passed to Prediction Fetcher: ', this.props);
        return <button id='predictionButton'>Run Object Detector</button>;
    }

    render() {
        return this.renderPredictionButton();
    }
}

export default PredictionFetcher;