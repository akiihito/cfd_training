import numpy as np
import matplotlib.pyplot as plt

nmax = 400 ## 時間

dx = dy = 0.05 ## 空間分割粒度

M = 0.5    ## 一様流マッハ数（< 1.0）
Uinf = 0.1 ## 主流（一様流）

alpha2 = 1 - M ** 2

## 解析境界（start, end）
#xs, xe = -5.0, 6.0
#ys, ye = 0.0, 5.0
xs, xe = -1.0, 2.0
ys, ye = 0.0, 1.0

x_le, x_te = 0.0, 1.0 ## 翼の前縁(leading edge)と後縁（trailing edge）

jmax = int((xe - xs) / dx) + 1 ## x 方向の分割数
kmax = int((ye - ys) / dy) + 1 ## y 方向の分割数

j_le = int((x_le - xs) / dx)     ## x軸上の前縁の位置
j_te = int((x_te - xs) / dx) + 1 ## x軸上の後縁の位置

x = np.linspace(xs, xe, jmax)
y = np.linspace(ys, ye, kmax)

phi = np.zeros([jmax, kmax]) ## 速度ポテンシャル
u = np.zeros([jmax, kmax])   ## X方向の速度
v = np.zeros([jmax, kmax])   ## Y方向の速度

## 翼のある場所では、翼の断面関数にしたがって傾きを計算しておく
## max: 1.2, min: -1.2
dydx = np.array([0.4 * (1.0 - 2.0 * x[j]) if j_le <= j < j_te else 0.0 for j in range(jmax)])

X, Y = np.meshgrid(x, y) ## 可視化用格子点配列

residual = np.zeros(nmax) ## 残渣（これが nmax の時点で 0 に近づいていることが望ましい）


###################################################################
### 最初に速度ポテンシャル(phi)を計算する
for n in range(nmax):
    phiold = phi.copy()

    ## 境界条件（下辺は計算しないので境界条件を入れていない）
    phi[0, :] = 0.0      ## 左辺
    phi[jmax-1, :] = 0.0 ## 右辺
    phi[:, kmax-1] = 0.0 ## 上辺

    for j in range(jmax):
        phi[j, 0] = phi[j, 1] - dydx[j] * dy

    ## Gauss-Seidal 法
    for k in range(1, kmax - 1):
        for j in range(1, jmax - 1):
            phi[j, k] = 1.0 / (2.0 * alpha2 + 2.0) * (alpha2 * (phi[j-1, k] + phi[j+1, k]) + phi[j, k-1] + phi[j, k+1])

    residual[n] = np.sqrt(((phi-phiold) ** 2).sum() / (jmax * kmax))

###################################################################
### 速度ポテンシャル(phi)をベースに、各格子点の X 方向の速度を計算する
for j in range(1, jmax - 1):
    u[j, :] = Uinf * (1.0 + (phi[j + 1, :] - phi[j - 1, :]) / (2 * dx))
u[0, :] = Uinf * (1.0 + (phi[1, :] - phi[0, :]) / dx)
u[-1, :] = Uinf * (1.0 + (phi[-1, :] - phi[-2, :]) / dx)

###################################################################
### 速度ポテンシャル(phi)をベースに、各格子点の Y 方向の速度を計算する
for k in range(1, kmax - 1):
    v[:, k] = Uinf * (phi[:, k + 1] - phi[:, k - 1]) / (2 * dy)
v[:, 0] = Uinf * (phi[:, 1] - phi[:, 0]) / dy
v[:, -1] = Uinf * (phi[:, -1] - phi[:, -2]) /dy

## 最後に X, Y 方向の速度ベクトルから速度の大きさを計算
va = np.sqrt(u ** 2, v ** 2)


## 可視化
fig, ax1 = plt.subplots(figsize=(9, 3), dpi=100)
plt.rcParams["font.size"] = 22
cnt = plt.contourf(X, Y, va.transpose(1, 0), cmap='Greys', levels=100)


sty = np.arange(0.02, ye, 0.05)
stx = np.full(len(sty), -1.0)
startpoints = np.array([stx, sty]).transpose(1, 0)
plt.streamplot(X, Y, u.transpose(1, 0), v.transpose(1, 0), color="red", start_points=startpoints, linewidth=0.5, arrowstyle='->')
plt.xlabel('x')
plt.ylabel('y')
plt.xticks([xs, 0, 1, xe])
plt.subplots_adjust(left=0.17)
plt.show()



