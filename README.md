# ai_site_generator

В качестве пакетного менеджера на проекта используется [uv](https://docs.astral.sh/uv/).

[Установите uv](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/Uv-package-manager#1-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-uv) и в корне репозитория выполните команду

```shell
$ uv sync
```

[uv](https://docs.astral.sh/uv/) создаст виртуальное окружение, установит необходимую версию Python и все необходимые зависимости.

После этого активируйте виртуальное окружение в текущей сессии терминала:

```shell
$ source .venv/bin/activate  # для Linux
$ .\.venv\Scripts\activate  # Для Windows
```
## Переменные окружения 
Для работы приложения потребуются следующие групповые настройки(`example.env`):
```json
    DEEPSEEK__API_KEY=
    DEEPSEEK__MAX_CONNECTIONS=
    DEEPSEEK__TIMEOUT=
    UNSPLASH__CLIENT_ID=
    UNSPLASH__MAX_CONNECTIONS=
    UNSPLASH__TIMEOUT=
    DEBUG_MODE=
    S3__ENDPOINT_URL=
    S3__AWS_ACCESS_KEY_ID=
    S3__AWS_SECRET_ACCESS_KEY=
    S3__BUCKET_NAME=
    S3__MAX_POOL_CONNECTIONS=
    S3__CONNECT_TIMEOUT=
    S3__READ_TIMEOUT=
    GOTENBERG__URL=
    GOTENBERG__WIDTH=
    GOTENBERG__SCREENSHOTHTMLREQUEST_WAIT_DELAY=
    GOTENBERG__SCREENSHOTHTMLREQUEST_FORMAT=
    GOTENBERG__SCREENSHOTHTMLREQUEST_WIDTH=
    GOTENBERG__TIMEOUT=
```
где:
- `DEEPSEEK__API_KEY`* - API-ключ аутентификации. [Получить.](https://api-docs.deepseek.com/)
- `DEEPSEEK__MAX_CONNECTIONS` - максимальное количество одновременных HTTP-соединений к API
- `DEEPSEEK__TIMEOUT` - лимит времени ожидания ответа от API
- `UNSPLASH__CLIENT_ID`* - Access Key созданного Unsplash приложения. [Получить.](https://unsplash.com/documentation#creating-a-developer-account)
- `DEBUG_MODE`- при `True` будет логироваться в консоль все действия агента
- `S3__ENDPOINT_URL` - url адрес сервера где развернут S3
- `S3__AWS_ACCESS_KEY_ID` - имя пользователя S3
- `S3__AWS_SECRET_ACCESS_KEY` - пароль S3
- `S3__BUCKET_NAME` - бакет куда будут падать загруженные файлы
- `S3__MAX_POOL_CONNECTIONS` - кол-во параллельных операций
- `S3__CONNECT_TIMEOUT` - кол-во сек на подключение
- `S3__READ_TIMEOUT` - кол-во сек на чтение данных
- `GOTENBERG__URL` - url адрес сервера где развернут GOTENBERG
- `GOTENBERG__SCREENSHOTHTMLREQUEST_WAIT_DELAY` - время ожидания завершения анимаций на html-странице. По-умолчанию - 2 секунды.
- `GOTENBERG__SCREENSHOTHTMLREQUEST_FORMAT` - формат скриншота (может принимать значения jpeg, png, webp). По-умолчанию - jpeg.
- `GOTENBERG__SCREENSHOTHTMLREQUEST_WIDTH` - ширина скриншота в пикселях
- `GOTENBERG__TIMEOUT` - лимит времени ожидания ответа от API

Файл `.env` следует добавить в `.gitignore`

## Как запустить код

Находясь в корневой директории проекта, запустить проект можно командой:

```shell
$ fastapi dev src/main.py
```

Проект будет работать по адресу http://127.0.0.1:8000/
