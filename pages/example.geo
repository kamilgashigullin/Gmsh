
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
    