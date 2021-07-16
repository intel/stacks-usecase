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

function StreamPicker({selectStreamType, streamType, streamTypes, setStreamType}) {
    const classes = useStyles();
    return (
        <div>
            <h2>Select the stream type</h2>
            <FormControl className={classes.formControl}>
                <InputLabel htmlFor="stream-native-helper">Stream Type</InputLabel>
                <NativeSelect
                    onChange={selectStreamType}
                    value={streamType.name}
                    inputProps={{
                        name: 'StreamType',
                        id: 'stream-native-helper',
                    }}
                >
                    <option aria-label="None" value="" />
                    {streamTypes.map((streamType, key) =>
                        <option id={key} value={streamType.name}>{streamType.name}</option>
                    )}
                </NativeSelect>
                <FormHelperText>Choose stream type from list</FormHelperText>
            </FormControl>
        </div>
    )
}

export default StreamPicker
