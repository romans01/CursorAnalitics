#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка качества аналитического проекта
"""

import os
import re
from pathlib import Path
from datetime import datetime, timedelta
import argparse


class QualityChecker:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.issues = []
        self.warnings = []
        self.suggestions = []
    
    def check_required_files(self):
        """Проверяет наличие обязательных файлов"""
        required_files = [
            '00_Администрирование/бриф.md',
            '00_Администрирование/заинтересованные_стороны.md',
            '02_Требования/видение.md',
            '02_Требования/критерии_приемки.md',
            '07_Качество_и_тестирование/план_тестирования.md',
            'README.md'
        ]
        
        for file_path in required_files:
            full_path = self.project_path / file_path
            if not full_path.exists():
                self.issues.append(f"❌ Отсутствует обязательный файл: {file_path}")
            elif full_path.stat().st_size < 100:  # Меньше 100 байт
                self.warnings.append(f"⚠️ Файл слишком короткий: {file_path}")
    
    def check_file_freshness(self):
        """Проверяет актуальность файлов"""
        week_ago = datetime.now() - timedelta(days=7)
        month_ago = datetime.now() - timedelta(days=30)
        
        important_files = [
            '00_Администрирование/дорожная_карта.md',
            '02_Требования/BRD_бизнес_требования.md',
            '02_Требования/SRS_системные_требования.md'
        ]
        
        for file_path in important_files:
            full_path = self.project_path / file_path
            if full_path.exists():
                modified_time = datetime.fromtimestamp(full_path.stat().st_mtime)
                if modified_time < month_ago:
                    self.warnings.append(f"⚠️ Файл не обновлялся больше месяца: {file_path}")
                elif modified_time < week_ago:
                    self.suggestions.append(f"💡 Рекомендуется обновить: {file_path}")
    
    def check_content_quality(self):
        """Проверяет качество содержимого"""
        # Проверка брифа
        brief_path = self.project_path / '00_Администрирование/бриф.md'
        if brief_path.exists():
            content = brief_path.read_text(encoding='utf-8')
            
            # Проверяем заполненность ключевых разделов
            if '[описание]' in content or '[TODO]' in content:
                self.issues.append("❌ Бриф содержит незаполненные плейсхолдеры")
            
            if len(content) < 500:
                self.warnings.append("⚠️ Бриф слишком короткий (менее 500 символов)")
            
            # Проверяем наличие ключевых слов
            keywords = ['цель', 'проблема', 'метрики', 'результат']
            missing_keywords = [kw for kw in keywords if kw.lower() not in content.lower()]
            if missing_keywords:
                self.suggestions.append(f"💡 В брифе желательно упомянуть: {', '.join(missing_keywords)}")
        
        # Проверка пользовательских историй
        stories_path = self.project_path / '02_Требования/пользовательские_истории'
        if stories_path.exists():
            story_files = list(stories_path.glob('*.md'))
            if len(story_files) < 3:
                self.warnings.append("⚠️ Мало пользовательских историй (менее 3)")
            
            # Проверяем формат User Stories
            for story_file in story_files:
                if story_file.name == 'README.md':
                    continue
                content = story_file.read_text(encoding='utf-8')
                if 'Как' not in content or 'я хочу' not in content or 'чтобы' not in content:
                    self.warnings.append(f"⚠️ Неправильный формат User Story: {story_file.name}")
    
    def check_data_documentation(self):
        """Проверяет документацию данных"""
        data_section = self.project_path / '03_Данные'
        
        # Проверяем источники данных
        sources_file = data_section / 'источники_данных.md'
        if not sources_file.exists() or sources_file.stat().st_size < 200:
            self.issues.append("❌ Недостаточно информации об источниках данных")
        
        # Проверяем словари данных
        dict_folder = data_section / 'словари_данных'
        if dict_folder.exists():
            dict_files = list(dict_folder.glob('*.md'))
            if not dict_files:
                self.warnings.append("⚠️ Отсутствуют словари данных")
        
        # Проверяем примеры данных
        samples_folder = data_section / 'выборки_и_примеры'
        if samples_folder.exists():
            sample_files = list(samples_folder.glob('*.csv')) + list(samples_folder.glob('*.json'))
            if not sample_files:
                self.suggestions.append("💡 Добавьте примеры данных для лучшего понимания")
    
    def check_testing_coverage(self):
        """Проверяет покрытие тестированием"""
        testing_section = self.project_path / '07_Качество_и_тестирование'
        
        # Проверяем тест-кейсы
        test_cases_folder = testing_section / 'тест_кейсы'
        if test_cases_folder.exists():
            test_files = list(test_cases_folder.glob('*.md'))
            if len(test_files) < 2:  # Меньше 2 файлов (включая README)
                self.warnings.append("⚠️ Мало тест-кейсов для качественного тестирования")
        
        # Проверяем UAT сценарии
        uat_folder = testing_section / 'сценарии_UAT'
        if uat_folder.exists():
            uat_files = list(uat_folder.glob('*.md'))
            if len(uat_files) < 2:
                self.suggestions.append("💡 Добавьте UAT сценарии для приемочного тестирования")
    
    def check_empty_folders(self):
        """Проверяет пустые папки"""
        empty_folders = []
        
        for item in self.project_path.rglob('*'):
            if item.is_dir() and not any(item.iterdir()):
                # Игнорируем системные папки
                if not any(part.startswith('.') for part in item.parts):
                    empty_folders.append(item.relative_to(self.project_path))
        
        if empty_folders:
            self.warnings.append(f"⚠️ Найдено {len(empty_folders)} пустых папок")
            for folder in empty_folders[:5]:  # Показываем первые 5
                self.suggestions.append(f"💡 Заполните папку: {folder}")
    
    def check_documentation_links(self):
        """Проверяет ссылки в документации"""
        readme_path = self.project_path / 'README.md'
        if readme_path.exists():
            content = readme_path.read_text(encoding='utf-8')
            
            # Ищем markdown ссылки
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            broken_links = []
            
            for link_text, link_path in links:
                if link_path.startswith('http'):
                    continue  # Пропускаем внешние ссылки
                
                # Проверяем внутренние ссылки
                full_link_path = self.project_path / link_path
                if not full_link_path.exists():
                    broken_links.append(f"{link_text} -> {link_path}")
            
            if broken_links:
                self.warnings.append(f"⚠️ Найдено {len(broken_links)} битых ссылок в README")
    
    def calculate_score(self):
        """Вычисляет общий балл качества проекта"""
        # Базовый балл
        score = 100
        
        # Снимаем баллы за проблемы
        score -= len(self.issues) * 10  # Критичные проблемы
        score -= len(self.warnings) * 5  # Предупреждения
        # Предложения не влияют на балл
        
        return max(0, score)
    
    def get_quality_level(self, score):
        """Определяет уровень качества"""
        if score >= 90:
            return "🏆 Отличное качество"
        elif score >= 70:
            return "✅ Хорошее качество"
        elif score >= 50:
            return "⚠️ Удовлетворительное качество"
        else:
            return "❌ Требует доработки"
    
    def run_all_checks(self):
        """Запускает все проверки"""
        print(f"🔍 Проверка качества проекта: {self.project_path.name}")
        print("=" * 50)
        
        self.check_required_files()
        self.check_file_freshness()
        self.check_content_quality()
        self.check_data_documentation()
        self.check_testing_coverage()
        self.check_empty_folders()
        self.check_documentation_links()
        
        # Подсчет результатов
        score = self.calculate_score()
        quality_level = self.get_quality_level(score)
        
        return {
            'score': score,
            'quality_level': quality_level,
            'issues': self.issues,
            'warnings': self.warnings,
            'suggestions': self.suggestions
        }


def generate_quality_report(project_path: Path, results: dict):
    """Генерирует отчет о качестве проекта"""
    report = f"""# 🔍 Отчет о качестве проекта: {project_path.name}

