import { withStyles } from '@material-ui/core'
import React from 'react'

import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

//import PhotoCameraIcon from '@material-ui/icons/PhotoCamera';
import SettingsRemoteIcon from '@material-ui/icons/SettingsRemote';

import {Link} from "react-router-dom";
import styles from './Sidebar.styles'

const Sidebar = ({classes}) => {
    return (
        <div className={classes.sideMenu}>
        <List className={classes.navList}>
            <ListItem divider component={Link} to={'/'} button key='effects'>
              <ListItemIcon className={classes.navListIcon}> <SettingsRemoteIcon /> </ListItemIcon>
              <ListItemText className={classes.whiteText} primary="Effects Controller" />
            </ListItem>
            <Divider className={classes.whiteBg}/>
	    {/*
            <ListItem divider component={Link} to={'/camera-preview'} button key='fullpreview'>
              <ListItemIcon className={classes.navListIcon}> <PhotoCameraIcon/> </ListItemIcon>
              <ListItemText className={classes.whiteText} primary="Full Camera Preview" />
            </ListItem>
            <Divider className={classes.whiteBg}>
	     */}
        </List>
      </div>
    )
}

export default withStyles(styles)(Sidebar);
