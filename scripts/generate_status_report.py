#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор отчета о статусе проекта
"""

import os
from pathlib import Path
from datetime import datetime
import argparse


def count_files_in_section(section_path: Path) -> dict:
    """Подсчитывает файлы в секции проекта"""
    if not section_path.exists():
        return {"files": 0, "folders": 0, "empty_folders": 0}
    
    files = 0
    folders = 0
    empty_folders = 0
    
    for item in section_path.rglob('*'):
        if item.is_file():
            files += 1
        elif item.is_dir():
            folders += 1
            # Проверяем, пустая ли папка
            if not any(item.iterdir()):
                empty_folders += 1
    
    return {"files": files, "folders": folders, "empty_folders": empty_folders}


def analyze_project_completeness(project_path: Path) -> dict:
    """Анализирует полноту заполнения проекта"""
    sections = [
        "00_Администрирование",
        "01_Инициация_и_контекст", 
        "02_Требования",
        "03_Данные",
        "04_Аналитика",
        "05_Решение_и_дизайн",
        "06_Поставка_и_отчетность",
        "07_Качество_и_тестирование",
        "08_Документация"
    ]
    
    analysis = {}
    total_files = 0
    total_empty_folders = 0
    
    for section in sections:
        section_path = project_path / section
        stats = count_files_in_section(section_path)
        analysis[section] = stats
        total_files += stats["files"]
        total_empty_folders += stats["empty_folders"]
    
    # Оценка готовности проекта
    if total_files > 50:
        completeness = "Высокая"
    elif total_files > 25:
        completeness = "Средняя"
    else:
        completeness = "Низкая"
    
    return {
        "sections": analysis,
        "total_files": total_files,
        "total_empty_folders": total_empty_folders,
        "completeness": completeness
    }


def generate_report(project_path: Path) -> str:
    """Генерирует отчет о статусе проекта"""
    project_name = project_path.name
    analysis = analyze_project_completeness(project_path)
    
    report = f"""# 📊 Отчет о статусе проекта: {project_name}

**Дата создания:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Общая готовность:** {analysis['completeness']}  
**Всего файлов:** {analysis['total_files']}  
**Пустых папок:** {analysis['total_empty_folders']}

## 📈 Статистика по разделам

| Раздел | Файлов | Папок | Пустых папок | Статус |
|--------|---------|-------|--------------|---------|"""

    for section, stats in analysis['sections'].items():
        # Определяем статус секции
        if stats['files'] == 0:
            status = "❌ Не начат"
        elif stats['empty_folders'] > 0:
            status = "⚠️ В процессе"
        else:
            status = "✅ Готов"
        
        report += f"\n| {section} | {stats['files']} | {stats['folders']} | {stats['empty_folders']} | {status} |"

    # Добавляем рекомендации
    report += f"""

## 🎯 Рекомендации

### Приоритетные действия:"""

    # Анализируем какие разделы нужно заполнить в первую очередь
    priority_sections = []
    for section, stats in analysis['sections'].items():
        if stats['files'] < 2:  # Мало файлов в секции
            priority_sections.append(section)
    
    if priority_sections:
        report += "\n- 🔥 **Заполните критически важные разделы:**"
        for section in priority_sections[:3]:  # Топ 3
            report += f"\n  - {section}"
    
    if analysis['total_empty_folders'] > 0:
        report += f"\n- 📁 **Заполните {analysis['total_empty_folders']} пустых папок**"
    
    # Оценка времени до завершения
    if analysis['completeness'] == "Низкая":
        estimate = "3-5 дней"
    elif analysis['completeness'] == "Средняя":
        estimate = "1-2 дня"
    else:
        estimate = "Проект готов к передаче"
    
    report += f"""

### Оценка времени до готовности: {estimate}

## 📋 Следующие шаги

1. **Сегодня:** Заполните бриф проекта и основные требования
2. **На этой неделе:** Завершите анализ данных и создайте тест-кейсы  
3. **На следующей неделе:** Подготовьте документацию для передачи

---
*Отчет сгенерирован автоматически. Для обновления запустите: `python scripts/generate_status_report.py`*
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Генерация отчета о статусе проекта')
    parser.add_argument('--project', type=str, help='Путь к проекту')
    parser.add_argument('--all', action='store_true', help='Отчет по всем проектам')
    
    args = parser.parse_args()
    
    if args.project:
        project_path = Path(args.project)
        if not project_path.exists():
            print(f"❌ Проект не найден: {project_path}")
            return
        
        report = generate_report(project_path)
        
        # Сохраняем отчет
        report_path = project_path / f"STATUS_REPORT_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Отчет сохранен: {report_path}")
        print("\n" + "="*50)
        print(report)
        
    elif args.all:
        # Найти все аналитические проекты
        projects = []
        for item in Path('.').iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name == 'scripts':
                # Проверяем, что это аналитический проект
                if (item / '00_Администрирование').exists():
                    projects.append(item)
        
        if not projects:
            print("❌ Аналитические проекты не найдены")
            return
        
        print(f"📊 Найдено {len(projects)} проектов:")
        
        for project in projects:
            analysis = analyze_project_completeness(project)
            print(f"  📁 {project.name}: {analysis['completeness']} готовность, {analysis['total_files']} файлов")
    
    else:
        print("❌ Укажите --project или --all")


if __name__ == '__main__':
    main()
