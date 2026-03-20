import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 读取数据
df = pd.read_excel('ddPCR.xlsx')
X = df[['PDE4C', 'FHL2', 'ELOV2index']].values
y = df['Chro.Age'].values

# 固定模型参数
intercept = -19.398
coef = np.array([0.463, 0.774, 0.156])

def predict_fixed(X, coef, intercept):
    return X @ coef + intercept

## ------------------------------
# 2. 3折交叉验证 (3-fold cross validation)
# ------------------------------
print("="*50)
print("3折交叉验证")
print("="*50)

kf = KFold(n_splits=3, shuffle=True, random_state=42)
mae_scores = []
rmse_scores = []
models = []  # 保存每次训练的模型（可选）

for fold, (train_idx, val_idx) in enumerate(kf.split(X), 1):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]

    # 训练线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    models.append(model)

    # 预测验证集
    y_pred = model.predict(X_val)

    # 计算MAD和RMSE
    mae = mean_absolute_error(y_val, y_pred)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    mae_scores.append(mae)
    rmse_scores.append(rmse)

    print(f"Fold {fold}: MAD = {mae:.3f} 年, RMSE = {rmse:.3f} 年")

print(f"\n平均MAD: {np.mean(mae_scores):.3f} 年 (±{np.std(mae_scores):.3f})")
print(f"平均RMSE: {np.mean(rmse_scores):.3f} 年 (±{np.std(rmse_scores):.3f})")

# 可选：查看各折的模型系数
for i, model in enumerate(models, 1):
    print(f"Fold {i} 系数: {model.coef_.round(4)}, 截距: {model.intercept_.round(4)}")

# ------------------------------
# 3. 留出法交叉验证 (Holdout cross validation)
# ------------------------------
print("\n" + "="*50)
print("留出法交叉验证")
print("="*50)

# 将数据集划分为训练集和验证集（常见比例：70%训练，30%验证）
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, random_state=42, shuffle=True
)

# 训练模型
model_holdout = LinearRegression()
model_holdout.fit(X_train, y_train)

# 训练集评估
y_train_pred = model_holdout.predict(X_train)
mae_train = mean_absolute_error(y_train, y_train_pred)
rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))

# 验证集评估
y_val_pred = model_holdout.predict(X_val)
mae_val = mean_absolute_error(y_val, y_val_pred)
rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))

print(f"训练集样本数: {len(y_train)}, 验证集样本数: {len(y_val)}")
print(f"训练集 MAD: {mae_train:.3f} 年, RMSE: {rmse_train:.3f} 年")
print(f"验证集 MAD: {mae_val:.3f} 年, RMSE: {rmse_val:.3f} 年")

# 输出模型系数（可与论文对比）
print(f"模型系数: {model_holdout.coef_.round(4)}")
print(f"模型截距: {model_holdout.intercept_.round(4)}")