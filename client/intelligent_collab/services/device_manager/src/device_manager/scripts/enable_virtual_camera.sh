#!/usr/bin/env bash


LATEST_ID=$(v4l2-ctl --list-devices | grep '/dev/video' | sort |  awk -F 'video' '{print $2}' | tail -n1)
DEVICE_ID=$((LATEST_ID+1))
CAMERA_DEVICE=/dev/video$DEVICE

if [[ ! -w "$CAMERA_DEVICE" ]]; then
    sudo modprobe v4l2loopback exclusive_caps=1 video_nr=$DEVICE_ID card_label="icollab"
fi

# TODO: Validate that device has been created

echo $DEVICE_ID
