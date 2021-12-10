# Yamdb final 
## ![example workflow](https://github.com/RomanInBar/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание:
### CI и CD проекта api_yamdb  
## Реализация:
 - Автоматический запуск тестов  
 проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final.
 - Обновление образов на Docker Hub  
 сборка и доставка докер-образа для контейнера web на Docker Hub.
 - Автоматический деплой на боевой сервер при пуше в главную ветку master.
 - Отправка уведомления в Telegram о том, что процесс деплоя успешно завершился.
 ## Зпуск:
 - Склонируйте репозиторий на свой локальный компьютер, откройте проект.
 - Установите виртуальное окружение `python3 -m venv venv`, активируйте его `. venv/bin/activate`.
 - Установите зависимости командой `pip install -r requirements.txt`
 - Выполните миграции `python manage.py migarte`  
 Убедиесь что вы находитесь в той же дирректории, что и файл `manage.py`.
 - Запустить проекто локально `python manage.py runserver`
 ## Шаблон .env файла:
DB_ENGINE  
DB_NAME  
POSTGRES_USER  
POSTGRES_PASSWORD  
DB_HOST  
DB_PORT
 ## Автор:
 ### Барабин Роман
