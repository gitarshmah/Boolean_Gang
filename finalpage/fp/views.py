from django.shortcuts import render
import nsepy as nse
import datetime
from datetime import date as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_percentage_error as MAPE
from keras.callbacks import EarlyStopping
from plotly.subplots import make_subplots
import plotly as py
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam
from keras.losses import Huber
from keras.callbacks import EarlyStopping


# Create your views here.

def data_prep(dataset, timestep):
  X, y = [], []
  for i in range(timestep, dataset.shape[0]):
    X.append(dataset[i-timestep:i, 0])
    y.append(dataset[i,0])
  
  return (np.array(X), np.array(y))

    
def index(request):
    
    return render(request, 'base.html')

def prev_prediction(timestep, inp, scaler, model):
  pred_days = 45
  input = inp[-(timestep+pred_days):]

  input = scaler.fit_transform(np.array(input).reshape(-1,1))

  x_test = []
  for i in range(timestep, input.shape[0]):
    x_test.append(input[(i - timestep) : i , 0])
  x_test = np.array(x_test)

  x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], 1))

  y_pred = model.predict(x_test)
  y_pred = scaler.inverse_transform(y_pred)
  
  return y_pred

def future_prediction(timestep, inp, pred_days, scaler, model):
  input = inp[-(timestep):]

  input = scaler.fit_transform(np.array(input).reshape(-1,1))

  i=0
  y_predicted = []

  while(i<pred_days):

    if (len(input) > timestep):
      input = input[1:]
      temp_inp = input.reshape((1, timestep, 1))
      yhat = model.predict(temp_inp)
      y_predicted.append(yhat[0][0])
      input = np.concatenate((input, yhat), axis=0)
      i+=1

    else:
      temp_inp = input.reshape((1, timestep, 1))
      yhat = model.predict(temp_inp)
      y_predicted.append(yhat[0][0])
      input = np.concatenate((input, yhat), axis=0)
      i+=1

    # y_predicted = np.concatenate(y_predicted, axis=0)
    
    y_pred = np.array(y_predicted).reshape(-1,1)

    y_pred = scaler.inverse_transform(y_pred)
  
  return y_pred
    
def plotting(request):
  if request.method=='POST':
    print("req:", request)
    comp_symbol = request.POST['Company_Name']
    print(comp_symbol)
     
    
    
    today = dt.today()
    two_yrs = today - datetime.timedelta(days = int(2.5*365))
    
    #Load dataset
    stock = nse.get_history(symbol=comp_symbol, index = False, start=two_yrs, end=today)
    
    stock
    
    df = stock
    
    """## Analysis"""
    
    stock['MA60'] = df['Close'].rolling(window=45, min_periods=0).mean()
    stock['MA45'] = df['Close'].rolling(window=15, min_periods=0).mean()
    stock['MA90'] = df['Close'].rolling(window=90, min_periods=0).mean()

    
    scaler = MinMaxScaler((0,1))
    pred_days = 45
    timestep = 90
    df = df[['Close']]
    df_test = df[-pred_days:]
    df_train = df[:-pred_days]
    df_test.shape, df_train.shape
    
    # Train-Val split (70-30)
    trainSize = int(len(df_train) * 0.8)
    df_val = df_train[trainSize:]
    df_train = df_train[:trainSize]
    
    # Create Train-Val 
    train_set = df_train.values
    val_set = df_val.values
    
    train_set = scaler.fit_transform(np.array(train_set).reshape(-1,1))
    val_set = scaler.fit_transform(np.array(val_set).reshape(-1,1))

    (x_train, y_train) = data_prep(train_set, timestep)
    (x_val, y_val) = data_prep(val_set, timestep)
    
    x_train = np.reshape(x_train, newshape = (x_train.shape[0], x_train.shape[1], 1))
    x_val = np.reshape(x_val, newshape = (x_val.shape[0], x_val.shape[1], 1))

    model = Sequential()
    model.add(LSTM(60, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    
    opt = Adam(learning_rate = 0.00015)
    huber = Huber()
    model.compile(optimizer = opt, loss=huber)
    model.summary()

    early_stop = EarlyStopping(monitor='val_loss', patience=5)

    hist = model.fit(x_train, y_train, batch_size=32 , epochs=150, verbose=2, validation_data=(x_val, y_val), callbacks=[early_stop])
    
    train_pred = model.predict(x_train)
    val_pred = model.predict(x_val)

    train_pred = scaler.inverse_transform(train_pred)
    val_pred = scaler.inverse_transform(val_pred)

    train_set_temp = scaler.inverse_transform(train_set)
    val_set_temp = scaler.inverse_transform(val_set)

    train_dataset = pd.concat([df_train, df_val])

    train_values = train_dataset.values
    
    y_pred_prev = prev_prediction(timestep, train_values, scaler, model)
    y_pred_future = future_prediction(timestep, train_values, pred_days, scaler, model)
    accuracy = (1 - MAPE(df_test.values, y_pred_prev))*100
    plt.figure(figsize=(15,5))

    plt.plot(df_test.values, color='black', label='Real Price')
    plt.plot(y_pred_prev, color='red', label='Predicted Price')
    plt.grid()
    plt.legend()
    plt.title(f"Stock Price Predicted for {comp_symbol}")
    plt.xlabel("Next Days")
    plt.ylabel("Price (Rs/Share)")

    plt.style.use('seaborn-dark')
    print("Accurarcy = " + str(accuracy))
# 
    date_list = [today + datetime.timedelta(days=x) for x in range(pred_days)]
    pred_df = pd.DataFrame(data=y_pred_future, index=date_list)
    plt.figure(figsize=(15, 15))
    plt.plot(df[-(timestep+pred_days):], color='black', label='Real Stock Price')
    plt.plot(pred_df, color='red', label='Predicted Stock Price')
    plt.plot(df_test.index, y_pred_prev, color='red')

    plt.grid()
    plt.legend()
    plt.title(f"Historical and Predicted Stock Price for {comp_symbol}")
    plt.xlabel("Dates")
    plt.ylabel("Price (Rs/Share)")

    plt.style.use('seaborn-dark')
    print("Accurarcy = " + str(accuracy))

    return render(request, 'base.html')

