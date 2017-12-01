import React from 'react';
import Loader from './Components/PacManLoader';

import './SearchPage.css';

const API_SERVER = "http://localhost:8010/";

export default class SearchPage extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            query: "",
            searchResults: [],
            searching: true,
            error: false,
            overlayMsg: ""
        }
    }

    componentDidMount() {
        if (this.props.location.state === undefined){
            const url = window.location.href;
            const query = url.split("search?q=")[1];
            this.setState(() => {
                return {query: query}
            }, this.search(query));
        } else {
            this.setState(() => {
                return {query: this.props.location.state.query}
            }, this.search(this.props.location.state.query));
        }  
    }
    
    search = (query) => {
        fetch(API_SERVER + query)
        .catch(()=>{
            this.setState(()=>{return {error: true, overlayMsg: "Sorry, we couldn't contact the backend server. Make sure your computer is connected to the Internet and try again."}});
        })
        .then((response) => response.json())
        .catch((e) => {this.parseResults("Result is not json")})
        .then((responsejson) => this.parseResults(responsejson))
        .catch((error) => console.error(error));
    }

    parseResults = (responsejson) => {
        if (responsejson.head === 'success') {
            this.setState(()=>{return {searching:false}});
        }
    }
    
    render() {
        if (this.state.searching && !this.state.error) {
            return <Loader className="loader" loading={true} size={16} margin={-8} />;
        }

        if (this.state.error) {
            return <div className="whitetext">{this.state.overlayMsg}</div>;
        }

        return (
        <div className="whitetext" >

        </div>
        );
    }
}