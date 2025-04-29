import subprocess
import time
import threading
import sys

# Функция для запуска команды python all.py
def run_all_py():
    try:
        subprocess.run(["python", "all.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске all.py: {e}")

# Функция для проверки ввода 0 в бесконечном режиме
def check_stop(stop_event):
    while not stop_event.is_set():
        user_input = input()
        if user_input.strip() == "0":
            print("Остановка скрипта...")
            stop_event.set()
            break

# Основная функция
def main():
    print("Выберите режим работы:")
    print("1. Бесконечный")
    print("2. Циклический")
    
    mode = input("Введите номер действия (1 или 2): ").strip()
    
    if mode == "1":
        print("Запущен бесконечный режим. Введите 0 для остановки.")
        stop_event = threading.Event()
        
        # Запускаем поток для проверки ввода 0
        stop_thread = threading.Thread(target=check_stop, args=(stop_event,))
        stop_thread.daemon = True
        stop_thread.start()
        
        cycle_count = 1
        while not stop_event.is_set():
            print(f"Запуск {cycle_count}")
            run_all_py()
            cycle_count += 1
            for _ in range(50):  # Ожидание 50 секунд с проверкой остановки
                if stop_event.is_set():
                    break
                time.sleep(1)
        
    elif mode == "2":
        try:
            cycles = int(input("Введите количество циклов: ").strip())
            if cycles <= 0:
                print("Количество циклов должно быть больше 0.")
                return
        except ValueError:
            print("Ошибка: введите корректное число.")
            return
        
        print(f"Запущен циклический режим на {cycles} циклов.")
        for cycle in range(1, cycles + 1):
            print(f"Запуск {cycle}")
            run_all_py()
            if cycle < cycles:  # Не ждём после последнего цикла
                time.sleep(50)
    else:
        print("Ошибка: выберите 1 или 2.")

if __name__ == "__main__":
    main()
