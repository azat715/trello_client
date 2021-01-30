# D1.10 Домашнее задание
## Мини-клиент к Trello

### Зависимости
* python = "^3.8"
* requests = "^2.25.1"
* fire = "^0.4.0"

### Установка 
`pip install trello_client-0.1.0.tar.gz`

### Использование
необходимо установить переменные окружения
* export API_KEY={API_KEY}
* export API_TOKEN={API_TOKEN}
* export BOARD_ID={BOARD_ID}

```
NAME
    trello_client

SYNOPSIS
    trello_client COMMAND

COMMANDS
    COMMAND is one of the following:

     read
       Печать списка задач

     create_task
       Создание задачи

     move
       Перемещение карточки в колонку

     create_colmn
       Создание колонки
```
