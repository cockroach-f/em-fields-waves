# 公式速查

按章节整理全书最常用的公式。约定：时谐因子 $\mathrm e^{\je\omega t}$，复振幅取峰值；分界面法向 $\an$ 由媒质 2 指向媒质 1。

---

## 第 1 章 矢量分析与场论

| 内容 | 公式 |
|---|---|
| 点积 / 叉积 | $\vv A\cdot\vv B=AB\cos\theta$；$\vv A\times\vv B=\begin{vmatrix}\ax&\ay&\az\\A_x&A_y&A_z\\B_x&B_y&B_z\end{vmatrix}$ |
| 三重积 | $\vv A\cdot(\vv B\times\vv C)=\vv B\cdot(\vv C\times\vv A)$；$\vv A\times(\vv B\times\vv C)=\vv B(\vv A\cdot\vv C)-\vv C(\vv A\cdot\vv B)$ |
| 度量系数 $(h_1,h_2,h_3)$ | 直角 $(1,1,1)$；圆柱 $(1,\rho,1)$；球 $(1,r,r\sin\theta)$ |
| 梯度 | $\nabla u=\sum_i\dfrac{1}{h_i}\dfrac{\partial u}{\partial u_i}\vv a_i$；方向导数 $\dfrac{\partial u}{\partial l}=\nabla u\cdot\vv a_l$ |
| 散度 | $\nabla\cdot\vv F=\dfrac{1}{h_1h_2h_3}\sum_i\dfrac{\partial}{\partial u_i}\Big(\dfrac{h_1h_2h_3}{h_i}F_i\Big)$ |
| 圆柱 / 球散度 | $\dfrac1\rho\dfrac{\partial(\rho F_\rho)}{\partial\rho}+\dfrac1\rho\dfrac{\partial F_\phi}{\partial\phi}+\dfrac{\partial F_z}{\partial z}$；$\dfrac{1}{r^2}\dfrac{\partial(r^2F_r)}{\partial r}+\dfrac{1}{r\sin\theta}\dfrac{\partial(\sin\theta F_\theta)}{\partial\theta}+\dfrac{1}{r\sin\theta}\dfrac{\partial F_\phi}{\partial\phi}$ |
| 旋度 | $\nabla\times\vv F=\dfrac{1}{h_1h_2h_3}\begin{vmatrix}h_1\vv a_1&h_2\vv a_2&h_3\vv a_3\\\partial_1&\partial_2&\partial_3\\h_1F_1&h_2F_2&h_3F_3\end{vmatrix}$ |
| 散度定理 / 斯托克斯定理 | $\oint_S\vv F\cdot\dd\vv S=\int_V\nabla\cdot\vv F\dd V$；$\oint_l\vv F\cdot\dd\vv l=\int_S(\nabla\times\vv F)\cdot\dd\vv S$ |
| 零恒等式 | $\nabla\times\nabla u=\vv 0$；$\nabla\cdot(\nabla\times\vv A)=0$ |
| 拉普拉斯 | $\nabla^2u=\nabla\cdot\nabla u$；$\nabla^2\vv A=\nabla(\nabla\cdot\vv A)-\nabla\times\nabla\times\vv A$ |
| 亥姆霍兹定理 | $\vv F=-\nabla\phi+\nabla\times\vv A$ |

## 第 2 章 静电场和恒定电场