**Дата проверки:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Общий балл:** {results['score']}/100  
**Уровень качества:** {results['quality_level']}

## 📊 Сводка

- ❌ Критичные проблемы: {len(results['issues'])}
- ⚠️ Предупреждения: {len(results['warnings'])}  
- 💡 Предложения: {len(results['suggestions'])}

"""

    if results['issues']:
        report += "## ❌ Критичные проблемы\n\n"
        for issue in results['issues']:
            report += f"- {issue}\n"
        report += "\n"
    
    if results['warnings']:
        report += "## ⚠️ Предупреждения\n\n"
        for warning in results['warnings']:
            report += f"- {warning}\n"
        report += "\n"
    
    if results['suggestions']:
        report += "## 💡 Рекомендации по улучшению\n\n"
        for suggestion in results['suggestions']:
            report += f"- {suggestion}\n"
        report += "\n"
    
    # Добавляем план действий
    report += "## 🎯 План действий\n\n"
    
    if results['score'] < 50:
        report += """### Критический уровень - немедленные действия:
1. Устраните все критичные проблемы
2. Заполните обязательные файлы
3. Добавьте базовую документацию
4. Проведите повторную проверку через 1-2 дня
"""
    elif results['score'] < 70:
        report += """### Требует улучшения:
1. Исправьте критичные проблемы
2. Обратите внимание на предупреждения
3. Улучшите качество документации
4. Добавьте недостающие тест-кейсы
"""
    elif results['score'] < 90:
        report += """### Хорошее качество - финальные штрихи:
