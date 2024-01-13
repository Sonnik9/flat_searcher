
class TECHNIQUESS():
    def __init__(self) -> None:
        super().__init__()
# ///////////////////////////////////////////////////////////////////////////////////////////////////
    def in_squeeze(self, df):
        last_6_rows = df.iloc[-6:]
        return (last_6_rows['lower_band'] > last_6_rows['lower_keltner']).all() and \
            (last_6_rows['upper_band'] < last_6_rows['upper_keltner']).all()

    async def squeeze_unMomentum(self, data):
        df = data.copy()
        df['20sma'] = df['Close'].rolling(window=20).mean()
        df['stddev'] = df['Close'].rolling(window=20).std()
        df['lower_band'] = df['20sma'] - (self.BB_stddev_MULTIPLITER * df['stddev'])
        df['upper_band'] = df['20sma'] + (self.BB_stddev_MULTIPLITER * df['stddev'])

        df['TR'] = abs(df['High'] - df['Low'])
        df['ATR'] = df['TR'].rolling(window=20).mean()

        df['lower_keltner'] = df['20sma'] - (df['ATR'] * self.KC_stddev_MULTIPLITER)
        df['upper_keltner'] = df['20sma'] + (df['ATR'] * self.KC_stddev_MULTIPLITER)
        
        df['squeeze_on'] = df.apply(self.in_squeeze, axis=1)
        df['squeeze_off'] = df.iloc[-2]['squeeze_on'] and not df.iloc[-1]['squeeze_on']
        df['no_squeeze'] = ~df['squeeze_on'] & ~df['squeeze_off'] # --??

        return df 
  