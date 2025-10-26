# Разработчикам бэкенда


## Как развернуть локально

### Необходимое ПО

Для запуска ПО вам понадобятся консольный Git и Make. Инструкции по их установке ищите на
официальных сайтах:

- [Git SCM](https://git-scm.com/)
- [GNU Make](https://www.gnu.org/software/make/)

Вы можете проверить, установлены ли эти программы с помощью команд:

```shell
$ git --version
git version 2.37.1.windows.1

$ make --version
GNU Make 4.4.1
Built for Windows32
<...>
```

Для тех, кто использует Windows необходимы также программы **git** и **git bash**. В **git bash** необходимо дополнительно установить
**make**:

- Перейдите на сайт [ezwinports](https://sourceforge.net/projects/ezwinports/files/)
- Скачайте `make-4.4.1-without-guile-w32-bin.zip` (выберите версию без `guile`)
- Извлеките архив
- Скопируйте содержимое архива в `C:\ProgramFiles\Git\mingw64\` **БЕЗ** перезаписи/замены любых вложенных файлов.

Все дальнейшие команды запускать из-под **git bash**.

### Создание виртуального окружения для работы с IDE

IDE для корректной работы подсказок необходимо развернуть виртуальное окружение со всеми установленными зависимостями.

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

### Настройка pre-commit хуков

В репозитории используются хуки [pre-commit](https://pre-commit.com/), чтобы автоматически запускать линтеры и автотесты.

В корне репозитория в **активированном виртуальном окружении** запустите команду для настройки хуков:

```shell
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

В последующем при коммите автоматически будут запускаться линтеры и другие проверки. Если проверки не пройдут, то коммит прервётся с ошибкой.

Если вам потребуется сделать коммит без проверок, то вы можете отключить их с помощью флага `--no-verify`:

```shell
git commit -m 'Message' --no-verify
```

## Как вести разработку

Код проекта находится в папке `/src`.

Находясь в корневой директории проекта, запустить проект можно командой:

```shell
$ fastapi dev src/main.py
```

Проект будет работать по адресу http://127.0.0.1:8000/

### Как установить python-пакет в виртуальное окружение

В качестве менеджера пакетов используется [uv](https://docs.astral.sh/uv/).

Вот пример как добавить в зависимости библиотеку `beautifulsoup4`.

```shell
$ uv add beautifulsoup4
```

Конфигурационные файлы `pyproject.toml` и `uv.lock` обновятся автоматически.

Аналогичным образом можно удалять python-пакеты:

```shell
$ uv remove beautifulsoup4
```

Если необходимо обновить `uv.lock` вручную, то используйте команду:

```shell
$ uv lock
```

### Команды для быстрого запуска с помощью make

Для вывода списка часто используемых коротких команд используйте команду

```shell
$ make list
...
```

### Устройство схем бэкенда:

- [Локальная инсталляция бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_local_installation.drawio.png)
- [Prod инсталляция бэкенда](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_prod_installation.drawio.png)
- [Декомпозиция бэкенда по подсистемам](https://gitlab.dvmn.org/root/fastapi-articles/-/wikis/fastai/backend_decomposition.drawio.png)

### Разворачивание фронтенда в локальной инсталляции

Файлы фронтенда следует положить в папку src/ предварительно добавив в `.gitignore` а также добавить файл `frontend-settings.json` со значением

```json
{
  "backendBaseUrl": "http://127.0.0.1:8000/"
}
```

чтобы фронтенд [знал](https://dvmn.org/media/filer_public/a6/72/a6723390-983e-48df-b1ac-e2785682c671/readme.html) куда ходить за данными к бэкенду

### Работа с библиотекой HTML Page Generator

Библиотека для генерации HTML страниц с помощью ИИ. Пользователю достаточно описать своими словами страницу, которую он хочет получить. ИИ сами подберут изображения и напишут код страницы.

Работает с двумя сервисами:

- Unsplash - для поиска подходящих картинок.
- Deepseek - для управления процессом и собственно генерации кода страницы.

Инициализация клиентов:
```python
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient


async def main():
    async with (
        AsyncUnsplashClient.setup("UNSPLASH_CLIENT_ID", timeout=3),
        AsyncDeepseekClient.setup(
            "DEEPSEEK_API_KEY",
            "DEEPSEEK_BASE_URL",
            "DEEPSEEK_MODEL",
        ),
    ):
        ...
```
Генерация:
```python
from html_page_generator import AsyncPageGenerator
import os

DEBUG_MODE = os.getenv("DEBUG_MODE", False)

async def generate_page(user_prompt: str):
    generator = AsyncPageGenerator(debug_mode=DEBUG_MODE)
    async for chunk in generator(user_prompt):
        print(chunk, end="", flush=True)

    with open(generator.html_page.title + '.html', 'w') as f:
        f.write(generator.html_page.html_code)

    print('Файл успешно сохранён!')
```
### Разворачивание S3 сервера(локально на *unix системах)
Для установки в *nix системах, надо скачать бинарник
```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio -O minio
```
сделать его исполняемым:
```bash
chmod +x minio
```
Предварительно создав папку для хранения данных, запустить сервер командой:
```bash
minio server ~/minio-data --console-address ":9090"
```
В консоле отобразятся креды для подключения к API и WebUI.

Для создания бакета надо установить MinIO Client командой:
```bash
wget https://dl.min.io/client/mc/release/linux-amd64/mc -O mc
chmod +x mc
sudo mv mc /usr/local/bin/
```
Подключить ранее созданный сервер Minio:
```bash
mc alias set local http://localhost:9000 minioadmin minioadmin
```
Создать бакет:
```bash
mc mb local/my-bucket
```
Сделать бакет публичным:
```bash
mc anonymous set public local/my-bucket
```

Взимодействие с S3 через Web интерфейс:
- Перейти в Web интерфейс http://localhost:9001/
- Нажать "+ Create Bucket"
- Задать имя бакета 
- Нажать кнопку "Upload"
- Выбрать любой файл из локального компьютера(например `index.png` или `index.html`)
- Найти загруженный файл через ссылку "http://localhost:9000/bucket-name/index.htm"


Взимодействие с S3 через python код:
```python
import aioboto3
from aiobotocore.config import AioConfig

config = AioConfig(
    max_pool_connections=50,
    connect_timeout=10,
    read_timeout=30
)

s3_config = {
    "endpoint_url": "http://192.168.1.102:9000",
    "aws_access_key_id": "minioadmin",
    "aws_secret_access_key": "minioadmin"
}

with open("ai_site_generator/src/static/testHTML.html", "rb") as file:
    html_content = file.read()

upload_params ={
    "Bucket": "mybucket",
    "Key": "data/testHTML.html",
    "Body": html_content,
    "ContentType": "text/html",
    "ContentDisposition": "inline" #inline означает, что файл будет открываться прямо в браузере в соответствии с его MIME-типом
}


async def create_s3_client():
    session = aioboto3.Session()
    async with session.client('s3', **s3_config, config=config) as client:
        await client.put_object(**upload_params)

```

### Использование Gotenberg API — для генерации скриншотов из html файла

Для запуска требуется указать следующие настройки:
- `httpx.AsyncClient.base_url` - базовый адрес Gotenberg API. Обязательная настройка.
- `ScreenshotHTMLRequest.width` - ширина скриншота в пикселях. Обязательная настройка.
- `ScreenshotHTMLRequest.format` - формат скриншота (может принимать значения jpeg, png, webp). По-умолчанию - jpeg.
- `ScreenshotHTMLRequest.wait_delay` - время ожидания завершения анимаций на html-странице. По-умолчанию - 2 секунды.
опциональные настройки асинхронного клиента

Пример запроса:
```python
import httpx

from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest

 try:
    async with httpx.AsyncClient(
        base_url=settings_var.get().GOTENBERG_URL,
        timeout=15,
    ) as client:
        screenshot_bytes = await ScreenshotHTMLRequest(
            index_html=raw_html,
            width=1000,
            format='png',
            wait_delay=5,
        ).asend(client)
except GotenbergServerError as e:
    logger.error(e)
    screenshot_bytes = None
```