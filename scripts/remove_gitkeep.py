#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт удаления .gitkeep файлов из проектов
"""

from pathlib import Path
import os


def remove_gitkeep_files():
    """Удаляет все .gitkeep файлы из проектов"""
    
    base_path = Path('.')
    removed_count = 0
    
    # Ищем все .gitkeep файлы
    for gitkeep_file in base_path.rglob('.gitkeep'):
        try:
            gitkeep_file.unlink()
            print(f"🗑️  Удален: {gitkeep_file}")
            removed_count += 1
        except Exception as e:
            print(f"❌ Ошибка удаления {gitkeep_file}: {e}")
    
    if removed_count == 0:
        print("✅ .gitkeep файлы не найдены")
    else:
        print(f"✅ Удалено {removed_count} .gitkeep файлов")


if __name__ == '__main__':
    remove_gitkeep_files()
