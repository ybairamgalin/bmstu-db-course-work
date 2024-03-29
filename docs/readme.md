# Курсовой проект по базам данных

## Цель

Сделать веб-приложение для отслеживания задач (аналог gira
и yandex.tracker).

## Core features

- авторизация;
- возможность создавать, удалять редактировать задачи;
- в каждой задаче возможность: указывать и отслеживать 
автора, исполнителя, дату создания, дедлайд, оценку сложности (sp),
статус, топик (например, для распределения задач по командам);
- экран со всеми задачами по фильтрам
- теги для задач
- time-tracker для задач (фича, которой мне не хватает в 
существующих решениях (кнопки start, end при нажатии на которые 
начинает считаться время, которое занимает выполнение задачи));

## Optional features

- поиск по задачам (прикрутить elastic search), optional так как
не знаю насколько это имеет отношение к предметной области БД;
- сделать проект горзонтально масштабируемым в отношении БД
(добавить репликацию БД);
- динамические атрибуты для задач...;
- agile доски со статусами задач (open, blocked, pull-request,
merged, deployed, closed);
- алерты на дедлайны... .

## Примерный план работ

- написать несколько стартовых ручек для тестирования;
- поднять бек и фронт сервера, бд, CI с линтерами и автотестами;
- 1 тестовый экран фронта;
- отладить процесс разработки в поднятой инфраструктуре;
- экраны авторизации, добавления пользователя;
- аналит часть РПЗ
- экран создания задач, задачи;
- экран списка задач;
- добавление time-tracker а к задаче;
- optional features;
- оформление РПЗ.

## Технологический стек
- сервер: nginx
- back: python fastapi
- db: postgres
- front: js, bootstrap...
- ci: gitlab ci/teamcity
- linters: ?
- tests: pytest

## Что нужно сделать на фронте

Я не фронтэндер, поэтому не уверен, что получится сделать качественно

- нулевой экран авторизации (самый простой, где вводится логин и пароль);
- экран создания аккаунта;
- экран отображения всех тасок;
- экран создания задачи;
- экран отображения конкретной таски подробно.

## Схема БД

TODO

## Роли в бд

TODO

## Схемы api

- `GET: /tasks` 

Получить все id и краткое описание задач по user_id/topic_name/...

Пример:

Request body
```json
{
  "topic_name": "team_1"
}
```

Response body
```json
{
  "tasks": [
    {
      "id": 1,
      "topic": "BMSTU",
      "name": "Сделать курсовую работу",
      "executor": {
        "id": 1,
        "name": "Ярослав"
      },
      "status": "open",
      "date_start": "2022-10-10"
    },
    {
      "id": 1,
      "topic": "BMSTU",
      "name": "Не отчислиться",
      "executor": {
        "id": 1,
        "name": "Ярослав"
      },
      "status": "open",
      "date_start": "2020-10-10"
    }
  ]
}
```

- `GET: /task`

Получить всю информацию по id задачи.

- `POST: /task`

Создать задачу

- `DELETE: /task`

Удалить задачу по id.

- `UPDATE: /task`

Обновить задачу

TODO
