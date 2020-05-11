# WIET_sourcing_app
Simple gui client for [WIET-sourcing](https://github.com/XertDev/WIET-sourcing) created with [KivyMD](https://github.com/HeaTTheatR/KivyMD).
### Basic setup 
You can clone the app source and create venv with all requirements installed by running the code below. 
```shell script
git clone https://github.com/XertDev/WIET_sourcing_app
cd WIET_sourcing_app
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
Then everytime you need, you can access the venv created by running the command below. 
```shell script
source venv/bin/activate
```

### Android development with buildozer
This app is multi platform by nature to the point, that it can be deployed on both desktop and mobile systems. To build the app for android target, one can use [Buildozer](https://github.com/kivy/buildozer), as noted in kivyMD [readme](https://github.com/HeaTTheatR/KivyMD/blob/master/README.md#how-to-use-with-buildozer). 

Buildozer compilation job is specified via *buildozer.spec* file. Please, pay attention to the lines:
* line 39: requirements with which the app is being built.  
* line 88: android permissions that should be granted to the app after deployment. 

**Note that app compiled with buildozer gets a separate to both requirements.txt and venv set of dependencies.**   

#### Simple usage of buildozer 
Before running the commands below, please install buildozer and enter your app folder first.

For full android build and deployment you can use:
```shell script
buildozer android debug deploy run
```
It runs the app with adb after installation. If you only need *.apk* package, please use command below. 
```shell script
buildozer android debug
```
It will be places in *bin* folder. 

You can then debug the application with standard android development toolset, like Android Studio. 
#### Buildozer installation 
For buildozer installation, please run
```shell script
sudo pip install buildozer
```
*It may also require a bunch of system requirements.* 

#### Target phone configuration 
The app can be run on both hardware android phones and android emulators. In the first case, you first need to enable [developer options](https://developer.android.com/studio/debug/dev-options). For the instructions on emulator usage, please follow [this](https://developer.android.com/studio/run/emulator) guide by google. 