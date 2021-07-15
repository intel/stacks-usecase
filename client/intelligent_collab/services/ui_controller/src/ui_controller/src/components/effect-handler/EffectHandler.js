import React, { useState } from 'react'
import { withStyles } from '@material-ui/core';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Typography from '@material-ui/core/Typography';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import 'react-notifications/lib/notifications.css';

import styles from './EffectHandler.styles'

const MAIN_CONTROLLER_API = (process.env.REACT_APP_MAIN_CONTROLLER_API)?
      process.env.REACT_APP_MAIN_CONTROLLER_API : "http://localhost:8000"


const createNotification = (type, title, message) => {
	switch (type) {
        case 'info':
            NotificationManager.info(message, title, 1500);
            break;
        case 'success':
            NotificationManager.success(message, title, 1500) ;
            break;
        case 'warning':
            NotificationManager.warning(message, title, 3000);
            break;
        case 'error':
            NotificationManager.error('Error message', 'Click me!', 5000, () => {
		alert('callback');
            });
            break;
	default:
	    break;
	}
}

const getCache = () => {
    const fetch = require('sync-fetch')
    var response = fetch(MAIN_CONTROLLER_API+'/cache').json()
    if (response.cache)
	return true
    return false
}

const EffectHandler = ({ classes, title, effects }) => {
    const [handlerValues, sethandlerValues] = useState({})
    const [cache, setCache] = useState(getCache())

    const waitForEffect = async (effect, enabled) => {
	await new Promise(r => setTimeout(r, 1000));
	while (1) {
	    try {
		const fetch = require('sync-fetch')
		var apiConfig = fetch(MAIN_CONTROLLER_API+'/config/').json()
		effects = apiConfig['ic-effects-service']['config']['effects']
		var efx = effects.find(el => el.name === effect)
		if (efx.enabled && enabled && !efx.loading) {
		    createNotification('success', 'Enable Effect', effect + ' effect is enabled')
		    break
		}
		if (!enabled && !efx.enabled){
		    createNotification('success', 'Disable Effect', effect + ' effect is disabled')
		    break
		}
	    }catch(e) {
		console.log('Error when fetching configuration')
		break
	    }
	}

    }

    const handleSwitchCase = async (event) => {
        sethandlerValues({...handlerValues, [event.target.name]: true})
	effects[event.target.value].enabled =  event.target.checked

	effects.forEach(function callback(element, index) {
	     // eslint-disable-next-line
	    if (index != event.target.value) {
		element.enabled = false
	    }
	})
	if (event.target.checked) {
	    createNotification('info', 'Enable Effect', 'Loading effect: '+event.target.name)
	    await fetch(MAIN_CONTROLLER_API+'/effect/'+event.target.name, {method: 'POST'})
	} else {
	    createNotification('info', 'Disable Effect', 'Disabling effect: '+event.target.name)
	    await fetch(MAIN_CONTROLLER_API+'/effect', {method: 'DELETE'})
	}
	waitForEffect(event.target.name, event.target.checked)
    }

    const handleCacheSwitch = async (event) => {
        setCache(event.target.checked)
	var cacheVal = 0
	if (event.target.checked)
	    cacheVal = 1
	const fetch = require('sync-fetch')
	fetch(MAIN_CONTROLLER_API+'/cache?cache='+cacheVal, {method: 'POST'})
    }

    return (
        <div className={classes.handlerContainer}>
	    {(effects.length) ?
	     <>
	    {effects.map((effect, key) =>
		<div key={key}>
		    <>
			<FormControlLabel
			    control={<Switch checked={effect.enabled} onChange={handleSwitchCase} value={key} color="primary" name={effect.name} />}
			    label={<Typography component="p" variant="h6">{effect.name}</Typography>}
			    labelPlacement="end"
			/>
		    </>
		    <>
			<a href={effect.meta.link} target="_blank"  rel="noreferrer">{effect.meta.desc}</a>
		    </>
		</div>
            )}
	     </>: <h3>No effects available</h3>
	    }
	    <>
		<h4> Enable cache for slow models </h4>
		<FormControlLabel
		    control={<Switch checked={cache} onChange={handleCacheSwitch} value="cache" color="secondary" name="cache" />}
		    label={<Typography component="p" variant="h6">cache</Typography>}
		    labelPlacement="end"
		/>
	    </>
	    <NotificationContainer/>
        </div>
    )
}

export default withStyles(styles)(EffectHandler);
