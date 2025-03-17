
            //Physical Volume
            SetFactory("OpenCASCADE");
            Box(1) = {0, 0, 0, 1, 1, 1};
            Sphere(2) = {0.5, 0.5, 0.5, 0.5};
            BooleanDifference(3) = {Volume{1}; Delete; }{ Volume{2}; Delete; };

            Physical Volume("Hollow Cube") = {3};

            // Генерация 3D-сетки
            Mesh 3;

            