"""Capítulos 4 a 7 del manual."""

from __future__ import annotations

from pathlib import Path

from manual_style import Manual


def add_chapters(m: Manual, assets: Path) -> None:
    # =====================================================================
    # 4. MÉTODO GRÁFICO
    # =====================================================================
    m.h1("4. Método gráfico")
    m.lead(
        "El método gráfico resuelve modelos de programación lineal con dos variables. Su valor "
        "principal es visual: permite ver la región factible, entender por qué el óptimo está en "
        "un vértice y comprobar el efecto de cambiar una restricción."
    )
    m.figure(
        assets / "mod_grafico.png",
        "Pestaña «Método gráfico» con el ejemplo de maximización de Z = 3x1 + 5x2.",
        16.4,
    )

    m.h2("4.1 ¿Qué resuelve?")
    m.p(
        "Resuelve un modelo de la forma **optimizar Z = c1 x1 + c2 x2** sujeto a restricciones "
        "lineales y a las condiciones de no negatividad x1 ≥ 0, x2 ≥ 0. La aplicación calcula "
        "todos los vértices de la región factible, evalúa la función objetivo en cada uno y "
        "selecciona el mejor."
    )
    m.p(
        "El resultado incluye la región factible dibujada, las rectas de cada restricción, los "
        "vértices con su valor de Z y la recta objetivo en el punto óptimo. También detecta si el "
        "problema es infactible o si la función objetivo no está acotada."
    )

    m.h2("4.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Campo de x1", "Coeficiente de x1 en la función objetivo.", "`3`"],
            ["Campo de x2", "Coeficiente de x2 en la función objetivo.", "`5`"],
            ["Maximizar / Minimizar", "Sentido de la optimización.", "Maximizar"],
            ["Restricciones", "Una restricción por línea: `a1 a2 <= | >= | = b`.", "`3 2 <= 18`"],
            ["Gráfico", "Región factible, rectas, vértices y recta objetivo.", "—"],
            ["Resultados", "Estado, valor óptimo y tabla de vértices.", "—"],
            ["Resolver / Ejemplo / Limpiar", "Acciones del módulo.", "—"],
        ],
        widths=[3.6, 8.2, 4.6],
        first_col_bold=True,
        caption="Elementos de la pestaña «Método gráfico».",
    )
    m.p(
        "Las restricciones se escriben sin la parte «x1» y «x2»: solo los coeficientes, el operador "
        "y el lado derecho. Por ejemplo, `3x1 + 2x2 <= 18` se escribe `3 2 <= 18`. La aplicación "
        "añade automáticamente x1 ≥ 0 y x2 ≥ 0."
    )

    m.h2("4.3 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **Método gráfico**.",
            "Escriba los coeficientes de la función objetivo en los campos de x1 y x2.",
            "Seleccione **Maximizar** o **Minimizar**.",
            "Escriba una restricción por línea en el área de texto. Use punto decimal y los "
            "operadores `<=`, `>=` o `=`.",
            "Presione **Resolver**. También puede usar Cmd + Enter o Ctrl + Enter.",
            "Lea el estado y el valor óptimo en el panel derecho; observe el vértice marcado en el gráfico.",
            "Revise la tabla de vértices para comprobar que evaluó todas las esquinas.",
            "Presione **Guardar .txt** si desea conservar el informe.",
        ]
    )

    m.h2("4.4 Ejemplo guiado")
    m.callout(
        "example",
        "Maximización con tres restricciones",
        [
            "Una fábrica produce dos artículos. Cada unidad de x1 consume 1 hora de corte y 3 horas "
            "de ensamble; cada unidad de x2 consume 2 horas de ensamble. Hay 4 horas de corte, 12 "
            "horas de ensamble y 18 horas de acabado. La ganancia es 3 por unidad de x1 y 5 por "
            "unidad de x2. Maximice la ganancia.",
            "Modelo: Max Z = 3x1 + 5x2, sujeto a x1 ≤ 4; 2x2 ≤ 12; 3x1 + 2x2 ≤ 18; x1, x2 ≥ 0.",
        ],
    )
    m.code(
        [
            "Función objetivo:  Z = 3 x1 + 5 x2      (Maximizar)",
            "",
            "Restricciones:",
            "1 0 <= 4",
            "0 2 <= 12",
            "3 2 <= 18",
        ],
        caption="Datos que debe introducir en la pestaña «Método gráfico».",
    )
    m.p("La aplicación informa **ÓPTIMO**, con **Z = 36** en el punto **(x1, x2) = (2, 6)**.")
    m.table(
        ["Vértice", "x1", "x2", "Z = 3x1 + 5x2", "¿Óptimo?"],
        [
            ["V1", "0", "0", "0", ""],
            ["V2", "0", "6", "30", ""],
            ["V3", "2", "6", "36", "★"],
            ["V4", "4", "3", "27", ""],
            ["V5", "4", "0", "12", ""],
        ],
        widths=[2.4, 2.6, 2.6, 5.6, 3.2],
        aligns=["c", "r", "r", "r", "c"],
        caption="Tabla de vértices que aparece en el informe del ejemplo.",
    )
    m.p(
        "La región factible es el polígono de vértices (0,0), (4,0), (4,3), (2,6) y (0,6). El "
        "óptimo se alcanza en (2,6), donde se cruzan las restricciones 2x2 ≤ 12 y 3x1 + 2x2 ≤ 18."
    )

    m.h2("4.5 Cómo leer el gráfico")
    m.table(
        ["Elemento del gráfico", "Interpretación"],
        [
            ["Zona verde sombreada", "Región factible: todos los pares (x1, x2) que cumplen las restricciones."],
            ["Líneas de colores", "Cada restricción. La etiqueta R1, R2, R3 identifica su ecuación."],
            ["Puntos azules", "Vértices de la región factible."],
            ["Punto rojo grande", "Solución óptima."],
            ["Línea roja discontinua", "Recta objetivo en el valor óptimo. Todos los puntos de esa recta tienen el mismo Z."],
            ["Mensaje superior", "Aparece cuando el problema es infactible o no acotado."],
        ],
        widths=[5.2, 11.2],
        first_col_bold=True,
        caption="Lectura de los elementos visuales del método gráfico.",
    )
    m.p(
        "Si la recta objetivo es paralela a una restricción activa, puede haber **óptimos "
        "alternativos**: todos los puntos del segmento entre dos vértices tienen el mismo valor "
        "óptimo. La aplicación sigue mostrando un vértice, pero la interpretación debe mencionar "
        "la familia de soluciones."
    )

    m.h2("4.6 Interpretación de los resultados")
    m.bullets(
        [
            "**Estado:** indica si el modelo tiene solución óptima, es infactible o no está acotado.",
            "**Z óptimo:** valor de la función objetivo en la mejor solución.",
            "**x1, x2:** cantidades óptimas de cada variable. Verifique que sean coherentes con las unidades del problema.",
            "**Región acotada:** si es «no», el óptimo puede estar en el infinito; revise el modelo.",
            "**Vértices:** permiten explicar por qué el óptimo está en una esquina y no en el interior.",
        ]
    )
    m.callout(
        "tip",
        "Cómo explicar el resultado en un informe",
        [
            "No basta con escribir «Z = 36». Redacte: «La ganancia máxima es 36, produciendo 2 "
            "unidades del artículo 1 y 6 del artículo 2. Las restricciones de ensamble y acabado "
            "están activas; la de corte tiene holgura de 2 horas».",
        ],
    )

    m.h2("4.7 Casos especiales")
    m.table(
        ["Situación", "Cómo se ve en la aplicación", "Qué significa"],
        [
            ["Infactible", "Estado **INFACTIBLE** y ausencia de región factible.", "Ningún punto cumple todas las restricciones. Revise los signos y los valores del lado derecho."],
            ["No acotado", "Estado **NO ACOTADO**.", "La función objetivo puede crecer o decrecer sin límite en la dirección factible. Puede faltar una restricción."],
            ["Óptimos alternativos", "Dos vértices consecutivos con el mismo Z.", "La recta objetivo es paralela a una restricción activa; hay infinitas soluciones óptimas."],
            ["Restricción redundante", "Una recta no toca la región factible.", "No limita el problema; se puede eliminar sin cambiar el óptimo."],
        ],
        widths=[3.4, 6.0, 7.0],
        first_col_bold=True,
        caption="Casos especiales del método gráfico y su lectura.",
    )

    m.h2("4.8 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«Use el formato coef1 coef2 <= valor»", "Falta un coeficiente o el operador.", "Escriba exactamente dos coeficientes, un operador y el valor."],
            ["«Operador no válido»", "Se escribió `<` o `>` en lugar de `<=` o `>=`.", "Use `<=`, `>=` o `=`."],
            ["Resultado extraño con decimales", "Se usó coma decimal.", "Cambie `2,5` por `2.5`."],
            ["Infactible inesperado", "Restricciones contradictorias o lado derecho negativo.", "Revise la dirección de las desigualdades y el signo del lado derecho."],
            ["No se ve el gráfico", "La ventana es demasiado pequeña.", "Amplíe la ventana o maximícela."],
        ],
        widths=[5.4, 5.2, 5.8],
        caption="Errores frecuentes en el método gráfico.",
    )

    m.h2("4.9 Ejercicio propuesto")
    m.p(
        "Resuelva: **Min Z = 4x1 + 3x2**, sujeto a `2 1 >= 8`, `1 1 >= 6`, `1 0 <= 8`, `0 1 <= 8`. "
        "Identifique la región factible, calcule los vértices y compruebe el valor óptimo. "
        "Después cambie el coeficiente de x1 a 3 y observe si cambia el vértice óptimo."
    )

    # =====================================================================
    # 5. SIMPLEX
    # =====================================================================
    m.h1("5. Método Simplex")
    m.lead(
        "El método simplex resuelve modelos de programación lineal con cualquier número de "
        "variables. La aplicación implementa el método de dos fases, que permite trabajar con "
        "restricciones de tipo <=, >= e = y con lados derechos negativos."
    )
    m.figure(
        assets / "mod_simplex.png",
        "Pestaña «Simplex»: función objetivo, restricciones y tablas del desarrollo por fases.",
        16.4,
    )

    m.h2("5.1 ¿Qué resuelve?")
    m.p(
        "Resuelve un modelo lineal en forma estándar: optimizar Z = c1x1 + … + cnxn sujeto a "
        "restricciones lineales con operadores <=, >= o =, y variables no negativas. A diferencia "
        "del método gráfico, no hay límite en el número de variables ni de restricciones."
    )
    m.p(
        "El informe muestra todas las tablas del algoritmo: la fase 1 (que busca una solución "
        "factible inicial minimizando variables artificiales) y la fase 2 (que optimiza la función "
        "objetivo original). También indica qué variable entra y cuál sale en cada iteración."
    )

    m.h2("5.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Coeficientes", "Coeficientes de la función objetivo, separados por espacios.", "`3 5`"],
            ["Maximizar / Minimizar", "Sentido de la optimización.", "Maximizar"],
            ["Restricciones", "Una por línea: coeficientes, operador y valor.", "`3 2 <= 18`"],
            ["Variables no negativas", "Condición implícita del modelo.", "x1, x2 ≥ 0"],
            ["Panel de resultados", "Estado, solución y tablas por fase e iteración.", "—"],
        ],
        widths=[3.8, 8.2, 4.4],
        first_col_bold=True,
        caption="Elementos de la pestaña «Simplex».",
    )
    m.p(
        "El número de coeficientes de la función objetivo define el número de variables. Todas "
        "las restricciones deben tener exactamente esa cantidad de coeficientes. Si una variable "
        "no aparece en una restricción, escriba un 0 en su lugar."
    )

    m.h2("5.3 Formato del modelo y método de dos fases")
    m.p(
        "Escriba la función objetivo y las restricciones como en estos ejemplos:"
    )
    m.code(
        [
            "Max Z = 3x1 + 5x2",
            "",
            "1 0 <= 4",
            "0 2 <= 12",
            "3 2 <= 18",
            "",
            "Otro formato válido (minimización con >=):",
            "2 3 1",
            "1 1 0 >= 4",
            "0 1 1 = 6",
            "2 0 3 <= 12",
        ],
        caption="Ejemplos de funciones objetivo y restricciones para Simplex.",
    )
    m.p("La aplicación sigue estos pasos internos:")
    m.steps(
        [
            "**Normalización:** convierte cada restricción a igualdad añadiendo variables de "
            "holgura (para <=), variables de exceso y artificiales (para >=) o artificiales (para =).",
            "**Fase 1:** minimiza la suma de variables artificiales. Si el mínimo es mayor que cero, "
            "el problema es infactible.",
            "**Fase 2:** parte de la base factible encontrada y optimiza la función objetivo original.",
            "**Criterio de optimalidad:** en maximización, ninguna variable no básica debe tener "
            "costo reducido positivo; en minimización, ninguno debe ser negativo.",
            "**Iteración:** entra la variable con el costo reducido más favorable y sale la que "
            "preserva la factibilidad (prueba de la razón mínima).",
        ]
    )

    m.h2("5.4 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **Simplex**.",
            "Escriba los coeficientes de la función objetivo separados por espacios.",
            "Seleccione el sentido de optimización.",
            "Escriba una restricción por línea, con tantos coeficientes como variables haya.",
            "Presione **Resolver**.",
            "Lea el estado y la solución óptima al inicio del informe.",
            "Revise la fase 1 para comprobar que se encontró una base factible.",
            "Siga las tablas de la fase 2 para ver cómo mejora Z en cada iteración.",
            "Guarde el informe con **Guardar .txt**.",
        ]
    )

    m.h2("5.5 Ejemplo guiado")
    m.p(
        "Use el mismo modelo del capítulo anterior: **Max Z = 3x1 + 5x2**, sujeto a `1 0 <= 4`, "
        "`0 2 <= 12`, `3 2 <= 18`. La aplicación confirma **ÓPTIMO**, con **Z* = 36**, "
        "**x1 = 2** y **x2 = 6**."
    )
    m.p("La primera tabla de la fase 2 es la siguiente:")
    m.table(
        ["Base", "x1", "x2", "s1", "s2", "s3", "RHS"],
        [
            ["s1", "1", "0", "1", "0", "0", "4"],
            ["s2", "0", "2", "0", "1", "0", "12"],
            ["s3", "3", "2", "0", "0", "1", "18"],
            ["Z", "−3", "−5", "0", "0", "0", "0"],
        ],
        widths=[2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 3.2],
        aligns=["l"] + ["r"] * 6,
        caption="Fase 2, tabla 1: base inicial con variables de holgura.",
    )
    m.p(
        "Entra **x2** porque tiene el costo reducido más negativo (−5) y sale **s3** por la prueba "
        "de la razón mínima. Después de cuatro tablas de fase 2 se llega a:"
    )
    m.table(
        ["Base", "x1", "x2", "s1", "s2", "s3", "RHS"],
        [
            ["x1", "1", "0", "0", "−1/3", "1/3", "2"],
            ["s1", "0", "0", "1", "1/3", "−1/3", "2"],
            ["x2", "0", "1", "0", "1/2", "0", "6"],
            ["Z", "0", "0", "0", "3/2", "1", "36"],
        ],
        widths=[2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 3.2],
        aligns=["l"] + ["r"] * 6,
        caption="Fase 2, tabla final: solución óptima x1 = 2, x2 = 6, Z = 36.",
    )
    m.p(
        "La fila Z no tiene costos reducidos negativos, así que la solución es óptima. Los valores "
        "de la columna RHS de las filas básicas son los valores de las variables: x1 = 2, s1 = 2 "
        "y x2 = 6. La holgura s1 = 2 corresponde a la restricción de corte."
    )

    m.h2("5.6 Cómo leer una tabla simplex")
    m.table(
        ["Parte de la tabla", "Significado"],
        [
            ["Columna «Base»", "Variables básicas de la solución actual."],
            ["Columnas de variables", "Coeficientes tecnológicos después de las operaciones de fila."],
            ["Columna RHS", "Lado derecho; en las filas básicas contiene el valor de cada variable básica."],
            ["Fila Z", "Costos reducidos. En maximización, un valor negativo indica que conviene entrar."],
            ["Variable que entra", "La de costo reducido más favorable (negativo al maximizar)."],
            ["Variable que sale", "La que produce la razón RHS/coeficiente positiva más pequeña."],
        ],
        widths=[5.0, 11.4],
        first_col_bold=True,
        caption="Interpretación de las partes de una tabla simplex.",
    )

    m.h2("5.7 Interpretación de la solución")
    m.bullets(
        [
            "**Z\\*:** valor óptimo de la función objetivo.",
            "**Variables de decisión:** cantidades que debe producir, asignar o contratar.",
            "**Variables de holgura:** recursos no utilizados. Una holgura positiva indica que la restricción no está activa.",
            "**Variables de exceso:** cantidad por encima del mínimo exigido en restricciones >=.",
            "**Costos reducidos:** mejoran Z si se fuerza una unidad de una variable no básica; también se usan para detectar óptimos alternativos.",
        ]
    )
    m.callout(
        "tip",
        "Verificación rápida",
        [
            "Sustituya la solución en cada restricción original. Si alguna se viola o el valor de Z "
            "no coincide, revise el número de coeficientes y los operadores. La aplicación muestra "
            "la solución, pero la verificación manual es una buena práctica de presentación.",
        ],
    )

    m.h2("5.8 Casos especiales")
    m.table(
        ["Estado", "Qué significa", "Cómo proceder"],
        [
            ["ÓPTIMO", "Se encontró la mejor solución factible.", "Interprete las variables y las holguras."],
            ["INFACTIBLE", "La fase 1 no pudo eliminar las variables artificiales.", "Revise restricciones contradictorias, signos y lados derechos."],
            ["NO ACOTADO", "Existe una dirección factible que mejora Z indefinidamente.", "Falta una restricción o el sentido está invertido."],
            ["ÓPTIMOS ALTERNATIVOS", "Una variable no básica tiene costo reducido cero.", "Hay infinitas soluciones con el mismo Z; describa la familia."],
            ["LÍMITE DE ITERACIONES", "El algoritmo se detuvo por seguridad.", "Puede haber ciclismo; revise el modelo o simplifique restricciones redundantes."],
        ],
        widths=[3.6, 7.2, 5.6],
        first_col_bold=True,
        caption="Estados posibles del método simplex.",
    )
    m.p(
        "La aplicación también admite lados derechos negativos. En ese caso multiplica la "
        "restricción por −1 y cambia el sentido de la desigualdad antes de construir la tabla; "
        "el informe muestra el modelo ya normalizado."
    )

    m.h2("5.9 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«Se esperaban N coeficientes, un operador y el valor»", "Una restricción tiene menos o más coeficientes que variables.", "Cuente las variables de la función objetivo y complete con ceros."],
            ["«Los operadores válidos son <=, >=, =»", "Se usó `<`, `>` o un carácter inválido.", "Corrija el operador."],
            ["«Todas las filas de A deben tener el mismo número de columnas»", "Filas con longitudes distintas.", "Iguale la cantidad de coeficientes en todas las líneas."],
            ["Infactible inesperado", "Dirección de la desigualdad incorrecta.", "Compruebe si el problema pide al menos (>=) o como máximo (<=)."],
            ["No aparece la solución esperada", "Se olvidó declarar una variable (por ejemplo, un coeficiente 0).", "Incluya todas las variables, aunque su coeficiente sea cero."],
        ],
        widths=[5.8, 5.0, 5.6],
        caption="Errores frecuentes en Simplex.",
    )

    m.h2("5.10 Ejercicio propuesto")
    m.p(
        "Resuelva: **Max Z = 2x1 + 3x2 + x3**, sujeto a `1 2 0 <= 8`, `0 1 2 <= 6`, `1 0 1 <= 4`. "
        "Identifique la solución óptima, las holguras y el valor de Z. Después agregue la "
        "restricción `1 1 1 >= 7` y explique por qué el problema cambia de estado."
    )

    # =====================================================================
    # 6. TRANSPORTE
    # =====================================================================
    m.h1("6. Modelo de transporte")
    m.lead(
        "El modelo de transporte decide cuánto enviar desde cada origen hacia cada destino para "
        "satisfacer la demanda con el menor costo posible. La aplicación incluye tres métodos de "
        "solución inicial y la optimización MODI, que verifica y mejora la solución."
    )
    m.figure(
        assets / "mod_transporte.png",
        "Pestaña «Transporte» con la matriz de costos, la oferta, la demanda y la solución final.",
        16.4,
    )

    m.h2("6.1 ¿Qué resuelve?")
    m.p(
        "Dados **m orígenes** con oferta disponible y **n destinos** con demanda requerida, y una "
        "matriz de costos unitarios de transporte, el modelo busca las cantidades xij que minimizan "
        "el costo total. Si la oferta total es mayor que la demanda, o viceversa, la aplicación "
        "agrega automáticamente una fila o columna ficticia con costo cero."
    )
    m.p(
        "También puede maximizar ganancias. En ese caso la aplicación transforma las ganancias en "
        "costos de oportunidad y resuelve el problema equivalente de minimización; el informe "
        "etiqueta el resultado como «Ganancia total máxima»."
    )

    m.h2("6.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Matriz de costos", "Una fila por origen y una columna por destino.", "`8 6 10 9`"],
            ["Oferta", "Disponibilidad de cada origen, separada por espacios.", "`35 50 40`"],
            ["Demanda", "Requerimiento de cada destino, separado por espacios.", "`45 20 30 30`"],
            ["Método inicial", "Vogel, costo mínimo o esquina noroeste.", "Vogel"],
            ["Maximizar ganancia", "Interpreta la matriz como beneficios en lugar de costos.", "Desactivado"],
            ["Nombres", "Etiquetas opcionales para orígenes y destinos.", "Planta 1, Centro 1…"],
        ],
        widths=[3.6, 8.6, 4.2],
        first_col_bold=True,
        caption="Elementos de la pestaña «Transporte».",
    )
    m.p(
        "Los nombres son opcionales. Si se dejan vacíos, la aplicación usa O1, O2, … para los "
        "orígenes y D1, D2, … para los destinos. Si se escriben, deben coincidir en cantidad con "
        "las filas y columnas de la matriz."
    )

    m.h2("6.3 Métodos de solución")
    m.table(
        ["Método", "Cómo construye la solución inicial", "Cuándo conviene"],
        [
            ["Esquina noroeste", "Asigna lo máximo posible empezando por la celda superior izquierda.", "Es el más simple y rápido, pero suele estar lejos del óptimo."],
            ["Costo mínimo", "Elige la celda de menor costo y asigna lo máximo posible.", "Mejor punto de partida que la esquina noroeste."],
            ["Vogel", "Penaliza no usar la fila o columna con mayor diferencia entre sus dos costos menores.", "Suele producir la mejor solución inicial y reducir las iteraciones MODI."],
            ["MODI", "Calcula potenciales u y v y costos de oportunidad para mejorar la solución.", "Se aplica siempre después del método inicial."],
        ],
        widths=[3.4, 8.4, 4.6],
        first_col_bold=True,
        caption="Métodos de solución inicial y optimización incluidos.",
    )
    m.p("El algoritmo MODI sigue estos pasos:")
    m.steps(
        [
            "Construir una solución básica factible con el método inicial elegido.",
            "Calcular potenciales u para las filas y v para las columnas usando las celdas básicas: u_i + v_j = c_ij.",
            "Calcular el costo de oportunidad Δ_ij = c_ij − (u_i + v_j) para cada celda no básica.",
            "Si todos los Δ_ij son mayores o iguales que cero (en minimización), la solución es óptima.",
            "Si hay un Δ negativo, entra la celda con el valor más negativo. Se forma un ciclo de asignación y se ajusta con θ.",
            "Repetir hasta que no haya costos de oportunidad negativos.",
        ]
    )

    m.h2("6.4 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **Transporte**.",
            "Escriba la matriz de costos con una fila por origen y una columna por destino.",
            "Escriba la oferta, separada por espacios, con un valor por fila.",
            "Escriba la demanda, separada por espacios, con un valor por columna.",
            "Elija el método inicial en la lista desplegable.",
            "Active **Maximizar ganancia** solo si los valores representan beneficios.",
            "Revise los nombres opcionales y corríjalos si no coinciden con las dimensiones.",
            "Presione **Resolver** y lea la solución inicial, las iteraciones y la solución final.",
            "Compruebe los potenciales u y v y los costos de oportunidad de la tabla final.",
        ]
    )

    m.h2("6.5 Ejemplo guiado")
    m.p(
        "Una empresa tiene tres plantas con ofertas de 35, 50 y 40 unidades, y cuatro centros de "
        "distribución con demandas de 45, 20, 30 y 30. La oferta total es 125 y la demanda total "
        "también es 125, por lo que el modelo está balanceado."
    )
    m.table(
        ["Origen / destino", "Centro 1", "Centro 2", "Centro 3", "Centro 4", "Oferta"],
        [
            ["Planta 1", "8", "6", "10", "9", "35"],
            ["Planta 2", "9", "12", "13", "7", "50"],
            ["Planta 3", "14", "9", "16", "5", "40"],
            ["Demanda", "45", "20", "30", "30", "125"],
        ],
        widths=[3.4, 2.6, 2.6, 2.6, 2.6, 2.6],
        aligns=["l"] + ["r"] * 5,
        first_col_bold=True,
        caption="Matriz de costos y datos del ejemplo de transporte.",
    )
    m.code(
        [
            "Costos:",
            "8 6 10 9",
            "9 12 13 7",
            "14 9 16 5",
            "",
            "Oferta: 35 50 40",
            "Demanda: 45 20 30 30",
            "Método: Vogel",
        ],
        caption="Datos que debe introducir en la pestaña «Transporte».",
    )
    m.p(
        "Con Vogel, la solución inicial ya es óptima. El costo total mínimo es **1020** y la "
        "asignación final es:"
    )
    m.table(
        ["Origen / destino", "Centro 1", "Centro 2", "Centro 3", "Centro 4", "Oferta"],
        [
            ["Planta 1", "0", "10", "25", "0", "35"],
            ["Planta 2", "45", "0", "5", "0", "50"],
            ["Planta 3", "0", "10", "0", "30", "40"],
            ["Demanda", "45", "20", "30", "30", "125"],
        ],
        widths=[3.4, 2.6, 2.6, 2.6, 2.6, 2.6],
        aligns=["l"] + ["r"] * 5,
        first_col_bold=True,
        caption="Solución óptima del ejemplo: costo total 1020.",
    )
    m.p(
        "Comprobación del costo: Planta 1 envía 10 unidades a C2 (6 cada una) y 25 a C3 (10 cada "
        "una), es decir 60 + 250 = 310. Planta 2 envía 45 a C1 (9) y 5 a C3 (13): 405 + 65 = 470. "
        "Planta 3 envía 10 a C2 (9) y 30 a C4 (5): 90 + 150 = 240. Total: 310 + 470 + 240 = 1020."
    )

    m.h2("6.6 Cómo leer la optimización MODI")
    m.p(
        "Para la solución anterior, la aplicación calcula **u = [0, 3, 3]** y **v = [6, 6, 10, 2]**. "
        "La matriz de costos de oportunidad es:"
    )
    m.table(
        ["", "Centro 1", "Centro 2", "Centro 3", "Centro 4"],
        [
            ["Planta 1", "2", "0", "0", "7"],
            ["Planta 2", "0", "3", "0", "2"],
            ["Planta 3", "5", "0", "3", "0"],
        ],
        widths=[3.4, 3.2, 3.2, 3.2, 3.2],
        aligns=["l", "r", "r", "r", "r"],
        first_col_bold=True,
        caption="Costos de oportunidad Δij de la solución óptima.",
    )
    m.p(
        "Todos los valores son mayores o iguales que cero, lo que confirma que no existe una "
        "reasignación que reduzca el costo. Un Δ negativo indicaría que esa celda debe entrar en "
        "la solución. Las celdas básicas tienen Δ = 0 por construcción."
    )
    m.callout(
        "info",
        "Qué son u y v",
        [
            "u_i es el precio sombra implícito del origen i y v_j el del destino j. En las celdas "
            "básicas se cumple u_i + v_j = c_ij. Los potenciales permiten comparar el costo real de "
            "una celda con el costo que el sistema «esperaría» pagar por ella.",
        ],
    )

    m.h2("6.7 Balanceo, fila ficticia y maximización")
    m.table(
        ["Situación", "Qué hace la aplicación", "Cómo interpretarlo"],
        [
            ["Oferta > demanda", "Agrega una columna ficticia con costo 0 y demanda igual a la diferencia.", "La asignación en la columna ficticia es capacidad no utilizada."],
            ["Demanda > oferta", "Agrega una fila ficticia con costo 0 y oferta igual a la diferencia.", "La asignación en la fila ficticia es demanda no satisfecha."],
            ["Maximizar ganancia", "Convierte el problema en minimización de costos negativos.", "El valor final se muestra como ganancia máxima."],
            ["Solución degenerada", "Completa la base con celdas de asignación cero cuando hace falta.", "Una celda básica con valor cero es normal; no significa un error."],
        ],
        widths=[4.0, 7.0, 5.4],
        first_col_bold=True,
        caption="Situaciones especiales del modelo de transporte.",
    )

    m.h2("6.8 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«El número de ofertas debe coincidir con las filas»", "La lista de oferta no tiene un valor por fila.", "Cuente las filas de la matriz y escriba esa cantidad de ofertas."],
            ["«El número de demandas debe coincidir con las columnas»", "La lista de demanda no coincide con las columnas.", "Escriba una demanda por columna."],
            ["«Todas las filas… deben tener igual longitud»", "Una fila de costos tiene menos columnas.", "Complete la fila que falta."],
            ["«Ofertas y demandas deben ser no negativas»", "Se ingresó un valor negativo.", "Corrija el signo; el modelo no admite oferta o demanda negativa."],
            ["«La cantidad de nombres… no coincide»", "Se escribieron más o menos nombres que filas o columnas.", "Deje los nombres vacíos o escriba exactamente la cantidad correcta."],
            ["Costo muy alto con una celda asignada", "Esa celda es la única forma de satisfacer la demanda.", "Revise si el modelo está balanceado y si los costos son correctos."],
        ],
        widths=[5.8, 5.0, 5.6],
        caption="Errores frecuentes en el modelo de transporte.",
    )

    m.h2("6.9 Ejercicio propuesto")
    m.p(
        "Resuelva el mismo ejemplo con el método de **esquina noroeste** y con **costo mínimo**. "
        "Compare el costo inicial de cada método, cuente las iteraciones MODI necesarias y "
        "compruebe que todas llegan al mismo costo óptimo de 1020. Explique por qué Vogel suele "
        "requerir menos iteraciones."
    )

    # =====================================================================
    # 7. ASIGNACIÓN
    # =====================================================================
    m.h1("7. Problema de asignación")
    m.lead(
        "El problema de asignación es un caso especial del transporte en el que cada agente se "
        "asigna a una sola tarea y cada tarea recibe exactamente un agente. La aplicación usa el "
        "algoritmo húngaro, que garantiza el óptimo global."
    )
    m.figure(
        assets / "mod_asignacion.png",
        "Pestaña «Asignación»: matriz de costos, asignación óptima y matriz marcada.",
        16.4,
    )

    m.h2("7.1 ¿Qué resuelve?")
    m.p(
        "Dada una matriz de costos (o beneficios) de tamaño m × n, donde la fila i representa al "
        "agente i y la columna j representa la tarea j, el objetivo es encontrar una asignación "
        "uno a uno que minimice el costo total o maximice el beneficio total."
    )
    m.p(
        "Si la matriz es rectangular, la aplicación equilibra el problema con filas o columnas "
        "ficticias de costo cero. Las tareas ficticias representan agentes sin asignar o tareas "
        "sin cubrir, según el caso."
    )

    m.h2("7.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Matriz", "Filas = agentes; columnas = tareas. Una fila por línea.", "`9 2 7 8`"],
            ["Maximizar beneficio", "Interpreta la matriz como ganancias en lugar de costos.", "Desactivado"],
            ["Resultados", "Asignación uno a uno, costo total y matriz marcada con *.", "—"],
        ],
        widths=[4.0, 8.4, 4.0],
        first_col_bold=True,
        caption="Elementos de la pestaña «Asignación».",
    )

    m.h2("7.3 Cómo funciona el algoritmo húngaro")
    m.steps(
        [
            "Restar el menor valor de cada fila a todos los elementos de esa fila.",
            "Restar el menor valor de cada columna a todos los elementos de esa columna.",
            "Cubrir todos los ceros con el menor número posible de líneas horizontales y verticales.",
            "Si el número de líneas es igual al tamaño del problema, la asignación óptima está en los ceros.",
            "Si no, restar el menor valor no cubierto a las celdas no cubiertas, sumarlo a las celdas cubiertas dos veces y repetir.",
        ]
    )
    m.p(
        "La aplicación realiza estas operaciones internamente y presenta directamente la asignación "
        "final. Para maximizar, convierte los beneficios en costos de oportunidad restando cada "
        "valor del máximo de la matriz."
    )

    m.h2("7.4 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **Asignación**.",
            "Escriba la matriz con una fila por agente y una columna por tarea.",
            "Active **Maximizar beneficio** si los valores son ganancias.",
            "Presione **Resolver**.",
            "Lea la tabla de asignación: agente, tarea y costo o beneficio individual.",
            "Compare la suma con el costo o beneficio total informado.",
            "Use la matriz marcada con * para verificar que no haya dos agentes en la misma tarea.",
            "Guarde el informe si lo necesita.",
        ]
    )

    m.h2("7.5 Ejemplo guiado")
    m.p(
        "Cuatro agentes deben realizar cuatro tareas. La matriz de costos es:"
    )
    m.table(
        ["", "Tarea 1", "Tarea 2", "Tarea 3", "Tarea 4"],
        [
            ["Agente 1", "9", "2", "7", "8"],
            ["Agente 2", "6", "4", "3", "7"],
            ["Agente 3", "5", "8", "1", "8"],
            ["Agente 4", "7", "6", "9", "4"],
        ],
        widths=[3.6, 3.2, 3.2, 3.2, 3.2],
        aligns=["l", "r", "r", "r", "r"],
        first_col_bold=True,
        caption="Matriz de costos del ejemplo de asignación.",
    )
    m.code(
        [
            "9 2 7 8",
            "6 4 3 7",
            "5 8 1 8",
            "7 6 9 4",
        ],
        caption="Datos que debe introducir en la pestaña «Asignación».",
    )
    m.p("La asignación óptima y el costo total son:")
    m.table(
        ["Agente", "Tarea asignada", "Costo"],
        [
            ["Agente 1", "Tarea 2", "2"],
            ["Agente 2", "Tarea 1", "6"],
            ["Agente 3", "Tarea 3", "1"],
            ["Agente 4", "Tarea 4", "4"],
            ["Total", "", "13"],
        ],
        widths=[4.2, 6.0, 4.2],
        aligns=["l", "l", "r"],
        first_col_bold=True,
        caption="Asignación óptima del ejemplo: costo total 13.",
    )
    m.p(
        "Cada fila y cada columna tienen exactamente una marca *. El costo total es la suma de "
        "los valores marcados: 2 + 6 + 1 + 4 = 13. Cambiar cualquier asignación aumenta el costo."
    )

    m.h2("7.6 Interpretación y variantes")
    m.bullets(
        [
            "**Costo total:** suma de los valores de las celdas asignadas. Es el valor mínimo posible.",
            "**Agente sin asignar:** aparece cuando la matriz es rectangular y hay más agentes que tareas.",
            "**Tarea sin cubrir:** aparece cuando hay más tareas que agentes. La aplicación la muestra como «sin asignar».",
            "**Maximización:** el valor informado es el beneficio máximo; las celdas marcadas son las que lo producen.",
        ]
    )
    m.table(
        ["Caso", "Qué hace la aplicación", "Ejemplo"],
        [
            ["Matriz cuadrada", "Asigna todos los agentes a todas las tareas.", "4 × 4"],
            ["Más agentes que tareas", "Agrega columnas ficticias de costo 0.", "5 × 3"],
            ["Más tareas que agentes", "Agrega filas ficticias de costo 0.", "3 × 5"],
            ["Maximizar", "Convierte beneficios en costos de oportunidad.", "Ventas por vendedor"],
        ],
        widths=[4.2, 7.2, 5.0],
        first_col_bold=True,
        caption="Variantes del problema de asignación.",
    )

    m.h2("7.7 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«La matriz de costos está vacía»", "No se escribió ningún valor.", "Escriba al menos una fila con números."],
            ["«Todas las filas deben tener la misma longitud»", "Una fila tiene menos o más columnas.", "Complete la matriz para que sea rectangular."],
            ["Asignación con tareas ficticias", "La matriz es rectangular.", "Es normal; interprete las ficticias como «sin asignar»."],
            ["Beneficio total menor de lo esperado", "Se activó maximización con una matriz de costos o viceversa.", "Revise el significado de los valores y la casilla **Maximizar beneficio**."],
        ],
        widths=[5.6, 5.2, 5.6],
        caption="Errores frecuentes en asignación.",
    )

    m.h2("7.8 Ejercicio propuesto")
    m.p(
        "Una empresa tiene cinco vendedores y cuatro zonas. La matriz de ventas esperadas (en miles) "
        "es `10 8 12 9`, `9 11 8 10`, `12 9 11 8`, `8 10 9 12`, `11 12 10 9`. Maximice las ventas "
        "totales, indique qué vendedor queda sin zona y explique por qué la aplicación agrega una "
        "columna ficticia."
    )
