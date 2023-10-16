import matplotlib.pyplot as plt
import numpy as np

def init(q1, q2, dx, jmax, sp=0.5):
    x = np.linspace(0, dx * (jmax - 1), jmax)
    q = np.array([float(q1) if i < sp * jmax else float(q2) for i in range(jmax)])
    return x, q


def minmod(x, y):
    sgn = np.sign(x)
    return sgn * max(min(abs(x), sgn * y), 0.0)


def do_computing2(x, q, c, dt, dx, jmax, nmax, ff, interval=2):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    plt.plot(x, q, marker='o', lw=2, label='n=0')

    ## 初期化
    delta = np.zeros(jmax) # 物理量の増分値
    flux  = np.zeros(jmax) # 数値流束
    g     = np.zeros(jmax) # 流速の急激な変化を防ぐ修正項

    for n in range(1, nmax + 1):
        qold = q.copy()
        for j in range(0, jmax - 1):
            delta[j] = qold[j + 1] - qold[j]
        for j in range(1, jmax - 1):
            g[j] = minmod(delta[j], delta[j-1])
        for j in range(0, jmax - 1):
            flux[j] = ff(qold, c, delta, g, dt, dx, j)
        
        ## メインの物理量計算
        for j in range(1, jmax - 1):
            q[j] = qold[j] - dt / dx * (flux[j] - flux[j - 1])

        if n % interval == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()

def do_computing_mc(x, q, c, dt, dx, jmax, nmax, interval=2):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    plt.plot(x, q, marker='o', lw=2, label='n=0')

    for n in range(1, nmax + 1):
        qbar = q.copy()

        # MacCormack法
        for j in range(0, jmax - 1):
            qbar[j] = q[j] - dt * c * (q[j + 1] - q[j]) / dx
        
        for j in range(1, jmax - 1):
            q[j] = 0.5 * ((q[j] + qbar[j]) - dt * c * (qbar[j] - qbar[j - 1]) / dx)

        if n % interval == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n={n}')

    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()




def TVD(q, c, delta, g, dt, dx, j):
    sigma = 0.5 * (np.abs(c) - dt / dx * c **2)
    gamma = sigma * (g[j + 1] - g[j]) * delta[j] / (delta[j] ** 2 + 1e-12)
    phi   = sigma * (g[j] + g[j + 1]) - abs(c + gamma) * delta[j]

    ur = q[j + 1]
    ul = q[j]
    fr = c * ur
    fl = c * ul
    return 0.5 * (fr + fl + phi)

c  = 1.0
dt = 0.05
dx = 0.1
nmax = 20
jmax = 21

q1 = 1
q2 = 0

x, q = init(q1, q2, dx, jmax, sp=0.05)
#do_computing2(x, q, c, dt, dx, jmax, nmax, TVD, interval=4)
do_computing_mc(x, q, c, dt, dx, jmax, nmax, interval=4)