| 内容 | 公式 |
|---|---|
| 库仑定律 / 点电荷场 | $\vv F=\dfrac{q_1q_2}{4\pi\varepsilon_0R^2}\vv a_R$；$\vv E=\dfrac{q}{4\pi\varepsilon_0R^2}\vv a_R$ |
| 连续分布 | $\vv E=\dfrac{1}{4\pi\varepsilon_0}\int\dfrac{\vv a_R\dd q}{R^2}$；$\phi=\dfrac{1}{4\pi\varepsilon_0}\int\dfrac{\dd q}{R}$ |
| 无限长线电荷 / 无限大面电荷 | $E=\dfrac{\rho_l}{2\pi\varepsilon_0\rho}$；$E=\dfrac{\rho_S}{2\varepsilon_0}$ |
| 基本方程 | $\nabla\cdot\vv D=\rho_V$，$\nabla\times\vv E=\vv 0$；$\oint\vv D\cdot\dd\vv S=q$，$\oint\vv E\cdot\dd\vv l=0$ |
| 电位 | $\vv E=-\nabla\phi$；$\nabla^2\phi=-\rho_V/\varepsilon$；$U_{AB}=\int_A^B\vv E\cdot\dd\vv l=\phi_A-\phi_B$ |
| 电偶极子 | $\phi=\dfrac{p\cos\theta}{4\pi\varepsilon_0r^2}$；$\vv E=\dfrac{p}{4\pi\varepsilon_0r^3}(2\cos\theta\ar+\sin\theta\atheta)$ |
| 介质 | $\vv D=\varepsilon_0\vv E+\vv P=\varepsilon\vv E$；$\rho_b=-\nabla\cdot\vv P$，$\rho_{Sb}=\vv P\cdot\an$ |
| 边界条件 | $\an\cdot(\vv D_1-\vv D_2)=\rho_S$，$\an\times(\vv E_1-\vv E_2)=\vv 0$；$\dfrac{\tan\theta_1}{\tan\theta_2}=\dfrac{\varepsilon_1}{\varepsilon_2}$ |
| 电容 | 平板 $\dfrac{\varepsilon S}{d}$；同轴 $\dfrac{2\pi\varepsilon l}{\ln(b/a)}$；同心球 $\dfrac{4\pi\varepsilon ab}{b-a}$；孤立球 $4\pi\varepsilon a$ |
| 静电能量 | $W_e=\dfrac12\int\rho_V\phi\dd V=\dfrac12\int\vv D\cdot\vv E\dd V=\dfrac12CU^2$；$\vv F=-\nabla W_e|_{q}$ |
| 恒定电场 | $\vv J=\sigma\vv E$，$\nabla\cdot\vv J=0$；$J_{1n}=J_{2n}$；$p=\vv J\cdot\vv E$ |
| 静电比拟 | $\dfrac{C}{G}=\dfrac{\varepsilon}{\sigma}$；半球接地体 $R=\dfrac{1}{2\pi\sigma a}$ |

## 第 3 章 边值问题的解法

| 内容 | 公式 |
|---|---|
| 唯一性定理 | 方程 + 全部边界上的 $\phi$ 或 $\partial\phi/\partial n$ ⇒ 解唯一 |
| 接地平面镜像 | $q$ 在 $h$ 处 → $-q$ 在 $-h$ 处 |
| 介质平面镜像 | $q'=\dfrac{\varepsilon_1-\varepsilon_2}{\varepsilon_1+\varepsilon_2}q$，$q''=\dfrac{2\varepsilon_2}{\varepsilon_1+\varepsilon_2}q$ |
| 接地导体球镜像 | $q'=-\dfrac adq$，距球心 $d'=\dfrac{a^2}{d}$ |
| 导体劈（夹角 $\pi/n$） | $2n-1$ 个镜像，正负交替 |
| 平行双导线电轴 | $b=\sqrt{(D/2)^2-a^2}$；$C_0=\dfrac{\pi\varepsilon}{\ln\big[(D/2a)+\sqrt{(D/2a)^2-1}\big]}\approx\dfrac{\pi\varepsilon}{\ln(D/a)}$ |
| 直角坐标分离变量 | $X''+k_x^2X=0$，$k_x^2+k_y^2=0$：一个方向取三角函数，另一个取双曲 / 指数函数 |
| 圆柱坐标 | $\phi=A_0+B_0\ln\rho+\sum(A_n\rho^n+B_n\rho^{-n})(C_n\cos n\phi+D_n\sin n\phi)$ |
| 有限差分（五点） | $\phi_0=\dfrac14(\phi_1+\phi_2+\phi_3+\phi_4)$；SOR：$\phi^{(k+1)}=\phi^{(k)}+\dfrac{\omega}{4}R$，$1<\omega<2$ |

## 第 4 章 恒定电流的磁场

