import numpy as np
import matplotlib.pyplot as plt

c = 1     # 輸送速度
dt = 0.05 # t の刻み幅
dx = 0.1  # x の刻み幅
jmax = 21 # 離散点の数
nmax = 6

x = np.linspace( 0, dx * (jmax - 1), jmax)
q = np.zeros(jmax)

# q(x)の関数モドキを作成（半分まで１を返して、半分過ぎたら０を返す）
for j in range(jmax):
    if (j < jmax / 2):
        q[j] = 1
    else:
        q[j] = 0

plt.figure(figsize=(7,7), dpi=100)
plt.rcParams["font.size"] = 22

plt.plot(x, q, marker='o', lw=2, label='n=0')

for n in range(1, nmax + 1):
    qold = q.copy()
    for j in range(1, jmax-1):
        # 時刻毎の波の形を作る
        q[j] = qold[j] - dt * c * (qold[j+1] - qold[j-1]) / (2 * dx) # 式2.7
    
    # グラフを見やすくするために１っこ飛ばしで描画
    if n % 2 == 0:
        plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

plt.grid(color='black', linestyle='dashed', linewidth=0.5)
plt.xlim([0, 2.0])
plt.xlabel('x')
plt.ylabel('q')
plt.legend()
plt.show()