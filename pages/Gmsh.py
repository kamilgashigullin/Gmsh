import streamlit as st
from PIL import Image
import base64
import subprocess
import os
import math

# Функция для отображения кода с возможностью копирования
def show_code(code, language="python"):
    st.code(code, language)

def run_gmsh(file_path):
    try:
        env = os.environ.copy()
        env["LIBGL_ALWAYS_SOFTWARE"] = "1"  # Используем программный рендеринг
        subprocess.run(["gmsh", file_path], check=True, env=env)
        st.success("Gmsh успешно запущен в программном режиме!")
    except FileNotFoundError:
        st.error("Gmsh не найден. Убедитесь, что он установлен и доступен в PATH.")
    except subprocess.CalledProcessError:
        st.error("Ошибка при запуске Gmsh.")

st.set_page_config(page_title="Руководство по работе с Gmsh", layout="wide")
st.sidebar.title("Навигация")
sections = {
    "Общая характеристика ПО": "Описание возможностей и предназначения Gmsh.",
    "Установка": "Инструкции по установке необходимых компонентов.",
    "Геометрические элементы": "Основные примитивы и способы их задания.",
    "Файл геометрии": "Формат и структура файлов геометрии в Gmsh.",
    "Создание области": "Методы задания расчетной области.",
    "Интерактивные возможности создания области": "Использование графического интерфейса для работы с геометрией.",
    "Составные области": "Работа со сложными геометрическими структурами.",
    "Маркирование подобластей и частей границ": "Назначение меток для различных частей геометрии.",
    "Генерация сетки": "Процесс создания расчетной сетки.",
    "Сгущение сетки": "Методы локального и глобального сгущения сетки.",
    "Подготовка сетки для FEniCS": "Экспорт и адаптация сетки для использования в FEniCS.",
    "Constructive Solid Geometry технология в Gmsh": "Применение CSG в построении геометрии.",
    "Библиотеки Python pygmsh и meshio": "Использование Python-библиотек для работы с сетками.",
}

choice = st.sidebar.radio("Выберите раздел", list(sections.keys()))

st.title(choice)
st.write(sections[choice])

if choice == "Общая характеристика ПО":
    st.header("Gmsh")
    st.write(
            """
            **Gmsh** — это открытое программное обеспечение для генерации конечных элементов (mesh generation).
            Оно используется в численном моделировании и вычислительной механике, особенно в методе конечных элементов (FEM).
            """
        )
    st.subheader("Основные возможности Gmsh")
    st.markdown(
        """
        - Генерация двумерных и трехмерных сеток
        - Поддержка различных типов элементов (треугольники, тетраэдры, гексаэдры и т. д.)
        - Встроенный язык сценариев (Gmsh scripting language)
        - Визуализация и постобработка
        - Импорт и экспорт в различные форматы (STEP, STL, MSH и др.)
        - Поддержка параметризированного моделирования
        """
        )
        
    st.subheader("Применение Gmsh")
    st.write(
        """
        Gmsh активно применяется в различных областях инженерии и науки:
        - Аэродинамика
        - Машиностроение
        - Биомеханика
        - Электромагнетизм
        - Геофизика
        """
        )
        
    st.subheader("Пример кода для создания сетки")
    code = """
        SetFactory("OpenCASCADE");
        lc = 1e-2;
        Point(1) = {0, 0, 0, lc};
        Point(2) = {.1, 0, 0, lc};
        Point(3) = {.1, .3, 0, lc};
        Point(4) = {0, .3, 0, lc};

        Line(1) = {1, 2};
        Line(2) = {2, 3}; // Обратите внимание на порядок
        Line(3) = {3, 4};
        Line(4) = {4, 1};

        Curve Loop(1) = {4, 1, -2, 3};
        Plane Surface(1) = {1};

        Physical Curve(5) = {1, 2, 4};
        Physical Surface("My surface") = {1};

        
        Rectangle(2) = {0.2, 0.0, 0.0, 0.1, 0.3};
        Geometry.PointNumbers = 1;
        Geometry.Color.Points = {0, 255, 0};
        General.Color.Text = White;
        Geometry.Color.Surfaces = Geometry.Color.Points;


        Mesh 2;
        
    """
    st.code(code, language="plaintext")
    
    if st.button("Запустить пример"):
        file_path = "example.geo"
        with open(file_path, "w") as f:
            f.write(code)
        run_gmsh(file_path)
    st.subheader("Ссылки и ресурсы")
    st.markdown("[Официальный сайт Gmsh](https://gmsh.info/)")
    st.markdown("[Документация Gmsh](https://gmsh.info/doc/texinfo/gmsh.html)")

elif choice == "Установка":

    st.write("""

    - **Windows:**
        1. Перейдите на страницу [с загрузками Gmsh для Windows](http://gmsh.info/).
        2. Скачайте и установите `.exe` файл для вашей системы (обычно это файл с расширением `.exe`).
        3. Следуйте инструкциям мастера установки.
        4. После установки Gmsh будет доступен для использования.

    - **Linux:**
        1. Используйте команду для установки Gmsh через пакетный менеджер:
            - Для Ubuntu/Debian:
              ```bash
              sudo apt-get install gmsh
              ```
            - Для Fedora:
              ```bash
              sudo dnf install gmsh
              ```

        2. Для установки последней версии Gmsh можно также скомпилировать из исходников с [официального репозитория Gmsh](http://gmsh.info/).

    - **macOS:**
        1. Используйте Homebrew для установки Gmsh:
            ```bash
            brew install gmsh
            ```

        2. Альтернативно можно скачать установщик с [официального сайта Gmsh](http://gmsh.info/).

    """)

    # Кнопка для скачивания Gmsh для Windows
    if st.button("Скачать Gmsh для Windows"):
        st.write("Вы можете скачать Gmsh для Windows по [ссылке](http://gmsh.info/#Download).")

    # Кнопка для установки Gmsh через Homebrew на macOS
    if st.button("Установить Gmsh на macOS"):
        st.write("Для установки Gmsh через Homebrew на macOS, выполните команду: `brew install gmsh`.")

    # Кнопка для установки Gmsh на Linux
    if st.button("Установить Gmsh на Linux"):
        st.write("Для установки Gmsh на Linux используйте команду: `sudo apt-get install gmsh` на Ubuntu/Debian или `sudo dnf install gmsh` на Fedora.")

