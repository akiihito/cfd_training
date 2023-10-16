import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import matplotlib.animation as animation


c = 1.0 # x 方向の輸送速度
d = 1.0 # y 方向の輸送速度

dt = 0.05 # ステップ時間
dx = 0.1  # x の格子幅
dy = 0.1  # y の格子幅

jmax = 41 # x の最大値
kmax = 41 # y の最大値
nmax = 30 # t の最大値


def init(dx, dy, jmax, kmax):
    x = np.linspace(0, dx * (jmax-1), jmax)
    y = np.linspace(0, dy * (kmax-1), kmax)
    q = init_q(x, y, jmax, kmax)
    return x, y, q

def init_q(x, y, jmax, kmax):
    ## 多次元正規分布の計算
    ## https://qiita.com/c60evaporator/items/d53053358105b0117f2c
    def gausfunc(x, y, mu, V):
        detV = np.linalg.det(V) # 行列式 ad-bc の計算
        invV = np.linalg.inv(V) # 逆行列の計算
        A = 1.0 / (2 * np.pi * np.sqrt(detV))
        # np.arrayの None は np.newaxis のエイリアスで次元数拡張を表す
        # mu[:, None, None]は１次元[a, b, c]から３次元行列への拡張
        # dX[:, :, None]は 3次元行列から 4次元行列への拡張
        # invV[None, None]は 2次元行列から 4次元行列への拡張
        # np.arrayの 0 は np.squeeze のエイリアスで次元数縮退を表す
        # a[:, :, 0, 0]は 4次元行列から 2次元行列への縮退
        # @ は行列の掛け算
        # transpose は転置行列(0, 1, 2)->(1, 2, 0)への変換
        dX = (np.array([x, y]) - mu[:, None, None]).transpose(1, 2, 0)
        return A * np.exp(-0.5 * dX[:, :, None] @ invV[None, None] @ dX[:, :, :, None])

    mu = np.array([dx * jmax / 4, dy * kmax / 4])
    V  = np.array([[dx * jmax / 40, 0], [0, dy * kmax / 40]])
    X, Y = np.meshgrid(x, y) 
    a = gausfunc(X, Y, mu, V)
    q = a[:, :, 0, 0]
    return q


def do_computing(x, y, q, dt, dx, dy, nmax, interval=2):
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(10, 7), dpi=100)
    plt.rcParams["font.size"] = 10

    ims = []

    ax1 = fig.add_subplot(1, 1, 1, projection='3d')
    #ax1.plot_wireframe(X, Y, q, color="black", rstride=1, cstride=1, linewidth=0.5)
    surf = ax1.plot_surface(X, Y, q, antialiased=True, cmap="bwr", vmax=np.max(q))
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    fig.colorbar(surf)
    ims.append([surf])

    for n in range(1, nmax + 1):
        qold = q.copy()
        for j in range(1, jmax - 1):
            for k in range(1, kmax - 1):
                # 式（2.57）
                q[j][k] = qold[j][k] - dt / dx * (
                    c * (qold[j][k] - qold[j-1][k]) + d * (qold[j][k] - qold[j][k-1])
                )

        if n % interval == 0:
            #ax1.plot_wireframe(X, Y, q, color="black", rstride=1, cstride=1, linewidth=0.5)
            surf = ax1.plot_surface(X, Y, q, antialiased=True, cmap="bwr", vmax=np.max(q))
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ims.append([surf])


    #アニメの生成
    ani = animation.ArtistAnimation(fig, ims, interval=100)

    #保存
    ani.save('wf_anim_art.mp4',writer='ffmpeg',dpi=100)


x, y, q = init(dx, dy, jmax, kmax)
do_computing(x, y, q, dt, dx, dy, nmax, interval=2)