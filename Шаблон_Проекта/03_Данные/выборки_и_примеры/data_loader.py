#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилиты для загрузки и валидации тестовых данных
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any


class DataLoader:
    """Класс для загрузки и валидации тестовых данных"""
    
    def __init__(self, data_dir: str = '.'):
        self.data_dir = Path(data_dir)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Загружает конфигурацию данных"""
        config_path = self.data_dir / 'data_config.json'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_customers(self) -> pd.DataFrame:
        """Загружает данные клиентов"""
        file_path = self.data_dir / 'sample_customers.csv'
        if not file_path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        df = pd.read_csv(file_path)
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        return df
    
    def load_sales(self) -> pd.DataFrame:
        """Загружает данные продаж"""
        file_path = self.data_dir / 'sample_sales.csv'
        if not file_path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        df = pd.read_csv(file_path)
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['price'] = pd.to_numeric(df['price'])
        return df
    
    def validate_data(self) -> Dict[str, list]:
        """Валидирует загруженные данные"""
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
        """Возвращает сводную информацию о данных"""
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
    
    print("\n🔍 Результаты валидации:")
    errors = loader.validate_data()
    for table, table_errors in errors.items():
        if table_errors:
            print(f"❌ {table}: {'; '.join(table_errors)}")
        else:
            print(f"✅ {table}: Ошибок не найдено")