| 内容 | 公式 |
|---|---|
| 毕奥–萨伐尔定律 | $\vv B=\dfrac{\mu_0}{4\pi}\oint\dfrac{I\dd\vv l\times\vv a_R}{R^2}$ |
| 典型结果 | 长直导线 $\dfrac{\mu_0I}{2\pi\rho}$；圆环中心 $\dfrac{\mu_0I}{2a}$；螺线管 $\mu_0nI$；面电流 $\dfrac{\mu_0}{2}\vv J_S\times\an$ |
| 基本方程 | $\nabla\cdot\vv B=0$，$\nabla\times\vv H=\vv J$；$\oint\vv H\cdot\dd\vv l=I$ |
| 磁矢位 | $\vv B=\nabla\times\vv A$，$\nabla^2\vv A=-\mu\vv J$，$\vv A=\dfrac{\mu}{4\pi}\int\dfrac{\vv J\dd V}{R}$；$\Phi=\oint\vv A\cdot\dd\vv l$ |
| 磁偶极子 | $\vv p_m=I\vv S$；$\vv B=\dfrac{\mu_0p_m}{4\pi r^3}(2\cos\theta\ar+\sin\theta\atheta)$ |
| 磁介质 | $\vv B=\mu_0(\vv H+\vv M)=\mu\vv H$；$\vv J_b=\nabla\times\vv M$，$\vv J_{Sb}=\vv M\times\an$ |
| 边界条件 | $\an\cdot(\vv B_1-\vv B_2)=0$，$\an\times(\vv H_1-\vv H_2)=\vv J_S$ |
| 电感 | $L=\Psi/I$；直导线内自感 $\dfrac{\mu_0}{8\pi}$；同轴线外自感 $\dfrac{\mu}{2\pi}\ln\dfrac ba$；双线 $\dfrac{\mu}{\pi}\ln\dfrac{D-a}{a}$ |
| 磁场能量 | $W_m=\dfrac12LI^2=\dfrac12\int\vv B\cdot\vv H\dd V$，$w_m=\dfrac{B^2}{2\mu}$ |
| 三种静态场的对偶 | $\vv E\leftrightarrow\vv H$，$\vv D\leftrightarrow\vv B$，$\varepsilon\leftrightarrow\mu$；$C\leftrightarrow L$；同一结构 $L_0C_0=\mu\varepsilon$ |

## 第 5 章 时变电磁场与电磁波

| 内容 | 公式 |
|---|---|
| 法拉第定律 | $\mathscr E=-\dfrac{\dd\Psi}{\dd t}$；$\nabla\times\vv E=-\dfrac{\partial\vv B}{\partial t}$；动生 $\mathscr E=\oint(\vv v\times\vv B)\cdot\dd\vv l$ |
| 位移电流 | $\vv J_d=\dfrac{\partial\vv D}{\partial t}$；$\nabla\cdot\Big(\vv J+\dfrac{\partial\vv D}{\partial t}\Big)=0$ |
| 麦克斯韦方程组 | $\nabla\times\vv H=\vv J+\dfrac{\partial\vv D}{\partial t}$，$\nabla\times\vv E=-\dfrac{\partial\vv B}{\partial t}$，$\nabla\cdot\vv B=0$，$\nabla\cdot\vv D=\rho_V$ |
| 时变边界条件 | $\an\times(\vv E_1-\vv E_2)=\vv 0$，$\an\times(\vv H_1-\vv H_2)=\vv J_S$，$B_{1n}=B_{2n}$，$D_{1n}-D_{2n}=\rho_S$ |
| 理想导体表面 | $\an\times\vv E=\vv 0$，$\an\times\vv H=\vv J_S$，$\an\cdot\vv B=0$，$\an\cdot\vv D=\rho_S$ |
| 坡印廷定理 | $-\oint_S(\vv E\times\vv H)\cdot\dd\vv S=\dfrac{\dd}{\dd t}\int_V\Big(\dfrac12\vv E\cdot\vv D+\dfrac12\vv H\cdot\vv B\Big)\dd V+\int_V\vv J\cdot\vv E\dd V$ |
| 相量 | $\vv E(\vv r,t)=\Re[\dot{\vv E}(\vv r)\mathrm e^{\je\omega t}]$；$\partial/\partial t\to\je\omega$；$\nabla\times\dot{\vv H}=\dot{\vv J}+\je\omega\varepsilon\dot{\vv E}$ |
| 平均坡印廷矢量 | $\vv S_{\text{av}}=\dfrac12\Re[\dot{\vv E}\times\dot{\vv H}^*]$ |
| 波动方程 | $\nabla^2\vv E-\mu\varepsilon\dfrac{\partial^2\vv E}{\partial t^2}=\vv 0$；亥姆霍兹 $\nabla^2\dot{\vv E}+k^2\dot{\vv E}=\vv 0$，$k=\omega\sqrt{\mu\varepsilon}$ |

## 第 6 章 平面电磁波

