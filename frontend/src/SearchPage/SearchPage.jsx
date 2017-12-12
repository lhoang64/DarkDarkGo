import React from 'react'
import Loader from './Components/PacManLoader'
import Suggestions from './Components/Suggestions/Suggestion'
import NavigationButton from './Components/NavigationButton/NavigationButton'
import logoStatic from './Components/skull_only.png'
// import logoStatic from '../LandingPage/skull.png'
import {Link} from 'react-router-dom'
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
            totalPossibleResults: 0,
            timeTaken: 0,
            error: ""
        }
    }

    componentDidMount() {
        if (this.props.location.state === undefined){
            const url = window.location.href
            let query = queryParser.getQueryString('q',url)
            query = query.replace(/[|&;$@"<>()+,]/g, " ").replace(/%20/g,' ')
            let offset = parseInt(queryParser.getQueryString('offset',url), 10)
            if (isNaN(offset))
                offset = 0
            this.setState(() => {
                return {query: query.toLowerCase(), searchOffset: offset}
            }, this.search)
        } else {
            this.setState(() => {
                return {query: this.props.location.state.query.toLowerCase()}
            }, this.search)
        }
        const el = document.getElementById("search-box")
        if (el) el.focus()        
    }
    
    search = () => {
        if (this.state.query.length < 1)
            return
        fetch(API_SERVER_QUERY_ENDPOINT + this.state.query + "&offset=" + this.state.searchOffset)
            .catch(() => {
                this.setState({ error: "Sorry, we couldn't contact the backend server. Either your computer is not connected to the Internet or our backend server is offline." })
            })
            .then((response) => response.json())
            .catch(() => { if (this.state.error.length === 0) this.setState({ error: "Sorry, our backend server has gone berserk. Instead of returning json, they did something else. Email them at sashankaryal@bennington.edu." }) })
            .then((responsejson) => { if (this.state.error.length === 0) this.parseResult(responsejson) })
            .catch((error) => console.error(error))
    }


    parseResult = (responsejson) => {
        if (responsejson.head === 'success') {
            this.setState((prevState, prevProps) => {
                console.log(responsejson)
                return {
                    totalPossibleResults : responsejson.totalResults,
                    searchResults: responsejson.message,
                    timeTaken: responsejson.timetaken,
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
              return {query: val.toLowerCase()}
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
        if (this.state.query.length < 1)
            return
        this.props.history.push('/search?q='+this.state.query)
        this.search()
    }

    changeOffsetBy = (offset) => {
        this.setState((prevState) => {
            return {searchOffset: prevState.searchOffset + offset}},
            () => {
                this.props.history.push('/search?q='+this.state.query + '&offset=' + this.state.searchOffset)
                this.search()
            }
        )
    }

    render() {
        const searchResultsHtml = this.state.searchResults.map((result, index) => {
            return (
                <div key={result.rank} className={"resultblock_" + index + " results"}>
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
                    <div className="logoandbar">
                        <Link to="/">
                            <img src={logoStatic} className="searchBarLogo" alt="logoStatic" />
                        </Link>
                        <div className="search-bar">
                            <input id="search-box" onKeyPress={(e)=>{if (e.key === 'Enter') this.handleSearch()}} onChange={(e)=>{this.changeQuery(e.target.value)}} placeholder="Search the dark net" value={this.state.query}/>
                            <Suggestions className="suggestions" suggestions={suggestions} />
                        </div>
                    </div>


                    <div className="whitetext searchresultsnum">
                        {this.state.totalPossibleResults} results found in {parseFloat(this.state.timeTaken, 10) / 1000.0} seconds
                    </div>

                    <div className="searchresults">
                        {searchResultsHtml}
                    </div>
                    <NavigationButton changeOffsetBy={this.changeOffsetBy} offset={this.state.searchOffset} />
             </div>
        }

        return <Loader className="loader center" loading={true} size={16} margin={-8} />
    }
}
