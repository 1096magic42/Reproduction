import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error

df = pd.read_excel('ddPCR.xlsx')
X = df[['ELOV2index', 'FHL2', 'PDE4C']].values
y = df['Chro. Age'].values
kf = KFold(n_splits=3, shuffle=True, random_state=42)
mae_scores = []

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]

    # 拟合线性回归
    from sklearn.linear_model import LinearRegression

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # 预测验证集
    y_pred = lr.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)
    mae_scores.append(mae)

print(f"3折交叉验证MAE: {np.mean(mae_scores):.3f} ± {np.std(mae_scores):.3f}")