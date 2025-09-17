# Шаблон для Jupyter Notebook
# Сохраните как .ipynb файл

# =============================================================================
# Анализ данных: [Название проекта]
# Автор: [ФИО]
# Дата: [YYYY-MM-DD]
# Цель: [Описание цели анализа]
# =============================================================================

# %% [markdown]
# # Анализ данных: [Название]
# 
# ## Цель исследования
# [Описать цель анализа]
# 
# ## Гипотезы
# 1. [Гипотеза 1]
# 2. [Гипотеза 2]
# 
# ## Источники данных
# - [Источник 1]: описание
# - [Источник 2]: описание

# %% Импорты и настройки
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Настройки визуализации
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
sns.set_palette("husl")

# Настройки pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

print("✅ Библиотеки загружены")

# %% [markdown]
# ## 1. Загрузка и первичный осмотр данных

# %% Загрузка данных
# Замените на ваши источники данных
data = pd.read_csv('data/sample_data.csv')

print(f"Размер данных: {data.shape}")
print(f"Период данных: {data['date'].min()} - {data['date'].max()}")

# %% Первичный анализ
print("Информация о данных:")
data.info()

print("\nСтатистические характеристики:")
data.describe()

print("\nПропущенные значения:")
missing = data.isnull().sum()
print(missing[missing > 0])

# %% [markdown]
# ## 2. Исследовательский анализ данных (EDA)

# %% Распределения числовых переменных
numeric_cols = data.select_dtypes(include=[np.number]).columns
n_cols = len(numeric_cols)
n_rows = (n_cols + 2) // 3

fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5*n_rows))
axes = axes.flatten() if n_rows > 1 else [axes]

for i, col in enumerate(numeric_cols):
    if i < len(axes):
        data[col].hist(bins=30, ax=axes[i])
        axes[i].set_title(f'Распределение {col}')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Частота')

# Скрываем лишние subplot'ы
for i in range(len(numeric_cols), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.show()

# %% Корреляционная матрица
plt.figure(figsize=(10, 8))
correlation_matrix = data[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Корреляционная матрица')
plt.show()

# %% [markdown]
# ## 3. Проверка гипотез

# %% Гипотеза 1
# [Код для проверки первой гипотезы]
print("Результаты проверки гипотезы 1:")
# Ваш код здесь

# %% Гипотеза 2
# [Код для проверки второй гипотезы]
print("Результаты проверки гипотезы 2:")
# Ваш код здесь

# %% [markdown]
# ## 4. Выводы и рекомендации

# %% Ключевые инсайты
insights = [
    "Инсайт 1: [описание]",
    "Инсайт 2: [описание]", 
    "Инсайт 3: [описание]"
]

print("🔍 Ключевые выводы:")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")

# %% Рекомендации
recommendations = [
    "Рекомендация 1: [описание]",
    "Рекомендация 2: [описание]",
    "Рекомендация 3: [описание]"
]

print("\n💡 Рекомендации:")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

# %% [markdown]
# ## 5. Следующие шаги
# 
# - [ ] Собрать дополнительные данные по [тема]
# - [ ] Провести A/B тест для проверки [гипотеза]
# - [ ] Создать модель для предсказания [целевая переменная]
# - [ ] Автоматизировать анализ в виде дашборда
