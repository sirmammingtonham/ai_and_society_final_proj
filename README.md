# FakeBlock
Proof of concept Google Chrome extension that blocks deepfakes.

[![how it works:](https://github.com/sirmammingtonham/FakeBlock/blob/master/demo.gif?raw=true)](https://docs.google.com/presentation/d/1CHGox3OH4PVB3Ks_ThE1JMyCckJGKKIai0LA9rffEec/edit?usp=sharing)

## Installation:
Clone this repository, then run install dependencies with ```pip install -r requirements.txt```.

Once installed, run ```python3 detect.py``` locally, then in a chrome browser that allows Cross-Origin Resource Sharing (CORS), load the plugin folder as an extension (you will need to enable developer mode).

## Usage:
Go to a website with possible deepfakes and click on the extension icon. FakeBlock will check possible deepfakes and AI generated content through a neural network and automatically block them for you.

Check the demo video for more info.
