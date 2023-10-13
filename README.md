# Quiz
Задание заключается в создании api, которое принимает post-запросы вида {"questions_num": integer}. После получения
корректного запроса приложение в свою очередь отправляет запрос на сайт с вопросами для викторин
(https://jservice.io/api/random?count=1), чтобы получить нужное количество новых вопросов и записать их в базу данных.
Если был получен вопрос, который уже содержится в базе данных, то нужно отправлять новые запросы, пока не будет  получен
уникальный вопрос. В качестве ответа за post-запрос приложение отправляет информацию о последнем сохраненном
вопросе в базе данных до получения текущего запроса. Если база данных была пуста, то возвращается пустой объект. Из текста
задания мне было не совсем понятно какие конкретно поля с id и датой нужно отправлять, поэтому я отправлял поля с двумя
id (в моей базе данных и оригинальный на сайте вопросов) и двумя датами (создание записи в моей бд и в оригинальной).


### Пример Post-запроса
{"questions_num": 2}
### Пример ответа:
{
    "id": 7,
    "initial_id": 206887,
    "question": "This 10-letter word is used for the process of orienting & integrating a new employee into a company",
    "answer": "onboarding",
    "original_date": "2022-12-30 21:54:31.679000+00:00",
    "created_at": "2023-10-13 19:33:02.520716+00:00"
}

## Установка и настройка
    * Клонировать проект: git clone https://github.com/DigitalSmilingCat/Test_task_quiz.git
    * В папке, где находится manage.py создать файл .env и прописать зависимости, необходимые для работы проекта. Ниже указан пример заполнения
    * Установить необходимые пакеты из requirements.txt: pip install -r requirements.txt
    * Собрать докер-образ: sudo docker-compose up -d
    * Провести миграции: docker-compose exec web python manage.py migrate --noinput
    * После этого должна появиться возможность отправлять post-запросы с ip, указанных в DJANGO_ALLOWED_HOSTS

## Пример заполнения файла .env
    * SQL_ENGINE=django.db.backends.postgresql
    * SQL_DATABASE=quiz
    * SQL_USER=username
    * SQL_PASSWORD=password
    * SQL_HOST=db
    * SQL_PORT=5432
    * DATABASE=postgres
    * SECRET_KEY='Django_secret_key'
    * DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0 [::1]