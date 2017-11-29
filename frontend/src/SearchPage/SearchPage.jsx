import React from 'react';

import './SearchPage.css';

export default class SearchPage extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            query: ""
        }
    }

    componentDidMount() {
        if (this.props.location.state === undefined){
            const url = window.location.href;
            const query = url.split("search?q=")[1];
            this.setState(() => {
                return {query: query}
            });
        } else {
            this.setState(() => {
                return {query: this.props.location.state.query}
            });
        }  
        this.search();
    }
    
    search = () => {
        const query = this.state.query;
        fetch('http://0.0.0.0:8010/' + query)
        .then((response) => response.json)
        .then((responsejson) => this.parseResults(responsejson))
        .catch((error) => console.error(error))
    }

    parseResults = () => {
        
    }
    
    render() {
        return (<div className="whitetext" >
            {this.state.query}</div>
        );
    }
}