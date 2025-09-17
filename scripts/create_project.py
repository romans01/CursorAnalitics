#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Основной скрипт создания аналитического проекта
"""

import argparse
import sys
from pathlib import Path

# Добавляем папку sections в путь
sys.path.insert(0, str(Path(__file__).parent / 'sections'))

# Импортируем модули разделов
try:
    import admin
    import initiation
    import requirements
    import data
    import analytics
    import solution
    import delivery
    import quality
    import docs
    import cursor_config
except ImportError as e:
    print(f"❌ Ошибка импорта модуля: {e}")
    print("Убедитесь, что все модули созданы в папке scripts/sections/")
    sys.exit(1)


def create_directory(path: Path) -> None:
    """Создает директорию, если она не существует"""
    path.mkdir(parents=True, exist_ok=True)


def write_text_file(path: Path, content: str) -> None:
    """Записывает текстовый файл в UTF-8"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def create_base_structure(root: Path) -> None:
    """Создает базовую структуру директорий"""
    directories = [
        '00_Администрирование',
        '01_Инициация_и_контекст',
        '02_Требования', 
        '03_Данные',
        '04_Аналитика',
        '05_Решение_и_дизайн',
        '06_Поставка_и_отчетность',
        '07_Качество_и_тестирование',
        '08_Документация'
    ]
    
    for dir_path in directories:
        create_directory(root / dir_path)


def create_top_level_files(root: Path) -> None:
    """Создает файлы верхнего уровня"""
    
    # README.md
    write_text_file(root / 'README.md', f"""# {root.name}

Аналитический проект, созданный по стандартному шаблону.

## Структура проекта
- 00_Администрирование — управление проектом, бриф, стейкхолдеры
- 01_Инициация_и_контекст — исследование предметной области
- 02_Требования — формализация требований (BRD, SRS)
- 03_Данные — управление данными и источниками
- 04_Аналитика — исследовательская аналитика
- 05_Решение_и_дизайн — проектирование решения
- 06_Поставка_и_отчетность — результаты и артефакты
- 07_Качество_и_тестирование — обеспечение качества
- 08_Документация — техническая документация

## Начало работы
1. Заполните `00_Администрирование/бриф.md`
2. Определите заинтересованные стороны
3. Проведите интервью и зафиксируйте текущее состояние
4. Формализуйте требования в BRD/SRS

См. также `.cursor/промпты/` для готовых промптов.
""")
    
    # CONTRIBUTING.md
    write_text_file(root / 'CONTRIBUTING.md', """# Правила работы с проектом

## Структура и именование
- Следуйте установленной структуре папок
- Используйте русские названия для документов
- Ведите журнал решений в `00_Администрирование/журнал_решений_ADR.md`

## Workflow
1. Обновляйте CHANGELOG.md при значимых изменениях
2. Используйте ADR-формат для архитектурных решений
3. Переносите устаревшие материалы в `99_Архив/`

## Критерии готовности
- [ ] Заполнен бриф проекта
- [ ] Определены критерии приемки
- [ ] Создан план тестирования
- [ ] Проведена валидация решения
""")
    
    # CHANGELOG.md
    write_text_file(root / 'CHANGELOG.md', """# История изменений

## [0.1.0] - Инициализация проекта
- Создана базовая структура проекта
- Добавлены шаблоны документов
- Настроены промпты для Cursor
""")
    
    # CODEOWNERS
    write_text_file(root / 'CODEOWNERS', """# Владельцы кода
* @team-analytics

# Критичные документы
00_Администрирование/ @lead-analyst
02_Требования/ @business-analyst @lead-analyst
07_Качество_и_тестирование/ @qa-lead
""")
    
    # .cursorignore
    write_text_file(root / '.cursorignore', """# Архив
99_Архив/

# Большие файлы данных
**/*.csv
**/*.parquet
**/*.xlsx
**/*.json
**/*.xml

# Временные файлы
**/*.tmp
**/tmp/
**/temp/
**/.ipynb_checkpoints/
**/build/
**/dist/

# Системные файлы
**/.DS_Store
**/Thumbs.db
""")


def main():
    parser = argparse.ArgumentParser(
        description='Создание аналитического проекта с модульной структурой'
    )
    parser.add_argument(
        '--name', '-n',
        default='Новый_Проект',
        help='Имя проекта'
    )
    parser.add_argument(
        '--destination', '-d', 
        default='.',
        help='Путь для создания проекта'
    )
    parser.add_argument(
        '--sections', '-s',
        nargs='*',
        help='Конкретные разделы для создания (по умолчанию: все)'
    )
    parser.add_argument(
        '--as-template',
        action='store_true',
        help='Создать как шаблон с примерами'
    )
    
    args = parser.parse_args()
    
    # Создание корневой папки
    destination = Path(args.destination)
    project_root = destination / args.name
    
    print(f"🚀 Создание проекта: {project_root}")
    
    # Исправляем проблему с кодировкой в Windows
    if "роекта" in str(project_root) or "роект" in str(project_root):
        corrected_name = args.name.replace("роекта", "Проекта").replace("роект", "Проект")
        # Дополнительно исправляем возможные ошибки
        corrected_name = corrected_name.replace("ППроекта", "Проекта")
        project_root = destination / corrected_name
        print(f"🔧 Исправлено имя на: {project_root}")
    
    # Базовая структура
    create_base_structure(project_root)
    create_top_level_files(project_root)
    
    # Модули разделов
    sections_map = {
        'admin': admin,
        'initiation': initiation, 
        'requirements': requirements,
        'data': data,
        'analytics': analytics,
        'solution': solution,
        'delivery': delivery,
        'quality': quality,
        'docs': docs,
        'cursor': cursor_config
    }
    
    # Определяем какие разделы создавать
    if args.sections:
        selected_sections = {k: v for k, v in sections_map.items() if k in args.sections}
    else:
        selected_sections = sections_map
    
    # Создаем разделы
    for section_name, module in selected_sections.items():
        try:
            print(f"📁 Создание раздела: {section_name}")
            module.create_section(project_root, as_template=args.as_template)
        except Exception as e:
            print(f"❌ Ошибка в разделе {section_name}: {e}")
    
    print(f"✅ Проект создан: {project_root.absolute()}")
    
    if args.as_template:
        print("📝 Создан шаблон с примерами и подробными описаниями")
    else:
        print("📝 Создан базовый проект с плейсхолдерами")


if __name__ == '__main__':
    main()
