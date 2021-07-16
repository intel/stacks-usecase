import React from 'react'
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import NativeSelect from '@material-ui/core/NativeSelect';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
}));

function CameraPicker({selectDevice, device, devices, setDevice}) {
    const classes = useStyles();
    return (
        <div>
            <FormControl className={classes.formControl}>
                <InputLabel htmlFor="camera-native-helper">Physical Camera</InputLabel>
                <NativeSelect
                    onChange={selectDevice}
                    value={(device) ? device.label : ""}
                    inputProps={{
                        name: 'Camera',
                        id: 'camera-native-helper',
                    }}
                >
                    <option aria-label="None" value="" />
                    {devices.map((device, key) =>
                        <option key={key} value={device.label}>{device.label}</option>
                    )}
                </NativeSelect>
                <FormHelperText>Choose device from list</FormHelperText>
            </FormControl>
        </div>
    )
}

export default CameraPicker
