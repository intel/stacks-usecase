import './App.css';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import {  withStyles } from '@material-ui/core';

import styles from './App.styles'

import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import EffectsController from '../pages/effects-controller/EffectsController';
import Sidebar from '../components/sidebar/Sidebar';

function App({ classes }) {
  return (
    <div className="App">
      <AppBar className={classes.appBar}>
        <Toolbar>
          <Typography component="h1" variant="h6" color="inherit" noWrap>
            Intelligent Collaboration
          </Typography>
        </Toolbar>
      </AppBar>
      <Router>
        <Sidebar/>
        <div className={classes.mainContent}>
          <Switch>
            <Route exact path="/">
              <EffectsController />
            </Route>
          </Switch>
        </div>
      </Router>

    </div>
  );

}

export default withStyles(styles)(App);
