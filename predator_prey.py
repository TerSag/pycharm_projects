import matplotlib.pyplot as plt


def get_dH(H, W, alpha, beta):
    return alpha * H - beta * H * W


def get_dW(H, W, delta, gamma):
    return delta * H * W - gamma * W


def main():
    H = 10.0
    W = 5.0
    alpha = 1.1
    beta = 0.4
    delta = 0.1
    gamma = 0.4
    dt = 0.05
    t_max = 100.0

    t_values = [0.0]
    H_values = [H]
    W_values = [W]

    t = 0.0

    while t < t_max:
        dH = get_dH(H, W, alpha, beta)
        dW = get_dW(H, W, delta, gamma)

        H = H + dH * dt
        W = W + dW * dt
        t = t + dt

        t_values.append(t)
        H_values.append(H)
        W_values.append(W)

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.plot(t_values, H_values, label='Зайці (Жертви)', color='blue', linewidth=2)
    plt.plot(t_values, W_values, label='Вовки (Хижаки)', color='red', linewidth=2)
    plt.title('Зміна популяцій у часі')
    plt.xlabel('Час (t)')
    plt.ylabel('Чисельність популяції')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(H_values, W_values, color='green', linewidth=1.5)
    plt.title('Фазовий портрет системи')
    plt.xlabel('Чисельність зайців (H)')
    plt.ylabel('Чисельність вовків (W)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()