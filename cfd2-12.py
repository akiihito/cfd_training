import numpy as np
import matplotlib.pyplot as plt


def init(q1, q2, dx, jmax):
    # 格子点が -1.0 から始まるように修正
    xs = -1.0
    x = np.linspace(xs, xs + dx * (jmax-1), jmax)
    # 0 を境目にして流量（物理量）が変化するように修正
    q = np.array([float(q1) if i < 0.0 else float(q2) for i in x])
    return x, q


def do_computing(x, q, dt, dx, jmax, nmax, ff, order=1, interval=2):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    plt.plot(x, q, marker='o', lw=2, label='n=0')

    for n in range(1, nmax + 1):
        qold = q.copy()
        for j in range(order, jmax - order):
            # 輸送速度 c は q から計算するので必要ない
            ff1 = ff(qold, None, dt, dx, j)
            ff2 = ff(qold, None, dt, dx, j-1)
            q[j] = qold[j] - dt / dx * (ff1 - ff2)

        if n % interval == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()

def MC(q, c, dt, dx, j):
    # Murman-Cole 法による数値流束の計算
    # 輸送速度(c) が方向と量の両方を変化させる物理量(q)をベースとしている場合の計算方法
    ur = q[j + 1]
    ul = q[j]
    fr = 0.5 * ur ** 2
    fl = 0.5 * ul ** 2
    c = 0.5 * (ur + ul)
    ## np.sign(c)の符号の向きによって、q[j+1] か q[j] のどちらかが ff = 1/2q^2 という形で残る
    return 0.5 * (fr + fl - np.sign(c) * (fr - fl))


if __name__ == "__main__":
    q1 = 1
    q2 = 0
    nmax = 20

    dt = 0.05
    dx = 0.1
    jmax = 21

    x, q = init(q1, q2, dx, jmax)
    do_computing(x, q, dt, dx, jmax, nmax, MC, interval = 5)

