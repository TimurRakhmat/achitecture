## Задание 01

### Задание

Разработать два HTTP REST API сервиса для системы, спроектированной в первом задании (социальная сеть):

1. Реализовать как минимум два сервиса:
   - user-service — управление пользователями (регистрация, вход, JWT-аутентификация)
   - wall-service — работа со "стеной" пользователя (добавление и чтение постов)
2. Поддержка JWT-аутентификации (Bearer)
3. Отдельный endpoint для получения токена по логину и паролю
4. Реализация минимум методов GET и POST
5. Хранение данных в памяти (без базы данных)
6. Наличие мастер-пользователя: `admin` / `secret`
7. Генерация OpenAPI-спецификаций в формате JSON и сохранение в директорию `api_specs`
8. Актуализация архитектурной модели в Structurizr DSL
9. Запуск всех сервисов через `docker-compose up`

---

## Docker / Docker Compose

- Каждый сервис содержит свой `Dockerfile`
- Все сервисы запускаются одной командой:
```bash
docker-compose up --build

```

- Для генерации OpenAPI схем:
```bash
docker compose run userService python openapi.py
docker compose run confService python openapi.py
```

---

## OpenAPI спецификации

- Сгенерированы автоматически с помощью FastAPI
- Сохраняются в директории `api_specs`:
  - `user_service.openapi.json`
  - `conf_service.openapi.json`

---