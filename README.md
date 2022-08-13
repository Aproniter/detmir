# detmir

### Технологии
Python 3.7
Selenium 4
Argparse 


### Description
Парсинг товаров с сайта Детского мира, по заданной в аргументе командной строки категории


### Запуск
В проекте используется вебдрайвер для Windows
  - Создаем виртуальное окружение
    - python3 -m venv venv
  - Активируем
    - venv/Scripts/activate
  - Устанавливаем зависимости
    - pip install -r requirements.txt
  - Запускаем парсинг
    - <путь до папки виртуального окружения>/Scripts/python.exe <путь до scraper.py>/scraper.py -c <категория>
