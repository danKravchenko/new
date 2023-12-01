import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Початкові значення x та y для інтерполяції та регресії
x = [1, 2, 3, 4, 5, 6, 7, 8]
y = [56.9, 67.3, 81.6, 201, 240, 474, 490, 518]

# Ініціалізація змінних для розрахунків регресії
s_1 = 0
s_2 = 0
s_3 = 0
s_4 = 0
a = 0
b = 0

# Максимальна кількість точок для видалення
max_points = 3

# Флаги для відстеження останнього використаного методу
use_regression = False
use_interpolation = False

# Створення вікна та графіка
root = tk.Tk()
root.geometry("800x700")
root.title("Інтерполяція та регресія")

# Створення об'єктів для графіка
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def build_regression_line(a, b):
    y_regression = []
    for i in x:
        y_regression.append(a * i + b)
    return y_regression

def total_least_squares(s_1, s_2, s_3, s_4, a, b):
    # Розрахунок параметрів a та b методом найменших квадратів
    for i, j in zip(x, y):
        s_1 += i * j
        s_2 += i
        s_3 += j
        s_4 += i ** 2

    a = (len(x) * s_1 - s_2 * s_3) / (len(x) * s_4 - s_2 ** 2)
    b = (s_3 - (a * s_2)) / len(x)

    return s_1, s_2, s_3, s_4, a, b

def lagrange_interpolation(x, y, targetX):
    # Функція для інтерполяції методом Лагранжа
    result = []
    n = len(x)

    for target in targetX:
        interp_value = 0
        for i in range(n):
            term = y[i]
            for j in range(n):
                if j != i:
                    term *= (target - x[j]) / (x[i] - x[j])
            interp_value += term
        result.append(interp_value)

    return result

def build_graph(result=None):
    # Функція для побудови графіка
    ax.clear()
    ax.scatter(x, y, color='red', s=30, zorder=2, label='Експериментальні точки')
    ax.legend()
    ax.grid()

    if use_regression:
        if result is None:
            result = total_least_squares(s_1, s_2, s_3, s_4, a, b)
        update_result = build_regression_line(result[4], result[5])
        ax.plot(x, update_result, color='blue', zorder=0, alpha=0.8, label='Пряма регресії', linewidth=2.5)
    elif use_interpolation:
        if result is None:
            result = lagrange_interpolation(x, y, x)
        ax.plot(x, result, color='green', zorder=0, alpha=0.8, label='Пряма регресії', linewidth=2.5, linestyle='-')

    canvas.draw()

build_graph()

def res_total_least_squares():
    # Обчислення регресії методом найменших квадратів
    global use_regression, use_interpolation, s_1, s_2, s_3, s_4, a, b
    s_1, s_2, s_3, s_4, a, b = total_least_squares(s_1, s_2, s_3, s_4, a, b)
    use_regression = True
    use_interpolation = False
    build_graph()

def res_lagrange_interpolation():
    # Обчислення інтерполяції методом Лагранжа
    global use_regression, use_interpolation
    lagrange_result = lagrange_interpolation(x, y, x)
    use_regression = False
    use_interpolation = True
    build_graph(lagrange_result)

# Створення рамки для кнопок та поля введення
frame_buttons = tk.Frame(root, padx=30, pady=10)
frame_buttons.pack(side=tk.LEFT)

frame_entry = tk.Frame(root, padx=30, pady=10)
frame_entry.pack(side=tk.RIGHT)

# Створення кнопок для виклику функцій регресії та інтерполяції
button_regression = tk.Button(frame_buttons, text="Обчислити регресію", command=res_total_least_squares)
button_regression.pack()

button_interpolation = tk.Button(frame_buttons, text="Обчислити інтерполяцію", command=res_lagrange_interpolation)
button_interpolation.pack()

# Створення поля для введення координат
label_entry_x = tk.Label(frame_entry, text="X:")
label_entry_x.pack()

entry_x = tk.Entry(frame_entry)
entry_x.pack()

label_entry_y = tk.Label(frame_entry, text="Y:")
label_entry_y.pack()

entry_y = tk.Entry(frame_entry)
entry_y.pack()

def add_point():
    global max_points
    if max_points > 0:
        if not entry_x.get() and not entry_y.get():
            messagebox.showwarning("Попередження", "Будь ласка, заповніть обидва поля")
        elif not entry_x.get():
            messagebox.showwarning("Попередження", "Будь ласка, заповніть поле 'X'")
        elif not entry_y.get():
            messagebox.showwarning("Попередження", "Будь ласка, заповніть поле 'Y'")
        else:
            max_points -= 1
            x.append(float(entry_x.get()))
            y.append(float(entry_y.get()))
            build_graph()

def remove_point():
    global max_points
    if len(x) > 3:
        x.pop()
        y.pop()
        build_graph()

button_add_point = tk.Button(frame_entry, text="Додати точку", command=add_point)
button_add_point.pack()

button_remove_point = tk.Button(frame_entry, text="Видалити точку", command=remove_point)
button_remove_point.pack()

root.mainloop()
