import React from 'react'
import { withStyles } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import { useState, useRef, useEffect } from 'react';
import styles from './EffectsController.styles';

import EffectHandler from '../../components/effect-handler/EffectHandler';
import CameraPicker from '../camera-picker/CameraPicker';
//import StreamPicker from '../stream-picker/StreamPicker';



const MAIN_CONTROLLER_API = (process.env.REACT_APP_MAIN_CONTROLLER_API)?
      process.env.REACT_APP_MAIN_CONTROLLER_API : "http://localhost:8000"

const streamTypes = [
    //{id: 1, name: 'incoming'},
    {id: 2, name: 'outgoing'},
]

const getConfig =  () => {

    var baseConfig = {}
    const fetch = require('sync-fetch')

    try {
	var apiConfig = fetch(MAIN_CONTROLLER_API+'/config/').json()

	//baseConfig.streamType = streamTypes.find(el => el.name === apiConfig['icollab-videoproxy']['config']['stream_type'])
	baseConfig.streamType = streamTypes[0]
	var webcams = apiConfig['ic-device-manager']['config']['webcams']
	if (apiConfig['ic-video-proxy']['config']['video_source']) {
	    var source =  apiConfig['ic-video-proxy']['config']['video_source']['source']
	    baseConfig.source = webcams.find(el => el.devices.includes("/dev/video"+source))
	} else
	    baseConfig.source = null
	baseConfig.effects = apiConfig['ic-effects-service']['config']['effects']
	baseConfig.cameras = webcams
    } catch (e){
    }
    return baseConfig
}

const EffectsController = ({ classes }) => {

    const [cameraHidden, setcameraHidden] = useState(true)
    //const [streamType, setStreamType] = useState({});
    const [physicalDevice, setPhysicalDevice] = useState({});
    const [config] = useState(getConfig());

    const videoRef = useRef(null);

    useEffect(() => {
        const getMedia = async () => {
            if (config.source) {
		navigator.mediaDevices.getUserMedia({video: true});
		const devices =  await navigator.mediaDevices.enumerateDevices()
		const cameras = devices.filter(device => device.kind === 'videoinput' &&  device.label.startsWith("icollab") );
		if (cameras.length > 0) {
		    const camera = cameras[0]
                    const stream = await navigator.mediaDevices.getUserMedia({ video: { deviceId: { exact: camera.deviceId} } });
                    if (!cameraHidden) {
			let video = videoRef.current;
			video.srcObject = stream;
			video.play();
                    }
		}
            } else if (videoRef.current) {
                videoRef.current.srcObject = null;
            }
        }
	getMedia()
    }, [physicalDevice, cameraHidden, config.source]);


    const selectPhysicalDevice = async (event) => {
        const camera = config.cameras.find(el => el.label === event.target.value)
        if (!camera){
            setPhysicalDevice({})
            setcameraHidden(true)
        } else {
	    config.source = camera
            setPhysicalDevice(camera)
	    var device_id = camera.devices[0].split('video')[1]
	    const fetch = require('sync-fetch')
	    try {
		fetch(MAIN_CONTROLLER_API+'/video_source/', {
		    method: 'POST',
		    body: JSON.stringify({source: device_id})
		})
            } catch (e) {
		console.log("Error when setting new camera")
	    }
	    try {
		fetch(MAIN_CONTROLLER_API+'/video/', {method: 'POST'})
            } catch (e) {
		console.log("Error when starting new video stream")
	    }
	}
    }

    /*
    const selectStreamType = async (event) => {
	const streamType = streamTypes.find(el => el.name === event.target.value);
        if (!streamType) {
            //setStreamType({})
	    config.streamType = {}
            setcameraHidden(true)
	    setPhysicalDevice({})
        } else {
            //setStreamType(streamType);
	    config.streamType = streamType
	    console.log(config.streamType)
	    if (streamType.name === "outgoing") {
	    } else {
		console.log('Not supported stream type')
	    }
        }
    }
    */

    if (Object.keys(config).length === 0) {
	return (
	    <div>
		<h2>There was an error when loading configuration</h2>
		<h3>Verify that Main Controller service is running</h3>
	    </div>
		)
    }

    return (
        <div>
	    {/*
		<h1 className={classes.headline}>Effects Controller</h1>
		<br/>
		<StreamPicker selectStreamType={selectStreamType} streamType={config.streamType} streamTypes={streamTypes} setStreamType={setStreamType}/>
	    */}
	    {(config.streamType.name === "outgoing") ?
	     <div>
		 <h2>Select the physical camera</h2>
		 <CameraPicker selectDevice={selectPhysicalDevice} device={config.source} devices={config.cameras} setDevice={setPhysicalDevice} />

		 {(config.source) ?
		  <>
		      <h2>Select the effects</h2>
		      <div className={classes.effectsHandler}>
			  <EffectHandler title="Effects" effects={config.effects}/>
		      </div>

		      <Button color="primary" className={classes.previewButton} onClick={() => {
				  if(!cameraHidden || (physicalDevice))
				      setcameraHidden(value => !value)
			      }											}>
			  {cameraHidden ? "Show preview" : "Hide preview"}
		      </Button>
		      {(!cameraHidden && physicalDevice) ?
		       <>
			   {cameraContainerComponent()}
		       </> : null}
		  </>: null
		 }
	     </div> : null
	    }
        </div>

    )

    function cameraContainerComponent() {
        return <div className={classes.cameraContainer}>
            <video ref={videoRef} />
        </div>;
    }
}

export default withStyles(styles)(EffectsController);
