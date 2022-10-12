# %% [markdown]
# <img src="http://hilpisch.com/tpq_logo.png" alt="The Python Quants" width="35%" align="right" border="0"><br>

# %% [markdown]
# # Python for Algorithmic Trading 

# %% [markdown]
# **Chapter 07 &mdash; Working with Real-Time Data and Sockets**

# %% [markdown]
# ## Visualizing Streaming Data with Plotly

# %% [markdown]
# ### The Basics

# %%
import zmq
from datetime import datetime
import plotly.graph_objects as go

# %%
symbol = 'SYMBOL'

# %%
fig = go.FigureWidget()
fig.add_scatter()
fig

# %%
context = zmq.Context()

# %%
socket = context.socket(zmq.SUB)

# %%
socket.connect('tcp://127.0.0.1:5555')

# %%
socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

# %%
times = list()
prices = list()

# %%
for _ in range(50):
    msg = socket.recv_string()
    t = datetime.now()
    times.append(t)
    _, price = msg.split()
    prices.append(float(price))
    fig.data[0].x = times
    fig.data[0].y = prices

# %%
fig = go.FigureWidget()
fig.add_scatter(name='SYMBOL')
fig.add_scatter(name='SMA1', line=dict(width=1, dash='dot'),
                mode='lines+markers')
fig.add_scatter(name='SMA2', line=dict(width=1, dash='dash'),
                mode='lines+markers')
fig

# %%
import pandas as pd

# %%
df = pd.DataFrame()

# %%
for _ in range(75):
    msg = socket.recv_string()
    t = datetime.now()
    sym, price = msg.split()
    df = pd.concat([df,pd.DataFrame({sym: float(price)}, index=[t])])
    df['SMA1'] = df[sym].rolling(5).mean()
    df['SMA2'] = df[sym].rolling(10).mean()
    fig.data[0].x = df.index
    fig.data[1].x = df.index
    fig.data[2].x = df.index
    fig.data[0].y = df[sym]
    fig.data[1].y = df['SMA1']
    fig.data[2].y = df['SMA2']

# %%
from plotly.subplots import make_subplots

# %%
f = make_subplots(rows=3, cols=1, shared_xaxes=True)
f.append_trace(go.Scatter(name='SYMBOL'), row=1, col=1)
f.append_trace(go.Scatter(name='RETURN', line=dict(width=1, dash='dot'),
                mode='lines+markers', marker={'symbol': 'triangle-up'}),
                row=2, col=1)
f.append_trace(go.Scatter(name='MOMENTUM', line=dict(width=1, dash='dash'),
                mode='lines+markers', marker={'symbol': 'x'}), row=3, col=1)
# f.update_layout(height=600)

# %%
fig = go.FigureWidget(f)

# %%
fig

# %%
import numpy as np

# %%
df = pd.DataFrame()

# %%
for _ in range(75):
    msg = socket.recv_string()
    t = datetime.now()
    sym, price = msg.split()
    df = df.append(pd.DataFrame({sym: float(price)}, index=[t]))
    df['RET'] = np.log(df[sym] / df[sym].shift(1))
    df['MOM'] = df['RET'].rolling(10).mean()
    fig.data[0].x = df.index
    fig.data[1].x = df.index
    fig.data[2].x = df.index
    fig.data[0].y = df[sym]
    fig.data[1].y = df['RET']
    fig.data[2].y = df['MOM']

# %%
socket = context.socket(zmq.SUB)

# %%
socket.connect('tcp://127.0.0.1:5555')

# %%
socket.setsockopt_string(zmq.SUBSCRIBE, '')

# %%
for _ in range(5):
    msg = socket.recv_string()
    print(msg)

# %%
fig = go.FigureWidget()
fig.add_bar()
fig

# %%
x = list('abcdefgh')
fig.data[0].x = x
for _ in range(100):
    msg = socket.recv_string()
    y = msg.split()
    y = [float(n) for n in y]
    fig.data[0].y = y

# %% [markdown]
# <img src="http://hilpisch.com/tpq_logo.png" alt="The Python Quants" width="35%" align="right" border="0"><br>
# 
# <a href="http://tpq.io" target="_blank">http://tpq.io</a> | <a href="http://twitter.com/dyjh" target="_blank">@dyjh</a> | <a href="mailto:training@tpq.io">training@tpq.io</a>


