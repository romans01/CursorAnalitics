#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт добавления недостающих файлов в шаблон проекта
"""

from pathlib import Path


def write_text_file(path: Path, content: str) -> None:
    """Записывает текстовый файл в UTF-8"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def add_missing_files():
    """Добавляет недостающие файлы в шаблон проекта"""
    
    template_path = Path('Шаблон_Проекта')
    if not template_path.exists():
        print("❌ Папка Шаблон_Проекта не найдена")
        return
    
    data_path = template_path / '03_Данные'
    
    # CSV файлы с примерами данных
    print("📄 Добавляю CSV файлы с примерами...")
    
    write_text_file(data_path / 'выборки_и_примеры/sample_customers.csv', 
                    """customer_id,name,email,registration_date,status
1001,ООО "Альфа",alpha@example.com,2023-01-15,active
1002,ИП Петров,petrov@example.com,2023-02-20,active
1003,ЗАО "Бета",beta@example.com,2023-03-10,inactive
1004,ООО "Гамма",gamma@example.com,2023-04-05,active
1005,ООО "Дельта",delta@example.com,2023-05-01,active""")
    
    write_text_file(data_path / 'выборки_и_примеры/sample_sales.csv', 
                    """order_id,customer_id,product_name,quantity,price,order_date
O-2024-001,1001,Продукт A,2,1500.00,2024-01-10
O-2024-002,1002,Продукт B,1,2500.00,2024-01-11
O-2024-003,1001,Продукт C,3,800.00,2024-01-12
O-2024-004,1004,Продукт A,1,1500.00,2024-01-13
O-2024-005,1005,Продукт B,2,2500.00,2024-01-14""")
    
    # JSON файл с конфигурацией
    write_text_file(data_path / 'выборки_и_примеры/data_config.json', 
                    """{
  "data_sources": {
    "crm": {
      "connection": "postgresql://user:pass@crm-db:5432/crm",
      "tables": ["customers", "contacts", "leads"],
      "refresh_frequency": "daily"
    },
    "erp": {
      "connection": "postgresql://user:pass@erp-db:5432/erp", 
      "tables": ["orders", "products", "inventory"],
      "refresh_frequency": "hourly"
    }
  },
  "quality_rules": {
    "customers": {
      "required_fields": ["customer_id", "name", "email"],
      "unique_fields": ["customer_id", "email"],
      "data_types": {
        "customer_id": "integer",
        "registration_date": "date",
        "status": "enum"
      }
    },
    "orders": {
      "required_fields": ["order_id", "customer_id", "order_date"],
      "foreign_keys": {
        "customer_id": "customers.customer_id"
      },
      "business_rules": {
        "total_amount": "> 0",
        "quantity": "> 0"
      }
    }
  },
  "test_data": {
    "sample_size": 1000,
    "anonymization": {
      "email": "hash_domain",
      "phone": "mask_digits",
      "name": "pseudonymize"
    }
  }
}""")
    
    # Python скрипт для работы с данными
    write_text_file(data_path / 'выборки_и_примеры/data_loader.py', 
                    """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Утилиты для загрузки и валидации тестовых данных
\"\"\"

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any


class DataLoader:
    \"\"\"Класс для загрузки и валидации тестовых данных\"\"\"
    
    def __init__(self, data_dir: str = '.'):
        self.data_dir = Path(data_dir)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        \"\"\"Загружает конфигурацию данных\"\"\"
        config_path = self.data_dir / 'data_config.json'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_customers(self) -> pd.DataFrame:
        \"\"\"Загружает данные клиентов\"\"\"
        file_path = self.data_dir / 'sample_customers.csv'
        if not file_path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        df = pd.read_csv(file_path)
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        return df
    
    def load_sales(self) -> pd.DataFrame:
        \"\"\"Загружает данные продаж\"\"\"
        file_path = self.data_dir / 'sample_sales.csv'
        if not file_path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        df = pd.read_csv(file_path)
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['price'] = pd.to_numeric(df['price'])
        return df
    
    def validate_data(self) -> Dict[str, list]:
        \"\"\"Валидирует загруженные данные\"\"\"
        errors = {'customers': [], 'sales': []}
        
        try:
            customers = self.load_customers()
            sales = self.load_sales()
            
            # Проверка клиентов
            if customers['customer_id'].duplicated().any():
                errors['customers'].append('Найдены дублирующиеся customer_id')
            
            if customers['email'].duplicated().any():
                errors['customers'].append('Найдены дублирующиеся email')
            
            # Проверка продаж
            if sales['order_id'].duplicated().any():
                errors['sales'].append('Найдены дублирующиеся order_id')
            
            # Проверка референциальной целостности
            missing_customers = set(sales['customer_id']) - set(customers['customer_id'])
            if missing_customers:
                errors['sales'].append(f'Клиенты не найдены: {missing_customers}')
            
            # Проверка бизнес-правил
            if (sales['price'] <= 0).any():
                errors['sales'].append('Найдены цены <= 0')
            
            if (sales['quantity'] <= 0).any():
                errors['sales'].append('Найдены количества <= 0')
                
        except Exception as e:
            errors['general'] = [f'Ошибка валидации: {str(e)}']
        
        return errors
    
    def get_summary(self) -> Dict[str, Any]:
        \"\"\"Возвращает сводную информацию о данных\"\"\"
        try:
            customers = self.load_customers()
            sales = self.load_sales()
            
            return {
                'customers': {
                    'count': len(customers),
                    'date_range': {
                        'from': customers['registration_date'].min().strftime('%Y-%m-%d'),
                        'to': customers['registration_date'].max().strftime('%Y-%m-%d')
                    },
                    'status_distribution': customers['status'].value_counts().to_dict()
                },
                'sales': {
                    'count': len(sales),
                    'date_range': {
                        'from': sales['order_date'].min().strftime('%Y-%m-%d'),
                        'to': sales['order_date'].max().strftime('%Y-%m-%d')
                    },
                    'total_revenue': float(sales['price'].sum()),
                    'avg_order_value': float(sales['price'].mean())
                }
            }
        except Exception as e:
            return {'error': str(e)}


if __name__ == '__main__':
    # Пример использования
    loader = DataLoader()
    
    print("📊 Сводка по данным:")
    summary = loader.get_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    print("\\n🔍 Результаты валидации:")
    errors = loader.validate_data()
    for table, table_errors in errors.items():
        if table_errors:
            print(f"❌ {table}: {'; '.join(table_errors)}")
        else:
            print(f"✅ {table}: Ошибок не найдено")
""")
    
    print("✅ Добавлены файлы:")
    print("   - sample_customers.csv")
    print("   - sample_sales.csv") 
    print("   - data_config.json")
    print("   - data_loader.py")
    
    print("\n📁 Теперь в папке выборки_и_примеры есть:")
    samples_path = data_path / 'выборки_и_примеры'
    for file in samples_path.iterdir():
        if file.is_file():
            print(f"   - {file.name}")


if __name__ == '__main__':
    add_missing_files()
