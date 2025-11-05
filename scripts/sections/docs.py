#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

def write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def create_universal_startup_guide(section_path: Path, as_template: bool) -> None:
    """Создает универсальную инструкцию по запуску с платформо-независимыми блоками"""
    if as_template:
        content = """# Инструкция по запуску системы

## Обзор архитектуры

Система состоит из следующих компонентов:
- **Аналитическое ядро**: `{ANALYTICS_CORE_TECH}` — основная логика обработки данных
- **База данных**: `{DATABASE_TECH}` — хранение структурированных данных  
- **Кэш**: `{CACHE_TECH}` — кэширование часто используемых данных
- **Очереди**: `{QUEUE_TECH}` — асинхронная обработка задач
- **Веб-интерфейс**: `{WEB_FRAMEWORK}` — пользовательский интерфейс
- **API**: `{API_FRAMEWORK}` — программный интерфейс

> **Примечание**: Значения в фигурных скобках `{VARIABLE}` нужно заменить на конкретные технологии вашего проекта.

---

## 🚀 Запуск аналитического ядра

### Предварительные требования
- **Язык программирования**: `{ANALYTICS_LANGUAGE}` версии `{LANGUAGE_VERSION}+`
- **Пакетный менеджер**: `{PACKAGE_MANAGER}` (например: pip, npm, yarn, composer)
- **Память**: минимум `{MIN_MEMORY}` ГБ ОЗУ
- **Процессор**: `{MIN_CPU_CORES}` ядер

### Установка зависимостей
```bash
# Для Python проектов
{PACKAGE_MANAGER} install -r requirements.txt

# Для Node.js проектов  
{PACKAGE_MANAGER} install

# Для других технологий
{PACKAGE_MANAGER} {INSTALL_COMMAND}
```

### Конфигурация
1. **Создание файла конфигурации**:
   ```bash
   cp {CONFIG_TEMPLATE} {CONFIG_FILE}
   ```

2. **Основные параметры** (заполните в `{CONFIG_FILE}`):
   ```ini
   # Подключение к базе данных
   DATABASE_URL={DATABASE_CONNECTION_STRING}
   DATABASE_HOST={DB_HOST}
   DATABASE_PORT={DB_PORT}
   DATABASE_NAME={DB_NAME}
   DATABASE_USER={DB_USER}
   DATABASE_PASSWORD={DB_PASSWORD}

   # Настройки кэширования
   CACHE_URL={CACHE_CONNECTION_STRING}
   CACHE_TTL={CACHE_TIMEOUT_SECONDS}

   # Настройки очередей
   QUEUE_URL={QUEUE_CONNECTION_STRING}
   QUEUE_WORKERS={NUMBER_OF_WORKERS}

   # Настройки приложения
   APP_HOST={APPLICATION_HOST}
   APP_PORT={APPLICATION_PORT}
   APP_DEBUG={DEBUG_MODE}
   LOG_LEVEL={LOGGING_LEVEL}
   ```

3. **Инициализация базы данных**:
   ```bash
   # Создание схемы
   {DB_MIGRATION_COMMAND}
   
   # Заполнение начальными данными
   {DB_SEED_COMMAND}
   ```

### Запуск системы
```bash
# Запуск основного приложения
{START_COMMAND}

# Запуск в режиме разработки
{DEV_START_COMMAND}

# Запуск в фоновом режиме
{BACKGROUND_START_COMMAND}
```

### Проверка работоспособности
```bash
# Проверка статуса приложения
curl http://{APP_HOST}:{APP_PORT}/health

# Проверка подключения к БД
{DB_CHECK_COMMAND}

# Проверка кэша
{CACHE_CHECK_COMMAND}

# Просмотр логов
{LOG_VIEW_COMMAND}
```

---

## 📊 Подготовка BI-дашбордов

### Инструменты визуализации
Выберите один из следующих инструментов:
- **`{BI_TOOL_1}`** — `{BI_TOOL_1_DESCRIPTION}`
- **`{BI_TOOL_2}`** — `{BI_TOOL_2_DESCRIPTION}`  
- **`{BI_TOOL_3}`** — `{BI_TOOL_3_DESCRIPTION}`

### Настройка подключения к данным
1. **Создание источника данных**:
   - Тип подключения: `{DATA_SOURCE_TYPE}`
   - Строка подключения: `{BI_CONNECTION_STRING}`
   - Схема данных: `{DATA_SCHEMA}`

2. **Настройка обновления данных**:
   ```yaml
   refresh_schedule:
     frequency: {REFRESH_FREQUENCY}  # hourly, daily, weekly
     time: {REFRESH_TIME}           # время обновления
     timeout: {REFRESH_TIMEOUT}     # таймаут в минутах
   ```

3. **Создание витрин данных**:
   ```sql
   -- Создание представления для дашборда
   CREATE VIEW {DASHBOARD_VIEW_NAME} AS
   SELECT 
     {METRIC_COLUMNS},
     {DIMENSION_COLUMNS},
     {TIME_COLUMNS}
   FROM {SOURCE_TABLES}
   WHERE {FILTER_CONDITIONS};
   ```

### Развертывание дашбордов
```bash
# Экспорт дашборда из разработки
{BI_EXPORT_COMMAND}

# Импорт в продуктивную среду  
{BI_IMPORT_COMMAND}

# Настройка прав доступа
{BI_PERMISSIONS_COMMAND}
```

### Мониторинг производительности
- **Время загрузки дашборда**: должно быть < `{DASHBOARD_LOAD_TIME}` секунд
- **Время выполнения запросов**: < `{QUERY_EXECUTION_TIME}` секунд
- **Частота обновления**: каждые `{UPDATE_FREQUENCY}` минут
- **Размер кэша**: не более `{CACHE_SIZE_LIMIT}` МБ

---

## 🔗 Интеграция в пайплайн

### CI/CD настройка
1. **Файл конфигурации пайплайна** (`{CI_CONFIG_FILE}`):
   ```yaml
   stages:
     - build
     - test  
     - deploy
     - monitor

   variables:
     APP_NAME: {APPLICATION_NAME}
     ENVIRONMENT: {TARGET_ENVIRONMENT}
     DATABASE_URL: {PIPELINE_DB_URL}

   build_job:
     stage: build
     script:
       - {BUILD_COMMANDS}
     artifacts:
       paths:
         - {BUILD_ARTIFACTS}

   test_job:
     stage: test
     script:
       - {TEST_COMMANDS}
     coverage: {COVERAGE_REGEX}

   deploy_job:
     stage: deploy
     script:
       - {DEPLOY_COMMANDS}
     environment:
       name: {ENVIRONMENT_NAME}
       url: {ENVIRONMENT_URL}
   ```

2. **Переменные окружения для пайплайна**:
   ```bash
   # Секреты (настроить в CI/CD системе)
   DATABASE_PASSWORD={SECURE_DB_PASSWORD}
   API_KEYS={SECURE_API_KEYS}
   CERTIFICATES={SECURE_CERTIFICATES}

   # Публичные переменные
   APP_VERSION={APPLICATION_VERSION}
   ENVIRONMENT={TARGET_ENVIRONMENT}
   LOG_LEVEL={PIPELINE_LOG_LEVEL}
   ```

### Автоматическое тестирование
```bash
# Модульные тесты
{UNIT_TEST_COMMAND}

# Интеграционные тесты
{INTEGRATION_TEST_COMMAND}

# Тесты производительности
{PERFORMANCE_TEST_COMMAND}

# Проверка качества кода
{CODE_QUALITY_COMMAND}
```

### Развертывание
```bash
# Подготовка окружения
{ENVIRONMENT_SETUP_COMMAND}

# Развертывание приложения
{DEPLOY_APPLICATION_COMMAND}

# Миграция данных
{DATA_MIGRATION_COMMAND}

# Проверка развертывания
{DEPLOYMENT_VERIFICATION_COMMAND}
```

### Мониторинг пайплайна
- **Время сборки**: < `{BUILD_TIME_LIMIT}` минут
- **Покрытие тестами**: > `{TEST_COVERAGE_THRESHOLD}`%
- **Успешность развертывания**: > `{DEPLOYMENT_SUCCESS_RATE}`%
- **Время отката**: < `{ROLLBACK_TIME_LIMIT}` минут

---

## ⚙️ Настройка параметров

### Шаблон заполнения переменных
Скопируйте и заполните следующий шаблон для вашего проекта:

```yaml
# Основные технологии
ANALYTICS_CORE_TECH: "Python/Pandas"  # или R, Scala, Java
ANALYTICS_LANGUAGE: "Python"
LANGUAGE_VERSION: "3.9"
PACKAGE_MANAGER: "pip"

# База данных  
DATABASE_TECH: "PostgreSQL"  # или MySQL, MongoDB, ClickHouse
DATABASE_CONNECTION_STRING: "postgresql://user:pass@host:5432/dbname"
DB_HOST: "localhost"
DB_PORT: "5432"
DB_NAME: "analytics_db"
DB_USER: "analytics_user"
DB_PASSWORD: "secure_password"

# Кэширование
CACHE_TECH: "Redis"  # или Memcached, Hazelcast
CACHE_CONNECTION_STRING: "redis://localhost:6379/0"
CACHE_TIMEOUT_SECONDS: "3600"

# Очереди
QUEUE_TECH: "Celery/Redis"  # или RabbitMQ, Apache Kafka
QUEUE_CONNECTION_STRING: "redis://localhost:6379/1"
NUMBER_OF_WORKERS: "4"

# Веб-фреймворк
WEB_FRAMEWORK: "Flask"  # или Django, FastAPI, Express.js
API_FRAMEWORK: "Flask-RESTful"  # или DRF, FastAPI, Express

# Приложение
APPLICATION_HOST: "localhost"
APPLICATION_PORT: "8000"
DEBUG_MODE: "false"
LOGGING_LEVEL: "INFO"

# Команды
INSTALL_COMMAND: "install"
CONFIG_TEMPLATE: ".env.example"
CONFIG_FILE: ".env"
START_COMMAND: "python app.py"
DEV_START_COMMAND: "python app.py --debug"
BACKGROUND_START_COMMAND: "nohup python app.py &"

# Миграции и проверки
DB_MIGRATION_COMMAND: "python manage.py migrate"
DB_SEED_COMMAND: "python manage.py seed"
DB_CHECK_COMMAND: "python manage.py check_db"
CACHE_CHECK_COMMAND: "redis-cli ping"
LOG_VIEW_COMMAND: "tail -f logs/app.log"

# BI инструменты
BI_TOOL_1: "Grafana"
BI_TOOL_1_DESCRIPTION: "мониторинг и алертинг"
BI_TOOL_2: "Tableau"  
BI_TOOL_2_DESCRIPTION: "интерактивная аналитика"
BI_TOOL_3: "Power BI"
BI_TOOL_3_DESCRIPTION: "корпоративная отчетность"

# Дашборды
DATA_SOURCE_TYPE: "PostgreSQL"
BI_CONNECTION_STRING: "postgresql://readonly:pass@host:5432/analytics"
DATA_SCHEMA: "public"
REFRESH_FREQUENCY: "hourly"
REFRESH_TIME: "00:00"
REFRESH_TIMEOUT: "30"
DASHBOARD_VIEW_NAME: "dashboard_metrics"
DASHBOARD_LOAD_TIME: "5"
QUERY_EXECUTION_TIME: "10"
UPDATE_FREQUENCY: "15"
CACHE_SIZE_LIMIT: "500"

# CI/CD
CI_CONFIG_FILE: ".gitlab-ci.yml"  # или .github/workflows/main.yml
APPLICATION_NAME: "analytics-platform"
TARGET_ENVIRONMENT: "production"
PIPELINE_DB_URL: "$DATABASE_URL"
BUILD_COMMANDS: "pip install -r requirements.txt && python setup.py build"
BUILD_ARTIFACTS: "dist/"
TEST_COMMANDS: "pytest tests/ --coverage"
COVERAGE_REGEX: "TOTAL.*?(\\d+%)$"
DEPLOY_COMMANDS: "python deploy.py --environment=production"
ENVIRONMENT_NAME: "production"
ENVIRONMENT_URL: "https://analytics.company.com"

# Тестирование
UNIT_TEST_COMMAND: "pytest tests/unit/"
INTEGRATION_TEST_COMMAND: "pytest tests/integration/"
PERFORMANCE_TEST_COMMAND: "locust -f tests/performance/locustfile.py"
CODE_QUALITY_COMMAND: "flake8 src/ && mypy src/"

# Развертывание
ENVIRONMENT_SETUP_COMMAND: "ansible-playbook setup.yml"
DEPLOY_APPLICATION_COMMAND: "docker-compose up -d"
DATA_MIGRATION_COMMAND: "python migrate.py --target=production"
DEPLOYMENT_VERIFICATION_COMMAND: "python verify_deployment.py"

# Лимиты и пороги
MIN_MEMORY: "4"
MIN_CPU_CORES: "2"
BUILD_TIME_LIMIT: "15"
TEST_COVERAGE_THRESHOLD: "80"
DEPLOYMENT_SUCCESS_RATE: "95"
ROLLBACK_TIME_LIMIT: "5"
```

### Пример заполнения для Python/Django проекта
```yaml
ANALYTICS_CORE_TECH: "Python/Django + Pandas"
ANALYTICS_LANGUAGE: "Python"
LANGUAGE_VERSION: "3.9"
PACKAGE_MANAGER: "pip"
DATABASE_TECH: "PostgreSQL 13"
CACHE_TECH: "Redis 6"
QUEUE_TECH: "Celery + Redis"
WEB_FRAMEWORK: "Django 4.0"
API_FRAMEWORK: "Django REST Framework"
START_COMMAND: "python manage.py runserver"
DB_MIGRATION_COMMAND: "python manage.py migrate"
BI_TOOL_1: "Grafana"
CI_CONFIG_FILE: ".github/workflows/django.yml"
```

### Пример заполнения для Node.js проекта
```yaml
ANALYTICS_CORE_TECH: "Node.js + D3.js"
ANALYTICS_LANGUAGE: "JavaScript"
LANGUAGE_VERSION: "16"
PACKAGE_MANAGER: "npm"
DATABASE_TECH: "MongoDB"
CACHE_TECH: "Redis"
QUEUE_TECH: "Bull Queue"
WEB_FRAMEWORK: "Express.js"
API_FRAMEWORK: "Express + Swagger"
START_COMMAND: "npm start"
DB_MIGRATION_COMMAND: "npm run migrate"
BI_TOOL_1: "Chart.js Dashboard"
CI_CONFIG_FILE: ".github/workflows/node.yml"
```

---

## 🔧 Устранение неполадок

### Частые проблемы

#### Проблема: Не удается подключиться к базе данных
**Симптомы**: Ошибки подключения, таймауты
**Решение**:
1. Проверьте параметры подключения в `{CONFIG_FILE}`
2. Убедитесь, что сервис БД запущен: `{DB_STATUS_COMMAND}`
3. Проверьте сетевые настройки и firewall
4. Проверьте права доступа пользователя БД

#### Проблема: Медленная работа дашбордов
**Симптомы**: Долгая загрузка, таймауты запросов
**Решение**:
1. Оптимизируйте SQL запросы
2. Добавьте индексы на часто используемые поля
3. Настройте кэширование результатов
4. Увеличьте ресурсы сервера

#### Проблема: Ошибки в пайплайне
**Симптомы**: Падающие тесты, неудачные развертывания
**Решение**:
1. Проверьте логи пайплайна: `{PIPELINE_LOGS_COMMAND}`
2. Убедитесь в корректности переменных окружения
3. Проверьте доступность внешних сервисов
4. Запустите тесты локально для отладки

### Контакты поддержки
- **Техническая поддержка**: `{TECH_SUPPORT_CONTACT}`
- **Администратор БД**: `{DBA_CONTACT}`
- **DevOps команда**: `{DEVOPS_CONTACT}`
- **Документация**: `{DOCS_URL}`

---

## 📚 Дополнительные ресурсы

### Полезные ссылки
- **Техническая документация**: `{TECH_DOCS_URL}`
- **API документация**: `{API_DOCS_URL}`
- **Мониторинг системы**: `{MONITORING_URL}`
- **Логи приложения**: `{LOGS_URL}`

### Обучающие материалы
- **Видео-туториалы**: `{VIDEO_TUTORIALS_URL}`
- **Примеры кода**: `{CODE_EXAMPLES_URL}`
- **Best practices**: `{BEST_PRACTICES_URL}`
- **FAQ**: `{FAQ_URL}`

---

**Версия документа**: 2.0  
**Дата создания**: [дата]  
**Последнее обновление**: [дата]  
**Ответственный**: DevOps/Platform Team
"""
    else:
        content = """# Инструкция по запуску системы

## Обзор архитектуры
- **Аналитическое ядро**: `{ANALYTICS_CORE_TECH}` — основная логика
- **База данных**: `{DATABASE_TECH}` — хранение данных
- **Кэш**: `{CACHE_TECH}` — кэширование
- **Веб-интерфейс**: `{WEB_FRAMEWORK}` — пользовательский интерфейс

> Замените переменные в `{СКОБКАХ}` на конкретные технологии вашего проекта.

## 🚀 Запуск аналитического ядра

### Предварительные требования
- `{ANALYTICS_LANGUAGE}` версии `{LANGUAGE_VERSION}+`
- `{PACKAGE_MANAGER}` для установки зависимостей

### Установка и запуск
```bash
{PACKAGE_MANAGER} {INSTALL_COMMAND}
{START_COMMAND}
```

### Проверка работоспособности
```bash
curl http://{APP_HOST}:{APP_PORT}/health
```

## 📊 Подготовка BI-дашбордов

### Настройка
1. Выберите инструмент: `{BI_TOOL}`
2. Настройте подключение: `{BI_CONNECTION_STRING}`
3. Создайте витрины данных

### Развертывание
```bash
{BI_DEPLOY_COMMAND}
```

## 🔗 Интеграция в пайплайн

### CI/CD настройка
```yaml
# {CI_CONFIG_FILE}
build:
  script: {BUILD_COMMANDS}
test:
  script: {TEST_COMMANDS}
deploy:
  script: {DEPLOY_COMMANDS}
```

### Переменные окружения
```bash
DATABASE_URL={DATABASE_CONNECTION_STRING}
APP_HOST={APPLICATION_HOST}
APP_PORT={APPLICATION_PORT}
```

## ⚙️ Шаблон параметров

Создайте файл `deployment_config.yml` и заполните:

```yaml
# Основные технологии
ANALYTICS_CORE_TECH: "Python/Pandas"
ANALYTICS_LANGUAGE: "Python"
DATABASE_TECH: "PostgreSQL"
CACHE_TECH: "Redis"
WEB_FRAMEWORK: "Flask"

# Команды
PACKAGE_MANAGER: "pip"
INSTALL_COMMAND: "install -r requirements.txt"
START_COMMAND: "python app.py"

# Подключения
APPLICATION_HOST: "localhost"
APPLICATION_PORT: "8000"
DATABASE_CONNECTION_STRING: "postgresql://user:pass@host:5432/db"

# BI и CI/CD
BI_TOOL: "Grafana"
CI_CONFIG_FILE: ".github/workflows/main.yml"
BUILD_COMMANDS: "pip install -r requirements.txt"
TEST_COMMANDS: "pytest tests/"
DEPLOY_COMMANDS: "docker-compose up -d"
```

## 🔧 Устранение неполадок

### Частые проблемы
- **Ошибка подключения к БД**: Проверьте `{DATABASE_CONNECTION_STRING}`
- **Медленные дашборды**: Оптимизируйте запросы и добавьте кэширование
- **Ошибки пайплайна**: Проверьте переменные окружения

### Контакты
- Техподдержка: `{TECH_SUPPORT_CONTACT}`
- Документация: `{DOCS_URL}`
"""
    
    write_text_file(section_path / 'как_запустить.md', content)


