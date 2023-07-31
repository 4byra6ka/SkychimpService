# <img src="https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f412.svg" width="89"/>

## Курсовой проект по Django "Сервис Skychimp"

#### Проект модуля 6 реализована рассылка для отправки уведомлений клиентам, блог для продвижения сервиса.
***
#### Реализованы задачи:
* Интерфейс заполнения рассылок, то есть CRUD механизм для управления рассылками.
* Скрипт рассылки, который работает по расписанию.
* Настройка конфигурации для периодического запуска задачи.
* Блог для продвижения сервиса.
* Интерфейс менеджера. Функционал менеджера:
  * <span style="color : green">может</span> просматривать любые рассылки
  * <span style="color : green">может</span> просматривать список пользователей сервиса
  * <span style="color : green">может</span> блокировать пользователей сервиса
  * <span style="color : green">может</span> отключать рассылки
  * <span style="color : red">не может</span> редактировать рассылки
  * <span style="color : red">не может</span> управлять списком рассылок
  * <span style="color : red">не может</span> изменять рассылки и сообщения
* Ограничение доступа к рассылкам для разных пользователей.
* Интерфейс для входа, регистрации и подтверждения почтового ящика.
* Модель пользователя для регистрации по почте, а также верификации.
* Главная страница со статистикой и 3 случайных блогов.
* Кеширование нескольких страниц.
***
### Прежде чем начать использовать проект нужно:
* Установить PostgreSQL на сервер или ПК и предварительно настроить БД.
* Установить БД Redis `sudo apt install redis`.
* Создать файл `.evn` для передачи личных данных в Django настройки.

    
    SECRET_KEY=<SECRET_KEY_DJANGO[django-insecure-tom...]>
    ALLOWED_HOSTS=*
    LANGUAGE_CODE=ru-ru
    TIME_ZONE=Europe/Moscow
    CACHE_ENABLED=True
    CACHES_LOCATION=redis://127.0.0.1:6379
    EMAIL_USER=<EMAIL_USER>
    EMAIL_PASSWORD=<EMAIL_PASSWORD>
    DATABASES_USER=<DATABASES_USER>
    DATABASES_PASSWORD=<DATABASES_PASSWORD>

***
### Разворачивание проекта "Сервис Skychimp"
    git cline https://github.com/4byra6ka/CourseWorkModule6.git
    cd CourseWorkModule6
    poetry install
    python manage.py runserver <IP>:<PORT>
    python manage.py crontab add
