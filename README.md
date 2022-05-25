# Geo-treasure

Веб проект по агрегации интересных локаций для путешественников в регионе (в текущей версии только Республика Адыгея и Краснодарский край). Интересные места собираются из нескольких источников, затем происходит кластеризация и вывод результатов на интерактивную карту.

## Используемые источники

- [geocaching.su](https://geocaching.su/) - Туристская игра с применением спутниковых навигационных систем, состоящая в нахождении тайников, спрятанных другими участниками игры.
- [altertravel.ru](https://altertravel.ru/) - Альтернативный путеводитель.
- [autotravel.ru](https://autotravel.ru/) - Здесь собраны и постоянно дополняются сведения, помогающие спланировать содержательную поездку по стране.

## Использование проекта

Эти инструкции помогут Вам сделать копию проекта и запустить его локально для использования в ваших целях.

### Установка проекта

Вначале репозиторий необходимо склонировать:

```shell
    $ git clone https://github.com/Shevelsm/geo-treasure
    $ cd geo-treasure
```

Для корректной работы проекта рекомендуется создавать виртуальное окружение (Python 3.6) и активировать его.

Для Linux/Mac:

```bash
    $ python3 -m venv venv
    $ . venv/bin/activate
```

Для Windows:

```cmd
    py -3 -m venv venv
    venv\Scripts\activate.bat
```

Для установки необходимого окружения так же удобно использовать менеджер `conda` ([установка](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html))

```bash
    conda create python=3.6 -n geo-treasure
```

Далее необходимо установить все требуемые зависимости для работы проекта с помощью пакетного менеджера pip.

```bash
    pip install -r ./requirements.txt
```

Так как название веб приложения отличается от дефолтного, нужно определить переменную окружения  `FLASK_APP`.

Для Linux/Mac:

```bash
    $ export FLASK_APP=geotreasure/__init__.py
```

Для Windows:

```cmd
    set FLASK_APP=geotreasure/__init__.py
```

После установки требуется инициализирвать базу данных (SQLite) и применить миграции, используя flask.

```bash
    flask db upgrade
```

Затем, запустите парсеры используемых источников при помощи скрипта. Это заполнит базу данных точками.
Скрипт можно запустить для всех источников сразу, либо отдельно для каждого.

```bash
    # Парсинг всех источников:
    python parse_points.py
    # Парсинг geocaching.su:
    python parse_points.py --geo
    # Парсинг altertraver.ru:
    python parse_points.py --alter
    # Парсинг autotravel.ru:
    python parse_points.py --auto
```

После того, как точки появятся в базе данных необходимо запустить скрипт по созданию кластеров и их записи в базу данных.

```bash
python calculate_clusters.py
```

Парсинг источников и запуск кластреизации может запускаться по расписанию при помощи `Celery` и выбранного Вами **message-broker**.
Для этого подготовлен worker - `tasks.py`.

**После этого всё готово для запуска flask приложения!**

## В планах проекта

- Testing Coverage;
- Переход на альтернативную СУБД;
- Добавление функционала пользователя;
- И так далее...

## Авторы

- **Алексей Шевелев** - _Initial work_ - [shevelsm](https://github.com/Shevelsm)
- **Дмитрий Магнич** - _Initial work_ - [dmitry-mag](https://github.com/dmitry-mag)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Большое спасибо Stanislav Khoshov ([khoshov](https://github.com/khoshov))
