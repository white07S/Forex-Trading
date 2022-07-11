import datetime as dt
import pandas as pd
import os
from helper import getMsByTimeStr
import numpy as np

epoch = dt.datetime.utcfromtimestamp(0)

def getMsByTime(dt):
  return int((dt - epoch).total_seconds() * 1000)

def getUTCTimeStrFromMs(time):
  return dt.datetime.fromtimestamp((time - 8 * 60 * 60 * 1000) / 1000.0)

def getTime(timeStr):
  return dt.datetime.strptime(timeStr,'%Y-%m-%dT%H:%M:%S.000000000Z')

def getMsByTimeStr(timeStr):
  return getMsByTime(getTime(timeStr))

def getDatesArr(startDate, endDate, str = '%Y-%m-%d'):
  return [d.strftime(str) for d in pd.date_range(startDate, endDate, freq='7D')]

def mkdir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)


def dataContentPicker(
  data,
  dataType,
):
  if dataType == 'mid':
    if data['complete']:
      return [
        data['mid']['o'],
        data['mid']['h'],
        data['mid']['l'],
        data['mid']['c'],
      ]
    else:
      return [0, 0, 0, 0]

def dataPicker(
  data,
  dataType = 'mid',
):
  arr = dataContentPicker(data, dataType)
  return np.concatenate((
    arr if type(arr).__module__ == 'numpy' else np.array(arr),
    [1 if data['complete'] else 0, getMsByTimeStr(data['time'])]
  ),axis = 0)