1. Рассмотрите рекомендации
2. Обновите устаревшую документацию
3. Добавьте примеры данных
4. Проверьте ссылки в документации
"""
    else:
        report += """### Отличная работа! 🎉
Проект готов к передаче. Рекомендуется:
1. Периодически обновлять документацию
2. Следить за актуальностью требований
3. Собирать обратную связь от команды
"""
    
    report += f"""
---
*Отчет сгенерирован автоматически*  
*Для повторной проверки: `python scripts/quality_check.py --project {project_path.name}`*
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Проверка качества аналитического проекта')
    parser.add_argument('--project', type=str, help='Путь к проекту')
    parser.add_argument('--all', action='store_true', help='Проверить все проекты')
    parser.add_argument('--save-report', action='store_true', help='Сохранить отчет в файл')
    
    args = parser.parse_args()
    
    if args.project:
        project_path = Path(args.project)
        if not project_path.exists():
            print(f"❌ Проект не найден: {project_path}")
            return
        
        checker = QualityChecker(project_path)
        results = checker.run_all_checks()
        
        # Вывод результатов
        print(f"\n🎯 Результат: {results['quality_level']}")
        print(f"📊 Балл качества: {results['score']}/100")
        
        if results['issues']:
            print(f"\n❌ Критичные проблемы ({len(results['issues'])}):")
            for issue in results['issues'][:5]:  # Показываем первые 5
                print(f"  {issue}")
        
        if results['warnings']:
            print(f"\n⚠️ Предупреждения ({len(results['warnings'])}):")
            for warning in results['warnings'][:5]:  # Показываем первые 5
                print(f"  {warning}")
        
        if results['suggestions']:
            print(f"\n💡 Рекомендации ({len(results['suggestions'])}):")
            for suggestion in results['suggestions'][:3]:  # Показываем первые 3
                print(f"  {suggestion}")
        
        # Сохранение отчета
        if args.save_report:
            report = generate_quality_report(project_path, results)
            report_path = project_path / f"QUALITY_REPORT_{datetime.now().strftime('%Y%m%d')}.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n✅ Отчет сохранен: {report_path}")
    
    elif args.all:
        # Проверка всех проектов
        projects = []
        for item in Path('.').iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name == 'scripts':
                if (item / '00_Администрирование').exists():
                    projects.append(item)
        
        if not projects:
            print("❌ Аналитические проекты не найдены")
            return
        
        print(f"🔍 Проверка {len(projects)} проектов:\n")
        
        for project in projects:
            checker = QualityChecker(project)
            results = checker.run_all_checks()
            print(f"📁 {project.name}: {results['score']}/100 - {results['quality_level']}")
    
    else:
        print("❌ Укажите --project или --all")


if __name__ == '__main__':
    main()
