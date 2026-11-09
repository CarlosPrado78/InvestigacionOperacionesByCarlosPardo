"""Capítulos 8 a 11 del manual."""

from __future__ import annotations

from pathlib import Path

from manual_style import Manual


def add_chapters(m: Manual, assets: Path) -> None:
    # =====================================================================
    # 8. COLAS
    # =====================================================================
    m.h1("8. Teoría de colas")
    m.lead(
        "La teoría de colas estudia sistemas en los que clientes llegan a recibir un servicio y, "
        "si el servicio no está disponible de inmediato, esperan. La aplicación calcula las medidas "
        "de desempeño de cinco modelos clásicos y permite comparar escenarios de capacidad."
    )
    m.figure(
        assets / "mod_colas.png",
        "Pestaña «Colas» con el modelo M/M/1 y las medidas de desempeño del ejemplo.",
        16.4,
    )

    m.h2("8.1 ¿Qué resuelve?")
    m.p(
        "Calcula la utilización del sistema, la probabilidad de que esté vacío, el número esperado "
        "de clientes en el sistema y en la cola, los tiempos de permanencia y de espera, la "
        "probabilidad de esperar y, cuando la capacidad es finita, la probabilidad de rechazo. "
        "También muestra la distribución del número de clientes P(N = n)."
    )
    m.p(
        "Los modelos incluidos son: **M/M/1**, **M/M/1/K**, **M/M/c**, **M/M/c/K** y **M/G/1**. "
        "La notación de Kendall A/B/c/K indica: llegadas A, servicio B, número de servidores c y "
        "capacidad del sistema K."
    )

    m.h2("8.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Modelo de cola", "Lista con los cinco modelos disponibles.", "M/M/1"],
            ["λ", "Tasa media de llegadas (clientes por unidad de tiempo).", "`2`"],
            ["μ", "Tasa media de servicio por servidor.", "`3`"],
            ["c", "Número de servidores. Se activa en M/M/c y M/M/c/K.", "`2`"],
            ["K", "Capacidad máxima del sistema. Se activa en M/M/1/K y M/M/c/K.", "`10`"],
            ["σ", "Desviación estándar del tiempo de servicio. Se activa en M/G/1.", "`1.5`"],
        ],
        widths=[3.4, 9.0, 4.0],
        first_col_bold=True,
        caption="Parámetros de la pestaña «Colas».",
    )
    m.callout(
        "warning",
        "Las unidades de tiempo deben ser coherentes",
        [
            "Si λ se expresa en clientes por hora, μ también debe estar en servicios por hora. "
            "Entonces W y Wq se obtienen en horas. Si λ está en clientes por minuto, los tiempos "
            "estarán en minutos. No mezcle horas con minutos sin convertir.",
        ],
    )

    m.h2("8.3 Modelos y condiciones de estabilidad")
    m.table(
        ["Modelo", "Descripción", "Condición"],
        [
            ["M/M/1", "Llegadas Poisson, servicio exponencial, un servidor, cola infinita.", "λ < μ"],
            ["M/M/1/K", "Un servidor y capacidad total K (incluye el cliente en servicio).", "λ y μ positivos; K ≥ 1"],
            ["M/M/c", "c servidores en paralelo, cola infinita.", "λ < cμ"],
            ["M/M/c/K", "c servidores y capacidad total K.", "K ≥ c"],
            ["M/G/1", "Un servidor, llegadas Poisson y servicio con distribución general.", "λ < μ y σ ≥ 0"],
        ],
        widths=[2.8, 9.4, 4.2],
        first_col_bold=True,
        caption="Modelos de cola incluidos y sus condiciones de validez.",
    )
    m.p(
        "En los modelos con capacidad finita, la tasa efectiva de llegada es λ(1 − P_K), donde P_K "
        "es la probabilidad de que el sistema esté lleno. Esa tasa, y no λ, se usa para calcular "
        "W y Wq. La aplicación lo hace automáticamente y lo indica en el informe."
    )

    m.h2("8.4 Fórmulas principales")
    m.p("Las medidas básicas se relacionan entre sí:")
    m.code(
        [
            "ρ = λ / (c μ)                      utilización",
            "L = Lq + λ_efectiva / μ            clientes en el sistema",
            "W = L / λ_efectiva                 tiempo en el sistema",
            "Wq = Lq / λ_efectiva               tiempo en la cola",
            "W = Wq + 1 / μ                     tiempo de servicio incluido",
        ],
        caption="Relaciones de Little y definiciones básicas.",
    )
    m.p("Para los modelos más frecuentes:")
    m.table(
        ["Modelo", "Fórmulas características"],
        [
            ["M/M/1", "P0 = 1 − ρ;  L = ρ/(1 − ρ);  Lq = ρ²/(1 − ρ);  W = 1/(μ − λ);  Wq = λ/[μ(μ − λ)]."],
            ["M/M/1/K", "ρ = λ/μ;  P0 = (1 − ρ)/(1 − ρ^(K+1));  Pn = P0 ρ^n;  P_K = P0 ρ^K."],
            ["M/M/c", "P0 = [Σ(n=0…c−1) (cρ)^n/n! + (cρ)^c/(c!(1−ρ))]^(−1);  Lq = P0 (cρ)^c ρ/[c!(1−ρ)²]."],
            ["M/G/1", "Lq = (ρ² + λ²σ²) / [2(1 − ρ)]  (fórmula de Pollaczek-Khinchine);  Wq = Lq/λ."],
        ],
        widths=[2.8, 13.6],
        first_col_bold=True,
        caption="Fórmulas que utiliza la aplicación.",
    )

    m.h2("8.5 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **Colas**.",
            "Seleccione el modelo en la lista desplegable. Los campos que no aplican se deshabilitan.",
            "Escriba λ y μ en las mismas unidades de tiempo.",
            "Si el modelo lo requiere, escriba c, K o σ.",
            "Presione **Resolver**.",
            "Lea la tabla de medidas de desempeño y la nota del modelo.",
            "Si el modelo tiene capacidad finita, revise la probabilidad de rechazo.",
            "Consulte la distribución P(N = n) para ver la probabilidad de cada cantidad de clientes.",
        ]
    )

    m.h2("8.6 Ejemplo guiado: M/M/1")
    m.p(
        "Un cajero atiende en promedio a 3 clientes por hora y llegan 2 clientes por hora. "
        "Suponga llegadas Poisson y servicio exponencial. Los datos son λ = 2 y μ = 3."
    )
    m.code(
        [
            "Modelo: M/M/1",
            "λ = 2",
            "μ = 3",
        ],
        caption="Datos del ejemplo M/M/1.",
    )
    m.table(
        ["Símbolo", "Significado", "Valor"],
        [
            ["ρ", "Utilización del sistema", "0.666667"],
            ["P0", "Probabilidad de sistema vacío", "0.333333"],
            ["L", "Número esperado en el sistema", "2"],
            ["Lq", "Número esperado en la cola", "1.333333"],
            ["W", "Tiempo esperado en el sistema", "1 hora"],
            ["Wq", "Tiempo esperado en la cola", "0.666667 h = 40 min"],
            ["P(espera)", "Probabilidad de esperar", "0.666667"],
            ["λ efectiva", "Tasa efectiva de llegada", "2"],
            ["P(rechazo)", "Probabilidad de rechazo", "0"],
        ],
        widths=[2.8, 7.6, 6.0],
        aligns=["c", "l", "r"],
        first_col_bold=True,
        caption="Medidas de desempeño del ejemplo M/M/1 con λ = 2 y μ = 3.",
    )
    m.p(
        "Interpretación: el cajero está ocupado el 66.67 % del tiempo. En promedio hay 2 clientes "
        "en el sistema, de los cuales 1.333 están esperando. Un cliente tarda 1 hora en total y "
        "40 minutos en la cola. Dos de cada tres clientes deben esperar."
    )
    m.table(
        ["n", "P(N = n)", "P(N ≤ n)"],
        [
            ["0", "0.333333", "0.333333"],
            ["1", "0.222222", "0.555556"],
            ["2", "0.148148", "0.703704"],
            ["3", "0.098765", "0.802469"],
            ["4", "0.065844", "0.868313"],
        ],
        widths=[3.0, 5.4, 5.4],
        aligns=["r", "r", "r"],
        caption="Primeras filas de la distribución del número de clientes para el ejemplo M/M/1.",
    )

    m.h2("8.7 Ejemplo guiado: M/M/c")
    m.p(
        "Un centro de atención tiene 3 servidores, recibe 8 llamadas por hora y cada servidor "
        "atiende 3 llamadas por hora. Con λ = 8, μ = 3 y c = 3, la utilización es ρ = 8/(3×3) = "
        "0.8889. El sistema es estable porque λ < cμ."
    )
    m.table(
        ["Medida", "Valor", "Interpretación"],
        [
            ["ρ", "0.888889", "Los tres servidores están ocupados, en promedio, el 88.89 % del tiempo."],
            ["P0", "0.028037", "Solo el 2.80 % del tiempo el sistema está totalmente vacío."],
            ["L", "9.046729", "Hay 9.05 clientes en el sistema en promedio."],
            ["Lq", "6.380062", "6.38 clientes esperan en la cola."],
            ["W", "1.130841 h", "Un cliente permanece 1.13 horas en el sistema."],
            ["Wq", "0.797508 h", "La espera media es de 0.80 horas (≈ 47.9 minutos)."],
            ["P(espera)", "0.797508", "Casi 8 de cada 10 clientes deben esperar."],
        ],
        widths=[2.8, 4.0, 9.6],
        aligns=["c", "r", "l"],
        first_col_bold=True,
        caption="Resultados del ejemplo M/M/c con λ = 8, μ = 3 y c = 3.",
    )
    m.p(
        "Este ejemplo muestra el efecto de la utilización alta: aunque hay tres servidores, la "
        "cola media supera los seis clientes. Si se reduce λ o se aumenta c, Lq disminuye de forma "
        "no lineal; pruebe distintos valores para construir un análisis de capacidad."
    )

    m.h2("8.8 Cómo interpretar los resultados")
    m.table(
        ["Medida", "Qué pregunta responde", "Uso práctico"],
        [
            ["ρ", "¿Qué fracción del tiempo están ocupados los servidores?", "Si se acerca a 1, la cola crece y los tiempos se disparan."],
            ["P0", "¿Con qué probabilidad no hay nadie?", "Dimensiona la probabilidad de inactividad."],
            ["L y Lq", "¿Cuántos clientes hay en promedio?", "Espacio físico, número de turnos, inventario en proceso."],
            ["W y Wq", "¿Cuánto espera un cliente?", "Nivel de servicio y cumplimiento de acuerdos."],
            ["P(espera)", "¿Qué probabilidad hay de tener que esperar?", "Percepción del cliente y diseño de la sala de espera."],
            ["P(rechazo)", "¿Qué fracción de clientes no puede entrar?", "Solo en capacidad finita; pérdida de demanda."],
            ["Pn", "¿Cómo se distribuye el número de clientes?", "Probabilidades de saturación y dimensionamiento."],
        ],
        widths=[3.0, 7.4, 6.0],
        first_col_bold=True,
        caption="Interpretación práctica de las medidas de cola.",
    )

    m.h2("8.9 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«Para M/M/1 se requiere lambda < mu»", "La llegada es mayor o igual que el servicio.", "Aumente μ, reduzca λ o use un modelo con más servidores."],
            ["«Para M/M/c se requiere lambda < c*mu»", "La capacidad total de servicio es insuficiente.", "Aumente c o μ, o reduzca λ."],
            ["«K debe ser un entero mayor o igual a c»", "La capacidad es menor que el número de servidores.", "Use un K mayor o igual a c."],
            ["«La desviación estándar del servicio debe ser ≥ 0»", "Se ingresó un valor negativo en σ.", "Corrija el valor; σ = 0 corresponde a servicio determinístico."],
            ["Tiempos en unidades extrañas", "λ y μ están en unidades distintas.", "Convierta ambas a la misma base (por hora, por minuto, etc.)."],
            ["ρ mayor que 1", "En un modelo infinito no hay equilibrio.", "El sistema es inestable; los resultados no son válidos."],
        ],
        widths=[5.8, 5.0, 5.6],
        caption="Errores frecuentes en teoría de colas.",
    )

    m.h2("8.10 Ejercicio propuesto")
    m.p(
        "Un banco tiene 2 cajeros. Llegan 18 clientes por hora y cada cajero atiende 12 por hora. "
        "Calcule ρ, Lq, Wq y la probabilidad de esperar. Luego evalúe qué ocurre si se agrega un "
        "tercer cajero. Compare los tiempos de espera y discuta si la mejora justifica el costo."
    )

    # =====================================================================
    # 9. MARKOV
    # =====================================================================
    m.h1("9. Cadenas de Markov")
    m.lead(
        "Una cadena de Markov describe un sistema que pasa de un estado a otro con probabilidades "
        "que dependen solo del estado actual. La aplicación calcula la evolución en n pasos, la "
        "distribución estacionaria, la clasificación de estados y, cuando existe, el análisis de "
        "absorción."
    )
    m.figure(
        assets / "mod_markov.png",
        "Pestaña «Markov»: matriz de transición, distribución inicial, pasos y clasificación de estados.",
        16.4,
    )

    m.h2("9.1 ¿Qué resuelve?")
    m.p(
        "Dada una matriz de transición P de tamaño n × n, donde p_ij es la probabilidad de pasar "
        "del estado i al estado j en un paso, la aplicación calcula P^n, la distribución después "
        "de n pasos, la distribución estacionaria π (si existe), las clases de estados, su carácter "
        "recurrente o transitorio, el período y los estados absorbentes."
    )
    m.p(
        "Si la cadena tiene estados absorbentes, también calcula el número esperado de pasos hasta "
        "la absorción y la probabilidad de absorberse en cada estado absorbente."
    )

    m.h2("9.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Matriz P", "Una fila por estado; cada fila debe sumar 1.", "`0.7 0.2 0.1`"],
            ["Distribución inicial", "Probabilidad de comenzar en cada estado. Es opcional.", "`1 0 0`"],
            ["Número de pasos n", "Entero no negativo para calcular P^n.", "`3`"],
            ["Resultados", "P^n, distribución, estado estable, clases y absorción.", "—"],
        ],
        widths=[3.6, 9.0, 3.8],
        first_col_bold=True,
        caption="Elementos de la pestaña «Markov».",
    )
    m.p(
        "La matriz debe ser cuadrada y cada fila debe sumar 1 (con tolerancia de 10⁻⁷). Si una fila "
        "no suma 1, la aplicación indica el número de fila y la suma calculada para facilitar la "
        "corrección."
    )

    m.h2("9.3 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **Markov**.",
            "Escriba la matriz de transición, una fila por estado.",
            "Escriba la distribución inicial separada por espacios, o déjela vacía si no la necesita.",
            "Indique el número de pasos n.",
            "Presione **Resolver**.",
            "Revise P^n y la distribución después de n pasos.",
            "Lea la distribución estacionaria y compruebe que sus valores suman 1.",
            "Consulte las clases, la periodicidad y, si hay estados absorbentes, el análisis de absorción.",
        ]
    )

    m.h2("9.4 Ejemplo guiado")
    m.p(
        "Una marca tiene tres estados: E1 (cliente leal), E2 (cliente ocasional) y E3 (cliente en "
        "riesgo). La matriz de transición mensual es:"
    )
    m.table(
        ["", "E1", "E2", "E3"],
        [
            ["E1", "0.7", "0.2", "0.1"],
            ["E2", "0.3", "0.4", "0.3"],
            ["E3", "0.2", "0.2", "0.6"],
        ],
        widths=[2.4, 3.6, 3.6, 3.6],
        aligns=["l", "r", "r", "r"],
        first_col_bold=True,
        caption="Matriz de transición del ejemplo de Markov.",
    )
    m.code(
        [
            "Matriz P:",
            "0.7 0.2 0.1",
            "0.3 0.4 0.3",
            "0.2 0.2 0.6",
            "",
            "Distribución inicial: 1 0 0",
            "Número de pasos n: 3",
        ],
        caption="Datos del ejemplo de Markov.",
    )
    m.p("La distribución estacionaria que reporta la aplicación es:")
    m.table(
        ["Estado", "π"],
        [
            ["E1", "0.45"],
            ["E2", "0.25"],
            ["E3", "0.30"],
            ["Suma", "1.00"],
        ],
        widths=[4.0, 5.0],
        aligns=["l", "r"],
        first_col_bold=True,
        caption="Distribución estacionaria del ejemplo.",
    )
    m.p("La matriz P³ es:")
    m.table(
        ["", "E1", "E2", "E3"],
        [
            ["E1", "0.509", "0.248", "0.243"],
            ["E2", "0.423", "0.256", "0.321"],
            ["E3", "0.384", "0.248", "0.368"],
        ],
        widths=[2.4, 3.6, 3.6, 3.6],
        aligns=["l", "r", "r", "r"],
        first_col_bold=True,
        caption="Matriz de transición en 3 pasos.",
    )
    m.p(
        "Si se parte de E1 con certeza, la distribución después de 3 pasos es la primera fila de "
        "P³: **(0.509, 0.248, 0.243)**. Es decir, la probabilidad de seguir en E1 es 50.9 %, la de "
        "estar en E2 es 24.8 % y la de estar en E3 es 24.3 %. A largo plazo, la distribución se "
        "aproxima a (0.45, 0.25, 0.30), independientemente del estado inicial."
    )
    m.table(
        ["Clase", "Estados", "Tipo", "Período"],
        [
            ["Clase 1", "{E1, E2, E3}", "Recurrente", "1"],
        ],
        widths=[3.0, 6.0, 4.0, 3.4],
        aligns=["l", "l", "l", "r"],
        first_col_bold=True,
        caption="Clasificación de estados del ejemplo.",
    )
    m.p(
        "La cadena es **irreducible** (todos los estados se comunican) y **aperiódica** (período 1). "
        "No tiene estados absorbentes. Por eso existe una única distribución estacionaria y la "
        "convergencia no depende del estado inicial."
    )

    m.h2("9.5 Potencia, distribución y estado estable")
    m.table(
        ["Concepto", "Definición", "Cómo leerlo en el informe"],
        [
            ["P^n", "Probabilidad de pasar de i a j en exactamente n pasos.", "Matriz de n × n."],
            ["π^(n)", "Distribución después de n pasos: π^(0) · P^n.", "Tabla Estado / π0 / π0·P^n."],
            ["Estado estable π", "Vector que cumple πP = π y Σπ = 1.", "Tabla Estado / π; debe sumar 1."],
            ["Irreducible", "Todos los estados se comunican entre sí.", "Una sola clase recurrente."],
            ["Período", "Máximo común divisor de los tiempos de retorno.", "Período 1 = aperiódica."],
            ["Absorbente", "Estado del que no se puede salir (p_ii = 1).", "Se lista en «Estados absorbentes»."],
        ],
        widths=[3.4, 7.8, 5.2],
        first_col_bold=True,
        caption="Conceptos que aparecen en el informe de Markov.",
    )
    m.callout(
        "tip",
        "Compruebe siempre dos cosas",
        [
            "Primero, que cada fila de P sume 1. Segundo, que la distribución estacionaria sume 1. "
            "Si alguna suma no coincide, revise la captura de datos antes de interpretar el resultado.",
        ],
    )

    m.h2("9.6 Absorción")
    m.p(
        "Un estado es absorbente si la probabilidad de permanecer en él es 1. Cuando la cadena "
        "tiene estados absorbentes y estados transitorios, la aplicación calcula cuántos pasos se "
        "esperan hasta la absorción y con qué probabilidad se termina en cada estado absorbente."
    )
    m.p(
        "Ejemplo: P = `1 0 0` / `0.2 0.5 0.3` / `0.1 0.2 0.7`. El estado E1 es absorbente; E2 y E3 "
        "son transitorios. Partiendo de E2 se esperan 6.667 pasos hasta la absorción; partiendo de "
        "E3, 7.778 pasos. En ambos casos la probabilidad de absorberse en E1 es 1."
    )
    m.table(
        ["Estado transitorio", "Pasos esperados", "Probabilidad de absorción en E1"],
        [
            ["E2", "6.667", "1.000"],
            ["E3", "7.778", "1.000"],
        ],
        widths=[5.0, 5.0, 6.4],
        aligns=["l", "r", "r"],
        first_col_bold=True,
        caption="Resultados de absorción del ejemplo con un estado absorbente.",
    )

    m.h2("9.7 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«La matriz de transición debe ser cuadrada»", "Se escribieron filas con distinta cantidad de columnas.", "Iguale el número de filas y columnas."],
            ["«La fila N suma X; cada fila debe sumar 1»", "Error de captura o de redondeo.", "Ajuste los valores de esa fila hasta que sumen 1."],
            ["«La fila N contiene una probabilidad negativa»", "Se ingresó un valor negativo.", "Corrija el signo; las probabilidades están entre 0 y 1."],
            ["«La distribución inicial debe tener el mismo tamaño que la matriz»", "La cantidad de valores iniciales no coincide con n.", "Escriba una probabilidad por estado."],
            ["«La distribución inicial debe sumar más que cero»", "Todos los valores iniciales son cero.", "Asigne probabilidad a al menos un estado."],
            ["No aparece estado estacionario único", "La cadena tiene más de una clase recurrente.", "Es normal; interprete cada clase por separado."],
        ],
        widths=[5.8, 5.0, 5.6],
        caption="Errores frecuentes en cadenas de Markov.",
    )

    m.h2("9.8 Ejercicio propuesto")
    m.p(
        "Una máquina puede estar **operativa**, **en mantenimiento** o **averiada**. La matriz de "
        "transición diaria es `0.8 0.15 0.05`, `0.2 0.6 0.2`, `0.1 0.3 0.6`. Calcule la "
        "distribución estacionaria, la probabilidad de estar operativa después de 5 días partiendo "
        "de operativa y clasifique los estados. ¿Qué interpretación operativa tiene el estado "
        "estacionario?"
    )

    # =====================================================================
    # 10. PERT / CPM
    # =====================================================================
    m.h1("10. PERT / CPM")
    m.lead(
        "PERT y CPM son técnicas para planificar y controlar proyectos. La aplicación calcula la "
        "duración esperada de cada actividad, el cronograma más temprano y más tardío, las "
        "holguras, la ruta crítica y la probabilidad de terminar antes de un plazo."
    )
    m.figure(
        assets / "mod_pert.png",
        "Pestaña «PERT / CPM»: actividades con duraciones optimista, probable y pesimista, y plazo objetivo.",
        16.4,
    )

    m.h2("10.1 ¿Qué resuelve?")
    m.p(
        "Dado un conjunto de actividades con duraciones estimadas y predecesores, la aplicación "
        "construye la red, calcula el inicio y fin más temprano (ES, EF), el inicio y fin más "
        "tardío (LS, LF), la holgura y la ruta crítica. Si se indica un plazo T, estima la "
        "probabilidad de cumplirlo mediante una aproximación normal."
    )
    m.p(
        "El módulo sirve tanto para PERT (duraciones probabilísticas con tres estimaciones) como "
        "para CPM (duraciones determinísticas, usando el mismo valor en las tres columnas)."
    )

    m.h2("10.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Actividades", "Una por línea: nombre, optimista, probable, pesimista, predecesores.", "`A, 2, 4, 6, -`"],
            ["Plazo objetivo", "Tiempo T para calcular P(terminar ≤ T). Es opcional.", "`16`"],
            ["Cronograma", "Tabla con te, varianza, ES, EF, LS, LF, holgura y crítica.", "—"],
            ["Ruta crítica", "Secuencia de actividades con holgura cero.", "A → C → D"],
        ],
        widths=[3.6, 9.4, 3.8],
        first_col_bold=True,
        caption="Elementos de la pestaña «PERT / CPM».",
    )
    m.p(
        "El nombre de cada actividad debe ser único. Los predecesores se separan con comas, "
        "punto y coma o espacios. Use `-` o deje vacío el campo cuando la actividad no tenga "
        "predecesores."
    )

    m.h2("10.3 Fórmulas")
    m.code(
        [
            "te = (optimista + 4 · probable + pesimista) / 6",
            "Varianza = ((pesimista - optimista) / 6)²",
            "ES = máximo(EF de los predecesores)",
            "EF = ES + te",
            "LF = mínimo(LS de los sucesores)",
            "LS = LF - te",
            "Holgura = LS - ES = LF - EF",
            "z = (T - duración esperada) / desviación estándar de la ruta crítica",
        ],
        caption="Fórmulas utilizadas por el módulo PERT/CPM.",
    )
    m.p(
        "La varianza de la ruta crítica es la suma de las varianzas de sus actividades. La "
        "desviación estándar es la raíz cuadrada de esa suma. La probabilidad se obtiene con la "
        "función de distribución normal estándar."
    )

    m.h2("10.4 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **PERT / CPM**.",
            "Escriba una actividad por línea con el formato indicado.",
            "Use `-` para las actividades iniciales sin predecesores.",
            "Escriba el plazo objetivo T si desea la probabilidad de cumplimiento; déjelo vacío si no.",
            "Presione **Resolver**.",
            "Revise la duración esperada, la varianza y la ruta crítica.",
            "Lea el cronograma y localice las actividades con holgura cero.",
            "Si indicó T, interprete la probabilidad y el valor z.",
        ]
    )

    m.h2("10.5 Ejemplo guiado")
    m.p("Considere el siguiente proyecto:")
    m.table(
        ["Actividad", "Optimista", "Probable", "Pesimista", "Predecesores"],
        [
            ["A", "2", "4", "6", "—"],
            ["B", "3", "5", "8", "A"],
            ["C", "4", "6", "9", "A"],
            ["D", "2", "3", "5", "B, C"],
        ],
        widths=[2.6, 3.0, 3.0, 3.0, 4.6],
        aligns=["l", "r", "r", "r", "l"],
        first_col_bold=True,
        caption="Actividades y estimaciones del ejemplo PERT.",
    )
    m.code(
        [
            "A, 2, 4, 6, -",
            "B, 3, 5, 8, A",
            "C, 4, 6, 9, A",
            "D, 2, 3, 5, B, C",
            "",
            "Plazo objetivo: 16",
        ],
        caption="Datos del ejemplo PERT.",
    )
    m.p(
        "La duración esperada del proyecto es **13.3333**, la varianza de la ruta crítica es "
        "**1.3889** y la desviación estándar es **1.1785**. La ruta crítica es **A → C → D**."
    )
    m.table(
        ["Act.", "te", "Var.", "ES", "EF", "LS", "LF", "Holgura", "Crítica"],
        [
            ["A", "4.000", "0.4444", "0.000", "4.000", "0.000", "4.000", "0.000", "Sí"],
            ["B", "5.167", "0.6944", "4.000", "9.167", "5.000", "10.167", "1.000", "No"],
            ["C", "6.167", "0.6944", "4.000", "10.167", "4.000", "10.167", "0.000", "Sí"],
            ["D", "3.167", "0.2500", "10.167", "13.333", "10.167", "13.333", "0.000", "Sí"],
        ],
        widths=[1.8, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.2, 1.6],
        aligns=["l"] + ["r"] * 7 + ["l"],
        caption="Cronograma del ejemplo PERT.",
    )
    m.p(
        "La actividad B tiene una holgura de 1.000: puede retrasarse hasta una unidad sin afectar "
        "la duración total, siempre que sus predecesores y sucesores mantengan sus fechas. Las "
        "actividades A, C y D tienen holgura cero y forman la ruta crítica."
    )
    m.p(
        "Con T = 16, la aplicación calcula z = (16 − 13.3333) / 1.1785 = **2.2627** y una "
        "probabilidad **P(T ≤ 16) = 98.82 %**. Es decir, hay aproximadamente 98.8 % de probabilidad "
        "de terminar en 16 unidades de tiempo o antes, bajo el supuesto de independencia de las "
        "duraciones."
    )

    m.h2("10.6 Interpretación del cronograma")
    m.table(
        ["Columna", "Significado", "Cómo usarla"],
        [
            ["te", "Duración esperada de la actividad.", "Planificación de recursos y tiempos."],
            ["Var.", "Varianza de la duración (solo PERT).", "Identifica actividades con mayor incertidumbre."],
            ["ES / EF", "Inicio y fin más tempranos posibles.", "Fecha de inicio del proyecto y compromisos."],
            ["LS / LF", "Inicio y fin más tardíos sin retrasar el proyecto.", "Margen de maniobra."],
            ["Holgura", "Diferencia entre LS y ES.", "Cero = crítica; positiva = puede esperar."],
            ["Crítica", "Indica si la actividad pertenece a la ruta crítica.", "Priorizar el control de estas actividades."],
        ],
        widths=[2.6, 7.0, 6.8],
        first_col_bold=True,
        caption="Interpretación de las columnas del cronograma.",
    )
    m.callout(
        "warning",
        "La probabilidad es una aproximación",
        [
            "El cálculo supone que la duración del proyecto sigue una distribución normal y que las "
            "duraciones de las actividades son independientes. Si la red tiene varias rutas casi "
            "críticas o las duraciones están muy correlacionadas, la probabilidad puede ser una "
            "aproximación optimista. Interprete el valor como una estimación, no como una garantía.",
        ],
    )

    m.h2("10.7 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«Los nombres de las actividades deben ser únicos»", "Dos actividades tienen el mismo nombre.", "Renombre una de ellas."],
            ["«La actividad X tiene un predecesor desconocido»", "El predecesor no existe o está mal escrito.", "Corrija el nombre o agregue la actividad."],
            ["«Hay un ciclo en las dependencias»", "A depende de B y B depende de A.", "Revise la lógica del proyecto."],
            ["«La actividad X tiene duraciones negativas»", "Se ingresó un valor negativo.", "Use duraciones positivas o cero."],
            ["«Debe cumplirse optimista <= probable <= pesimista»", "Las tres estimaciones están fuera de orden.", "Ordene los valores de menor a mayor."],
            ["Probabilidad muy baja", "El plazo T es menor que la duración esperada.", "Es posible; aumente T o revise la estimación."],
        ],
        widths=[5.8, 5.0, 5.6],
        caption="Errores frecuentes en PERT/CPM.",
    )

    m.h2("10.8 Ejercicio propuesto")
    m.p(
        "Un proyecto tiene las actividades A (3, 4, 5), B (2, 3, 4, después de A), C (4, 6, 8, "
        "después de A), D (1, 2, 3, después de B), E (2, 4, 6, después de C) y F (2, 3, 4, después "
        "de D y E). Calcule la duración esperada, la ruta crítica y la probabilidad de terminar en "
        "18 unidades. Identifique qué actividad tiene mayor holgura."
    )

    # =====================================================================
    # 11. INVENTARIOS
    # =====================================================================
    m.h1("11. Modelos de inventario")
    m.lead(
        "Los modelos de inventario responden dos preguntas: cuánto pedir y cada cuánto pedir. La "
        "aplicación incluye el lote económico clásico (EOQ), el EOQ con faltantes y el lote "
        "económico de producción (EPQ)."
    )
    m.figure(
        assets / "mod_inventarios.png",
        "Pestaña «Inventarios»: selección del modelo, parámetros anuales y política óptima.",
        16.4,
    )

    m.h2("11.1 ¿Qué resuelve?")
    m.p(
        "Calcula la cantidad óptima por pedido que minimiza el costo total relevante, compuesto "
        "por el costo de ordenar y el costo de mantener inventario. Cuando el modelo lo permite, "
        "incluye el costo de faltantes; en el EPQ, considera que la producción y el consumo ocurren "
        "simultáneamente."
    )
    m.p(
        "El informe muestra la cantidad óptima, el número de pedidos por año, el tiempo entre "
        "pedidos, el inventario máximo, el faltante máximo y el desglose de costos."
    )

    m.h2("11.2 Elementos de la pantalla")
    m.table(
        ["Elemento", "Descripción", "Ejemplo"],
        [
            ["Modelo", "EOQ básico, EOQ con faltantes o EPQ (producción).", "EOQ básico"],
            ["D", "Demanda anual (unidades por año).", "`1200`"],
            ["S", "Costo de ordenar o preparar un pedido.", "`50`"],
            ["H", "Costo de mantener una unidad en inventario durante un año.", "`2`"],
            ["B", "Costo de faltante por unidad y por año (solo EOQ con faltantes).", "`8`"],
            ["p", "Tasa anual de producción (solo EPQ).", "`2000`"],
        ],
        widths=[2.4, 10.0, 4.0],
        first_col_bold=True,
        caption="Parámetros de la pestaña «Inventarios».",
    )
    m.callout(
        "warning",
        "Use unidades coherentes",
        [
            "D, p y la base de tiempo de H y B deben referirse al mismo periodo. Si D es anual, H "
            "debe ser el costo anual de mantener una unidad. Si H se da por mes, conviértalo a "
            "anual antes de calcular (por ejemplo, multiplique por 12).",
        ],
    )

    m.h2("11.3 Modelos y fórmulas")
    m.table(
        ["Modelo", "Cantidad óptima", "Costo total relevante"],
        [
            ["EOQ básico", "Q* = √(2DS / H)", "CT = DS/Q + HQ/2"],
            ["EOQ con faltantes", "Q* = √(2DS(H + B) / (HB))", "CT = DS/Q + H(Q−F)²/(2Q) + BF²/(2Q)"],
            ["EPQ (producción)", "Q* = √(2DS / [H(1 − D/p)])", "CT = DS/Q + H·inventario_máximo/2"],
        ],
        widths=[4.0, 7.0, 5.4],
        first_col_bold=True,
        caption="Fórmulas de los tres modelos de inventario.",
    )
    m.p(
        "En el EOQ con faltantes, F es el faltante máximo y se calcula como F = QH/(H + B). En el "
        "EPQ, el inventario máximo es Q(1 − D/p), porque parte de la producción se consume mientras "
        "se produce."
    )

    m.h2("11.4 Paso a paso")
    m.steps(
        [
            "Abra la pestaña **Inventarios**.",
            "Seleccione el modelo en la lista desplegable.",
            "Escriba la demanda anual D, el costo de ordenar S y el costo de mantener H.",
            "Si eligió EOQ con faltantes, escriba B. Si eligió EPQ, escriba p.",
            "Presione **Resolver**.",
            "Revise la política óptima: Q*, pedidos por año, tiempo entre pedidos e inventario máximo.",
            "Compare los tres componentes del costo y el costo total relevante.",
            "Guarde el informe si necesita comparar escenarios.",
        ]
    )

    m.h2("11.5 Ejemplo guiado: EOQ básico")
    m.p(
        "Una tienda vende 1200 unidades al año. Cada pedido cuesta 50 y mantener una unidad "
        "durante un año cuesta 2. Con D = 1200, S = 50 y H = 2:"
    )
    m.code(
        [
            "Modelo: EOQ básico",
            "D = 1200",
            "S = 50",
            "H = 2",
        ],
        caption="Datos del ejemplo EOQ básico.",
    )
    m.table(
        ["Concepto", "Fórmula", "Valor"],
        [
            ["Cantidad óptima Q*", "√(2DS/H)", "244.949"],
            ["Pedidos por año", "D/Q*", "4.89898"],
            ["Tiempo entre pedidos", "1/(pedidos por año)", "0.204124 años ≈ 74.5 días"],
            ["Inventario máximo", "Q*", "244.949"],
            ["Costo anual de ordenar", "DS/Q*", "244.949"],
            ["Costo anual de mantener", "HQ*/2", "244.949"],
            ["Costo total relevante", "Suma", "489.898"],
        ],
        widths=[5.0, 6.0, 5.4],
        aligns=["l", "l", "r"],
        first_col_bold=True,
        caption="Política óptima del ejemplo EOQ básico.",
    )
    m.p(
        "En el óptimo, el costo de ordenar y el de mantener son iguales. Esa es una propiedad "
        "característica del EOQ clásico y una forma rápida de comprobar el resultado."
    )

    m.h2("11.6 Ejemplo guiado: EOQ con faltantes")
    m.p(
        "Con los mismos datos y un costo de faltante B = 8, se permite que parte de la demanda "
        "quede pendiente. La aplicación obtiene:"
    )
    m.table(
        ["Concepto", "Valor"],
        [
            ["Cantidad óptima Q*", "273.861"],
            ["Pedidos por año", "4.38178"],
            ["Tiempo entre pedidos", "0.228218 años ≈ 83.3 días"],
            ["Inventario máximo", "219.089"],
            ["Faltante máximo", "54.772"],
            ["Costo de ordenar", "219.089"],
            ["Costo de mantener", "175.271"],
            ["Costo de faltantes", "43.818"],
            ["Costo total relevante", "438.178"],
        ],
        widths=[6.0, 10.4],
        aligns=["l", "r"],
        first_col_bold=True,
        caption="Política óptima del ejemplo EOQ con faltantes (B = 8).",
    )
    m.p(
        "El costo total baja de 489.898 a 438.178 porque el ahorro en mantenimiento compensa el "
        "costo de los faltantes. El lote es mayor, pero parte de él se usa para cubrir la demanda "
        "pendiente. Si B es muy alto, el faltante máximo se reduce y el modelo se aproxima al EOQ "
        "básico."
    )

    m.h2("11.7 Ejemplo guiado: EPQ")
    m.p(
        "Si la empresa produce a una tasa de 2000 unidades al año mientras la demanda es 1200, el "
        "lote económico de producción es:"
    )
    m.table(
        ["Concepto", "Valor"],
        [
            ["Cantidad óptima Q*", "387.298"],
            ["Pedidos (lotes) por año", "3.09839"],
            ["Tiempo entre lotes", "0.322749 años ≈ 117.8 días"],
            ["Inventario máximo", "154.919"],
            ["Costo de ordenar / preparar", "154.919"],
            ["Costo de mantener", "154.919"],
            ["Costo total relevante", "309.839"],
        ],
        widths=[6.0, 10.4],
        aligns=["l", "r"],
        first_col_bold=True,
        caption="Política óptima del ejemplo EPQ (p = 2000).",
    )
    m.p(
        "El EPQ es mayor que el EOQ porque la producción se acumula mientras se consume. El "
        "inventario máximo es menor que el lote, ya que parte de la producción se vende durante "
        "el ciclo. El costo total es el más bajo de los tres ejemplos porque el costo de mantener "
        "se aplica a un inventario promedio menor."
    )

    m.h2("11.8 Interpretación de los costos")
    m.table(
        ["Componente", "Qué mide", "Cómo reducirlo"],
        [
            ["Costo de ordenar", "Trámites, transporte, preparación de la máquina.", "Pedidos más grandes y menos frecuentes."],
            ["Costo de mantener", "Almacenamiento, capital inmovilizado, seguro, obsolescencia.", "Pedidos más pequeños y frecuentes."],
            ["Costo de faltantes", "Pérdida de ventas, penalizaciones, clientes insatisfechos.", "Mayor inventario de seguridad o lotes más grandes."],
            ["Costo total relevante", "Suma de los componentes anteriores.", "Equilibrio en Q*."],
        ],
        widths=[4.0, 7.4, 5.0],
        first_col_bold=True,
        caption="Interpretación de los componentes del costo de inventario.",
    )
    m.callout(
        "tip",
        "Análisis de sensibilidad",
        [
            "Cambie un parámetro a la vez y observe cómo se mueve Q*. Por ejemplo, si duplica la "
            "demanda, Q* aumenta por un factor de √2 ≈ 1.41, no al doble. Esa es una conclusión "
            "útil para explicar el comportamiento del modelo.",
        ],
    )

    m.h2("11.9 Errores comunes")
    m.table(
        ["Mensaje o síntoma", "Causa probable", "Solución"],
        [
            ["«La demanda anual D debe ser mayor que cero»", "D es cero o negativo.", "Escriba una demanda positiva."],
            ["«El costo de ordenar S debe ser mayor que cero»", "S es cero o negativo.", "Use un costo positivo."],
            ["«El costo de mantener H debe ser mayor que cero»", "H es cero o negativo.", "Use un costo positivo; con H = 0 el modelo no tiene solución finita."],
            ["«El costo de faltante B debe ser mayor que cero»", "B es cero o negativo en EOQ con faltantes.", "Use un costo positivo."],
            ["«La tasa de producción p debe ser mayor que la demanda D»", "La producción no cubre la demanda.", "Aumente p o revise D."],
            ["El tiempo entre pedidos parece muy pequeño", "La demanda está en otra unidad de tiempo.", "Revise si D es anual y H es anual."],
        ],
        widths=[6.0, 4.8, 5.6],
        caption="Errores frecuentes en modelos de inventario.",
    )

    m.h2("11.10 Ejercicio propuesto")
    m.p(
        "Una empresa tiene una demanda anual de 5000 unidades, costo de ordenar de 80 y costo de "
        "mantener de 4 por unidad y año. Calcule Q*, el número de pedidos y el costo total. Luego "
        "evalúe un costo de faltante de 10 y una tasa de producción de 8000; compare los tres "
        "escenarios y explique cuál conviene según la política de servicio."
    )
