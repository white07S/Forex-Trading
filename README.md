# Forex-Trading
A simple implementation of HFT (High-Frequency Trading) in Python on the concept of DQN 

# Goal : 
* Finding patterns for avoiding spread loss and limiting the order book
* Automating the trading by certain default values (you can find the config file inside the file) by using the DQN model.
* Making a model that can handle multiple orders without avoiding conflict with the analysis
* Avoid using any extra library or API

# Some basic information:
* Support tensorboard 
* Written in TensorFlow v1 
* if you using TensorFlow v2 then import this on top of the code to avoid conflict of depreciated function like random_seed_set and session

```
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
```

* HFT (High-Frequency Trading): High-frequency trading (HFT) is a type of algorithmic financial trading characterized by high speeds, high turnover rates, and high order-to-trade ratios that leverages high-frequency financial data and electronic trading tools. 
* More info: https://www.investopedia.com/terms/h/high-frequency-trading.asp

# Testing Data
* EURUSD (5 min interval - 2 Year Period)
* GBPUSD (5 min interval -2 Year Period)

# Install
* Check config file based on your requirements
* Install lib
```
pip install -r requirements.txt
```
* Training
```
python3 main.py
```
* Code Documentation
```
python3 main.py -h
```
* Results snapshot



# Remarks
* Results will be different if you are using leverage (for testing purpose 50x leverage is used) and charge based on your broker
* IT'S A EXPERIMENT [NO RESPONSIBILITY FOR ANY INTEGRATION IN THE LIVE MARKET]
