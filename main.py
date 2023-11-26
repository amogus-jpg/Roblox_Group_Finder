import requests
import os
import pygame
import random
import time
import os

def clear_console():
    # Очистка консоли для разных операционных систем
    os.system('cls' if os.name == 'nt' else 'clear')

def play_notification_sound():
    # Инициализация Pygame (если не было инициализации ранее)
    pygame.init()

    # Получение директории текущего исполняемого файла
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Путь к звуковому файлу
    sound_file_path = os.path.join(script_directory, 'notification.mp3')

    # Воспроизведение звука
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play()

    # Ждем, пока звук не закончится
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def download_notification_sound():
    sound_url = "https://www.myinstants.com/media/sounds/gta-v-notification.mp3"
    sound_file_path = "notification.mp3"

    try:
        # Скачиваем звук
        response = requests.get(sound_url, stream=True)
        response.raise_for_status()

        # Записываем звук в файл
        with open(sound_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("Звук успешно скачан.")
        return True
    except Exception as e:
        print(f"Ошибка при скачивании звука: {e}")
        return False

def generate_unique_id(used_ids):
    new_id = random.randint(1, 10000000)
    while new_id in used_ids:
        new_id = random.randint(1, 10000000)
    used_ids.add(new_id)
    return new_id

def save_to_file(group_number, group_name, group_id, file_path):
    with open(file_path, 'a') as file:
        file.write(f"[{group_number}] Найдена группа \"{group_name}\": {group_id}\n")

def search_groups():
    base_url = "https://groups.roblox.com/v1/groups/"

    used_ids = set()
    group_number = 1
    file_path = "saved_ids.txt"

    # Проверяем наличие файла и создаем его, если не существует
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass

    # Проверяем наличие файла звука
    if not os.path.exists("notification.mp3"):
        print("Файл notification.mp3 не найден. Загружаем...")
        if download_notification_sound():
            print("Звук успешно загружен. Надпись уберется через 5 секунд.")
            time.sleep(5)
            clear_console()
        else:
            print("Не удалось загрузить звук.")
            return
        
    clear_console()

    while True:
        group_id = generate_unique_id(used_ids)
        group_url = f"{base_url}{group_id}"
        response = requests.get(group_url)

        if response.status_code == 200:
            group_info = response.json()
            group_name = group_info["name"]
            member_count = group_info["memberCount"]
            allowed = group_info["publicEntryAllowed"]
            is_locked = group_info["isLocked"]

            if member_count == 0 and allowed and not is_locked:
                print(f"Найдена группа {group_id} ({group_name})!\nЗаписано в saved_ids.txt")
                play_notification_sound()
                save_to_file(group_number, group_name, group_id, file_path)
                group_number += 1
            else:
                print(f"Группа {group_id} ({group_name}) не подошла.")
        elif response.status_code == 403:
            print(f"Группа {group_id} приватная.\n")
        elif response.status_code == 404:
            print(f"Группы {group_id} не существует. (Ошибка 404).")
        else:
            print(f"Сервер не принимает вызов с вашего IP, либо группа недоступна.")

        time.sleep(random.randint(6, 10))

        # Если чисел в генерации не осталось, завершаем цикл
        if len(used_ids) == 10000000:
            clear_console()
            print("Генерация групп закончилась, все найденные группы будут в документе")
            play_notification_sound()
            break

# Вызываем функцию для поиска групп
search_groups()