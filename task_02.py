import time
import re
from hyperloglog import HyperLogLog
from typing import List


def load_log_file(file_path: str) -> List[str]:
    """
    Завантажує IP-адреси з лог-файлу.
    
    Args:
        file_path (str): Шлях до лог-файлу.
    
    Returns:
        List[str]: Список знайдених IP-адрес.
    """
    ip_pattern = re.compile(r'\b\d{1,3}(\.\d{1,3}){3}\b')
    ip_addresses = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = ip_pattern.search(line)
                if match:
                    ip_addresses.append(match.group())
                else:
                    print(f"Не вдалося знайти IP у рядку: {line.strip()}")
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено. Перевірте шлях до файлу.")
    except UnicodeDecodeError:
        print(f"Помилка кодування. Спробуйте змінити кодування файлу.")

    return ip_addresses


def exact_count(ip_addresses: List[str]) -> int:
    """
    Точно підраховує кількість унікальних IP-адрес.
    
    Args:
        ip_addresses (List[str]): Список IP-адрес.
    
    Returns:
        int: Кількість унікальних IP-адрес.
    """
    return len(set(ip_addresses))


def approximate_count(ip_addresses: List[str]) -> int:
    """
    Використовує HyperLogLog для наближеного підрахунку унікальних IP-адрес.
    
    Args:
        ip_addresses (List[str]): Список IP-адрес.
    
    Returns:
        int: Наближена кількість унікальних IP-адрес.
    """
    hll = HyperLogLog(0.01)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


def compare_methods(file_path: str) -> None:
    """
    Порівнює продуктивність точного та наближеного підрахунку унікальних IP-адрес.
    
    Args:
        file_path (str): Шлях до лог-файлу.
    """
    print(f"Завантаження даних із файлу: {file_path}")
    ip_addresses = load_log_file(file_path)

    if not ip_addresses:
        print("Не знайдено жодних IP-адрес у файлі.")
        return

    print(f"Завантажено {len(ip_addresses)} IP-адрес")

    # Точний підрахунок
    start_time = time.time()
    exact_result = exact_count(ip_addresses)
    exact_time = time.time() - start_time

    # Наближений підрахунок
    start_time = time.time()
    approximate_result = approximate_count(ip_addresses)
    approximate_time = time.time() - start_time

    # Виведення результатів
    print("\nРезультати порівняння:")
    print(f"{'':<35}{'Точний підрахунок':<25}{'HyperLogLog':<25}")
    print(f"{'Унікальні елементи':<35}{exact_result:<25}{approximate_result:<25}")
    print(f"{'Час виконання (сек.)':<35}{exact_time:<25.6f}{approximate_time:<25.6f}")


if __name__ == "__main__":
    log_file_path = "lms-stage-access.log"
    compare_methods(log_file_path)