| 内容 | 公式 |
|---|---|
| 无耗媒质 | $\vv E=\ax E_0\mathrm e^{-\je kz}$，$\vv H=\ay\dfrac{E_0}{\eta}\mathrm e^{-\je kz}$；$v_p=\dfrac{1}{\sqrt{\mu\varepsilon}}$，$\lambda=\dfrac{2\pi}{k}$，$\eta=\sqrt{\dfrac\mu\varepsilon}$，$\eta_0=120\pi\ \Omega$ |
| 任意方向 | $\vv E=\vv E_0\mathrm e^{-\je\vv k\cdot\vv r}$，$\vv H=\dfrac1\eta\vv a_k\times\vv E$；$\vv S_{\text{av}}=\dfrac{|E_0|^2}{2\eta}\vv a_k$ |
| 复介电常数 | $\varepsilon_c=\varepsilon-\je\dfrac{\sigma}{\omega}$；$\tan\delta=\dfrac{\sigma}{\omega\varepsilon}$ |
| 导电媒质 | $\gamma=\je\omega\sqrt{\mu\varepsilon_c}=\alpha+\je\beta$；$\eta_c=\sqrt{\mu/\varepsilon_c}=|\eta_c|\mathrm e^{\je\psi}$ |
| 低损耗 | $\alpha\approx\dfrac\sigma2\sqrt{\dfrac\mu\varepsilon}$，$\beta\approx\omega\sqrt{\mu\varepsilon}$ |
| 良导体 | $\alpha=\beta=\sqrt{\pi f\mu\sigma}$，$\delta=\dfrac1\alpha$，$\eta_c=(1+\je)\sqrt{\dfrac{\pi f\mu}{\sigma}}$，$R_S=\dfrac{1}{\sigma\delta}$ |
| 极化 | $\Delta\varphi=\varphi_y-\varphi_x$：$0,\pm\pi$ 线极化；等幅且 $\pm\pi/2$ 圆极化；$+z$ 传播时 $-\pi<\Delta\varphi<0$ 右旋 |
| 群速 | $v_g=\dfrac{\dd\omega}{\dd\beta}=\dfrac{v_p}{1-\dfrac{\omega}{v_p}\dfrac{\dd v_p}{\dd\omega}}$ |
| 垂直入射 | $R=\dfrac{\eta_2-\eta_1}{\eta_2+\eta_1}$，$T=\dfrac{2\eta_2}{\eta_2+\eta_1}=1+R$；$S=\dfrac{1+|R|}{1-|R|}$ |
| 理想导体前的驻波 | $\vv E_1=-\ax\je2E_0\sin\beta z$，$\vv H_1=\ay\dfrac{2E_0}{\eta_1}\cos\beta z$ |
| 斜入射 | $\theta_r=\theta_i$，$k_1\sin\theta_i=k_2\sin\theta_t$ |
| 菲涅耳公式 | $R_\perp=\dfrac{\eta_2\cos\theta_i-\eta_1\cos\theta_t}{\eta_2\cos\theta_i+\eta_1\cos\theta_t}$，$R_\parallel=\dfrac{\eta_1\cos\theta_i-\eta_2\cos\theta_t}{\eta_1\cos\theta_i+\eta_2\cos\theta_t}$ |
| 全反射 / 全透射 | $\theta_c=\arcsin\sqrt{\varepsilon_2/\varepsilon_1}$；$\theta_B=\arctan\sqrt{\varepsilon_2/\varepsilon_1}$（只对平行极化） |
| 多层介质与传输线类比 | 夹层输入波阻抗 $Z(-d)=\eta_2\dfrac{\eta_3\cos\beta_2 d+\je\eta_2\sin\beta_2 d}{\eta_2\cos\beta_2 d+\je\eta_3\sin\beta_2 d}$，$R=\dfrac{Z(-d)-\eta_1}{Z(-d)+\eta_1}$；半波窗（$\eta_1=\eta_3$、$d=n\lambda_2/2$）全透射；$\lambda/4$ 匹配层（$d=(2n+1)\lambda_2/4$、$\eta_2=\sqrt{\eta_1\eta_3}$）无反射 |

## 第 7 章 传输线

约定：$z$ 从负载量起，指向电源；$R_0,L_0,G_0,C_0$ 为单位长度分布参数。

