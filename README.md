# Gmsh Project

![Gmsh Logo](https://gmsh.info/img/gmsh_logo.png)

## Описание
Этот проект использует **Gmsh** — мощный инструмент для генерации конечных элементов, построения сеток и работы с геометрией. Здесь вы найдете скрипты, примеры и инструкции по использованию Gmsh для различных задач.

## Возможности
- Создание 2D и 3D сеток
- Импорт и экспорт геометрии в различных форматах
- Настройка параметрических моделей
- Генерация конечных элементов различного порядка
- Автоматическое и адаптивное уплотнение сетки

## Установка
### Установка Gmsh
1. **Скачать и установить** Gmsh с [официального сайта](https://gmsh.info/):
   - Windows: установочный `.exe`
   - Linux: бинарный `.AppImage`
   - macOS: `.dmg` или компиляция из исходников
2. **Проверить установку**:
   ```bash
   gmsh -version
   ```

### Альтернативная установка через Python
Если вы используете Python, можно установить Gmsh как библиотеку:
```bash
pip install gmsh
```

## Использование
### Генерация сетки
1. **Создайте геометрию в файле `.geo`**, например `example.geo`:
   ```c
   SetFactory("OpenCASCADE");
   Rectangle(1) = {0, 0, 0, 10, 5};
   Mesh 2;
   Save("example.msh");
   ```
2. **Запустите Gmsh для генерации сетки**:
   ```bash
   gmsh example.geo -2 -o example.msh
   ```

### Использование API Gmsh в Python
Пример скрипта на Python для создания сетки:
```python
import gmsh

gmsh.initialize()
gmsh.model.add("square")
factory = gmsh.model.geo
factory.addRectangle(0, 0, 0, 10, 5)
factory.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write("square.msh")
gmsh.finalize()
```
Запуск:
```bash
python script.py
```

## Форматы файлов
- **`.geo`** — входной файл с описанием геометрии.
- **`.msh`** — выходной файл с сеткой (совместим с FEM-пакетами).
- **`.step`**, **`.stl`** — импорт/экспорт CAD-моделей.

## Полезные ресурсы
- [Официальный сайт Gmsh](https://gmsh.info/)
- [Документация](https://gmsh.info/doc/texinfo/gmsh.html)
- [Примеры](https://gitlab.onelab.info/gmsh/gmsh/-/tree/master/tutorials)

## Лицензия
Этот проект распространяется под лицензией **MIT**.

