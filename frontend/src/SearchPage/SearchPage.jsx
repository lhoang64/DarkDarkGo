import React from 'react'
import Loader from './Components/PacManLoader'
import Suggestions from './Components/Suggestions/Suggestion'
import NavigationButton from './Components/NavigationButton/NavigationButton'

import './SearchPage.css'

let queryParser = require('./utils/utils.js')

const API_SERVER_QUERY_ENDPOINT = "http://localhost:8010/search?q=";
const API_SERVER_CACHE_ENDPOINT = "http://localhost:8010/searchcache?q="

export default class SearchPage extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            query: "",
            searchResults: [],
            searchOffset : 0,
            searching: true,
            suggestions: [],
            error: ""
        }
    }

    componentDidMount() {
        if (this.props.location.state === undefined){
            const url = window.location.href
            let query = queryParser.getQueryString('q',url)
            query = query.replace(/[|&;$@"<>()+,]/g, " ").replace(/%20/g,' ')
            const offset = queryParser.getQueryString('offset',url)
            this.setState(() => {
                return {query: query, searchOffset: offset}
            }, this.search(query, offset));
        } else {
            this.setState(() => {
                return {query: this.props.location.state.query}
            }, this.search(this.props.location.state.query));
        }
        const el = document.getElementById("search-box")
        if (el) el.focus()        
    }
    
    search = (query, offset) => {
        fetch(API_SERVER_QUERY_ENDPOINT + query + "&offset=" + offset)
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
        if (val === this.state.query)
            return
        this.setState(
            () => {
              return {query: val}
            }, () => {
              //Prefetch and display suggestions
              if (val.length > 0) {
                fetch(API_SERVER_CACHE_ENDPOINT+this.state.query)
                .then((response) => response.json())
                .then((responsejson) => {
                    this.setState({suggestions: responsejson})
                })
            } else {
                this.setState({suggestions: []})
            }
            }
          );
    }

    handleSearch = () => {
        this.props.history.push('/search?q='+this.state.query)
        this.search(this.state.query)
    }

    changeOffsetBy = (offset) => {
        this.setState((prevState) => {
            return {searchOffset: prevState.searchOffset + offset}},
            () => {
                this.props.history.push('/search?q='+this.state.query + '&offset=' + this.state.searchOffset)
                this.search(this.state.query, this.state.offset)
            }
        )
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
            )
        })

        let suggestions = undefined

        if (this.state.suggestions) {
            suggestions = this.state.suggestions.map((suggestion, index) => {
                return (
                    <li className="suggestion" key={suggestion} onClick={()=>this.changeQuery(suggestion)}> {suggestion} </li>
                )
            })
        }

        if (this.state.error.length > 0)
            return <div className="whitetext center centertext">{this.state.error}</div>;
        
        if (!this.state.searching) {
            return <div id="searchpage">
                    <div className="search-bar">
                        <input id="search-box" onKeyPress={(e)=>{if (e.key === 'Enter') this.handleSearch()}} onChange={(e)=>{this.changeQuery(e.target.value)}} placeholder="Search the dark net" value={this.state.query}/>
                    </div>

                    <Suggestions className="suggestions_one" suggestions={suggestions} />

                    <div className="searchresults">
                        {searchResultsHtml}
                    </div>
                    <NavigationButton changeOffsetBy={this.changeOffsetBy} offset={this.state.searchOffset} />
             </div>
        }

        return <Loader className="loader center" loading={true} size={16} margin={-8} />
    }
}