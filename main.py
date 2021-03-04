from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import streamlit as st
import yfinance as yf

START = "2010-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

st.header('Parameters')
stocks = ("AAPL", "GOOG", "MSFT")
selected_stock = st.selectbox(
    "Select dataset for prediction",
    stocks
)


@st.cache
def load_data(ticker):
  data = yf.download(ticker, START, TODAY)
  data.reset_index(inplace=True)
  return data

st.header('Stock Data')
data = load_data(selected_stock)
st.subheader("Raw data")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Line(x=data['Date'],y=data['Close'], name='Price'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

n_years = st.slider("Years to predict:", 1, 5)
period = n_years * 365

df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
m = Prophet()
m.fit(df_train)

future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)
st.subheader("Forecasted data")
st.write(forecast.tail())

st.write("Forecasted Time Series")
fig1 = plot_plotly(m, forecast, trend=True)
st.plotly_chart(fig1)
