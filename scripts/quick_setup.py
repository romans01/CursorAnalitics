#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрая настройка нового проекта с интерактивными вопросами
"""

import os
from pathlib import Path
from datetime import datetime
import subprocess


def ask_question(question: str, default: str = "") -> str:
    """Задает вопрос пользователю"""
    if default:
        prompt = f"{question} [{default}]: "
    else:
        prompt = f"{question}: "
    
    answer = input(prompt).strip()
    return answer if answer else default


def ask_yes_no(question: str, default: bool = True) -> bool:
    """Задает вопрос да/нет"""
    default_str = "Y/n" if default else "y/N"
    answer = input(f"{question} [{default_str}]: ").strip().lower()
    
    if not answer:
        return default
    
    return answer in ['y', 'yes', 'да', 'д']


def create_project_brief(project_path: Path, project_info: dict):
    """Создает заполненный бриф проекта"""
    brief_path = project_path / '00_Администрирование' / 'бриф.md'
    
    brief_content = f"""# Бриф проекта: {project_info['name']}

## Контекст и предпосылки

**Проблема:** {project_info['problem']}

**Текущая ситуация:** {project_info['current_situation']}

## Цели проекта

### Бизнес-цели
- [ ] **Основная цель:** {project_info['main_goal']}
- [ ] **Метрики успеха:** {project_info['success_metrics']}
- [ ] **Временные рамки:** {project_info['timeline']}

## Участники проекта

**Заказчик:** {project_info['customer']}  
**Аналитик:** {project_info['analyst']}  
**Команда разработки:** {project_info['dev_team']}

## Ограничения

**Бюджет:** {project_info['budget']}  
**Сроки:** {project_info['deadline']}  
**Технические ограничения:** {project_info['tech_constraints']}

## Ожидаемые результаты

{project_info['expected_results']}

---
*Создано: {datetime.now().strftime('%Y-%m-%d')}*
*Аналитик: {project_info['analyst']}*
"""
    
    with open(brief_path, 'w', encoding='utf-8') as f:
        f.write(brief_content)


def create_stakeholders(project_path: Path, project_info: dict):
    """Создает список заинтересованных сторон"""
    stakeholders_path = project_path / '00_Администрирование' / 'заинтересованные_стороны.md'
    
    content = f"""# Заинтересованные стороны проекта

## Основные участники

### 🎯 Заказчик
**{project_info['customer']}**
- Роль: Владелец продукта
- Ответственность: Постановка задач, приемка результатов
- Контакты: {project_info.get('customer_contact', 'указать контакты')}

### 👨‍💻 Команда проекта
**Аналитик:** {project_info['analyst']}  
**Разработка:** {project_info['dev_team']}

## Матрица RACI

| Задача | {project_info['customer']} | {project_info['analyst']} | Разработка | Тестирование |
|--------|------------|------------|------------|--------------|
| Требования | A | R | C | I |
| Анализ данных | I | R | C | I |
| Разработка | A | C | R | C |
| Тестирование | A | C | C | R |

**Легенда:**
- R (Responsible) - Исполнитель
- A (Accountable) - Ответственный  
- C (Consulted) - Консультант
- I (Informed) - Информируемый

---
*Обновлено: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    with open(stakeholders_path, 'w', encoding='utf-8') as f:
        f.write(content)


def setup_git_and_cursor(project_path: Path):
    """Настраивает Git и Cursor для проекта"""
    os.chdir(project_path)
    
    # Инициализация Git
    try:
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial project structure'], check=True, capture_output=True)
        print("✅ Git репозиторий инициализирован")
    except subprocess.CalledProcessError:
        print("⚠️ Не удалось инициализировать Git (возможно, не установлен)")
    except FileNotFoundError:
        print("⚠️ Git не найден в системе")


def main():
    print("🚀 Быстрая настройка нового аналитического проекта")
    print("=" * 50)
    
    # Сбор информации о проекте
    project_info = {}
    
    print("\n📋 Основная информация:")
    project_info['name'] = ask_question("Название проекта", "Аналитика_Новый_Проект")
    project_info['problem'] = ask_question("Какую проблему решаем?", "Нужно улучшить процесс аналитики")
    project_info['current_situation'] = ask_question("Как решается проблема сейчас?", "Ручная обработка данных")
    
    print("\n🎯 Цели и результаты:")
    project_info['main_goal'] = ask_question("Основная цель проекта", "Автоматизировать аналитические процессы")
    project_info['success_metrics'] = ask_question("Метрики успеха", "Сокращение времени на 50%")
    project_info['timeline'] = ask_question("Временные рамки", "2-3 месяца")
    project_info['expected_results'] = ask_question("Ожидаемые результаты", "Автоматизированные дашборды и отчеты")
    
    print("\n👥 Команда:")
    project_info['customer'] = ask_question("Заказчик", "Менеджер продукта")
    project_info['analyst'] = ask_question("Аналитик", os.getenv('USERNAME', 'Аналитик'))
    project_info['dev_team'] = ask_question("Команда разработки", "Backend + Frontend разработчики")
    
    print("\n💰 Ограничения:")
    project_info['budget'] = ask_question("Бюджет", "В рамках спринта")
    project_info['deadline'] = ask_question("Крайний срок", "Конец квартала")
    project_info['tech_constraints'] = ask_question("Технические ограничения", "Использовать существующую инфраструктуру")
    
    # Дополнительные опции
    print("\n⚙️ Дополнительные настройки:")
    use_template = ask_yes_no("Создать с примерами и шаблонами?", True)
    setup_git = ask_yes_no("Инициализировать Git репозиторий?", True)
    
    # Создание проекта
    print(f"\n🔨 Создание проекта '{project_info['name']}'...")
    
    # Вызов скрипта создания проекта
    cmd = ['python', 'scripts/create_project.py', '--name', project_info['name']]
    if use_template:
        cmd.append('--as-template')
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Структура проекта создана")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка создания проекта: {e}")
        return
    
    project_path = Path(project_info['name'])
    
    # Заполнение брифа и участников
    print("📝 Заполнение брифа проекта...")
    create_project_brief(project_path, project_info)
    create_stakeholders(project_path, project_info)
    
    # Настройка Git
    if setup_git:
        print("🔧 Настройка Git...")
        setup_git_and_cursor(project_path)
    
    # Добавление CSV файлов если это шаблон
    if use_template:
        print("📊 Добавление примеров данных...")
        try:
            subprocess.run(['python', 'scripts/add_missing_files.py'], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("⚠️ Не удалось добавить примеры файлов")
    
    print("\n🎉 Проект успешно настроен!")
    print("=" * 50)
    print(f"📁 Путь к проекту: {project_path.absolute()}")
    print("\n📋 Следующие шаги:")
    print("1. Откройте проект в Cursor")
    print("2. Проведите интервью с заказчиком")
    print("3. Заполните требования и пользовательские истории")
    print("4. Начните анализ данных")
    
    # Генерация первого отчета
    if ask_yes_no("Сгенерировать отчет о статусе проекта?", True):
        try:
            subprocess.run(['python', 'scripts/generate_status_report.py', '--project', str(project_path)], 
                         check=True)
        except subprocess.CalledProcessError:
            print("⚠️ Не удалось создать отчет о статусе")


if __name__ == '__main__':
    main()
