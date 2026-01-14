### Описание
Стек - FastAPI, SQLAlchemy, Pydantic, Alembic, Redis.
Данный проект соответствует ТЗ.
Добавлены middleware для времени выполнения запроса и Redis кэширование.
При запуске применяется миграция создания таблицы и миграция добавления тестовых данных.


### Запуск с помощью Docker Compose
1. Перейдите в пустую папку и клонируйте репозиторий
 - ```git clone https://github.com/Stepan1771/NVI_Solutions_test_task```
 - ```cd NVI_Solutions_test_task```
2. Соберите образ
 - ```docker compose build```
3. Запустите
 - ```docker compose up -d```
4. Просмотрите логи
 - ```docker compose logs -f app```
 
### Приложение будет доступно по адресу:
 - "http://127.0.0.1:8000"

### Связь со мной:
- тг: @BonusYou
- резюме: https://hh.ru/resume/02efc04aff0f738fe90039ed1f47356d686a63