# Jupyter Notebooks

## Назначение
Интерактивные блокноты для исследовательского анализа данных, прототипирования алгоритмов и документирования результатов.

## Структура файлов
- `01_data_exploration.ipynb` — первичный анализ данных
- `02_data_cleaning.ipynb` — очистка и подготовка данных
- `03_feature_engineering.ipynb` — создание признаков
- `04_modeling.ipynb` — построение моделей
- `05_results_analysis.ipynb` — анализ результатов

## Соглашения по именованию
- Префикс с номером для порядка выполнения
- Описательное название на английском
- Расширение `.ipynb`

## Стандарты оформления

### Структура ноутбука
1. **Заголовок и описание** — цель анализа, краткое описание
2. **Импорты** — все необходимые библиотеки
3. **Загрузка данных** — подключение к источникам
4. **Исследовательский анализ** — EDA с визуализацией
5. **Выводы** — ключевые инсайты и рекомендации

### Требования к коду
- Комментарии на русском языке
- Markdown ячейки для пояснений
- Очистка вывода перед коммитом
- Версионирование больших датасетов отдельно

## Полезные библиотеки
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
```

## Шаблон ноутбука
```python
# Заголовок
# Анализ [название]: [краткое описание]
# Автор: [ФИО]
# Дата: [YYYY-MM-DD]

# Импорты
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Настройки
plt.style.use('seaborn')
pd.set_option('display.max_columns', None)

# Загрузка данных
data = pd.read_csv('path/to/data.csv')

# Первичный осмотр
print("Размер данных:", data.shape)
print("\nИнформация о данных:")
data.info()

# Анализ и выводы...
```
