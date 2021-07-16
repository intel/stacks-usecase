import React from 'react'
import Webcam from 'react-webcam';
import Typography from '@material-ui/core/Typography';
import styles from './FullCameraPreview.styles'
import { withStyles } from '@material-ui/core';

const FullCameraPreview = ({classes}) => {
    return (
        <div className={classes.camContainer}>
            <Webcam width='800' />
            <Typography component="h2" variant="h6" color="inherit">
                Preview of outgoing video stream
            </Typography>
        </div>
    )
}

export default withStyles(styles)(FullCameraPreview);