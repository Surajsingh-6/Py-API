import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import  r2_score

def pred(a='15-Oct-2024', b=160):
    df = pd.read_csv('data/data.csv')
    df_copy = df.copy()
    # print(df.head())
    df_copy['Date '] = pd.to_datetime(df_copy['Date '])
    df = df.replace(',', '', regex=True)
    df['Date '] = pd.to_datetime(df['Date '])
    df['Date '] = (df['Date '] - df['Date '].min()).dt.days
    for col in df.columns:
        if col != 'Date ': 
            df[col] = pd.to_numeric(df[col], errors='coerce')
    # print(df.head())
    x = df[['Date ', 'PREV. CLOSE ']][30:]
    y = df['OPEN '][30:]
    data = {
        'Date ': [a],
        'PREV. CLOSE ': [b]
    }
    dataset = pd.DataFrame(data)
    dataset['Date '] = pd.to_datetime(dataset['Date '])
    dataset['Date '] = (dataset['Date '] - df_copy['Date '].min()).dt.days
    model=LinearRegression()
    model.fit(x, y)
    pred=model.predict(dataset)
    accuracy = r2_score(df['OPEN '][:30],model.predict(df[['Date ','PREV. CLOSE ']][:30]))
    # print('Accuracy:', accuracy)
    # print('Predicted Open Price:', pred[0])
    return pred[0], accuracy
if __name__=='__main__':
    pred()
    
    
    