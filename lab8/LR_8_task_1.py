import numpy as np
import tensorflow as tf

# Параметри моделі
n_samples = 1000  # Кількість зразків
batch_size = 100  # Розмір міні-батча
num_steps = 20000  # Кількість ітерацій навчання

# Генерація вхідних даних
# Створюємо 1000 випадкових точок рівномірно на інтервалі [1; 10]
X_data = np.random.uniform(1, 10, (n_samples, 1)).astype(np.float32)
# Розрахунок y за формулою: y = 2x + 1 + шум (N(0, 2))
y_data = (2 * X_data + 1 + np.random.normal(0, 2, (n_samples, 1))).astype(np.float32)

# Ініціалізація параметрів моделі
# Змінна k (нахил), ініціалізована випадковим нормальним розподілом
k = tf.Variable(tf.random.normal((1, 1)), name='slope')
# Змінна b (зсув), ініціалізована нулем
b = tf.Variable(tf.zeros((1,)), name='bias')

# Передбачення: y = kx + b
y_pred = tf.matmul(X_data, k) + b

# Ініціалізація оптимізатора (стохастичний градієнтний спуск)
optimizer = tf.optimizers.SGD(learning_rate=0.0001)

# Кількість ітерацій для відображення проміжних результатів
display_step = 100

# Навчання моделі
for i in range(num_steps):
    # Вибір випадкового підмножини даних (міні-батч)
    indices = np.random.choice(n_samples, batch_size)
    X_batch, y_batch = X_data[indices], y_data[indices]

    # Відстеження градієнтів за допомогою GradientTape
    with tf.GradientTape() as tape:
        # Передбачення для поточного міні-батча
        y_pred = tf.matmul(X_batch, k) + b
        # Обчислення функції втрат: сума квадратів відхилень
        loss_val = tf.reduce_sum((y_batch - y_pred) ** 2)

    # Перевірка на випадок NaN у втраті
    if np.isnan(loss_val.numpy()):
        print(f"NaN value was found on step: {i + 1}")
        break

    # Обчислення градієнтів і оновлення параметрів моделі
    gradients = tape.gradient(loss_val, [k, b])
    optimizer.apply_gradients(zip(gradients, [k, b]))

    # Виведення інформації кожні display_step ітерацій
    if (i + 1) % display_step == 0:
        print(f'Епоха {i + 1}: {loss_val.numpy():.8f}, k={k.numpy()[0][0]:.4f}, b={b.numpy()[0]:.4f}')