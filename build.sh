#!/bin/bash
export PATH=${PATH}:`pwd`/android-sdk-linux/tools:`pwd`/android-sdk-linux/platform-tools

cd pygame-*/
python2.7 ./build.py --dir `pwd`/pet --package com.pypetandroid.pet --name "Python Pet" --version 1.0 --icon `pwd`/pet/icon.png --orientation landscape debug
adb kill-server
sudo `pwd`/android-sdk-linux/platform-tools/adb start-server
adb -d install -r bin/PythonPet-1.0-debug.apk

