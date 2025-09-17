#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт очистки созданных проектов и шаблонов
"""

import argparse
import shutil
from pathlib import Path
import os


def remove_directory(path: Path) -> bool:
    """Удаляет директорию и все её содержимое"""
    try:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            print(f"✅ Удалена папка: {path}")
            return True
        else:
            print(f"⚠️  Папка не найдена: {path}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при удалении {path}: {e}")
        return False


def list_analytics_projects(base_path: Path) -> list:
    """Находит все папки, похожие на аналитические проекты"""
    projects = []
    
    # Паттерны для поиска аналитических проектов
    patterns = [
        "*Проект*",
        "*проект*", 
        "*Шаблон*",
        "*шаблон*",
        "*Template*",
        "*template*"
    ]
    
    for pattern in patterns:
        for path in base_path.glob(pattern):
            if path.is_dir():
                # Проверяем, есть ли характерные папки аналитического проекта
                has_admin = (path / "00_Администрирование").exists()
                has_requirements = (path / "02_Требования").exists()
                has_cursor = (path / ".cursor").exists()
                
                if has_admin or has_requirements or has_cursor:
                    projects.append(path)
    
    return sorted(set(projects))


def main():
    parser = argparse.ArgumentParser(
        description='Очистка созданных аналитических проектов и шаблонов'
    )
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='Базовый путь для поиска проектов (по умолчанию: текущая директория)'
    )
    parser.add_argument(
        '--project-name', '-n',
        help='Имя конкретного проекта для удаления'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Удалить все найденные аналитические проекты'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Показать что будет удалено, но не удалять'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Удалить без подтверждения'
    )
    
    args = parser.parse_args()
    
    base_path = Path(args.path).resolve()
    
    if not base_path.exists():
        print(f"❌ Путь не существует: {base_path}")
        return
    
    # Удаление конкретного проекта
    if args.project_name:
        project_path = base_path / args.project_name
        if args.dry_run:
            print(f"🔍 Будет удалена папка: {project_path}")
        else:
            if args.force or input(f"Удалить проект '{args.project_name}'? (y/N): ").lower() == 'y':
                remove_directory(project_path)
        return
    
    # Поиск всех аналитических проектов
    projects = list_analytics_projects(base_path)
    
    if not projects:
        print("✨ Аналитические проекты не найдены")
        return
    
    print(f"🔍 Найдено {len(projects)} аналитических проектов:")
    for i, project in enumerate(projects, 1):
        print(f"  {i}. {project.name}")
    
    if args.dry_run:
        print("\n🔍 Dry run: файлы не будут удалены")
        return
    
    if args.all:
        if args.force or input(f"\nУдалить все {len(projects)} проектов? (y/N): ").lower() == 'y':
            removed_count = 0
            for project in projects:
                if remove_directory(project):
                    removed_count += 1
            print(f"\n✅ Удалено проектов: {removed_count}/{len(projects)}")
    else:
        # Интерактивный выбор
        while True:
            try:
                choice = input(f"\nВведите номер проекта для удаления (1-{len(projects)}) или 'q' для выхода: ")
                if choice.lower() == 'q':
                    break
                
                idx = int(choice) - 1
                if 0 <= idx < len(projects):
                    project = projects[idx]
                    if input(f"Удалить '{project.name}'? (y/N): ").lower() == 'y':
                        if remove_directory(project):
                            projects.pop(idx)
                            if not projects:
                                print("✨ Все проекты удалены")
                                break
                else:
                    print("❌ Неверный номер")
            except (ValueError, KeyboardInterrupt):
                print("\n👋 Выход")
                break


if __name__ == '__main__':
    main()
