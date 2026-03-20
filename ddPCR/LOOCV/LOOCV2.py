import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut

df = pd.read_excel('ddPCR.xlsx')
X = df[['ELOV2index', 'FHL2', 'PDE4C']].values
y = df['Chro.Age'].values
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, random_state=42
)
# 初始化 LOOCV 分割器
loo = LeaveOneOut()

# 存储每次迭代的真实值和预测值
y_true_list = []
y_pred_list = []

# 进行 LOOCV
for train_index, test_index in loo.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # 训练模型（以线性回归为例）
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)

    # 记录结果
    y_true_list.append(y_test[0])
    y_pred_list.append(y_pred[0])

# 转换为数组
y_true = np.array(y_true_list)
y_pred = np.array(y_pred_list)

# 计算整体评估指标
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print(f"LOOCV 平均绝对误差 (MAE): {mae:.2f} 岁")
print(f"LOOCV R² 分数: {r2:.3f}")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# 计算预测年龄
df['pred_age'] = -19.398 + 0.156*df['ELOV2index'] + 0.774*df['FHL2'] + 0.463*df['PDE4C']

# 计算Spearman相关系数
rho, p = spearmanr(df['Chro.Age'], df['pred_age'])

# 绘制散点图
plt.figure(figsize=(8, 6))
plt.scatter(df['Chro.Age'], df['pred_age'], alpha=0.7)
plt.plot([0, 100], [0, 100], 'r--', linewidth=2)  # 对角线
plt.xlabel('Chronological Age (years)')
plt.ylabel('Predicted Age (years)')
plt.title(f'Epigenetic vs Chronological Age (ρ = {rho:.3f})')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()