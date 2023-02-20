# Мини-проект для курса "Проектный семинар"

## Содержание

<ol>
    <li>
        О проекте
    </li>
    <li>
    Начало работы
    <ul>
        <li>Необходимые компоненты и зависимости</li>
        <li>Установка</li>
    </ul>
    </li>
    <li>Использование</li>
</ol>


<!-- ABOUT THE PROJECT -->

## О проекте

проект для курса "Проектный семинар" в НИУ ВШЭ МИЭМ.
Работа с API различных сервисов

В репозитории находятся файлы и папки:

* `main.py` - исполняемый файл программы
* `requirements.txt` - файл с зависимостями
* `static` - директория со статичными файлами для HTML страницы
* `templates` - директория с шаблоном для HTML страницы
* `README.md` - описание проекта

<!-- GETTING STARTED -->

## Начало работы

Программа после запуска обратится к Gitlab, Taiga, Jitsi и Zulip по их API для сбора статистики о человеке. После,
сгенирирует HTML страницу со статистикой.

### Необходимые компоненты и зависимости

* requests
* plotly
* jinja2

### Установка

1. Скопируйте репозиторий
   ```sh
   git clone https://github.com/andchch/Python-miniproject.git
   ```
2. Установите зависимости
   ```sh
   pip install -r requirements.txt
   ```
3. Запустите программу
   ```sh
   python main.py
   ```

<!-- USAGE EXAMPLES -->

## Использование

Программа после запуска обратится к Gitlab, Taiga, Jitsi и Zulip по их API для сбора статистики о человеке. После,
сгенирирует HTML страницу `outputpage.html` со статистикой в той же директории, где находится `main.py`.
