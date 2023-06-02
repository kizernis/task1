# Тестовое задание 1 (вопросы для викторины)

### Порядок запуска и использования:
1. Клонируйте репозиторий:
```
git clone https://github.com/kizernis/task1
```
2. Перейдите в директорию проекта:
```bash
cd task1
```
3. По желанию измените пароли пользователя и суперпользователя СУБД в файлах, соответственно, ```db_password.txt``` и ```db_root_password.txt``` (в конце файла ```db_password.txt``` не должно быть переноса строки).

4. По желанию в начале файла ```docker-compose.yml``` измените значения переменных **DB_USER_NAME** и **DB_DATABASE_NAME** и в конце раскомментируйте сервис **adminer** (для управления базой данных PostgreSQL через GUI).

5. Убедитесь, что TCP-порт **8000** на вашем компьютере не занят.

6. Запустите приложение (у вас должен поддерживаться **[Compose V2](https://docs.docker.com/compose/migrate/)**):
```
docker compose up
```
или в режиме detached:
```
docker compose up -d
```
7. Для проверки работы веб-сервиса перейдите по адресу **[http://localhost:8000/docs](http://localhost:8000/docs)** или воспользуйтесь приложением, умеющим отправлять POST-запросы, типа **Postman** или **curl**, например так:
```bash
curl -X 'POST' 'http://localhost:8000/new-questions/' \
-H 'accept: application/json' -H 'Content-Type: application/json' \
-d '{"questions_num": 5}'
```

8. Для доступа к базе данных откройте **Adminer** (если раскомментировали) по адресу **[http://localhost:8080](http://localhost:8080)** (адрес сервера PostgreSQL оставьте **db**) или наберите в терминале:
```
docker exec -it task1-db-1 sh
```
и воспользуйтесь командой **psql**, например так:
```
psql -U user1 task1
```

9. Для завершения работы приложения и удаления контейнеров и томов наберите команду:
```
docker compose down -v
```