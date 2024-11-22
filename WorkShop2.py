import gspread
import numpy as np

# Подключение к Google Sheets
gc = gspread.service_account(filename='unitydatascience-442516-75e88216de80.json')
sh = gc.open("AD_GameDev")

# Генерация данных
health = np.random.randint(0, 30, 10)
time_health = list(range(0, 10))
i = 1  # Начало со строки ниже

damage = np.random.randint(1, 15, 10)

# Основной цикл
while i <= len(time_health) + 1:  # Учёт сдвига на 2 строки
    current_health = health[i - 2] - damage[i - 2]  # Индексация массивов
    status = "Жив" if current_health > 0 else "Мертв"
    current_health = str(current_health).replace('.', ',')

    # Обновление значений в Google Sheets
    sh.sheet1.update(range_name=f'A{i}', values=[[i]])               # Номер итерации
    sh.sheet1.update(range_name=f'B{i}', values=[[int(health[i - 2])]])  # Исходное здоровье
    sh.sheet1.update(range_name=f'C{i}', values=[[int(current_health)]])      # Текущее здоровье
    sh.sheet1.update(range_name=f'D{i}', values=[[int(damage[i - 2])]])  # Урон
    sh.sheet1.update(range_name=f'E{i}', values=[[status]])              # Статус ("Жив"/"Мертв")

    i += 1  # Переход к следующей строке

    print(current_health, status)
