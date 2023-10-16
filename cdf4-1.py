import numpy as np
import matplotlib.pyplot as plt


def init(jmax):
    x = np.linspace(0, 1, jmax)
    q = np.sin(np.pi * x)
    return x, q

def do_computing(x, q, a, dt, dx, jmax, nmax, interval=2):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    plt.plot(x, q, marker='o', lw=2, label='n = 0')

    for n in range(1, nmax + 1):
        qold = q.copy()

        for j in range(1, jmax - 1):
            dq = a * dt * (qold[j+1] - 2.0 * qold[j] + qold[j-1]) / (dx ** 2)
            q[j] = qold[j] + dq

        ## 境界条件
        q[0]  = 0
        q[-1] = 0

        if n % interval == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n = {n}')

    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlim([0, 1])
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()

jmax = 11
nmax = 30

dt = 0.01
dx = 0.2
# a * dt / (dx ** 2) <= 5
a = 2

x, q = init(jmax)
do_computing(x, q, a, dt, dx, jmax, nmax, interval = 4)