| 内容 | 公式 |
|---|---|
| 电报方程 | $\dfrac{\dd U}{\dd z}=(R_0+\je\omega L_0)I$，$\dfrac{\dd I}{\dd z}=(G_0+\je\omega C_0)U$ |
| 通解 | $U(z)=A_1\mathrm e^{\gamma z}+A_2\mathrm e^{-\gamma z}$，$I(z)=\dfrac{1}{Z_0}(A_1\mathrm e^{\gamma z}-A_2\mathrm e^{-\gamma z})$ |
| 特性阻抗 | $Z_0=\sqrt{\dfrac{R_0+\je\omega L_0}{G_0+\je\omega C_0}}$；无耗 $Z_0=\sqrt{L_0/C_0}$ |
| 传播常数 | $\gamma=\sqrt{(R_0+\je\omega L_0)(G_0+\je\omega C_0)}=\alpha+\je\beta$；低耗 $\alpha=\dfrac{R_0}{2Z_0}+\dfrac{G_0Z_0}{2}$，$\beta=\omega\sqrt{L_0C_0}$ |
| 相速、线上波长 | $v_p=\dfrac{\omega}{\beta}=\dfrac{c}{\sqrt{\varepsilon_r}}$，$\lambda_g=\dfrac{\lambda_0}{\sqrt{\varepsilon_r}}$ |
| 反射系数 | $\Gamma_L=\dfrac{Z_L-Z_0}{Z_L+Z_0}=\lvert\Gamma_L\rvert\mathrm e^{\je\phi_L}$，$\Gamma(z)=\Gamma_L\mathrm e^{-\je2\beta z}$ |
| 输入阻抗 | $Z_{\mathrm{in}}(z)=Z_0\dfrac{Z_L+\je Z_0\tan\beta z}{Z_0+\je Z_L\tan\beta z}=Z_0\dfrac{1+\Gamma(z)}{1-\Gamma(z)}$ |
| 驻波比、行波系数 | $\rho=\dfrac{1+\lvert\Gamma_L\rvert}{1-\lvert\Gamma_L\rvert}$，$K=\dfrac1\rho$，$\lvert\Gamma_L\rvert=\dfrac{\rho-1}{\rho+1}$ |
| 波腹、波节 | $z_{\max}=\dfrac{\lambda}{4\pi}\phi_L+n\dfrac\lambda2$，$R_{\max}=Z_0\rho$；$z_{\min}=z_{\max}+\dfrac\lambda4$，$R_{\min}=\dfrac{Z_0}{\rho}$ |
| 由测量求负载 | $Z_L=Z_0\dfrac{1-\je\rho\tan\beta l_{\min1}}{\rho-\je\tan\beta l_{\min1}}$ |
| 短路线 / 开路线 | $Z_{\mathrm{in}}=\je Z_0\tan\beta l$；$Z_{\mathrm{in}}=-\je Z_0\cot\beta l$ |
| $\lambda/2$、$\lambda/4$ | $Z_{\mathrm{in}}(z+\lambda/2)=Z_{\mathrm{in}}(z)$；$Z_{\mathrm{in}}(z)\,Z_{\mathrm{in}}(z+\lambda/4)=Z_0^2$ |
| Smith 圆图 | $\Gamma=\dfrac{\bar Z-1}{\bar Z+1}$；电阻圆圆心 $\big(\frac{r}{1+r},0\big)$、半径 $\frac{1}{1+r}$；电抗圆圆心 $\big(1,\frac1x\big)$、半径 $\frac{1}{\lvert x\rvert}$；向电源顺时针 |
| 传输效率 | $\eta=\dfrac{1-\lvert\Gamma_L\rvert^2}{\mathrm e^{2\alpha l}-\lvert\Gamma_L\rvert^2\mathrm e^{-2\alpha l}}$，匹配时 $\mathrm e^{-2\alpha l}$ |
| 损耗 | $\alpha_c=\dfrac{R_0}{2Z_0}$，$\alpha_d=\dfrac{G_0Z_0}{2}=\dfrac{\pi\sqrt{\varepsilon_r}}{\lambda}\tan\delta$ |
| 功率容量 | $P_{\max}=\dfrac{U_M^2}{2\rho Z_0}$ |
| 双导线 / 同轴线 | $Z_0=\dfrac{120}{\sqrt{\varepsilon_r}}\ln\dfrac{2D}{d}$；$Z_0=\dfrac{60}{\sqrt{\varepsilon_r}}\ln\dfrac ba$；同轴单模 $\lambda_{\min}>\pi(a+b)$ |
| 微带线 | $\varepsilon_e=1+q(\varepsilon_r-1)$，$q=\dfrac12\Big[1+\Big(1+\dfrac{12h}{w}\Big)^{-1/2}\Big]$；$Z_0=\dfrac{Z_0^a}{\sqrt{\varepsilon_e}}$，$\lambda_g=\dfrac{\lambda_0}{\sqrt{\varepsilon_e}}$ |
| 匹配 | $\lambda/4$ 变换器 $Z_{01}=\sqrt{Z_0R_L}$（复负载：波腹处 $Z_0\sqrt\rho$，波节处 $Z_0/\sqrt\rho$）；共轭匹配 $Z_{\mathrm{in}}=Z_g^*$，$P_{\max}=\dfrac{\lvert E_g\rvert^2}{8R_g}$ |

