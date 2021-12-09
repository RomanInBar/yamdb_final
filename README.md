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
 ## Автор:
 ### Барабин Роман
