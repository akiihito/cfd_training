import numpy as np
import matplotlib.pyplot as plt


dt = 0.05 # 時間刻み
dx = 0.1  # 格子長

jmax = 21 # 格子点最大
nmax = 6  # 時間最大

def init(q1, q2, dx, jmax):
    x = np.linspace(0, dx * (jmax - 1), jmax)
    q = np.array([float(q1) if i < 0.5 * jmax else float(q2) for i in range(jmax)])
    return (x, q)

######### 以下、数値流束項（f~）のみを各方式で計算
# FTCS法
def FTCS(q, c, dt, dx, j):
    return 0.5 * c * (q[j+1] + q[j])

# 1次精度風上法
def UPWIND1(q, c, dt, dx, j):
    return c * q[j]

# LAX法
def LAX(q, c, dt, dx, j):
    nu2 = 1 / (c * dt / dx)
    return 0.5 * c * ((1 - nu2) * q[j+1] + (1 + nu2) * q[j])

# Lax-Wendroff法
def LAXWEN(q, c, dt, dx, j):
    nu = c * dt /dx
    return 0.5 * c * ((1 - nu) * q[j+1] + (1 + nu) * q[j])
######### ここまで ###########################


def do_computing(x, q, c, dt, dx, nmax, ff):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    # 初期分布
    plt.plot(x, q, marker='o', lw=2, label='n=0')

    for n in range(1, nmax + 1):
        qold = q.copy()
        for j in range(1, jmax - 1):
            # 数値流束項を使った移流方程式の計算
            ff1 = ff(qold, c, dt, dx, j)
            ff2 = ff(qold, c, dt, dx, j-1)
            q[j] = qold[j] - dt / dx * (ff1 - ff2)

        # 見やすくするため n が偶数のときだけ表示
        if n % 2 == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

    # グラフ表示
    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlim([0, 2])
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    c = 1
    q1, q2 = 1, 0

    ######### 各手法で移流方程式を計算
    ## 1次精度風上法
    x, q = init(q1, q2, dx, jmax)
    do_computing(x, q, c, dt, dx, nmax, UPWIND1)

    ## FTCS法
    x, q = init(q1, q2, dx, jmax)
    do_computing(x, q, c, dt, dx, nmax, FTCS)

    ## LAX法
    x, q = init(q1, q2, dx, jmax)
    do_computing(x, q, c, dt, dx, nmax, LAX)

    ## Lax-Wendroff法
    x, q = init(q1, q2, dx, jmax)
    do_computing(x, q, c, dt, dx, nmax, LAXWEN)

