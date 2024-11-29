ejercicios = [
    {
        "id": "ej1",
        "nombre": "Suma",
        "codigo": "def suma(a, b): return a + b",
        "tests": [{"input": "(1, 2)", "output": 3}]
    },
    {
        "id": "ej2",
        "nombre": "Resta",
        "codigo": "def resta(a, b): return a - b",
        "tests": [{"input": "(5, 3)", "output": 2}]
    },
    {
        "id": "ej3",
        "nombre": "Multiplicación",
        "codigo": "def multiplica(a, b): return a * b",
        "tests": [{"input": "(3, 4)", "output": 12}]
    },
    {
        "id": "ej4",
        "nombre": "División",
        "codigo": "def multiplica(a, b): return a * b",
        "tests": [{"input": "(3, 4)", "output": 12}]
    },
]

def evaluar_codigo(codigo: str, completados: list, incompletos: list) -> bool:
    try:
        # Crear un espacio de ejecución seguro
        local_context = {}
        exec(codigo, {}, local_context)

        tests = [
            [
                { "input": "(1, 2)", "output": 3 },
                { "input": "(3, 4)", "output": 7 },
                { "input": "(5, 1)", "output": 6 },
            ],
            [
                { "input": "(10, 7)", "output": 3 },
                { "input": "(8, 1)", "output": 7 },
                { "input": "(12, 6)", "output": 6 },
            ],
            [
                { "input": "(1, 3)", "output": 3 },
                { "input": "(3, 7)", "output": 21 },
                { "input": "(4, 7)", "output": 28 },
            ],
            [
                { "input": "(12, 2)", "output": 6 },
                { "input": "(24, 6)", "output": 4 },
                { "input": "(10, 5)", "output": 2 },
            ],
        ]
        
        # Obtener las funciónes definida
        funciones = list(local_context.values())  # Todas las funciones en el contexto
        
        # Validar todos los casos de prueba
        for i, tests_for_function in enumerate(tests, start=0): # Recorremos todos las funciones
                exercise = {"nombre": ejercicios[i]["nombre"]}

                # all_completes será True si todos los casos pasan correctamente, False en caso contrario
                all_completes = all(
                    funciones[i](*eval(test["input"])) == test["output"] for test in tests_for_function
                )

                if all_completes:
                    completados.append(exercise)
                else:
                    incompletos.append({
                        "nombre": exercise["nombre"], 
                        "expected": tests_for_function[0]["output"], 
                        "obtained": funciones[i](*eval(tests_for_function[0]["input"]))
                    })
        return True
    except Exception:
        return False