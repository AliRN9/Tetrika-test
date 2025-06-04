# Тестовое задание

Тестовое задание решено использую python 3.12

## Установка и запуск тестов

```bash
#Linux
git clone https://github.com/AliRN9/Tetrika-test
cd Tetrika-test
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
pytest tests

#Windows
git clone https://github.com/AliRN9/Tetrika-test
cd Tetrika-test
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
pytest tests 
```

## Структура

- `task1`: Декоратор типо данных
- `task2`: Парсер животных
- `task3`: Пересечение интервалов
- `test`: Тесты для всех задач 