def create_deployment_config_template(section_path: Path, as_template: bool) -> None:
    """Создает шаблон конфигурации для развертывания"""
    if as_template:
        content = """# Шаблон конфигурации развертывания

## Назначение
Этот файл содержит все параметры, необходимые для настройки универсальной инструкции по запуску системы. 
Заполните значения согласно вашему технологическому стеку.

## Инструкция по заполнению
1. Скопируйте этот файл в `deployment_config.yml`
2. Замените все значения на актуальные для вашего проекта
3. Используйте этот файл как справочник при настройке системы
4. Обновляйте конфигурацию при изменении технологий

---

## 🔧 Основные технологии

```yaml
# Аналитическое ядро
ANALYTICS_CORE_TECH: "Python/Pandas + Jupyter"
ANALYTICS_LANGUAGE: "Python"
LANGUAGE_VERSION: "3.9"
PACKAGE_MANAGER: "pip"

# База данных
DATABASE_TECH: "PostgreSQL 13"
DATABASE_CONNECTION_STRING: "postgresql://analytics:password@localhost:5432/analytics_db"
DB_HOST: "localhost"
DB_PORT: "5432"
DB_NAME: "analytics_db"
DB_USER: "analytics"
DB_PASSWORD: "secure_password_here"

# Кэширование
CACHE_TECH: "Redis 6"
CACHE_CONNECTION_STRING: "redis://localhost:6379/0"
CACHE_TIMEOUT_SECONDS: "3600"

# Очереди и асинхронные задачи
QUEUE_TECH: "Celery + Redis"
QUEUE_CONNECTION_STRING: "redis://localhost:6379/1"
NUMBER_OF_WORKERS: "4"

# Веб-интерфейс
WEB_FRAMEWORK: "Flask 2.0"
API_FRAMEWORK: "Flask-RESTful"

# Приложение
APPLICATION_HOST: "0.0.0.0"
APPLICATION_PORT: "8000"
DEBUG_MODE: "false"
LOGGING_LEVEL: "INFO"
```

---

## 📦 Команды управления

```yaml
# Управление зависимостями
INSTALL_COMMAND: "install -r requirements.txt"
CONFIG_TEMPLATE: ".env.example"
CONFIG_FILE: ".env"

# Запуск приложения
START_COMMAND: "python app.py"
DEV_START_COMMAND: "flask run --debug"
BACKGROUND_START_COMMAND: "gunicorn -w 4 -b 0.0.0.0:8000 app:app"

# База данных
DB_MIGRATION_COMMAND: "flask db upgrade"
DB_SEED_COMMAND: "python seed_data.py"
DB_CHECK_COMMAND: "python -c \"from app import db; db.engine.execute('SELECT 1')\""
DB_STATUS_COMMAND: "systemctl status postgresql"

# Кэш и мониторинг
CACHE_CHECK_COMMAND: "redis-cli ping"
LOG_VIEW_COMMAND: "tail -f logs/app.log"
PIPELINE_LOGS_COMMAND: "kubectl logs -f deployment/analytics-app"

# Системные требования
MIN_MEMORY: "4"
MIN_CPU_CORES: "2"
```

---

## 📊 BI и визуализация

```yaml
# Инструменты бизнес-интеллекта
BI_TOOL_1: "Grafana"
BI_TOOL_1_DESCRIPTION: "мониторинг метрик и алертинг"
BI_TOOL_2: "Apache Superset"
BI_TOOL_2_DESCRIPTION: "интерактивные дашборды и исследовательская аналитика"
BI_TOOL_3: "Tableau"
BI_TOOL_3_DESCRIPTION: "корпоративная отчетность и презентации"

# Подключение к данным
DATA_SOURCE_TYPE: "PostgreSQL"
BI_CONNECTION_STRING: "postgresql://readonly:readonly_password@localhost:5432/analytics_db"
DATA_SCHEMA: "public"

# Настройки обновления
REFRESH_FREQUENCY: "hourly"
REFRESH_TIME: "00:00"
REFRESH_TIMEOUT: "30"

# Витрины данных
DASHBOARD_VIEW_NAME: "v_dashboard_metrics"
METRIC_COLUMNS: "revenue, orders_count, conversion_rate"
DIMENSION_COLUMNS: "region, product_category, customer_segment"
TIME_COLUMNS: "date_created, date_updated"
SOURCE_TABLES: "orders o JOIN customers c ON o.customer_id = c.id"
FILTER_CONDITIONS: "o.status = 'completed'"

# Команды управления BI
BI_EXPORT_COMMAND: "grafana-cli dashboard export dashboard-id"
BI_IMPORT_COMMAND: "grafana-cli dashboard import dashboard.json"
BI_PERMISSIONS_COMMAND: "grafana-cli admin reset-admin-password"

# Производительность
DASHBOARD_LOAD_TIME: "5"
QUERY_EXECUTION_TIME: "10"
UPDATE_FREQUENCY: "15"
CACHE_SIZE_LIMIT: "500"
```

---

## 🚀 CI/CD и развертывание

```yaml
# Конфигурация пайплайна
CI_CONFIG_FILE: ".github/workflows/deploy.yml"
APPLICATION_NAME: "analytics-platform"
TARGET_ENVIRONMENT: "production"
PIPELINE_DB_URL: "$DATABASE_URL"

# Команды сборки и тестирования
BUILD_COMMANDS: "pip install -r requirements.txt && python setup.py build"
BUILD_ARTIFACTS: "dist/"
TEST_COMMANDS: "pytest tests/ --cov=src --cov-report=xml"
COVERAGE_REGEX: "TOTAL.*?(\\d+%)$"

# Команды развертывания
DEPLOY_COMMANDS: "docker build -t analytics-app . && docker-compose up -d"
ENVIRONMENT_NAME: "production"
ENVIRONMENT_URL: "https://analytics.company.com"

# Тестирование
UNIT_TEST_COMMAND: "pytest tests/unit/ -v"
INTEGRATION_TEST_COMMAND: "pytest tests/integration/ -v"
PERFORMANCE_TEST_COMMAND: "locust -f tests/performance/locustfile.py --host=http://localhost:8000"
CODE_QUALITY_COMMAND: "flake8 src/ && mypy src/ && bandit -r src/"

# Управление окружением
ENVIRONMENT_SETUP_COMMAND: "ansible-playbook -i inventory/production setup.yml"
DEPLOY_APPLICATION_COMMAND: "kubectl apply -f k8s/"
DATA_MIGRATION_COMMAND: "python scripts/migrate_data.py --env=production"
DEPLOYMENT_VERIFICATION_COMMAND: "python scripts/health_check.py --full"

# Пороговые значения
BUILD_TIME_LIMIT: "15"
TEST_COVERAGE_THRESHOLD: "80"
DEPLOYMENT_SUCCESS_RATE: "95"
ROLLBACK_TIME_LIMIT: "5"

# Секретные переменные (настроить в CI/CD системе)
SECURE_DB_PASSWORD: "{{ secrets.DATABASE_PASSWORD }}"
SECURE_API_KEYS: "{{ secrets.API_KEYS }}"
SECURE_CERTIFICATES: "{{ secrets.SSL_CERTIFICATES }}"

# Публичные переменные пайплайна
APPLICATION_VERSION: "v1.2.3"
PIPELINE_LOG_LEVEL: "INFO"
```

---

## 🔧 Контакты и ресурсы

```yaml
# Контакты поддержки
TECH_SUPPORT_CONTACT: "support@company.com"
DBA_CONTACT: "dba@company.com"
DEVOPS_CONTACT: "devops@company.com"

# Документация и ресурсы
DOCS_URL: "https://docs.company.com/analytics"
TECH_DOCS_URL: "https://docs.company.com/analytics/technical"
API_DOCS_URL: "https://api.company.com/docs"
MONITORING_URL: "https://monitoring.company.com"
LOGS_URL: "https://logs.company.com"

# Обучающие материалы
VIDEO_TUTORIALS_URL: "https://learn.company.com/analytics/videos"
CODE_EXAMPLES_URL: "https://github.com/company/analytics-examples"
BEST_PRACTICES_URL: "https://docs.company.com/best-practices"
FAQ_URL: "https://docs.company.com/faq"
```

---

## 🎯 Примеры конфигураций для популярных стеков

### Python + Django + PostgreSQL
```yaml
ANALYTICS_CORE_TECH: "Django + Pandas + Celery"
ANALYTICS_LANGUAGE: "Python"
LANGUAGE_VERSION: "3.9"
DATABASE_TECH: "PostgreSQL 13"
CACHE_TECH: "Redis 6"
WEB_FRAMEWORK: "Django 4.0"
START_COMMAND: "python manage.py runserver 0.0.0.0:8000"
DB_MIGRATION_COMMAND: "python manage.py migrate"
```

### Node.js + Express + MongoDB
```yaml
ANALYTICS_CORE_TECH: "Node.js + D3.js + Bull Queue"
ANALYTICS_LANGUAGE: "JavaScript"
LANGUAGE_VERSION: "16"
PACKAGE_MANAGER: "npm"
DATABASE_TECH: "MongoDB 5"
CACHE_TECH: "Redis"
WEB_FRAMEWORK: "Express.js"
START_COMMAND: "npm start"
DB_MIGRATION_COMMAND: "npm run migrate"
```

### R + Shiny + MySQL
```yaml
ANALYTICS_CORE_TECH: "R + Shiny + RMarkdown"
ANALYTICS_LANGUAGE: "R"
LANGUAGE_VERSION: "4.1"
PACKAGE_MANAGER: "install.packages"
DATABASE_TECH: "MySQL 8"
CACHE_TECH: "Memcached"
WEB_FRAMEWORK: "Shiny Server"
START_COMMAND: "Rscript app.R"
DB_MIGRATION_COMMAND: "Rscript migrate.R"
```

### Java + Spring Boot + Oracle
```yaml
ANALYTICS_CORE_TECH: "Spring Boot + Apache Spark"
ANALYTICS_LANGUAGE: "Java"
LANGUAGE_VERSION: "11"
PACKAGE_MANAGER: "mvn"
DATABASE_TECH: "Oracle 19c"
CACHE_TECH: "Hazelcast"
WEB_FRAMEWORK: "Spring Boot"
START_COMMAND: "java -jar target/analytics-app.jar"
DB_MIGRATION_COMMAND: "mvn flyway:migrate"
```

---

## ✅ Чек-лист настройки

### Предварительная подготовка
- [ ] Определен технологический стек
- [ ] Заполнены основные параметры конфигурации
- [ ] Настроены подключения к базе данных и кэшу
- [ ] Определены команды запуска и управления

### Настройка окружения
- [ ] Установлены необходимые зависимости
- [ ] Создан и настроен файл конфигурации
- [ ] Выполнены миграции базы данных
- [ ] Проверена работоспособность всех компонентов

### BI и визуализация
- [ ] Выбраны инструменты для дашбордов
- [ ] Настроены подключения к источникам данных
- [ ] Созданы витрины данных и представления
- [ ] Протестирована производительность запросов

### CI/CD настройка
- [ ] Создан файл конфигурации пайплайна
- [ ] Настроены переменные окружения
- [ ] Добавлены автоматические тесты
- [ ] Проверены процедуры развертывания

### Документация и поддержка
- [ ] Обновлена техническая документация
- [ ] Определены контакты для поддержки
- [ ] Созданы инструкции для команды
- [ ] Настроен мониторинг и алертинг

---

**Версия конфигурации**: 1.0  
**Дата создания**: [дата]  
**Ответственный**: DevOps/Platform Team  
**Следующий пересмотр**: [дата + 3 месяца]
"""
    else:
        content = """# Шаблон конфигурации развертывания

## Назначение
Параметры для настройки универсальной инструкции по запуску системы.

## Основные технологии
```yaml
ANALYTICS_CORE_TECH: "Python/Pandas"
ANALYTICS_LANGUAGE: "Python"
DATABASE_TECH: "PostgreSQL"
CACHE_TECH: "Redis"
WEB_FRAMEWORK: "Flask"

# Команды
START_COMMAND: "python app.py"
DB_MIGRATION_COMMAND: "python manage.py migrate"
BI_TOOL_1: "Grafana"
```

## Инструкция
1. Скопируйте в `deployment_config.yml`
2. Заполните значения для вашего проекта
3. Используйте как справочник при настройке
"""
    
    write_text_file(section_path / 'deployment_config_template.md', content)


