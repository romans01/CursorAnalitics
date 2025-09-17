-- ETL для загрузки данных клиентов
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
    COUNT(*) FILTER (WHERE email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
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