## 第 10 章 无线信道、电磁干扰与电磁兼容

| 内容 | 公式 |
|---|---|
| 弗里斯公式 | $P_r=P_{\mathrm{in}}G_tG_r\Big(\dfrac{\lambda}{4\pi r}\Big)^2$，有效接收面积 $A_e=\dfrac{\lambda^2}{4\pi}G_r$ |
| 自由空间损耗 | $L_{bf}=32.45+20\lg f_{\mathrm{MHz}}+20\lg r_{\mathrm{km}}$ dB（各向同性天线；有增益时再减 $G_t$、$G_r$ 的 dB 值） |
| 信道损耗 | $L_b=L_{bf}-A$，$A=20\lg\lvert E/E_0\rvert$ dB |
| 多普勒频移 | $f_D=\dfrac v\lambda\cos\theta$（$\theta$ 为运动方向与来波方向的夹角），最大多普勒频移 $f_m=v/\lambda$；深衰落间隔 $\approx\lambda/(2v)=1/(2f_m)$ |
| 多径容许带宽 | $\Delta f\approx\dfrac1\tau$（$\tau$ 为最大多径时延差） |
| 视线距离 | $r_v=3.57(\sqrt{h_1}+\sqrt{h_2})$ km；计入大气折射 $r_v=4.12(\sqrt{h_1}+\sqrt{h_2})$ km（$h$ 以 m 计） |
| 两径模型 | 程差 $\Delta r\approx 2h_1h_2/d$；掠入射 $R\approx-1$ 时路径因子 $\lvert F\rvert=2\Big\lvert\sin\dfrac{2\pi h_1h_2}{\lambda d}\Big\rvert$ |
| 两径远区（$1/d^4$） | 转折距离 $d_b=4h_1h_2/\lambda$；$d>d_b$ 时 $\lvert F\rvert\approx 4\pi h_1h_2/(\lambda d)$，接收功率 $P_r\approx P_{\mathrm{in}}G_tG_r h_1^2h_2^2/d^4$ |
| 第一菲涅耳区 | 半径 $F_1=\sqrt{\dfrac{\lambda d_1d_2}{d_1+d_2}}$，$F_n=\sqrt n\,F_1$；余隙 $\ge 0.6F_1$ 时可忽略绕射附加损耗 |
| 电离层 | $\varepsilon_r=1-\dfrac{80.8N}{f^2}$；垂直入射可反射的最高频率 $f_c=\sqrt{80.8N_{\max}}$ |
| 正割定律 | $f_{\max}=\sqrt{80.8N_{\max}}\sec\theta_0$；最佳工作频率 $f_{\mathrm{opt}}=0.85f_{\max}$ |
| 静区 | $\theta_{0\min}=\arcsin\sqrt{1-\dfrac{80.8N_{\max}}{f^2}}$ |
| 电磁兼容安全系数 | $m=P_s-P_I$（dB），$m>0$ 才兼容 |
| 屏蔽效能 | $\mathrm{SE}=20\lg(E_{\mathrm{inc}}/E_{\mathrm t})=\mathrm{SE}_a+\mathrm{SE}_r$；吸收 $\mathrm{SE}_a=8.686\,t/\delta$ dB，平面波反射 $\mathrm{SE}_r\approx 20\lg\dfrac{\eta_0}{4\lvert\eta_c\rvert}$，$\delta=1/\sqrt{\pi f\mu\sigma}$ |
| 接地方式 | $f<1$ MHz 单点接地；$f>10$ MHz 多点接地；其间混合接地 |
