#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт поиска пустых папок в проектах
"""

from pathlib import Path


def find_empty_folders(project_path: Path):
    """Находит пустые папки в проекте"""
    empty_folders = []
    
    for item in project_path.rglob('*'):
        if item.is_dir():
            # Проверяем, есть ли файлы в папке
            files = list(item.iterdir())
            if not files:
                empty_folders.append(item.relative_to(project_path))
    
    return empty_folders


def main():
    projects = ['Шаблон_Проекта', 'Пример_Проекта']
    
    for project_name in projects:
        project_path = Path(project_name)
        if not project_path.exists():
            print(f"❌ Проект {project_name} не найден")
            continue
            
        print(f"\n📁 Анализ проекта: {project_name}")
        print("=" * 50)
        
        empty_folders = find_empty_folders(project_path)
        
        if empty_folders:
            print(f"🔍 Найдено {len(empty_folders)} пустых папок:")
            for folder in sorted(empty_folders):
                print(f"   📂 {folder}")
        else:
            print("✅ Пустых папок не найдено")


if __name__ == '__main__':
    main()