elif choice == "Геометрические элементы":
    dimensions = st.selectbox("Выберите размерность",["0D", "1D", "2D", "3D"])
    if dimensions == "0D":
        element_0D = st.selectbox("Выберите тип элемента", ["Point", "Physical Point"])
        if element_0D == "Point":
            st.write("""
            ```bash 
            Point ( expression ) = { expression, expression, expression <, expression > }
            ```
            - **Тег точки**
            - **Координаты точки X, Y, Z**
            - **Размер элемента сетки в этой точке (не обязательный параметр)**
            """)
            code = """
            //Point
            lc = 1e-2;
            Point(1) = {0, 0, 0, lc};
            Point(2) = {.1, 0, 0, lc};
            Point(3) = {.1, .3, 0, lc};
            Point(4) = {0, .3, 0, lc};
            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;
            """
            st.code(code, language="plaintext")
    
            if st.button("Запустить пример"):
                file_path = "example.geo"
                with open(file_path, "w") as f:
                    f.write(code)
                run_gmsh(file_path)

        elif element_0D == "Physical Point":
            st.write("""

            ```bash 
            Physiacal Point ( expression ) = { expression, expression, expression <, expression > }
            ```
            - **Тег точки**
            - **Теги всех элементарных точек, которые необходимо сгруппировать внутри физической точки**

            Если вместо выражения внутри скобок указано строковое выражение, то с физическим тегом связывается строковая метка, которая может быть указана явно (после запятой) или нет (в этом случае автоматически создается уникальный тег).
            """)
            code = """
            //Physiacal Point
            lc = 1e-2;
            p = newp;
            Point(p) = {0.07, 0.15, 0.025, lc};
            Physical Point("Embedded point") = {p};

            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;
            """
            st.code(code, language="plaintext")

            if st.button("Запустить пример"):
                file_path = "example.geo"
                with open(file_path, "w") as f:
                    f.write(code)
                run_gmsh(file_path)

    elif dimensions == "1D":
        element_type = st.selectbox("Выберите тип элемента", ["Line", "Bezier", "Spline", "BSpline", "Circle", "Ellipse", "Curve Loop", "Physical Curve"])

        if element_type == "Line":
            st.write("""

            ```bash 
            Line ( expression ) = { expression, expression };
            ```
            - **Тег отрезка прямой линии**
            - **Теги начальной и конечной точек**

            """)
            x1, y1, z1 = st.number_input("X1", value=0.0), st.number_input("Y1", value=0.0), st.number_input("Z1", value=0.0)
            x2, y2, z2 = st.number_input("X2", value=1.0), st.number_input("Y2", value=0.0), st.number_input("Z2", value=0.0)
            geo_code = f"""
            //Line
            Point(1) = {{{x1}, {y1}, {z1}, 1.0}};
            Point(2) = {{{x2}, {y2}, {z2}, 1.0}};
            Line(1) = {{1, 2}};
            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;
            """

        elif element_type == "Bezier":
            st.write("""
            ```bash
            Bezier ( expression ) = { expression-list };
            ```
            - **Тег кривой Безье**
            - **Список выражений содержит теги контрольных точек**
            """)
            if "points" not in st.session_state:
                st.session_state.points = [(0, 0, 0), (5, 5, 5), (10, 0, 1)]  # Начальные точки

            new_points = []
            for i, (x, y, z) in enumerate(st.session_state.points):
                col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                x_val = col1.number_input(f"X{i+1}", value=x, key=f"x_{i}")
                y_val = col2.number_input(f"Y{i+1}", value=y, key=f"y_{i}")
                z_val = col3.number_input(f"Z{i+1}", value=z, key=f"z_{i}")
                if col4.button("❌", key=f"remove_{i}"):
                    st.session_state.points.pop(i)
                    st.rerun()
                new_points.append((x_val, y_val, z_val))
            st.session_state.points = new_points
            if st.button("Добавить точку"):
                st.session_state.points.append((0, 0, 0))
                st.rerun()
            geo_code = """//Bezier\n"""
            for i, (x, y, z) in enumerate(st.session_state.points, start=1):
                geo_code += f"Point({i}) = {{{x}, {y}, {z}, 1.0}};\n"
            geo_code += f"Bezier(1) = {{{', '.join(str(i+1) for i in range(len(st.session_state.points)))}}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {0, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

        elif element_type == "Spline":

            st.write("""

            ```bash 
            Spline ( expression ) = { expression-list };
            ```
            - **Тег сплайна**
            - **Теги точек сплайна**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. С помощью встроенного ядра геометрии создается сплайн Catmull-Rom.
            2. С помощью ядра OpenCASCADE создается BSpline.
            3. Если первая и последняя точка совпадают, тогда строится периодическая кривая.
            """)

            if "points" not in st.session_state:
                st.session_state.points = [(0, 0, 0), (5, 5, 5), (10, 0, 1)]  # Начальные точки

            new_points = []
            for i, (x, y, z) in enumerate(st.session_state.points):
                col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                x_val = col1.number_input(f"X{i+1}", value=x, key=f"x_{i}")
                y_val = col2.number_input(f"Y{i+1}", value=y, key=f"y_{i}")
                z_val = col3.number_input(f"Z{i+1}", value=z, key=f"z_{i}")
                if col4.button("❌", key=f"remove_{i}"):
                    st.session_state.points.pop(i)
                    st.rerun()
                new_points.append((x_val, y_val, z_val))
            st.session_state.points = new_points
            if st.button("Добавить точку"):
                st.session_state.points.append((0, 0, 0))
                st.rerun()
            geo_code = """//Spline\n"""
            for i, (x, y, z) in enumerate(st.session_state.points, start=1):
                geo_code += f"Point({i}) = {{{x}, {y}, {z}, 1.0}};\n"
            geo_code += f"Spline(1) = {{{', '.join(str(i+1) for i in range(len(st.session_state.points)))}}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {0, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()
        

        elif element_type == "BSpline":
            st.write("""

            ```bash 
            BSpline ( expression ) = { expression-list };
            ```
            - **Тег сплайна**
            - **Теги контрольных точек сплайна**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Если первая и последняя точка совпадают, тогда строится периодическая кривая.
            """)

            if "points" not in st.session_state:
                st.session_state.points = [(0, 0, 0), (5, 5, 5), (10, 0, 1)]  # Начальные точки

            new_points = []
            for i, (x, y, z) in enumerate(st.session_state.points):
                col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                x_val = col1.number_input(f"X{i+1}", value=x, key=f"x_{i}")
                y_val = col2.number_input(f"Y{i+1}", value=y, key=f"y_{i}")
                z_val = col3.number_input(f"Z{i+1}", value=z, key=f"z_{i}")
                if col4.button("❌", key=f"remove_{i}"):
                    st.session_state.points.pop(i)
                    st.rerun()
                new_points.append((x_val, y_val, z_val))
            st.session_state.points = new_points
            if st.button("Добавить точку"):
                st.session_state.points.append((0, 0, 0))
                st.rerun()
            geo_code = """//BSpline\n"""
            for i, (x, y, z) in enumerate(st.session_state.points, start=1):
                geo_code += f"Point({i}) = {{{x}, {y}, {z}, 1.0}};\n"
            geo_code += f"BSpline(1) = {{{', '.join(str(i+1) for i in range(len(st.session_state.points)))}}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {0, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

        elif element_type == "Circle":

            st.write("""

            ```bash 
            Circle ( expression ) = { expression, expression, expression <, ...> };
            ```
            - **Тег дуги окружности**
            - **Теги точек (начало дуги, центр, конечная точка дуги)**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Со встроенным ядрoм геометрии дуга должна быть строго меньше числа Пи.
            2. С ядром OpenCASCADE, если указано от 4 до 6 точек, первые три определяют координаты центра, следующие определяет радиус, а последние 2 определяют угол.
            """)

            if "center" not in st.session_state:
                st.session_state.center = (0, 0, 0)
            if "radius" not in st.session_state:
                st.session_state.radius = 5.0
        
            col1, col2, col3 = st.columns([3, 3, 3])
            cx = col1.number_input("X (центр)", value=st.session_state.center[0], key="cx")
            cy = col2.number_input("Y (центр)", value=st.session_state.center[1], key="cy")
            cz = col3.number_input("Z (центр)", value=st.session_state.center[2], key="cz")
            radius = st.number_input("Радиус", min_value=0.1, key="radius")

            if "center" in st.session_state:
                st.session_state.center = (cx, cy, cz)
    
            st.session_state.center = (cx, cy, cz)
        
            # Вычисление трёх точек для окружности
            p1 = (cx - radius, cy, cz)
            p2 = (cx, cy + radius, cz)
            p3 = (cx + radius, cy, cz)
    
        
            geo_code = """//Circle\n"""
            geo_code += f"Point(1) = {{{p1[0]}, {p1[1]}, {p1[2]}, 1.0}};\n"
            geo_code += f"Point(2) = {{{cx}, {cy}, {cz}, 1.0}}; // Центр\n"
            geo_code += f"Point(3) = {{{p3[0]}, {p3[1]}, {p3[2]}, 1.0}};\n"
            geo_code += f"Circle(1) = {{1, 2, 3}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {0, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

        elif element_type == "Ellipse":

            st.write("""

            ```bash 
            Ellipse ( expression ) = { expression, expression, expression <, ...> };
            ```
            - **Тег дуги эллипса**
            - **Тег начальной точки**
            - **Тег центральной точки**
            - **Тег точки на большей полуоси эллипса**
            - **Тег конечной точки**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Если первая точка является точкой большой оси, третье выражение можно опустить.
            2. С ядром OpenCASCADE, если указано от 5 до 7 выражений, первые три определяют координаты центра, следующие два определяют большой (вдоль оси x) и малый радиусы (вдоль оси y), а следующие два — начальный и конечный угол.
            3. OpenCASCADE не позволяет создавать дуги эллипса с большим радиусом, меньше малого радиуса.
            """)

            if "center" not in st.session_state:
                st.session_state.center = (0, 0, 0)
            if "semi_major_axis" not in st.session_state:
                st.session_state.semi_major_axis = 5.0
            if "semi_minor_axis" not in st.session_state:
                st.session_state.semi_minor_axis = 3.0
    
            col1, col2, col3 = st.columns([3, 3, 3])
            cx = col1.number_input("X (центр)", value=st.session_state.center[0], key="cx")
            cy = col2.number_input("Y (центр)", value=st.session_state.center[1], key="cy")
            cz = col3.number_input("Z (центр)", value=st.session_state.center[2], key="cz")
    
            # Получаем полуоси эллипса
            semi_major_axis = st.number_input("Полуось по X", min_value=0.1, key="semi_major_axis")
            semi_minor_axis = st.number_input("Полуось по Y", min_value=0.1, key="semi_minor_axis")
    
            # Обновляем состояние сессии только если это необходимо
            if "center" in st.session_state:
                st.session_state.center = (cx, cy, cz)

            # Вычисление четырёх точек для эллипса
            p1 = (cx - semi_major_axis, cy, cz)
            p2 = (cx, cy + semi_minor_axis, cz)
            p3 = (cx + semi_major_axis, cy, cz)
            p4 = (cx, cy - semi_minor_axis, cz)
    
        
            geo_code = """//Ellipse\n"""
            geo_code += f"Point(1) = {{{p1[0]}, {p1[1]}, {p1[2]}, 1.0}};\n"
            geo_code += f"Point(2) = {{{cx}, {cy}, {cz}, 1.0}}; // Центр эллипса\n"
            geo_code += f"Point(3) = {{{p3[0]}, {p3[1]}, {p3[2]}, 1.0}};\n"
            geo_code += f"Point(4) = {{{p4[0]}, {p4[1]}, {p4[2]}, 1.0}};\n"
            geo_code += f"Ellipse(1) = {{1, 2, 3, 4}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {0, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

        elif element_type == "Curve Loop":
            st.write("""

                ```bash 
                Curve Loop ( expression ) = { expression-list };
                ```
                - **Тег замкнутого конутра**
                - **Выражение в скобках является тегом цикла кривой**
                - **Список выражений справа должен содержать теги всех кривых, составляющих цикл кривой**
                """)
            st.subheader("Особенности:")
            st.write("""
                1. С помощью встроенного геометрического ядра кривые должны быть упорядочены и ориентированы, используя отрицательные теги для указания обратной ориентации.
                """)

            geo_code = """
            // Curve Loop
            Point(1) = {0, 0, 0, 1.0};
            Point(2) = {0.5, -0.3, 0, 1.0};  
            Point(3) = {1, -0.2, 0, 1.0};

            Point(4) = {1.2, 0.5, 0, 1.0};  
            Point(5) = {1.5, 1, 0, 1.0};

            Point(6) = {1.1, 1.5, 0, 1.0};  
            Point(7) = {0.5, 1.7, 0, 1.0};

            Point(8) = {-0.2, 1.6, 0, 1.0};  
            Point(9) = {-0.7, 1, 0, 1.0};

            Point(10) = {-0.6, 0.5, 0, 1.0};  
            Point(11) = {0, 0, 0};  

            Spline(1) = {1, 2, 3};
            Spline(2) = {3, 4, 5};
            Spline(3) = {5, 6, 7};
            Spline(4) = {7, 8, 9};
            Spline(5) = {9, 10, 11};

            Curve Loop(1) = {1, 2, 3, 4, 5};

            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {0, 255, 0}; 
            General.Color.Text = White;
            Geometry.Color.Surfaces = {200, 200, 200}; 
            """

        elif element_type == "Physical Curve":

            st.write("""

                ```bash 
                Physical Curve ( expression | string-expression <, expression> ) <+|->= {expression-list };
                ```
                - **Тег физической кривой**
                - **Список выражений справа должен содержать теги всех элементарных кривых, которые необходимо сгруппировать внутри физической кривой**
                """)
            st.subheader("Особенности:")
            st.write("""
                1. С помощью встроенного геометрического ядра кривые должны быть упорядочены и ориентированы, используя отрицательные теги для указания обратной ориентации.
                2. Если вместо выражения внутри скобок указано строковое выражение, то с физическим тегом связывается строковая метка, которая может быть указана явно (после запяой) или нет (в этом случае автоматически создается уникальный тег).
                3. В некоторых форматах файлов сетки (например, MSH2) указание отрицательных тегов в списке выражений изменит ориентацию элементов сетки, принадлежащих соответствующим элементарным кривым в сохраненном файле сетки.
                """)

            geo_code = """
            //Physical Curve
            Point(1) = {0, 0, 0};
            Point(2) = {1, 0, 0};
            Point(3) = {1, 1, 0};
            Point(4) = {0, 1, 0};

            Line(1) = {1, 2};
            Line(2) = {2, 3};
            Line(3) = {3, 4};
            Line(4) = {4, 1};

            Physical Curve("Boundary", 100) = {1, 2, 3, 4};
            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;
            """

        show_code(geo_code, "plaintext")
    
        def save_example_file():
            example_file_path = "./example.geo"
            with open(example_file_path, "w") as f:
                f.write(geo_code)
            return example_file_path
    
        if st.button("Перестроить геометрию"):
            example_file_path = save_example_file()
            run_gmsh(example_file_path)
        
    elif dimensions == "2D":
        element_type_2D = st.selectbox("Выберите тип элемента", ["Plane Surface", "Bezier(BSpline) Surface", "Surface Loop", "Physical Surface"])

        if element_type_2D == "Plane Surface":
            st.write("""
                ```bash
                Plane Surface ( expression ) = { expression-list };
                ```

                - **Тег плоской поверхности**
                - **Список выражений справа должен содержать теги всех контуров кривых, определяющих поверхность**
            """)
            st.subheader("Особенности:")
            st.write("""
                1. Первый контур кривых определяет внешнюю границу поверхности.    
                2. Все остальные контуры кривых определяют отверстия в поверхности.
                3. Контур кривых, определяющий отверстие, не должен иметь общих кривых с внешним контуром кривых (в этом случае он не является отверстием, и две поверхности должны быть определены отдельно).
                4. Аналогично, контур кривых, определяющий отверстие, не должен иметь общих кривых с другим контуром кривых, определяющим отверстие в той же поверхности (в этом случае два контура кривых должны быть объединены).
                """)

            geo_code = """
            //Plane Surface
            Point(1) = {0, 0, 0};
            Point(2) = {5, 0, 0};
            Point(3) = {5, 5, 0};
            Point(4) = {0, 5, 0};

            
            Point(5) = {2.5, 2.5, 0}; // Центр круга
            Point(6) = {3.5, 2.5, 0}; // Правая точка
            Point(7) = {2.5, 3.5, 0}; // Верхняя точка
            Point(8) = {1.5, 2.5, 0}; // Левая точка
            Point(9) = {2.5, 1.5, 0}; // Нижняя точка

            Line(1) = {1, 2};
            Line(2) = {2, 3};
            Line(3) = {3, 4};
            Line(4) = {4, 1};

            Circle(5) = {8, 5, 7};
            Circle(6) = {7, 5, 6};
            Circle(7) = {6, 5, 9};
            Circle(8) = {9, 5, 8};  

            Curve Loop(1) = {1, 2, 3, 4}; // Внешний квадрат
            Curve Loop(2) = {5, 6, 7, 8}; // Внутренний круг (отверстие)

            // Создание плоской поверхности с отверстием
            Plane Surface(1) = {1, 2};
            Geometry.PointNumbers = 1;

            // Настройки цветов
            Geometry.Color.Points = {0, 255, 0};   // Красные точки
            Geometry.Color.Lines = {0, 0, 255};    // Синие линии
            Geometry.Color.Surfaces = {200, 200, 200}; 

            //Генерация 2D-сетки
            Mesh 2;

            """

        
        elif element_type_2D == "Bezier(BSpline) Surface":
            st.write("""
                ```bash
                Bezier Surface ( expression ) = { expression-list };
                ```

                - **Тег поверхности, построенной на кривых Безье**
                - **Тег контура, построенного на 2, 3, 4 кривых Безье**
            """)
            st.write("""
                ```bash
                BSpline Surface ( expression ) = { expression-list };
                ```
                - **Тег поверхности, построенной на сплайнах**
                - **Теги контура, построенного на 2, 3, 4 сплайнах**
                
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Поверхность Безье доступна только с ядром OpenCASCADE.
            2. Поверхность Сплайнов доступна только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Bezier Surface
            SetFactory("OpenCASCADE");
            Point(1) = {0, 0, 0};
            Point(2) = {1, 0.5, 0};
            Point(3) = {2, 0, 0};

            Point(4) = {0, 1, 1};
            Point(5) = {2, 1, 1};

            Point(6) = {0, 2, 0};
            Point(7) = {1, 2.5, 0};
            Point(8) = {2, 2, 0};

            Bezier(1) = {1, 2, 3};  // Нижняя граница
            Bezier(3) = {6, 7, 8};  // Верхняя граница
            Bezier(4) = {1, 4, 6};  // Левая боковая кривая
            Bezier(5) = {3, 5, 8};  // Правая боковая кривая

            Curve Loop(1) = {1, 5, -3, -4};

            Bezier Surface(1) = {1};
            Geometry.PointNumbers = 1;
            // Настройки цветов
            Geometry.Color.Points = {0, 255, 0};
            Geometry.Color.Lines = {0, 0, 255};
            Geometry.Color.Surfaces = {200, 200, 200};

            //Генерация 2D-сетки
            Mesh 2;

            """
        
        elif element_type_2D == "Surface Loop":
            st.write("""
                ```bash
                Surface Loop ( expression ) = { expression-list } < Using Sewing >;
                ```

                - **Тег поверхности цикла**
                - **Список выражений справа должен содержать теги всех поверхностей, составляющих цикл поверхности**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Цикл поверхности всегда должен представлять собой замкнутую оболочку, а поверхности должны быть ориентированы последовательно (используя отрицательные теги для указания обратной ориентации).
            """)
            geo_code = """
            //Surface Loop
            lc = 1e-2;
            Point(1) = {0, 0, 0, lc};
            Point(2) = {.1, 0, 0, lc};
            Point(3) = {.1, .3, 0, lc};
            Point(4) = {0, .3, 0, lc};
            Line(1) = {1, 2};
            Line(2) = {3, 2};
            Line(3) = {3, 4};
            Line(4) = {4, 1};
            Curve Loop(1) = {4, 1, -2, 3};
            Plane Surface(1) = {1};
            Point(5) = {0, .4, 0, lc};
            Line(5) = {4, 5};
            Translate {-0.02, 0, 0} { Point{5}; }
            Rotate {{0,0,1}, {0,0.3,0}, -Pi/4} { Point{5}; }
            Translate {0, 0.05, 0} { Duplicata{ Point{3}; } }
            Line(7) = {3, 6};
            Line(8) = {6, 5};
            Curve Loop(10) = {5,-8,-7,3};
            Plane Surface(11) = {10};
            
            Point(100) = {0., 0.3, 0.12, lc}; Point(101) = {0.1, 0.3, 0.12, lc};
            Point(102) = {0.1, 0.35, 0.12, lc};
            xyz[] = Point{5}; // Get coordinates of point 5
            Point(103) = {xyz[0], xyz[1], 0.12, lc};
            Line(110) = {4, 100}; Line(111) = {3, 101};
            Line(112) = {6, 102}; Line(113) = {5, 103};
            Line(114) = {103, 100}; Line(115) = {100, 101};
            Line(116) = {101, 102}; Line(117) = {102, 103};
            Surface Loop(128) = {127, 119, 121, 123, 125, 11};
            Geometry.PointNumbers = 1;
            // Настройки цветов
            Geometry.Color.Points = {0, 255, 0};
            Geometry.Color.Lines = {0, 0, 255};
            Geometry.Color.Surfaces = {200, 200, 200};

            //Генерация 2D-сетки
            Mesh 2;

            """

        elif element_type_2D == "Physical Surface":
            st.write("""
                ```bash
                Physical Surface ( expression | string-expression <, expression> ) <+|->= { expression-list };
                ```

                - **Тег физической поверхности**
                - **Список выражений справа должен содержать теги всех поверхностей, составляющих цикл поверхности**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Список выражений справа должен содержать теги всех элементарных поверхностей, которые необходимо сгруппировать внутри физической поверхности.
            """)
            geo_code = """
            //Physiacal Surface
            SetFactory("OpenCASCADE");
            lc = 1e-2;
            Point(1) = {0, 0, 0, lc};
            Point(2) = {.1, 0, 0, lc};
            Point(3) = {.1, .3, 0, lc};
            Point(4) = {0, .3, 0, lc};

            Line(1) = {1, 2};
            Line(2) = {2, 3}; // Обратите внимание на порядок
            Line(3) = {3, 4};
            Line(4) = {4, 1};

            Curve Loop(1) = {4, 1, -2, 3};
            Plane Surface(1) = {1};

            Physical Curve(5) = {1, 2, 4};
            Physical Surface("My surface") = {1};

            
            Rectangle(2) = {0.2, 0.0, 0.0, 0.1, 0.3};
            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            //Генерация 2D-сетки
            Mesh 2;
            """

        show_code(geo_code, "plaintext")
    
        def save_example_file():
            example_file_path = "./example.geo"
            with open(example_file_path, "w") as f:
                f.write(geo_code)
            return example_file_path
    
        if st.button("Перестроить геометрию"):
            example_file_path = save_example_file()
            run_gmsh(example_file_path)
    
    elif dimensions == "3D":
        element_type_3D = st.selectbox("Выберите тип элемента", ["Volume", "Sphere", "Box", "Cylinder", "Torus", "Cone", "Wedge", "Physical Volume"])

        if element_type_3D == "Volume":
            st.write("""
                ```bash
                Volume ( expression ) = { expression-list };
                ```

                - **Тег объема**
                - **Список выражений справа должен содержать теги всех контуров поверхности, определяющих объем**
                - **Первый контур поверхности определяет внешнюю границу объема** 
                - **Все остальные контуры поверхности определяют отверстия в объеме**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Контур поверхности, определяющий отверстие, не должен иметь общих поверхностей с контуром внешней поверхности (в этом случае это не отверстие, и два объема должны быть определены отдельно).
            2. Точно так же контур поверхности, определяющий отверстие, не должен иметь общих поверхностей с другим контуром поверхности, определяющим отверстие в том же объеме (в этом случае два контура поверхности должны быть объединены).
            """)
            geo_code = """
            //Volume
            SetFactory("OpenCASCADE");
            Box(1) = {0, 0, 0, 1, 1, 1}; // Куб 1x1x1
            Sphere(2) = {0.5, 0.5, 0.5, 0.3}; // Сфера внутри куба
            Surface Loop(3) = {1, 2, 3, 4, 5, 6}; 
            Surface Loop(4) = {7};
            Volume(5) = {3, 4}; // Куб с вырезанной сферической областью
            Geometry.PointNumbers = 1;
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            
            """

        elif element_type_3D == "Sphere":
            st.write("""
                ```bash
                Sphere ( expression ) = { expression-list };
                ```

                - **Тег сферы, заданной тремя координатами ее центра и радиусом**
                - **Дополнительные выражения определяют три предела угла**
                - **Первые два необязательных аргумента определяют полярный угол раскрытия** 
                - **Все остальные контуры поверхности определяют отверстия в объеме**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Необязательный аргумент «angle3» определяет азимут раскрытия.
            2. Сфера доступна только с ядром OpenCASCADE.
            """)

            geo_code = """
            //Shere
            SetFactory("OpenCASCADE");

            Sphere(1) = {0, 0, 0, 1, -Pi/2, Pi/2}; // Полусфера радиусом 1
            Geometry.PointNumbers = 1;
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Box":
            st.write("""
                ```bash
                Box ( expression ) = { expression-list };
                ```

                - **Тег параллелипипеда, заданного диагональю**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Box
            SetFactory("OpenCASCADE");

            Box(1) = {0, 0, 0, 2, 1, 3}; // Параллелепипед
            Geometry.PointNumbers = 1;
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Cylinder":
            st.write("""
                ```bash
                Cylinder ( expression ) = { expression-list };
                ```

                - **Тег цилиндра, определяемого тремя координатами центра первой боковой поверхности, тремя компонентами вектора, определяющими его ось и радиус**
                - **Дополнительное выражение определяет угол основания**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Cylinder
            SetFactory("OpenCASCADE");

            Cylinder(1) = {0, 0, 0, 0, 3, 0, 0.5}; // Цилиндр вдоль оси Y
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Torus":
            st.write("""
                ```bash
                Torus ( expression ) = { expression-list };
                ```

                - **Тег тора, определяемого тремя координатами его центра и двумя радиусами**
                - **Дополнительное выражение определяет угловое раскрытие**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Torus
            SetFactory("OpenCASCADE");

            Torus(1) = {0, 0, 0, 2, 0.5}; // Тор
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Cone":
            st.write("""
                ```bash
                Cone ( expression ) = { expression-list };
                ```

                - **Создайте конус, определяемый тремя координатами центра основания, тремя компонентами вектора, определяющего его ось, и двумя радиусами средней линии и верхнего основания (эти радиусы могут быть нулевыми)**
                - **Дополнительное выражение определяет угловое раскрытие**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Cone
            SetFactory("OpenCASCADE");

            Cone(1) = {0, 0, 0, 0, 0, 2, 1, 0.3}; // Конус высотой 2
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Wedge":
            st.write("""
                ```bash
                Wedge ( expression ) = { expression-list };
                ```

                - **Тег прямого углового клина, определяемый тремя координатами точки прямого угла и тремя размерами**
                - **Дополнительный параметр определяет верхнюю протяженность (по умолчанию ноль)**
            """)
            st.subheader("Особенности:")
            st.write("""
            1. Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Wedge
            SetFactory("OpenCASCADE");

            Wedge(1) = {0, 0, 0, 2, 2, 1, 1}; // Клин

            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {0, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            """

        elif element_type_3D == "Physical Volume":
            st.write("""
                ```bash
                Physical Volume ( expression | string-expression <, expression> ) <+|->= { expression-list };

                ```

                - **Тег физического объема**
                - **Список выражений справа должен содержать теги всех элементарных томов, которые необходимо сгруппировать внутри физического объема**
            """)
            geo_code = """
            //Physical Volume
            SetFactory("OpenCASCADE");
            Box(1) = {0, 0, 0, 1, 1, 1};
            Sphere(2) = {0.5, 0.5, 0.5, 0.5};
            BooleanDifference(3) = {Volume{1}; Delete; }{ Volume{2}; Delete; };

            Physical Volume("Hollow Cube") = {3};

            // Генерация 3D-сетки
            Mesh 3;

            """

        show_code(geo_code, "plaintext")
    
        def save_example_file():
            example_file_path = "./example.geo"
            with open(example_file_path, "w") as f:
                f.write(geo_code)
            return example_file_path
    
        if st.button("Перестроить геометрию"):
            example_file_path = save_example_file()
            run_gmsh(example_file_path)


    
elif choice == "Файл геометрии":
    # 1. Установка фабрики геометрии
    st.header("1. Установка фабрики геометрии")
    st.write("""
    Команда `SetFactory("OpenCASCADE");` указывает GMSH использовать библиотеку OpenCASCADE для построения геометрии. 
    Это необходимо для создания сложных геометрических объектов, таких как окружности и экструзии.
    """)

    st.header("2. Определение геометрических объектов")
    st.write("""
    В этом разделе создаются базовые геометрические элементы.
    """)

    # Circle(x) = {...}
    st.subheader("Создание окружностей (Circle)")
    st.write("""
    Команда `Circle(x) = {...};` используется для создания окружности. 
    В примере задаются окружности с определёнными координатами центра и радиусом:
    - `Circle(1) = {0, 0, 0, 0.5};` создаёт окружность с центром в начале координат и радиусом 0.5.
    """)

    # Curve Loop(x) = {...}
    st.subheader("Создание кривых и замкнутых контуров (Curve Loop)")
    st.write("""
    Команда `Curve Loop(x) = {...};` объединяет несколько кривых в замкнутый контур, 
    который затем будет использоваться для создания поверхностей.
    - `Curve Loop(1) = {1};` создаёт контур на основе первой окружности.
    """)

    # ThruSections(x) = {...}
    st.subheader("Экструзия через сечения (ThruSections)")
    st.write("""
    Команда `ThruSections(x) = {...};` используется для создания 3D-объектов путём экструзии или вращения. 
    В примере используется экструзия нескольких окружностей, чтобы создать цилиндр.
    """)

    # Ruled ThruSections(x) = {...}
    st.subheader("Правила экструзии (Ruled ThruSections)")
    st.write("""
    Команда `Ruled ThruSections(x) = {...};` указывает, что необходимо экструзировать поверхность, используя определённые кривые.
    """)

    # Translate{...} {...}
    st.subheader("Перемещение объектов (Translate)")
    st.write("""
    Команда `Translate{...} {...};` перемещает геометрический объект в новое положение. 
    Например, команда перемещает экструзированный объект.
    """)

    # Fillet{...}
    st.subheader("Закругление объектов (Fillet)")
    st.write("""
    Команда `Fillet{...};` создаёт закругления на соединении объектов, сглаживая углы.
    """)

    st.header("3. Формирование 3D объектов и операций")

    # Volume
    st.subheader("Создание объемов (Volume)")
    st.write("""
    Команда `Volume{...};` используется для создания объемных объектов, которые могут быть использованы для дальнейшей генерации сетки.
    """)

    # Rotate{...}
    st.subheader("Поворот объектов (Rotate)")
    st.write("""
    Команда `Rotate{...};` осуществляет поворот объекта в пространстве. Например, можно повернуть поверхность или объем.
    """)

    # Extrude
    st.subheader("Экструзия объектов (Extrude)")
    st.write("""
    Команда `Extrude {...};` используется для создания объемных объектов путём экструзии поверхностей.
    """)

    st.header("4. Создание и обработка линий, поверхностей и тел")

    # Abs(Boundary{...})
    st.subheader("Обработка границ (Abs(Boundary))")
    st.write("""
    Команда `Abs(Boundary{ Volume{v(0)}; });` используется для создания абстрактных границ объемов, что необходимо для сетки и дальнейших расчётов.
    """)

    # Unique(Abs(Boundary{ Surface{f()}; })); 
    st.subheader("Создание уникальных поверхностей (Unique(Abs(Boundary{ Surface{f()}; })))")
    st.write("""
    Команда `Unique(Abs(Boundary{ Surface{f()}; }));` создаёт уникальные поверхности для дальнейшего использования.
    """)

    # Delete
    st.subheader("Удаление объектов (Delete)")
    st.write("""
    Команда `Delete{ Surface{1000}; };` удаляет геометрические объекты, которые больше не нужны, например, временные или промежуточные.
    """)

    st.header("5. Параметры для спирали")

    st.write("""
    В этом разделе создаётся спираль. Цикл For генерирует точки вдоль спирали с использованием параметров радиуса r, высоты h и угла theta.
    """)

    # Цикл For и генерация точек
    st.subheader("Цикл For для спирали")
    st.write("""
    Цикл For генерирует точки на спирали. Например:
    - `Point(1000 + i) = {r * Cos(theta), r * Sin(theta), i * h/npts};` создаёт точку на спирали с координатами.
    """)

    # Spline
    st.subheader("Создание сплайна (Spline)")
    st.write("""
    Команда `Spline(x) = {...};` используется для создания кривой (сплайна), которая проходит через сгенерированные точки.
    """)

    # Wire
    st.subheader("Создание проводника (Wire)")
    st.write("""
    Команда `Wire(x) = {...};` используется для создания проводника, который будет использован в последующих операциях.
    """)

    # Disk
    st.subheader("Создание диска (Disk)")
    st.write("""
    Команда `Disk(x) = {...};` создаёт диск с заданным радиусом, который может быть использован в экструзиях.
    """)

    st.header("6. Создание сетки")

    st.write("""
    После определения геометрии, необходимо настроить параметры сетки. В этом разделе настраиваются параметры сетки для всех объектов.
    """)

    # Geometry.NumSubEdges
    st.subheader("Количество под-ребер (Geometry.NumSubEdges)")
    st.write("""
    Параметр `Geometry.NumSubEdges` определяет количество под-ребер в геометрии, что влияет на детальность сетки.
    """)

    # Mesh.Size
    st.subheader("Размер элементов сетки (Mesh.MeshSizeFromCurvature, Mesh.MeshSizeMin, Mesh.MeshSizeMax)")
    st.write("""
    - `Mesh.MeshSizeFromCurvature` указывает размер сетки в зависимости от кривизны геометрии.
    - `Mesh.MeshSizeMin` и `Mesh.MeshSizeMax` задают минимальные и максимальные размеры элементов сетки.
    """)

    # Генерация сетки
    st.header("7. Генерация сетки")
    st.write("""
    После настройки геометрии и сетки, команда `Mesh 2;` создаёт сетку на основе описанных объектов.
    """)

    # Пример команды Mesh
    st.subheader("Команда для генерации сетки (Mesh 2)")
    st.write("""
    Команда `Mesh 2;` запускает процесс генерации сетки для всех объектов, описанных в файле .geo.
    """)

    st.header("2. Пример простого файла .geo")
    geo_code = """
    SetFactory("OpenCASCADE");
    Circle(1) = {0,0,0, 0.5}; Curve Loop(1) = 1;
    Circle(2) = {0.1,0.05,1, 0.1}; Curve Loop(2) = 2;
    Circle(3) = {-0.1,-0.1,2, 0.3}; Curve Loop(3) = 3;
    ThruSections(1) = {1:3};
    Circle(11) = {2+0,0,0, 0.5}; Curve Loop(11) = 11;
    Circle(12) = {2+0.1,0.05,1, 0.1}; Curve Loop(12) = 12;
    Circle(13) = {2-0.1,-0.1,2, 0.3}; Curve Loop(13) = 13;
    Ruled ThruSections(11) = {11:13};
    v() = Translate{4, 0, 0} { Duplicata{ Volume{1}; } };
    f() = Abs(Boundary{ Volume{v(0)}; });
    e() = Unique(Abs(Boundary{ Surface{f()}; }));
    Fillet{v(0)}{e()}{0.1}
    nturns = 1;
    npts = 20;
    r = 1;
    h = 1 * nturns;
    For i In {0 : npts - 1}
    theta = i * 2*Pi*nturns/npts;
    Point(1000 + i) = {r * Cos(theta), r * Sin(theta), i * h/npts};
    EndFor
    Spline(1000) = {1000 : 1000 + npts - 1};
    Wire(1000) = {1000};
    Disk(1000) = {1,0,0, 0.2};
    Rotate {{1, 0, 0}, {0, 0, 0}, Pi/2} { Surface{1000}; }
    Extrude { Surface{1000}; } Using Wire {1000}
    Delete{ Surface{1000}; }
    Geometry.NumSubEdges = 1000;
    Mesh.MeshSizeFromCurvature = 20;
    Mesh.MeshSizeMin = 0.001;
    Mesh.MeshSizeMax = 0.3;
    Mesh 2;

    """
    show_code(geo_code, "plaintext")

    # Загрузка файла примера
    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)

    # Возможность загрузки файла для Gmsh только в этом разделе
    uploaded_file = st.file_uploader("Загрузите файл для Gmsh", type=["geo", "msh", "step", "stl"])

    if uploaded_file is not None:
        file_path = os.path.join("./", uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Файл {uploaded_file.name} успешно загружен!")
        
        if st.button("Запустить Gmsh"):
            run_gmsh(file_path)

elif choice == "Создание области":
    st.header("1. Явное задание через точки, линии и поверхности")
    st.write("""
    Этот метод использует базовые геометрические элементы Gmsh: точки, линии, поверхностные петли и объемы.
     - **0D -> 1D -> 2D -> 3D**
    """)
    st.subheader("Шаг 1: Определение точек")

    geo_code1 = """
    // Создаем точки
    L = 1.0; // Длина ребра куба
    Nx = 10; // Число элементов по X
    Ny = 10; // Число элементов по Y
    Nz = 10; // Число элементов по Z

    Point(1) = {0, 0, 0, L/Nx};
    Point(2) = {L, 0, 0, L/Nx};
    Point(3) = {L, L, 0, L/Nx};
    Point(4) = {0, L, 0, L/Nx};
    Point(5) = {0, 0, L, L/Nx};
    Point(6) = {L, 0, L, L/Nx};
    Point(7) = {L, L, L, L/Nx};
    Point(8) = {0, L, L, L/Nx};
    """
    show_code(geo_code1, "plaintext")

    st.subheader("Шаг 2: Построение ребер куба")

    geo_code2 = """
    Line(1) = {1, 2};
    Line(2) = {2, 3};
    Line(3) = {3, 4};
    Line(4) = {4, 1};
    Line(5) = {5, 6};
    Line(6) = {6, 7};
    Line(7) = {7, 8};
    Line(8) = {8, 5};
    Line(9) = {1, 5};
    Line(10) = {2, 6};
    Line(11) = {3, 7};
    Line(12) = {4, 8};
    
    """
    show_code(geo_code2, "plaintext")

    st.subheader("Шаг 3: Построение поверхности куба")
    geo_code3 = """
    // Создаём поверхности
    Line Loop(13) = {1, 2, 3, 4};
    Plane Surface(14) = {13};
    Line Loop(15) = {5, 6, 7, 8};
    Plane Surface(16) = {15};
    Line Loop(17) = {1, 10, -5, -9};
    Plane Surface(18) = {17};
    Line Loop(19) = {2, 11, -6, -10};
    Plane Surface(20) = {19};
    Line Loop(21) = {3, 12, -7, -11};
    Plane Surface(22) = {21};
    Line Loop(23) = {4, 9, -8, -12};
    Plane Surface(24) = {23};

    """
    show_code(geo_code3, "plaintext")

    st.subheader("Шаг 4: Построение объема")

    geo_code4 = """
    // Создаём объем
    Surface Loop(25) = {14, 16, 18, 20, 22, 24};
    Volume(26) = {25};

    // Определяем сетку
    Transfinite Line {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12} = Nx+1 Using Progression 1;
    Transfinite Surface {14, 16, 18, 20, 22, 24};
    Transfinite Volume {26};
    Recombine Surface {14, 16, 18, 20, 22, 24};
    Physical Volume("Cube1") = {26};
    Color Red {Volume{26};}
    Mesh 3;
    """
    show_code(geo_code4, "plaintext")

    geo_full_code = geo_code1 + geo_code2 + geo_code3 + geo_code4

    # Загрузка файла примера
    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_full_code)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример 1"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)

    st.write("""
     - Недостатки: Сложно задавать сложную геометрию.
     - Преимущества: Полный контроль над топологией.
    """)

    st.header("2. OpenCASCADE")
    st.write("""
    Этот метод упрощает построение сложных геометрий за счет использования встроенных примитивов.
    """)
    geo_code5 = """
    // Определяем размеры кубов
    L = 1.0; // Длина ребра куба
    Nx = 10; // Число элементов по X
    Ny = 10; // Число элементов по Y
    Nz = 10; // Число элементов по Z

    // Первый куб (классический способ)
    Point(1) = {0, 0, 0, L/Nx};
    Point(2) = {L, 0, 0, L/Nx};
    Point(3) = {L, L, 0, L/Nx};
    Point(4) = {0, L, 0, L/Nx};
    Point(5) = {0, 0, L, L/Nx};
    Point(6) = {L, 0, L, L/Nx};
    Point(7) = {L, L, L, L/Nx};
    Point(8) = {0, L, L, L/Nx};

    Line(1) = {1, 2};
    Line(2) = {2, 3};
    Line(3) = {3, 4};
    Line(4) = {4, 1};
    Line(5) = {5, 6};
    Line(6) = {6, 7};
    Line(7) = {7, 8};
    Line(8) = {8, 5};
    Line(9) = {1, 5};
    Line(10) = {2, 6};
    Line(11) = {3, 7};
    Line(12) = {4, 8};

    Line Loop(13) = {1, 2, 3, 4};
    Plane Surface(14) = {13};
    Line Loop(15) = {5, 6, 7, 8};
    Plane Surface(16) = {15};
    Line Loop(17) = {1, 10, -5, -9};
    Plane Surface(18) = {17};
    Line Loop(19) = {2, 11, -6, -10};
    Plane Surface(20) = {19};
    Line Loop(21) = {3, 12, -7, -11};
    Plane Surface(22) = {21};
    Line Loop(23) = {4, 9, -8, -12};
    Plane Surface(24) = {23};

    Surface Loop(25) = {14, 16, 18, 20, 22, 24};
    Volume(26) = {25};

    Physical Volume("Cube1") = {26};
    Color Red {Volume{26};}

    // Второй куб (через OpenCASCADE)
    SetFactory("OpenCASCADE");
    Box(27) = {L + 0.5, 0, 0, L, L, L};
    Physical Volume("Cube2") = {27};
    Color Blue {Volume{27};}

    // Определяем сетку
    Transfinite Line {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12} = Nx+1 Using Progression 1;
    Transfinite Surface {14, 16, 18, 20, 22, 24};
    Transfinite Volume {26};
    Recombine Surface {14, 16, 18, 20, 22, 24};
    Mesh 3;
    """
    show_code(geo_code5, "plaintext")

    # Загрузка файла примера
    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code5)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример 2"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)

    st.write("""
     - Преимущества: Меньше кода, удобное управление геометрией.
     - Недостатки: Меньше контроля над отдельными гранями.
    """)

    st.header("3. Импорт CAD-модели")
    st.write("""
    Если у вас есть готовая CAD-модель цилиндра, например, в формате STEP, можно просто импортировать и создать сетку.
    """)

    geo_code6 = """
    // Импортируем CAD-модель
    Merge "cylinder.step";

    // Устанавливаем размер сетки
    MeshSize {1} = 0.2;

    // Генерируем объемную сетку
    Mesh 3;
    """
    show_code(geo_code6, "plaintext")

    st.write("""
     - Преимущества: Можно использовать сложные геометрии из других программ (SolidWorks, FreeCAD).
     - Недостатки: Нельзя редактировать геометрию в Gmsh.
    """)

    st.header("Вывод")

    st.write("""
     - Классический метод полезен для учебных целей и тонкого контроля.
     - OpenCASCADE — оптимальный вариант для большинства задач.
     - Импорт CAD хорош, если у вас уже есть модель.
    """)

elif choice == "Интерактивные возможности создания области":

    def run_gmsh_view():
        try:
            # Попытка запустить GMSH
            subprocess.run(["gmsh"], check=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Ошибка при запуске GMSH: {e}")
        except FileNotFoundError:
            st.error("GMSH не найден. Убедитесь, что GMSH установлен и доступен в пути.")

    if st.button("Запустить GMSH"):
        run_gmsh_view()

    # Шаг 1: Создание новой геометрии
    st.subheader("Шаг 1: Создание новой геометрии")
    st.write("""
    1. Откройте GMSH.
    2. Перейдите в меню "File" и выберите "New" для создания нового файла.
    """)
    # Место для картинки (шаг 1)
    st.image("step1_create_geometry.png", caption="Шаг 1: Создание новой геометрии",use_container_width=True)

    # Шаг 2: Определение точек
    st.subheader("Шаг 2: Определение точек")
    st.write("""
    Для создания прямоугольника начнем с определения 4 точек.
    В верхнем меню выберите "Geometry" -> "Elementary entitie" -> "Add" -> "Point"  и щелкните на рабочей области, чтобы разместить точки.
    - Точка 1: [0,0,0]
    - Точка 2: [L, 0, 0] — где L — длина области.
    - Точка 3: [L, W, 0] — где W — ширина области.
    - Точка 4: [0, W, 0]
    """)
    # Место для картинки (шаг 2)
    st.image("step2_define_points.png", caption="Шаг 2: Определение точек", use_container_width=True)

    # Шаг 3: Соединение точек
    st.subheader("Шаг 3: Соединение точек")
    st.write("""
    После того как точки размещены, их нужно соединить.
    1. В верхнем меню выберите "Geometry" -> "Elementary entitie" -> "Add" -> "Line".
    2. Соедините точки с помощью линий:
    - Линия 1: соединяет точку 1 и точку 2.
    - Линия 2: соединяет точку 2 и точку 3.
    - Линия 3: соединяет точку 3 и точку 4.
    - Линия 4: соединяет точку 4 и точку 1.
    """)
    # Место для картинки (шаг 3)
    st.image("step3_connect_points.png", caption="Шаг 3: Соединение точек", use_container_width=True)

    # Шаг 4: Создание поверхности
    st.subheader("Шаг 4: Создание поверхности")
    st.write("""
    Теперь, когда у нас есть все линии, можно создать поверхность, заключенную в этих линиях.
    1. Перейдите в меню "Geometry" -> "Elementary entitie" -> "Add" -> "Plane surface".
    2. Выберите линии для создания поверхности.
    """)
    # Место для картинки (шаг 4)
    st.image("step4_create_surface.png", caption="Шаг 4: Создание поверхности", use_container_width=True)

    # Шаг 5: Генерация сетки
    st.subheader("Шаг 5: Генерация сетки")
    st.write("""
    После создания геометрии можно генерировать сетку.
    1. Перейдите в меню "Mesh" и выберите "2D" для генерации двумерной сетки для поверхности.
    2. GMSH автоматически сгенерирует сетку для вашего прямоугольника.
    """)
    # Место для картинки (шаг 5)
    st.image("step5_generate_mesh.png", caption="Шаг 5: Генерация сетки", use_container_width=True)

    # Шаг 6: Визуализация
    st.subheader("Шаг 6: Визуализация")
    st.write("""
    После генерации сетки вы можете переключиться на вкладку "View" и включить отображение сетки.
    Вы также можете управлять цветами, отображением и другими параметрами визуализации.
    """)
    # Место для картинки (шаг 6)
    st.image("step6_visualize.png", caption="Шаг 6: Визуализация сетки", use_container_width=True)

    # Шаг 7: Сохранение файла
    st.subheader("Шаг 7: Сохранение файла")
    st.write("""
    1. Вы можете сохранить файл, выбрав "File" -> "Save Mesh".
    """)
    # Место для картинки (шаг 7)
    st.image("step7_save_file.png", caption="Шаг 7: Сохранение файла", use_container_width=True)

    # Пример команды GMSH
    st.subheader("Пример команд GMSH")
    st.write("""
    Вы также можете использовать GMSH с командами в языке GMSH для создания геометрии и сетки через текстовый файл. Вот пример скрипта для создания прямоугольной области:

    ```plaintext
    // Прямоугольная область с размерами LxW

    L = 10;  // длина
    W = 5;   // ширина

    // Определение точек
    Point(1) = {0, 0, 0, 1};
    Point(2) = {L, 0, 0, 1};
    Point(3) = {L, W, 0, 1};
    Point(4) = {0, W, 0, 1};

    // Определение линий
    Line(1) = {1, 2};
    Line(2) = {2, 3};
    Line(3) = {3, 4};
    Line(4) = {4, 1};

    // Создание поверхности
    Line Loop(1) = {1, 2, 3, 4};
    Plane Surface(1) = {1};

    // Генерация сетки
    Mesh 2;
    """)

    st.subheader("Заключение") 
    st.write(""" GMSH предоставляет множество инструментов для создания и визуализации геометрий с помощью графического интерфейса. Мы можем использовать GMSH для построения простых геометрических областей, генерации сеток и их визуализации. Визуализация и настройка сетки возможна через интерфейс, что упрощает процесс проектирования. """)


elif choice == "Подготовка сетки для FEniCS":
    st.header("Поддерживаемые сеточные форматы:")
    st.subheader("1. Собственный формат FEniCS (XML):")
    st.write("""
    
    - FEniCS изначально использует XML-формат для хранения сеток и данных.
    - Примеры файлов:
        - `mesh.xml` — файл сетки.
        - `mesh_facet_region.xml` — файл с метками граничных элементов.
        - `mesh_physical_region.xml` — файл с метками физических областей.
    - Эти файлы создаются с помощью утилиты `dolfin-convert` или вручную.
    """)
    st.subheader("2. Форматы, поддерживаемые через `dolfin-convert`:")
    st.write("""
    
    Утилита dolfin-convert позволяет конвертировать сетки из других форматов в формат, понятный FEniCS. 
    - Поддерживаемые форматы:
        - **Gmsh (.msh):** Популярный формат для генерации сеток.
        - **MEDIT (.mesh):** Формат, используемый в программе MEDIT.
        - **Triangle (.node, .ele):** Формат, используемый в программе Triangle для 2D-сеток.
        - **TetGen (.node, .ele):** Формат, используемый в программе TetGen для 3D-сеток.
    Пример использования `dolfin-convert`:
    ```bash
              dolfin-convert input_mesh.msh output_mesh.xml
              
              """)
    st.subheader("3. Форматы, поддерживаемые через `meshio`:")
    st.write("""
    
    Библиотека `meshio` предоставляет более широкую поддержку форматов и может использоваться для конвертации сеток в формат, совместимый с FEniCS. Поддерживаемые форматы:
    - Поддерживаемые форматы:
        - **Gmsh (.msh):**
        - **VTK (.vtk, .vtu)**
        - **XDMF (.xdmf)**
        - **ABAQUS (.inp)**
        - **COMSOL (.mphtxt)**
        - **STL (.stl)**
        - **MED (.med)**
        - и многие другие.
        
    Пример использования `meshio` для конвертации в формат XML:
    ```bash
            import meshio
            # Чтение сетки из формата Gmsh
            mesh = meshio.read("input_mesh.msh")
            # Запись сетки в формат FEniCS (XML)
            meshio.write("output_mesh.xml", mesh)
    """)
    st.write("""
    Пример импортирования сетки в FEniCS:
    ```bash
            from fenics import *
            # Загрузка сетки
            mesh = Mesh("mesh.xml")
            # Визуализация сетки
            plot(mesh)
            plt.title("Imported Mesh from Gmsh")
            plt.show()
    """)
    st.subheader("4. Формат XDMF:")
    st.write("""
    
    - XDMF (eXtensible Data Model and Format) — это современный формат, который поддерживает хранение сеток и данных (например, результатов вычислений).
    - FEniCS может читать и записывать XDMF-файлы, что особенно полезно для больших сеток и параллельных вычислений.
    - Пример использования:
    ```bash
            from dolfin import *
            # Чтение сетки из XDMF
            mesh = Mesh()
            with XDMFFile("mesh.xdmf") as infile:
                infile.read(mesh)
            # Запись сетки в XDMF
            with XDMFFile("output_mesh.xdmf") as outfile:
                outfile.write(mesh)
              """)
    st.subheader("5. Формат VTK:")
    st.write("""
    
    - VTK (Visualization Toolkit) — это формат, используемый для визуализации данных. 
    - FEniCS может экспортировать результаты в VTK для визуализации в программах, таких как Paraview.
    - Пример использования:
    ```bash
            ffrom dolfin import *

            # Создание функции и экспорт в VTK
            mesh = UnitSquareMesh(10, 10)
            V = FunctionSpace(mesh, 'P', 1)
            u = Function(V)
            File("output.pvd") << u
              """)
              
    st.subheader("6. Другие форматы:")
    st.write("""
    
    - **HDF5**: Используется для хранения больших данных и сеток в параллельных вычислениях. 
    - **DOLFIN HDF5**: Специальный формат для хранения сеток и данных в FEniCS.
    - **NETCDF:** Поддерживается для работы с данными.
              """)
    st.subheader("Некоторые рекомендации:")
    st.write("""
    
    - Для простых задач использовать XML-формат. 
    - Для больших сеток и параллельных вычислений лучше подходят XDMF или HDF5.
    - Для конвертации сеток из других форматов использовать `meshio`, так как оно поддерживает больше форматов, чем `dolfin-convert`.
              """)
    st.subheader("Пример подготовки сетки с граничными условиями:")
    st.write("""
    ```bash
    import meshio

    # Чтение .msh файла
    mesh = meshio.read("mesh_with_bc.msh")
    # Запись в .xdmf формат
    meshio.write("mesh_with_bc.xdmf", mesh)
    from fenics import *

    # Загрузка сетки
    mesh = Mesh()
    with XDMFFile("mesh_with_bc.xdmf") as infile:
        infile.read(mesh)

    # Загрузка граничных меток
    boundaries = MeshFunction("size_t", mesh, mesh.topology().dim() - 1)
    with XDMFFile("mesh_with_bc_boundaries.xdmf") as infile:
        infile.read(boundaries)

    # Определение граничных условий
    u_D = Constant(0.0)
    bc = DirichletBC(V, u_D, boundaries, 1)  # 1 — идентификатор границы

    # Визуализация граничных меток
    plot(boundaries)
    plt.title("Boundary Markers")
    plt.show()
              """)
    
    st.subheader("Итоги:")
    st.write("""

    - Для подготовки сетки в FEniCS нужно использовать Gmsh, `mshr` или другие инструменты. 
    - Конвертировать сетку в формат `.xml` или `.xdmf` с помощью `meshio` или `dolfin-convert`.
    - Загрузить сетку в FEniCS и определить граничные условия с помощью физических групп.
              """)
elif choice == "Constructive Solid Geometry технология в Gmsh":
    st.write("""**Constructive Solid Geometry (CSG)** — это технология, используемая для создания сложных геометрических моделей путём комбинирования простых фигур (примитивов) с помощью **булевых операций**: **объединение (union)**, **вычитание (difference)** и **пересечение (intersection)**. В Gmsh эта технология активно применяется для построения геометрии.""")
    st.subheader("Пример использования CSG в Gmsh")
    st.write("""Создадим геометрию состоящую из прямоугольников с круглым отверстием внутри, используя CSG.""")
    st.write("""
    1. **Создание примитивов:**
        - Прямоугольник (Rectangle).
        - Круг (Circle)
    2. **Применение булевых операций:**
        - Используем операцию **вычитания (Difference)**, чтобы удалить круг из прямоугольника.""")
        
    st.write("""
    Пример кода в Gmsh:
    ```bash
    // Создание прямоугольника
    Rectangle(1) = {0, 0, 0, 2, 1, 0};
    // Прямоугольник с координатами (0,0) и размерами 2x1
            
    // Создание круга
    Circle(2) = {1, 0.5, 0, 0.25, 0, 2*Pi};
    // Круг с центром в (1, 0.5) и радиусом 0.25
            
    // Применение булевой операции Difference
    BooleanDifference(3) = { Surface{1}; Delete; }{ Surface{2}; Delete; };
            
    // Генерация сетки
    Mesh 2;  // Генерация 2D-сетки""")
            
    st.write("""
            Объяснение кода:
            1. **Rectangle(1):**
            - Создает прямоугольник с координатами левого нижнего угла (0,0) и размерами 2 (по оси Х) на 1 (по оси Y).
            2. **Circle(2):**
            - Создает круг с центром в точке (1, 0.5) и радиусом 0.25.
            3. **BooleanDifference(3):**
            - Вычитает круг (Surface{2}) из прямоугольника (Surface{1}), создавая новую поверхность (Surface{3}).
            4. **Mesh 2:**
            - Генерирует 2D-сетку для полученной геометрии.""")
            
    st.subheader("Применение CSG в построении геометрии:")
    st.write("""
            CSG особенно полезна в задачах, где требуется создание сложных форм из простых примитивов.
            Примеры применения:
            1. **Инженерные конструкции:**
                - Создание деталей с отверстиями, пазами или сложными формами.
                - Пример: пластина с отверстиями для крепления.
            2. **Архитектурное моделирование:**
                - Построение зданий с окнами, дверьми и другими элементами.
                - Пример: здание с арочными проёмами.
            3. **Биомедицинское моделирование:**
                - Создание моделей органов или имплантатов.
                - Пример: кость с полостью для имплантата.
            4. **Физическое моделирование:**
                - Построение геометрии для задач CFD (вычислительной гидродинамики) или FEM (метода конечных элементов).
                - Пример: труба с внутренними перегородками.""")
            
    st.subheader("Преимущества CSG:")
    st.write("""
        - **Простота:** Использование простых примитивов (кубы, сферы, цилиндры) для создания сложных форм.
        - **Гибкость:** Возможность комбинировать фигуры с помощью булевых операций.
        - **Точность:** Точное задание геометрии, что важно для численного моделирования.
    """)
    
    st.subheader("Пример сложной геометрии с использованием CSG:")
    st.write("""
    Создадим геометрию, состоящую из двух пересекающихся цилиндров (труб).

    **Код в Gmsh:**
    ```bash
    // Создание первого цилиндра
    Cylinder(1) = {0, 0, 0, 2, 0, 0, 0.5, 2*Pi};
    // Центр (0,0,0), ось (2,0,0), радиус 0.5

    // Создание второго цилиндра
    Cylinder(2) = {1, -1, 0, 0, 2, 0, 0.5, 2*Pi};
    // Центр (1,-1,0), ось (0,2,0), радиус 0.5

    // Применение булевой операции Union
    BooleanUnion(3) = { Volume{1}; Delete; }{ Volume{2}; Delete; };

    // Генерация 3D-сетки
    Mesh 3;

    """)
                
    st.subheader("Итоги:")
    st.write("""
            CSG — это мощный инструмент для создания сложных геометрий в Gmsh. Он позволяет комбинировать простые фигуры с помощью булевых операций, что делает его незаменимым для инженерных, архитектурных и научных задач.""")
    




    

    

