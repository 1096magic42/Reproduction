import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import pandas as pd

df = pd.read_excel('ddPCR.xlsx')
X = df[['ELOV2index', 'FHL2', 'PDE4C']].values
y = df['Chro. Age'].values
# 计算预测年龄
df['pred_age'] = -19.398 + 0.156*df['ELOV2index']**2 + 0.774*df['FHL2'] + 0.463*df['PDE4C']

# 计算Spearman相关系数
rho, p = spearmanr(df['Chro. Age'], df['pred_age'])

# 绘制散点图
plt.figure(figsize=(8, 6))
plt.scatter(df['Chro. Age'], df['pred_age'], alpha=0.7)
plt.plot([0, 100], [0, 100], 'r--', linewidth=2)  # 对角线
plt.xlabel('Chronological Age (years)')
plt.ylabel('Predicted Age (years)')
plt.title(f'Epigenetic vs Chronological Age (ρ = {rho:.3f})')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()