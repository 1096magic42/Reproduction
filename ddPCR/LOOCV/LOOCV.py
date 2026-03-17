import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_excel('ddPCR.xlsx')
X = df[['ELOVL2sq', 'FHL2', 'PDE4C']].values
y = df['Chro. Age'].values
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, random_state=42
)

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred_train = lr.predict(X_train)
y_pred_val = lr.predict(X_val)

mae_train = mean_absolute_error(y_train, y_pred_train)
mae_val = mean_absolute_error(y_val, y_pred_val)

print(f"训练集MAE: {mae_train:.3f}")
print(f"验证集MAE: {mae_val:.3f}")