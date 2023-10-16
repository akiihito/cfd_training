import numpy as np
import matplotlib.pyplot as plt


def init(q1, q2, dx, jmax):
    x = np.linspace(0, dx * (jmax-1), jmax)
    q = np.array([float(q1) if i < 0.5 * jmax else float(q2) for i in range(jmax)])
    return x, q

def UPWIND1(q, c, dt, dx, j):
    ## 1次精度風上法の数値流束の c の方向に依存しない書き方
    ur = q[j+1]
    ul = q[j]
    fr = c * ur
    fl = c * ul
    return 0.5 * (fr + fl - abs(c) * (ur - ul)) # （式 2.39）

def UPWIND2(q, c, dt, dx, j):
    ## 2次精度風上法の数値流束の c の方向に依存しない書き方
    ur = 1.5 * q[j+1] - 0.5 * q[j+2]
    ul = 1.5 * q[j] - 0.5 * q[j-1]
    fr = c * ur
    fl = c * ul
    return 0.5 * (fr + fl - abs(c) * (ur - ul)) # （式 2.39）

def do_computing(ax, x, q, c, dt ,dx, nmax, jmax, ff, order=1, interval=2, ylim=None, yticks=None):
    #plt.figure(figsize=(7,7), dpi=100)
    #plt.rcParams["font.size"] = 22

    # 初期分布
    ax.plot(x, q, marker='o', lw=2, label='n=0')

    for n in range(1, nmax + 1):
        qold = q.copy()
        for j in range(order, jmax - order):
            ff1 = ff(qold, c, dt, dx, j)
            ff2 = ff(qold, c, dt, dx, j-1)
            q[j] = qold[j] - dt / dx * (ff1 - ff2)

        # 間が詰まると見えにくいので、interval 毎に可視化
        if n % interval == 0:
            ax.plot(x, q ,marker='o', lw=2, label=f'n={n}')
        
    #plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    #plt.xlabel('x')
    #plt.ylabel('q')
    #plt.legend()
    #if ylim is not None:
    #    plt.ylim(ylim)
    #if yticks is not None:
    #    plt.yticks(yticks)
    #plt.show()
     

if __name__ == "__main__":

    fig, axes = plt.subplots(2, 2)

    dt = 0.05  ## 時間間隔
    dx = 0.1   ## 格子点間の距離

    jmax = 21  ## 領域の大きさ
    nmax = 6   ## 最大時間

    ## (c > 0)の場合の1次精度風上法による移流方程式の計算と可視化
    c = 1  ## 輸送速度
    q1 = 1 ## 流速関数 q のパラメータ１
    q2 = 0 ## 流速関数 q のパラメータ２
    x, q = init(q1, q2, dx, jmax)
    do_computing(axes[0, 0], x, q, c, dt, dx, nmax, jmax, UPWIND1, order=1, interval=2)

    ## (c < 0)の場合の1次精度風上法による移流方程式の計算と可視化
    c = -1
    q1 = 0
    q2 = 1
    x, q = init(q1, q2, dx, jmax)
    do_computing(axes[0, 1], x, q, c, dt, dx, nmax, jmax, UPWIND1, order=1, interval=2)

    ## (c > 0)の場合の2次精度風上法による移流方程式の計算と可視化
    c = 1
    q1 = 1
    q2 = 0
    x, q = init(q1, q2, dx, jmax)
    do_computing(axes[1, 0], x, q, c, dt, dx, nmax, jmax, UPWIND2, order=2, interval=2, ylim=[-1, 1.1], yticks=np.arange(-1, 1.0, 0.2))

    ## (c < 0)の場合の2次精度風上法による移流方程式の計算と可視化
    c = -1
    q1 = 0
    q2 = 1
    x, q = init(q1, q2, dx, jmax)
    do_computing(axes[1, 1], x, q, c, dt, dx, nmax, jmax, UPWIND2, order=2, interval=2, ylim=[-1, 1.1], yticks=np.arange(-1, 1.0, 0.2))

    plt.show()