def create_section(root: Path, as_template: bool = False) -> None:
    section_path = root / '08_Документация'
    
    # Создаем универсальную инструкцию по запуску
    create_universal_startup_guide(section_path, as_template)
    
    # Создаем дополнительные универсальные документы
    create_deployment_config_template(section_path, as_template)
    
    write_text_file(section_path / 'руководство_по_структуре.md', """# Руководство по структуре проекта

## Назначение папок
- `00_Администрирование/` — управление проектом
- `01_Инициация_и_контекст/` — исследование области
- `02_Требования/` — формализация требований
- `03_Данные/` — управление данными
- `04_Аналитика/` — исследования и выводы
- `05_Решение_и_дизайн/` — проектирование
- `06_Поставка_и_отчетность/` — результаты
- `07_Качество_и_тестирование/` — обеспечение качества
- `08_Документация/` — техническая документация

## Правила работы
1. Обновляйте CHANGELOG.md при изменениях
2. Используйте ADR для архитектурных решений
3. Архивируйте устаревшие материалы в `99_Архив/`
""")
    
    write_text_file(section_path / 'FAQ.md', """# Часто задаваемые вопросы

## Q: Как добавить новое требование?
A: Добавьте в соответствующий раздел `02_Требования/` и обновите матрицу трассируемости.

## Q: Где хранить тестовые данные?
A: В папке `03_Данные/выборки_и_примеры/` с описанием в README.

## Q: Как оформить архитектурное решение?
A: Добавьте запись в `00_Администрирование/журнал_решений_ADR.md` по шаблону.

## Q: Куда поместить устаревшие документы?
A: Переместите в `99_Архив/` с указанием даты архивирования.
""")
    
    print(f"✅ Создан раздел: 08_Документация ({'с примерами' if as_template else 'базовый'})")
