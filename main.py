from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def init_browser():
    driver = webdriver.Edge()
    driver.get('https://ru.wikipedia.org/wiki')
    return driver

def search_wikipedia(driver, query):
    search_box = driver.find_element(By.NAME, 'search')
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

def get_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p')
    return [p.text for p in paragraphs if p.text.strip()]

def get_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, 'a')
    return {link.text: link.get_attribute('href') for link in links if link.text.strip()}

def main():
    driver = init_browser()

    try:
        query = input('Введите ваш запрос: ')
        search_wikipedia(driver, query)

        while True:
            print('\nВыберите действие:')
            print('1. Листать параграфы текущей статьи')
            print('2. Перейти на одну из связанных страниц')
            print('3. Выйти из программы')
            choice = input('Введите номер действия: ').strip()

            if choice == '1':
                paragraphs = get_paragraphs(driver)
                for i, paragraph in enumerate(paragraphs, 1):
                    print(f'[{i}] {paragraph}\n')
                    next_action = input("Нажмите Enter, чтобы продолжить или 'q' для выхода: ").strip().lower()
                    if next_action == 'q':
                        break

            elif choice == '2':
                links = get_links(driver)
                if not links:
                    print('Нет доступных ссылок.')
                    continue

                print('\nДоступные ссылки:')
                max_links_to_show = 20
                for i, (title, url) in enumerate(list(links.items())[:max_links_to_show], 1):
                    print(f'[{i}] {title} ({url})')
                if len(links) > max_links_to_show:
                    print('...Показаны только первые 20 ссылок.')

                link_choise = input("Введите номер ссылки для перехода или 'q' для выхода: ").strip()

                if link_choise.lower() == 'q':
                    continue

                try:
                    link_index = int(link_choise) - 1
                    selected_link = list(links.values())[link_index]
                    driver.get(selected_link)
                    time.sleep(2)
                except (ValueError, IndexError):
                    print('Некорректный выбор. Попробуйте снова.')
            elif link_choise.lower() == 'q':
                continue

            elif choice == '3':
                print('Выход из программы...')
                break
    finally:
        driver.quit()

if __name__ == '__main__':
    main()