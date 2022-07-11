import numpy as np
import json
import csv
import os
import sys
import getopt
import tensorflow as tf

from forex import Forex
from core import DeepNetwork
from config import getConfig
from helper import dataPicker
from helper import getDatesArr, mkdir

def readData(
  dates,
  dataType = 'mid',
):

  midPriceMap = {}
  featureNum = 0

  # start read
  for date in dates:
    tmp = []
    with open(f'candlestamps/{date}.json') as file:
      json_data = json.load(file)
      featureNum = len(dataPicker(json_data['candles'][0], dataType = dataType)) - 2

      tmp.extend(
          dataPicker(data, dataType=dataType) for data in json_data['candles'])
    # print(tmp)
    midPriceMap[date] = np.array(tmp)

  print('Read file done')

  return midPriceMap, featureNum

if __name__ == '__main__':

  FLAG = getConfig()

  try:
    opts, args = getopt.getopt(
      sys.argv[1:],
      'cd:hl:ot',
      ['dir=', 'help'],
    )
  except getopt.GetoptError:
    print('python3 train/index.py -h')
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-c'):
      FLAG['isTrain'] = False
      FLAG['episodes'] = 1
      FLAG['outputClose'] = True
    elif opt in ('-d', '--dir'):
      FLAG['dir'] = arg
    elif opt in ['-h', '--help']:
      print('python3 train/index.py')
      print('-d <dir>: assign the output directory to data/<dir>')
      print('-h --help: help')
      print('-l <num>: load ckpt file from <dir>/history/<num>')
      print('-o: command line output result')
      print('-t: testing mode, default: training mode')
      sys.exit()
    elif opt in ('-l'):
      FLAG['ckptFile'] = f'history/{arg}/train.ckpt'
      FLAG['loadHisNum'] = int(arg)
    elif opt in ('-o'):
      FLAG['isTrain'] = False
      FLAG['episodes'] = 1
      FLAG['cliOutput'] = True
    elif opt in ('-t'):
      FLAG['isTrain'] = False
      FLAG['episodes'] = 1

  mkdir('data')
  mkdir(f"data/{FLAG['dir']}")
  mkdir(f"data/{FLAG['dir']}/history")

  if not FLAG['isTrain']:
    with open(f"data/{FLAG['dir']}/param.csv") as csv_file:
      r = csv.DictReader(csv_file)
      for row in r:
        for column, value in row.items():
          if value != None and column not in FLAG['noLoadHeader']:
            if isinstance(FLAG[column], int):
              FLAG[column] = int(value)
            elif isinstance(FLAG[column], float):
              FLAG[column] = float(value)
            else:
              FLAG[column] = value
    FLAG['episodes'] = 1

  attr = sorted([a for a in FLAG.items() if a[0] not in FLAG['rmHeader']])

  print('')
  for key, value in attr:
    print(f'{key}: {value}')
  print('')

  if FLAG['isTrain']:
    item = [value for key, value in attr]
    itemHeader = [key for key, value in attr]

    if not os.path.isfile(f"data/{FLAG['dir']}/param.csv"):
      with open(f"data/{FLAG['dir']}/param.csv", 'a') as csv_file:
        w = csv.writer(csv_file)
        w.writerow(itemHeader)
        w.writerow(item)

  dates = getDatesArr(FLAG['dateStart'], FLAG['dateEnd'])

  midPriceMap, featureNum = \
    readData(
      dates = dates,
      dataType = FLAG['dataType'],
    )

  forex = Forex(
    midPriceMap = midPriceMap,
    count = FLAG['count'],
  )

  RL = DeepNetwork(
    forex = forex,
    dates = dates,
    featureNum = featureNum,
    config = FLAG,
  )

  RL.train()






