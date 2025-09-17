#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

def write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_section(root: Path, as_template: bool = False) -> None:
    section_path = root / '03_Данные'
    
    # Создаем подпапки
    subdirs = ['словари_данных', 'модели_данных', 'трансформации', 'выборки_и_примеры']
    for subdir in subdirs:
        (section_path / subdir).mkdir(parents=True, exist_ok=True)
    
    content_prefix = "# Управление данными с примерами" if as_template else "# Управление данными"
    
    write_text_file(section_path / 'источники_данных.md', f"""{content_prefix}

## Каталог источников данных

| Источник | Тип | Описание | Владелец | SLA | Доступ |
|----------|-----|----------|----------|-----|--------|
| [Система 1] | СУБД | Основные транзакционные данные | [Команда] | 99.9% | API/DB |
| [Файл] | CSV | Справочная информация | [Отдел] | Ежедневно | FTP |

## Требования к качеству данных
- Полнота: > 95%
- Актуальность: не старше 24 часов  
- Согласованность: единые справочники
""")
    
    write_text_file(section_path / 'политика_данных_PII.md', f"""{content_prefix}

## Классификация данных
- **Публичные:** можно использовать без ограничений
- **Внутренние:** только для сотрудников компании
- **Конфиденциальные:** ограниченный доступ
- **Персональные данные:** требуют особой защиты

## Работа с PII
- Маскирование в тестовых средах
- Шифрование при хранении
- Логирование доступа
- Право на удаление (GDPR)
""")
    
    # Добавляем примеры для режима шаблона
    if as_template:
        # Примеры выборок данных
        write_text_file(section_path / 'выборки_и_примеры/sample_customers.csv', """customer_id,name,email,registration_date,status
1001,ООО "Альфа",alpha@example.com,2023-01-15,active
1002,ИП Петров,petrov@example.com,2023-02-20,active
1003,ЗАО "Бета",beta@example.com,2023-03-10,inactive
1004,ООО "Гамма",gamma@example.com,2023-04-05,active""")
        
        write_text_file(section_path / 'выборки_и_примеры/sample_sales.csv', """order_id,customer_id,product_name,quantity,price,order_date
O-2024-001,1001,Продукт A,2,1500.00,2024-01-10
O-2024-002,1002,Продукт B,1,2500.00,2024-01-11
O-2024-003,1001,Продукт C,3,800.00,2024-01-12
O-2024-004,1004,Продукт A,1,1500.00,2024-01-13""")
        
        write_text_file(section_path / 'выборки_и_примеры/README.md', """# Тестовые данные

## Описание файлов

### sample_customers.csv
**Назначение:** Пример данных о клиентах  
**Источник:** CRM система  
**Обновление:** Ежедневно  
**Объем:** ~1000 записей в продуктиве  

**Поля:**
- `customer_id` — уникальный ID клиента
- `name` — название организации
- `email` — контактный email
- `registration_date` — дата регистрации
- `status` — статус клиента (active/inactive)

### sample_sales.csv
**Назначение:** Пример данных о продажах  
**Источник:** ERP система  
**Обновление:** В реальном времени  
**Объем:** ~10000 записей в месяц  

**Поля:**
- `order_id` — уникальный номер заказа
- `customer_id` — ID клиента (FK)
- `product_name` — название продукта
- `quantity` — количество
- `price` — цена за единицу
- `order_date` — дата заказа

## Использование

### Для разработки
```python
import pandas as pd

# Загрузка тестовых данных
customers = pd.read_csv('sample_customers.csv')
sales = pd.read_csv('sample_sales.csv')

# Объединение данных
result = sales.merge(customers, on='customer_id')
```

### Для тестирования
- Используйте эти данные для unit-тестов
- Проверьте корректность ETL-процессов
- Валидируйте бизнес-правила

## Требования к данным

### Качество
- ✅ Нет дубликатов по первичным ключам
- ✅ Все обязательные поля заполнены
- ✅ Форматы данных соответствуют схеме
- ✅ Референциальная целостность соблюдена

### Безопасность
- ⚠️  Данные обезличены для тестирования
- ⚠️  Не содержат реальной PII информации
- ⚠️  Email адреса используют домен example.com
""")
        
        # Примеры словарей данных
        write_text_file(section_path / 'словари_данных/customers_dictionary.md', """# Словарь данных: Клиенты

## Таблица: customers

| Поле | Тип | Размер | Обязательное | Описание | Пример | Источник |
|------|-----|--------|--------------|----------|--------|----------|
| customer_id | INTEGER | - | Да | Уникальный идентификатор клиента | 1001 | Автогенерация |
| name | VARCHAR | 255 | Да | Наименование организации | ООО "Альфа" | Ручной ввод |
| email | VARCHAR | 100 | Да | Контактный email | alpha@example.com | Ручной ввод |
| phone | VARCHAR | 20 | Нет | Телефон | +7-495-123-4567 | Ручной ввод |
| registration_date | DATE | - | Да | Дата регистрации | 2023-01-15 | Автоматически |
| status | VARCHAR | 20 | Да | Статус клиента | active, inactive | Бизнес-процесс |
| created_at | TIMESTAMP | - | Да | Дата создания записи | 2023-01-15 10:30:00 | Система |
| updated_at | TIMESTAMP | - | Да | Дата последнего обновления | 2023-01-15 10:30:00 | Система |

## Бизнес-правила

### Статусы клиентов
- **active** — активный клиент, может совершать заказы
- **inactive** — неактивный клиент, заказы запрещены
- **blocked** — заблокированный клиент (нарушения)
- **prospect** — потенциальный клиент (лид)

### Валидация
- Email должен быть уникальным
- Телефон в формате +7-XXX-XXX-XXXX
- Наименование не может содержать спецсимволы
- При создании статус по умолчанию = 'prospect'

### Связи
- `customer_id` → `orders.customer_id` (1:M)
- `customer_id` → `customer_contacts.customer_id` (1:M)

## История изменений
- 2024-01-15: Добавлено поле phone
- 2023-12-01: Добавлен статус 'prospect'
- 2023-10-01: Создание таблицы
""")
        
        # Примеры трансформаций
        write_text_file(section_path / 'трансформации/customer_etl.sql', """-- ETL для загрузки данных клиентов
-- Источник: CRM.customers → DWH.dim_customers

-- Очистка staging таблицы
TRUNCATE TABLE staging.customers;

-- Загрузка из источника
INSERT INTO staging.customers (
    source_customer_id,
    customer_name,
    email,
    phone,
    registration_date,
    status,
    load_date
)
SELECT 
    c.customer_id,
    TRIM(UPPER(c.name)) as customer_name,
    LOWER(c.email) as email,
    REGEXP_REPLACE(c.phone, '[^0-9+]', '') as phone,
    c.registration_date,
    CASE 
        WHEN c.status = 'А' THEN 'active'
        WHEN c.status = 'Н' THEN 'inactive' 
        ELSE 'unknown'
    END as status,
    CURRENT_TIMESTAMP as load_date
FROM crm.customers c
WHERE c.updated_at >= CURRENT_DATE - INTERVAL '1 day'
   OR c.customer_id NOT IN (SELECT source_customer_id FROM dwh.dim_customers);

-- Валидация данных
INSERT INTO etl.data_quality_log (
    table_name, 
    check_name, 
    records_count, 
    failed_count,
    check_date
)
SELECT 
    'staging.customers',
    'email_format',
    COUNT(*),
    COUNT(*) FILTER (WHERE email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CURRENT_TIMESTAMP
FROM staging.customers;

-- Загрузка в DWH (SCD Type 2)
MERGE dwh.dim_customers AS target
USING (
    SELECT 
        source_customer_id,
        customer_name,
        email,
        phone,
        registration_date,
        status,
        load_date,
        ROW_NUMBER() OVER (PARTITION BY source_customer_id ORDER BY load_date DESC) as rn
    FROM staging.customers
    WHERE rn = 1
) AS source
ON target.source_customer_id = source.source_customer_id 
   AND target.is_current = TRUE

WHEN MATCHED AND (
    target.customer_name != source.customer_name OR
    target.email != source.email OR
    target.phone != source.phone OR
    target.status != source.status
) THEN
    UPDATE SET 
        is_current = FALSE,
        valid_to = CURRENT_TIMESTAMP - INTERVAL '1 second'

WHEN NOT MATCHED THEN
    INSERT (
        source_customer_id,
        customer_name,
        email,
        phone,
        registration_date,
        status,
        valid_from,
        valid_to,
        is_current,
        created_at
    )
    VALUES (
        source.source_customer_id,
        source.customer_name,
        source.email,
        source.phone,
        source.registration_date,
        source.status,
        CURRENT_TIMESTAMP,
        '2099-12-31'::timestamp,
        TRUE,
        CURRENT_TIMESTAMP
    );

-- Вставка новых версий для измененных записей
INSERT INTO dwh.dim_customers (
    source_customer_id,
    customer_name,
    email,
    phone,
    registration_date,
    status,
    valid_from,
    valid_to,
    is_current,
    created_at
)
SELECT 
    s.source_customer_id,
    s.customer_name,
    s.email,
    s.phone,
    s.registration_date,
    s.status,
    CURRENT_TIMESTAMP,
    '2099-12-31'::timestamp,
    TRUE,
    CURRENT_TIMESTAMP
FROM staging.customers s
JOIN dwh.dim_customers d ON s.source_customer_id = d.source_customer_id
WHERE d.is_current = FALSE
  AND d.valid_to = CURRENT_TIMESTAMP - INTERVAL '1 second';

-- Логирование результатов
INSERT INTO etl.load_log (
    table_name,
    records_processed,
    records_inserted,
    records_updated,
    load_date,
    status
)
SELECT 
    'dim_customers',
    (SELECT COUNT(*) FROM staging.customers),
    (SELECT COUNT(*) FROM dwh.dim_customers WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'),
    0, -- обновления считаются как вставки новых версий
    CURRENT_TIMESTAMP,
    'SUCCESS';
""")
        
        # Пример модели данных
        write_text_file(section_path / 'модели_данных/logical_model.md', """# Логическая модель данных

## Основные сущности

### Клиенты (Customers)
**Описание:** Организации и физические лица, которые являются клиентами компании

**Атрибуты:**
- ID клиента (PK)
- Наименование
- Тип клиента (B2B/B2C)
- Контактная информация
- Дата регистрации
- Статус

### Продукты (Products)
**Описание:** Товары и услуги, которые продает компания

**Атрибуты:**
- ID продукта (PK)
- Название
- Категория
- Цена
- Описание
- Статус (активный/архивный)

### Заказы (Orders)
**Описание:** Заказы, размещенные клиентами

**Атрибуты:**
- ID заказа (PK)
- ID клиента (FK)
- Дата заказа
- Статус заказа
- Общая сумма
- Способ оплаты

### Позиции заказа (Order Items)
**Описание:** Детализация заказов по продуктам

**Атрибуты:**
- ID позиции (PK)
- ID заказа (FK)
- ID продукта (FK)
- Количество
- Цена за единицу
- Скидка

## Связи между сущностями

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : "размещает"
    ORDERS ||--o{ ORDER_ITEMS : "содержит"
    PRODUCTS ||--o{ ORDER_ITEMS : "включен в"
    
    CUSTOMERS {
        int customer_id PK
        string name
        string email
        string phone
        date registration_date
        string status
    }
    
    PRODUCTS {
        int product_id PK
        string name
        string category
        decimal price
        text description
        string status
    }
    
    ORDERS {
        int order_id PK
        int customer_id FK
        date order_date
        string status
        decimal total_amount
        string payment_method
    }
    
    ORDER_ITEMS {
        int item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
        decimal discount
    }
```

## Бизнес-правила

### Клиенты
- Каждый клиент должен иметь уникальный email
- Статус клиента влияет на возможность размещения заказов
- При регистрации клиент получает статус "prospect"

### Заказы
- Заказ не может быть создан без позиций
- Общая сумма заказа = сумма всех позиций
- Статусы заказа: draft → confirmed → paid → shipped → delivered

### Продукты
- Цена продукта не может быть отрицательной
- Архивные продукты нельзя добавлять в новые заказы
- Категория продукта обязательна

## Индексы и производительность

### Рекомендуемые индексы
- `customers.email` (unique)
- `orders.customer_id, orders.order_date`
- `order_items.order_id`
- `order_items.product_id`
- `products.category, products.status`

### Партиционирование
- Таблица `orders` — по дате заказа (месячное)
- Таблица `order_items` — по дате заказа (месячное)

## Архивирование данных
- Заказы старше 7 лет → архивная база
- Клиенты без активности > 3 года → пометка для архивирования
- Логи системы старше 1 года → удаление
""")
    
    print(f"✅ Создан раздел: 03_Данные ({'с примерами' if as_template else 'базовый'})")
