# Парсер картинок PNG формата
* Версия 0.6
## Требования:
* Python3 и выше
* PyQt5 и выше
## Описание:
*  Данное приложение является реализацией парсера картинок PNG формата. Выводит пользователю информацию о изображении PNG формата (информацию с контейнеров данных - chunks, из которых состоит PNG картинка). Реализована обработка ошибок ввода, чанков, проверка их корректности и т.д. (Почти соответсвует требованиям к декодеру PNG). 
## TODO:
* Попиксельная отрисовка изображения, вывод информации в GUI, добавление флага GUI на вывод доп. информации. 
## Состав:
* Консольная версия: png_main.py
* Изображения для тестирования (The "official" test-suite for PNG): pictures/
## Структура:
* PngInfo.py - Класс (контейнер-репрезентатор) информации о PNG изображении 
* PngParser.py - Класс, реализующий парсинг chunks
* window.py - Класс GUI
## Консольная версия:
* Справка по запуску: png_main.py -h
* Пример запуска: python png_main.py -f pictures/chroma.png -g

(c) rZb.K 2018.
