import React, { Component } from 'react';
import logoStatic from './skull.png';

import './LandingPage.css';

export default class LandingPage extends Component {

  constructor(props) {
      super(props);
      this.state = {
        query: ""
      }
  }

  handleSearch = () => {
    const query = this.state.query;
    this.props.history.push({
      pathname: '/search',
      search: '?q=' + query,
      state: {'query' : query}
    });
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

  render() {
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
          <div className="buttons">
              <button id="search-btn" className="btnsearch" onClick={() => this.handleSearch()}> Search </button>
              <button id="iamnotfeelinglucky" className="btnsearch" onClick={()=>{window.location = "https://www.google.com/"}}> I'm not feeling lucky </button> 
          </div>
        </div>
    );
  }

  componentDidMount() {
    document.getElementById("search-box").focus();    
  }
}
