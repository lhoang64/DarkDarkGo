import React from 'react'
import Loader from './Components/PacManLoader'
import {Link} from 'react-router-dom'
import './SearchPage.css'

const API_SERVER_QUERY_ENDPOINT = "http://localhost:8010/search?q=";

export default class SearchPage extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            query: "",
            searchResults: [],
            searching: true,
            error: ""
        }
    }

    componentDidMount() {
        if (this.props.location.state === undefined){
            const url = window.location.href;
            const query = url.split("search?q=")[1].replace(/[|&;$@"<>()+,]/g, " ").replace(/%20/g,' ');
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
        fetch(API_SERVER_QUERY_ENDPOINT + query)
        .catch(()=>{
            this.setState({error: "Sorry, we couldn't contact the backend server. Either your computer is not connected to the Internet or our backend server is offline."})
        })
        .then((response) => response.json())
        .catch(() => {if (this.state.error.length === 0) this.setState({error: "Sorry, our backend server has gone berserk. Instead of returning json, they did something else. Email them at sashankaryal@bennington.edu."})})
        .then((responsejson) => this.parseResult(responsejson))
        .catch((error) => console.error(error));
    }

    parseResult = (responsejson) => {
        if (responsejson.head === 'success') {
            this.setState((prevState, prevProps) => {
                return {
                    searchResults: responsejson.message,
                    searching: false
                }
            })
        } else {
            this.setState({searching:false})
            this.setState({error: responsejson.message})
        }
    }
    
    changeQuery = (val) => {
        this.setState(
            () => {
              return {query: val}
            }, () => {
              //Prefetch and display suggestions
            }
          );
    }

    handleSearch = () => {
        this.search(this.state.query)
    }

    render() {
        const searchResultsHtml = this.state.searchResults.map((result, index) => {
            return (
                <div key={result.href} className={"resultblock_" + index + " results"}>
                    <div className="resulttitle">
                        <a className="searchlink" href={result.href}>
                            {result.title}
                        </a>
                    </div>
                    <div className="resultdesc">
                        {result.desc}
                    </div>
                </div>
            );
        })

        if (this.state.error.length > 0)
            return <div className="whitetext center centertext">{this.state.error}</div>;
        
        if (!this.state.searching) {
            return <div id="searchpage">
                      <div className="search-bar">
                            <input id="search-box" onKeyPress={(e)=>{if (e.key === 'Enter') this.handleSearch()}} onChange={(e)=>{this.changeQuery(e.target.value)}} placeholder="Search the dark net" value={this.state.query}/>
                    </div>
                <div className="searchresults">
                    {searchResultsHtml}
                </div>
            </div>
        }

        return <Loader className="loader center" loading={true} size={16} margin={-8} />
    }
}