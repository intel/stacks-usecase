#!/bin/env bash


echo "get and install v4l2loopback, sudo required..."
git clone https://github.com/umlaeute/v4l2loopback
echo "--- Installing v4l2loopback (sudo privelege required)"
cd v4l2loopback
make && sudo make install
sudo depmod -a
cd ..
