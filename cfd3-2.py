import matplotlib.pyplot as plt
import numpy as np

def init(q1, q2, xs, dx, jmax):
    x = np.linspace(xs, xs + dx * (jmax-1), jmax)
    q = np.array([float(q1) if i < 0.0 else float(q2) for i in x])
    return x, q


# 1次精度風上法（cの伝搬方向がわからない場合）
def UPWIND1(alf, q, c, dt, dx, jmax):
    for j in range(0, jmax - 1):
        ur, ul = q[j+1], q[j]
        fr, fl = c * ur, c * ul
        alf[j] = 0.5 * (fr + fl - abs(c) * (ur - ul)) # 式2.34
        ## 元の配列を参照しているので、return していない


def do_computing_LDU(x, q, c, dt, dx, nmax, jmax, ff, interval=2, xlim=None):
    plt.figure(figsize=(7,7), dpi=100)
    plt.rcParams["font.size"] = 22

    # 初期分布
    plt.plot(x, q, marker='o', lw=2, label='n = 0')

    # 配列の初期化
    alf = np.zeros(jmax)
    dq = np.zeros(jmax)

    for n in range(1, nmax + 1):
        qold = q.copy()

        # 近似 LDU 分解
        c_a = abs(c)
        c_p = 0.5 * (c + c_a)
        c_n = 0.5 * (c - c_a)
        nu_a = c_a * dt / dx
        nu_p = c_p * dt / dx
        nu_n = c_n * dt / dx

        ff(alf, qold, c, dt, dx, jmax)
        R = np.append(0.0, np.diff(alf) / dx) # np.diff: a[i+1] - a[i]

        ## スイープの途中で dt が変るとまずいので、ループと連動させる必要あり？

        ## 第１スイープ
        for j in range(1, jmax - 1):
            # dq means q^* in this loop
            dq[j] = (-dt * R[j] + nu_p * dq[j-1]) / (1 + nu_a)

        ## 第２，第３スイープ
        for j in range(jmax - 2, 0, -1):
            dq[j] = dq[j] - nu_n * dq[j+1] / (1 + nu_a)

        ## delta_p = q(n+1) - q(n) => q(n+1) = q(n) + delta_p
        for j in range(1, jmax - 1):
            q[j] = qold[j] + dq[j]

        if n % interval == 0:
            plt.plot(x, q, marker='o', lw=2, label=f'n = {dt * n : .1f}')

    plt.grid(color='black', linestyle='dashed', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('q')
    if xlim is not None:
        plt.xlim(xlim)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    c = 1
    dt = 0.05
    dx = 0.1

    q1 = 1
    q2 = 0

    xs = -1

    jmax = 70
    nmax = 50

    x, q = init(q1, q2, xs, dx, jmax)
    do_computing_LDU(x, q, c, dt, dx, nmax, jmax, UPWIND1, interval=16, xlim=[-1, 5])