import React, { Component } from 'react';
import logoStatic from './skull.png';
import Suggestions from '../SearchPage/Components/Suggestions/Suggestion'

import './LandingPage.css';

const API_SERVER_CACHE_ENDPOINT = "http://localhost:8010/searchcache?q="

export default class LandingPage extends Component {

  constructor(props) {
      super(props);
      this.state = {
        query: "",
        suggestions: []
      }
  }

  componentDidMount() {
    document.getElementById("search-box").focus();    
  }

  handleSearch = () => {
    if (this.state.query.length < 1)
      return
    const query = this.state.query
    this.props.history.push({
      pathname: '/search',
      search: '?q=' + query,
      state: {'query' : query}
    });
  }

  changeQuery = (val) => {
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

  render() {
    let suggestions = undefined
    if (this.state.suggestions) {
      suggestions = this.state.suggestions.map((suggestion, index) => {
          return (
              <li className="suggestion_one" key={suggestion} onClick={()=>this.changeQuery(suggestion)}> {suggestion} </li>
          )
      })
  }

    return (
        <div className="App">
          <header className="App-header">
          <div className="logo-container">
            {/* <img src={logoSpin} className="App-logo-spin" alt="logoSpin" /> */}
            <img src={logoStatic} className="App-logo-static" alt="logoStatic" />
          </div>
            </header>
          <div className="search-bar">
              <input id="search-box" onKeyPress={(e)=>{if (e.key === 'Enter') this.handleSearch()}} onChange={(e)=>{this.changeQuery(e.target.value)}} placeholder="Search the dark net" value={this.state.query}/>
          </div>
          <Suggestions className="suggestions_one" suggestions={suggestions} />
          <div className="buttons">
              <button id="search-btn" className="btnsearch" onClick={() => this.handleSearch()}> Search </button>
              <button id="iamnotfeelinglucky" className="btnsearch" onClick={()=>{window.location = "https://www.google.com/"}}> I'm not feeling lucky </button> 
          </div>
        </div>
    );
  }
}
