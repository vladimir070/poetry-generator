# Генератор поэзии на основе цепи Маркова

Генератор стихотворений с использованием цепи Маркова, тематических словарей и системы рифмовки.

## Требования
- Python 3.8+
- Библиотеки: `nltk`, `random`

## Установите зависимости:
pip install nltk

## Использование
python poetry_generator.py

Пример вывода:

Moonlight weaves through silvered leaves.
Horizons breathe with ancient sighs.
Tides of time erode the shore.
The void between the stars implores.

## Особенности
Тематические словари (природа, время)
Автоматический подбор рифм
Контроль слоговой структуры
Защита от повторов
Fallback-система

## Структура
MarkovGenerator - построение цепей Маркова
RhymeEngine - система рифмовки
PoetryGenerator - основной генератор

Лицензия
MIT License
