#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт показа структуры проектов
"""

import os
from pathlib import Path


def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """Выводит дерево папок и файлов"""
    if current_depth >= max_depth:
        return
        
    try:
        items = list(Path(directory).iterdir())
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir() and current_depth < max_depth - 1:
                extension = "    " if is_last else "│   "
                print_tree(item, prefix + extension, max_depth, current_depth + 1)
                
    except PermissionError:
        print(f"{prefix}[Нет доступа]")


def show_projects():
    """Показывает структуру всех проектов"""
    base_path = Path('.')
    
    print("🗂️  Структура аналитических проектов:")
    print("=" * 50)
    
    # Находим папки проектов
    project_folders = []
    for item in base_path.iterdir():
        if item.is_dir() and ('Проект' in item.name or 'проект' in item.name):
            project_folders.append(item)
    
    project_folders.sort(key=lambda x: x.name)
    
    for project in project_folders:
        print(f"\n📁 {project.name}")
        print_tree(project, "   ", max_depth=3)
        print()


if __name__ == '__main__':
    show_projects()
