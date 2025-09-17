#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт исправления имен папок проектов
"""

import os
import shutil
from pathlib import Path


def fix_project_names():
    """Исправляет имена папок проектов"""
    base_path = Path('.')
    
    # Ищем папки с неправильными именами
    for item in base_path.iterdir():
        if item.is_dir() and ('роект' in item.name or 'ример' in item.name):
            old_name = item.name
            new_name = old_name
            
            # Исправляем распространенные ошибки
            new_name = new_name.replace('роекта', 'Проекта')
            new_name = new_name.replace('роект', 'Проект') 
            new_name = new_name.replace('ример', 'Пример')
            # Убираем дублирование букв
            new_name = new_name.replace('ПППроект', 'Проект')
            new_name = new_name.replace('ППример', 'Пример')
            new_name = new_name.replace('ППП', 'П')
            new_name = new_name.replace('ПП', 'П')
            
            if old_name != new_name:
                new_path = base_path / new_name
                print(f"🔧 Переименовываю: {old_name} → {new_name}")
                try:
                    item.rename(new_path)
                    print(f"✅ Успешно переименовано")
                except Exception as e:
                    print(f"❌ Ошибка переименования: {e}")
            else:
                print(f"✅ Имя корректно: {old_name}")


if __name__ == '__main__':
    fix_project_names()
