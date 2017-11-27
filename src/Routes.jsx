import React from 'react';
import {Route, Switch} from 'react-router-dom';

import LandingPage from './LandingPage/LandingPage';
import SearchPage from './SearchPage/SearchPage';
import F04Page from './404Page/404Page';

export default () => {
    return (
    <Switch>
        <Route exact path="/" render={props => <LandingPage {...props} /> } />

        <Route path="/search" render={props => <SearchPage {...props} /> } />

        <Route render={props => <F04Page {...props} /> } />

    </Switch>
    );
}