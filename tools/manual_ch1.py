"""Capítulos 1 a 3 del manual."""

from __future__ import annotations

from pathlib import Path

from manual_style import Manual


def add_chapters(m: Manual, assets: Path) -> None:
    # =====================================================================
    # 1. INTRODUCCIÓN
    # =====================================================================
    m.h1("1. Introducción")
    m.lead(
        "Esta aplicación reúne en un solo lugar las técnicas cuantitativas que se estudian "
        "en un curso típico de Investigación de Operaciones. Su propósito no es solo mostrar "
        "la respuesta final, sino también el desarrollo del algoritmo, las tablas intermedias "
        "y la interpretación de los resultados."
    )

    m.h2("1.1 ¿Qué es la Investigación de Operaciones?")
    m.p(
        "La Investigación de Operaciones (IO) es una disciplina que aplica modelos matemáticos, "
        "estadísticos y algorítmicos para apoyar la toma de decisiones. Se usa cuando hay recursos "
        "limitados —tiempo, dinero, personal, capacidad de producción o transporte— y se necesita "
        "decidir cómo asignarlos de la mejor manera posible."
    )
    m.p(
        "Un estudio de IO suele recorrer cuatro etapas: **formular** el problema, **construir** el "
        "modelo, **resolverlo** e **interpretar** la solución. La aplicación cubre con especial "
        "detalle las dos últimas: resuelve el modelo y presenta los cálculos de forma legible, "
        "pero también ayuda a construir el modelo porque cada pestaña muestra el formato exacto "
        "de los datos que debe introducir."
    )
    m.p("Los modelos incluidos pertenecen a las siguientes familias:")
    m.bullets(
        [
            "**Optimización lineal:** método gráfico y método simplex.",
            "**Optimización de redes y logística:** transporte y asignación.",
            "**Sistemas estocásticos:** teoría de colas y cadenas de Markov.",
            "**Gestión de proyectos:** PERT y CPM.",
            "**Gestión de inventarios:** EOQ, EOQ con faltantes y EPQ.",
        ]
    )

    m.h2("1.2 ¿Qué hace esta aplicación?")
    m.p(
        "La aplicación es una suite de escritorio con ocho módulos de cálculo y una pantalla de "
        "inicio. Cada módulo tiene datos de ejemplo precargados, de modo que puede explorar el "
        "formato y el tipo de resultados antes de introducir su propio problema."
    )
    m.p("Sus características principales son:")
    m.bullets(
        [
            "**Desarrollo visible:** muestra tablas, iteraciones y pasos intermedios, no solo el resultado.",
            "**Ejemplos incluidos:** el botón «Ejemplo» carga un caso resuelto en cada pestaña.",
            "**Validación de datos:** los mensajes explican qué línea o qué valor debe corregirse.",
            "**Resultados exportables:** el botón «Guardar .txt» crea un informe de texto listo para entregar.",
            "**Funcionamiento local:** no requiere internet ni envía datos a ningún servidor.",
            "**Multiplataforma:** se distribuye como aplicación para macOS y como ejecutable para Windows.",
        ]
    )

    m.h2("1.3 Módulos incluidos")
    m.table(
        ["Módulo", "Técnicas", "Resultados principales"],
        [
            ["Método gráfico", "Programación lineal con dos variables", "Región factible, vértices, recta objetivo, solución óptima y gráfico."],
            ["Simplex", "Método de dos fases, restricciones <=, >= e =", "Tablas por iteración, solución óptima, casos especiales."],
            ["Transporte", "Esquina noroeste, costo mínimo, Vogel y MODI", "Asignación de envíos, costo total, potenciales u y v, costos de oportunidad."],
            ["Asignación", "Algoritmo húngaro", "Pareja agente-tarea, costo o beneficio total."],
            ["Colas", "M/M/1, M/M/1/K, M/M/c, M/M/c/K y M/G/1", "ρ, P0, L, Lq, W, Wq, P(espera), rechazo y distribución Pn."],
            ["Markov", "Cadenas finitas de tiempo discreto", "P^n, distribución tras n pasos, estado estable, clases, período y absorción."],
            ["PERT / CPM", "Redes de actividades con duraciones probabilísticas", "Duración esperada, ES/EF/LS/LF, holguras, ruta crítica y probabilidad de cumplir un plazo."],
            ["Inventarios", "EOQ, EOQ con faltantes y EPQ", "Cantidad óptima, pedidos por año, inventario máximo, faltante y costos."],
        ],
        widths=[3.0, 6.2, 7.2],
        caption="Módulos de cálculo incluidos en la aplicación.",
    )

    m.h2("1.4 Requisitos y alcance")
    m.p(
        "La aplicación es autónoma: el paquete incluye todo lo necesario para ejecutarse. No hace "
        "falta instalar Python, Java ni complementos adicionales."
    )
    m.table(
        ["Aspecto", "Requisito"],
        [
            ["Sistema operativo", "macOS 10.15 (Catalina) o superior; Windows 10 u 11 de 64 bits."],
            ["Memoria", "4 GB de RAM recomendados."],
            ["Espacio en disco", "Alrededor de 100 MB para la aplicación y los informes."],
            ["Pantalla", "Resolución mínima de 1080 × 720; se recomienda 1280 × 800 o superior."],
            ["Internet", "No es necesario. Solo se requiere para descargar la aplicación."],
            ["Permisos", "Ninguno especial; los informes se guardan donde el usuario elija."],
        ],
        widths=[4.0, 12.4],
        first_col_bold=True,
        caption="Requisitos mínimos recomendados.",
    )

    m.h2("1.5 Supuestos y limitaciones")
    m.p(
        "Cada técnica trabaja bajo supuestos matemáticos concretos. Conocerlos es parte de una "
        "buena presentación de resultados."
    )
    m.table(
        ["Módulo", "Supuestos y límites que conviene declarar"],
        [
            ["Programación lineal", "Variables continuas y no negativas; función objetivo y restricciones lineales. No resuelve programación entera ni no lineal."],
            ["Método gráfico", "Exactamente dos variables de decisión. Sirve para visualizar, no para problemas de mayor dimensión."],
            ["Transporte", "Costos lineales por unidad, oferta y demanda conocidas. No incluye rutas prohibidas ni transbordo; puede modelar una ruta prohibida con un costo muy alto."],
            ["Asignación", "Cada agente se asigna a una tarea y cada tarea recibe un agente. Las matrices rectangulares se completan con filas o columnas ficticias."],
            ["Colas", "Régimen estacionario. En modelos con cola infinita se exige estabilidad (λ < cμ). Los tiempos se expresan en la misma unidad que λ y μ."],
            ["Markov", "Cadena finita, homogénea y de tiempo discreto. Las filas de la matriz deben sumar 1."],
            ["PERT / CPM", "Duraciones independientes y red sin ciclos. La probabilidad de cumplir el plazo usa una aproximación normal sobre la ruta crítica."],
            ["Inventarios", "Demanda anual constante y conocida, sin descuentos por volumen. El EPQ supone producción y consumo simultáneos."],
        ],
        widths=[3.4, 13.0],
        first_col_bold=True,
        caption="Alcance de cada módulo y supuestos que deben indicarse en un informe.",
    )
    m.callout(
        "warning",
        "Resultados con fines académicos y de apoyo",
        [
            "Las soluciones son exactas dentro del modelo matemático, pero la calidad de una decisión "
            "depende también de la calidad de los datos y de los supuestos. En un trabajo profesional, "
            "contraste los resultados con la realidad operativa y documente las simplificaciones.",
        ],
    )

    # =====================================================================
    # 2. INSTALACIÓN
    # =====================================================================
    m.h1("2. Instalación y puesta en marcha")
    m.lead(
        "La aplicación se distribuye como un paquete comprimido para macOS y como un ejecutable "
        "para Windows. En ambos casos la instalación consiste en descomprimir y ejecutar; no hay "
        "asistentes ni dependencias que instalar."
    )

    m.h2("2.1 Contenido del paquete")
    m.table(
        ["Archivo", "Descripción"],
        [
            ["Investigación de Operaciones By Carlos Pardo (macOS).zip", "Aplicación completa para macOS. Al descomprimir se obtiene un archivo .app."],
            ["Investigación de Operaciones By Carlos Pardo.exe", "Ejecutable autónomo para Windows de 64 bits."],
            ["Manual de Usuario.pdf / .docx", "Este documento, con la guía de todos los módulos."],
            ["README.md", "Resumen técnico, instrucciones de compilación y solución de problemas."],
            ["Código fuente (opcional)", "Carpeta con main.py, ui.py, orlib/ y pruebas automatizadas."],
        ],
        widths=[6.6, 9.8],
        caption="Archivos que puede recibir según la plataforma.",
    )
    m.p(
        "Si recibió un archivo ZIP, **descomprímalo antes de abrir la aplicación**. Ejecutar la "
        "aplicación desde dentro del ZIP puede impedir que el sistema operativo la firme o la "
        "reconozca correctamente."
    )

    m.h2("2.2 Instalación en macOS")
    m.steps(
        [
            "Descargue el archivo `Investigación de Operaciones By Carlos Pardo (macOS).zip`.",
            "Haga doble clic sobre el ZIP para descomprimirlo. Aparecerá el archivo "
            "`Investigación de Operaciones By Carlos Pardo.app`.",
            "Arrastre la aplicación a la carpeta **Aplicaciones** (Applications). También puede "
            "ejecutarla desde la carpeta Descargas.",
            "Haga doble clic en la aplicación. La primera vez, si macOS muestra el aviso "
            "«no se puede abrir porque proviene de un desarrollador no identificado», haga "
            "**clic derecho → Abrir** y confirme con **Abrir**.",
            "Si el aviso persiste, abra **Terminal** y ejecute el comando de la sección 2.5. "
            "Después vuelva a abrir la aplicación.",
        ]
    )
    m.callout(
        "info",
        "¿Por qué aparece el aviso de seguridad?",
        [
            "La aplicación está firmada de forma ad hoc, pero no está notarizada por Apple. macOS "
            "avisa cuando una aplicación no pasó por ese proceso. El aviso no significa que la "
            "aplicación tenga un problema: es una medida de protección del sistema.",
            "Si descargó la aplicación de una fuente confiable (su docente, un compañero o el "
            "repositorio del proyecto), puede abrirla siguiendo los pasos indicados.",
        ],
    )

    m.h2("2.3 Instalación en Windows")
    m.steps(
        [
            "Descomprima el paquete y localice `Investigación de Operaciones By Carlos Pardo.exe`.",
            "Haga doble clic en el ejecutable. No necesita instalador ni permisos de administrador.",
            "Si Windows SmartScreen muestra «Windows protegió su PC», haga clic en "
            "**Más información** y luego en **Ejecutar de todas formas**.",
            "Si el antivirus coloca el archivo en cuarentena, restáurelo y añada una exclusión. "
            "Los ejecutables creados con PyInstaller a veces generan falsos positivos.",
            "Para mayor comodidad, cree un acceso directo en el escritorio o ancle la aplicación "
            "a la barra de tareas.",
        ]
    )
    m.callout(
        "tip",
        "Mantenga el ejecutable en una carpeta propia",
        [
            "Cree una carpeta como `C:\\Program Files\\InvestigacionOperaciones` o "
            "`C:\\Users\\<usuario>\\Aplicaciones\\IO` y guarde allí el .exe. Evite ejecutarlo "
            "desde una carpeta temporal o desde una unidad de red lenta.",
        ],
    )

    m.h2("2.4 Ejecución desde el código fuente")
    m.p(
        "Esta opción es útil para docentes que quieren revisar el código o para estudiantes de "
        "ingeniería que desean modificarlo. Requiere Python 3.10 o superior con Tkinter, que viene "
        "incluido en las instalaciones oficiales de Python en Windows y macOS."
    )
    m.code(
        [
            "cd InvestigacionOperaciones",
            "python3 main.py",
        ],
        caption="Ejecución directa desde la carpeta del proyecto.",
    )
    m.p(
        "La aplicación no usa bibliotecas externas en tiempo de ejecución. Para generar los "
        "ejecutables se necesitan `pyinstaller` y, para este manual, `python-docx` y `pillow`; "
        "esas dependencias solo son necesarias durante la compilación."
    )

    m.h2("2.5 Primer arranque")
    m.p(
        "Al abrir la aplicación verá la pestaña **Inicio**. Desde allí puede leer las convenciones "
        "básicas y elegir el módulo que necesita. Todas las pestañas tienen un ejemplo cargado, "
        "así que la primera pantalla que abra ya mostrará un resultado."
    )
    m.steps(
        [
            "Elija una pestaña según el tipo de problema (por ejemplo, **Simplex** para un modelo "
            "de programación lineal con más de dos variables).",
            "Presione **Ejemplo** para cargar un caso resuelto y observar el formato de los datos.",
            "Sustituya los datos por los de su problema y presione **Resolver**.",
            "Revise el desarrollo y la interpretación; ajuste lo que sea necesario.",
            "Presione **Guardar .txt** para conservar el informe completo.",
        ]
    )
    m.callout(
        "tip",
        "Atajo para resolver",
        [
            "Presione **Cmd + Enter** en macOS o **Ctrl + Enter** en Windows para resolver la "
            "pestaña activa sin usar el ratón. Funciona en todos los módulos.",
        ],
    )

    m.h2("2.6 Atajos y acciones frecuentes")
    m.table(
        ["Acción", "macOS", "Windows"],
        [
            ["Resolver la pestaña activa", "Cmd + Enter", "Ctrl + Enter"],
            ["Moverse entre campos", "Tab / Mayús + Tab", "Tab / Mayús + Tab"],
            ["Copiar texto de resultados", "Seleccionar y Cmd + C", "Seleccionar y Ctrl + C"],
            ["Guardar el informe", "Botón «Guardar .txt»", "Botón «Guardar .txt»"],
            ["Cerrar la aplicación", "Cmd + Q", "Alt + F4"],
        ],
        widths=[6.0, 5.2, 5.2],
        first_col_bold=True,
        caption="Atajos de teclado disponibles.",
    )

    m.h2("2.7 Dónde se guardan los resultados")
    m.p(
        "La aplicación no guarda archivos automáticamente. Al presionar **Guardar .txt** se abre "
        "un diálogo del sistema en el que usted elige la carpeta y el nombre. Cada módulo propone "
        "un nombre distinto:"
    )
    m.table(
        ["Módulo", "Nombre sugerido"],
        [
            ["Método gráfico", "`metodo_grafico.txt`"],
            ["Simplex", "`simplex.txt`"],
            ["Transporte", "`transporte.txt`"],
            ["Asignación", "`asignacion.txt`"],
            ["Colas", "`colas.txt`"],
            ["Markov", "`markov.txt`"],
            ["PERT / CPM", "`pert.txt`"],
            ["Inventarios", "`inventarios.txt`"],
        ],
        widths=[6.0, 10.4],
        first_col_bold=True,
        caption="Nombres de archivo propuestos por cada módulo.",
    )
    m.p(
        "El informe se guarda en texto plano con codificación UTF-8, por lo que puede abrirse con "
        "el Bloc de notas, TextEdit, VS Code o cualquier procesador de textos. Para incluir las "
        "tablas en un trabajo, copie el texto y use una fuente monoespaciada como Consolas, "
        "Menlo o Courier New."
    )

    m.h2("2.8 Desinstalación")
    m.p(
        "La aplicación no crea entradas en el registro ni deja servicios en segundo plano. Para "
        "desinstalarla, arrastre la aplicación a la Papelera en macOS o elimine el .exe en Windows. "
        "Los informes que haya guardado permanecen donde usted los haya dejado."
    )

    # =====================================================================
    # 3. INTERFAZ
    # =====================================================================
    m.h1("3. Conocimientos básicos de la interfaz")
    m.lead(
        "Todas las pestañas comparten la misma estructura: los datos se introducen a la izquierda "
        "y los resultados aparecen a la derecha. Aprender esta organización permite moverse entre "
        "módulos sin volver a empezar."
    )

    m.figure(
        assets / "interfaz_general.png",
        "Anatomía de la ventana principal: pestañas, panel de datos, botones de acción y panel de resultados.",
        16.4,
    )

    m.h2("3.1 Estructura de la ventana")
    m.p("La ventana se divide en cinco zonas:")
    m.table(
        ["Zona", "Contenido", "Para qué sirve"],
        [
            ["Barra de título", "Nombre de la aplicación y del módulo.", "Identificar la ventana y cambiar entre aplicaciones."],
            ["Pestañas", "Inicio, Método gráfico, Simplex, Transporte, Asignación, Colas, Markov, PERT / CPM, Inventarios.", "Elegir el tipo de problema."],
            ["Panel izquierdo", "Campos, matrices, listas y opciones del módulo.", "Introducir y revisar los datos."],
            ["Panel derecho", "Resultados, tablas y desarrollo del algoritmo.", "Leer, copiar e interpretar la solución."],
            ["Barra inferior", "Atajo de teclado y autor.", "Recordar cómo resolver y ver el estado de la aplicación."],
        ],
        widths=[3.2, 7.6, 5.6],
        first_col_bold=True,
        caption="Zonas de la ventana principal y su función.",
    )

    m.h2("3.2 Pestañas")
    m.table(
        ["Pestaña", "Cuándo usarla", "Capítulo"],
        [
            ["Inicio", "Para leer las instrucciones y ver el mapa de módulos.", "3"],
            ["Método gráfico", "Modelos lineales con exactamente dos variables y deseo de ver la región factible.", "4"],
            ["Simplex", "Modelos lineales con cualquier número de variables y restricciones <=, >= o =.", "5"],
            ["Transporte", "Distribuir productos desde varios orígenes hacia varios destinos.", "6"],
            ["Asignación", "Asignar agentes a tareas uno a uno (personas, máquinas, proyectos).", "7"],
            ["Colas", "Analizar tiempos de espera, utilización y capacidad de servicio.", "8"],
            ["Markov", "Modelar transiciones entre estados y estudiar su comportamiento a largo plazo.", "9"],
            ["PERT / CPM", "Planificar proyectos con actividades, predecesores y duraciones.", "10"],
            ["Inventarios", "Decidir cuánto pedir y cuándo pedir para minimizar costos.", "11"],
        ],
        widths=[3.3, 10.4, 2.7],
        first_col_bold=True,
        caption="Guía rápida para elegir la pestaña adecuada.",
    )

    m.h2("3.3 Panel de datos")
    m.p(
        "El panel izquierdo contiene los campos del módulo. Los controles más frecuentes son:"
    )
    m.bullets(
        [
            "**Campos de texto:** aceptan números, matrices o listas. El formato se indica justo encima del campo.",
            "**Listas desplegables:** seleccionan el modelo o el método (por ejemplo, M/M/1 o Vogel).",
            "**Casillas de verificación:** activan variantes como maximizar ganancia o maximizar beneficio.",
            "**Botones de opción:** eligen entre maximizar y minimizar.",
            "**Áreas de texto:** permiten escribir varias líneas, una por restricción, fila o actividad.",
        ]
    )
    m.p(
        "Los campos que no aplican al modelo seleccionado se deshabilitan automáticamente. Por "
        "ejemplo, en **Colas**, el campo σ solo se activa para M/G/1, y el campo K solo para los "
        "modelos con capacidad finita."
    )

    m.h2("3.4 Panel de resultados")
    m.p(
        "El panel derecho muestra el informe completo. Los encabezados de sección aparecen en azul, "
        "los resultados exitosos en verde, las advertencias en ámbar y los errores en rojo. El texto "
        "es seleccionable y se puede copiar con Cmd + C o Ctrl + C."
    )
    m.table(
        ["Color / símbolo", "Significado"],
        [
            ["Azul con encabezado (§)", "Sección del informe: resultado, desarrollo, tablas, fórmulas."],
            ["Verde con «+»", "Resultado correcto o condición verificada."],
            ["Ámbar con «*»", "Advertencia: supuesto, dato ficticio o caso especial."],
            ["Rojo con «!»", "Error de datos o imposibilidad del modelo."],
            ["Texto normal", "Cálculos, tablas y explicaciones."],
        ],
        widths=[5.0, 11.4],
        caption="Códigos visuales del panel de resultados.",
    )
    m.p(
        "El botón **Guardar .txt** copia exactamente el contenido visible, incluyendo encabezados "
        "y tablas. Si desea solo una parte, selecciónela y cópiela antes de guardar."
    )

    m.h2("3.5 Botones de acción")
    m.table(
        ["Botón", "Acción", "Qué esperar"],
        [
            ["Resolver", "Valida los datos, ejecuta el algoritmo y actualiza los resultados.", "Si hay un error, aparece un cuadro de diálogo con la causa."],
            ["Ejemplo", "Restaura los datos del caso de demostración del módulo.", "Borra lo que haya escrito y resuelve el ejemplo automáticamente."],
            ["Limpiar", "Vacía los campos del módulo.", "No borra los resultados de otros módulos."],
            ["Guardar .txt", "Abre el diálogo para guardar el informe.", "El archivo se crea con codificación UTF-8."],
        ],
        widths=[2.8, 7.0, 6.6],
        first_col_bold=True,
        caption="Acciones disponibles en todos los módulos.",
    )
    m.callout(
        "warning",
        "«Ejemplo» y «Limpiar» sustituyen los datos actuales",
        [
            "Si escribió un problema y presiona **Ejemplo**, los datos se reemplazan por los del "
            "caso demostrativo. Guarde el informe antes si necesita conservar el resultado. "
            "La aplicación no pregunta si desea descartar los cambios.",
        ],
    )

    m.h2("3.6 Convenciones para introducir datos")
    m.p(
        "La mayoría de los errores de captura se evitan respetando estas reglas:"
    )
    m.table(
        ["Tipo de dato", "Formato", "Ejemplo"],
        [
            ["Número decimal", "Punto como separador decimal, sin separador de miles.", "`2.5`   ·   `0.075`   ·   `-3`"],
            ["Lista de números", "Separados por espacios, comas o punto y coma.", "`3 5`   ·   `2, 4, 6`"],
            ["Matriz", "Una fila por línea; todas con la misma cantidad de columnas.", "`8 6 10`\n`9 12 13`"],
            ["Restricción lineal", "Coeficientes, operador y valor.", "`3 2 <= 18`"],
            ["Actividad PERT", "Nombre, optimista, probable, pesimista, predecesores.", "`A, 2, 4, 6, -`"],
            ["Comentario", "Todo lo que sigue a # se ignora.", "`3 2 <= 18   # horas`"],
            ["Línea en blanco", "Se ignora.", "—"],
        ],
        widths=[3.8, 7.2, 5.4],
        first_col_bold=True,
        caption="Formatos aceptados por los analizadores de datos.",
    )
    m.callout(
        "danger",
        "No use la coma como separador decimal",
        [
            "La aplicación interpreta la coma como separador entre valores. Si escribe `2,5` "
            "obtendrá dos números (2 y 5), no el número 2.5. Escriba siempre `2.5`.",
            "Tampoco use separadores de miles: `1,200` se interpreta como dos valores. Escriba `1200`.",
        ],
    )
    m.p(
        "Los operadores `<=`, `>=` e `=` son los recomendados. También se aceptan los símbolos "
        "`≤` y `≥` si los copia de un documento. En las restricciones no se permiten productos "
        "entre variables ni expresiones no lineales."
    )

    m.h2("3.7 Flujo de trabajo recomendado")
    m.figure(
        assets / "flujo_trabajo.png",
        "Flujo recomendado: elegir el módulo, cargar o escribir los datos, resolver y analizar el informe.",
        16.4,
    )
    m.p(
        "El flujo se puede repetir tantas veces como sea necesario. Los datos de cada pestaña se "
        "conservan mientras la aplicación permanece abierta, así que puede comparar escenarios "
        "sin volver a escribirlos."
    )

    m.h2("3.8 Qué ocurre al presionar «Resolver»")
    m.steps(
        [
            "**Lectura:** la aplicación interpreta los campos según el formato del módulo. Los "
            "comentarios y las líneas vacías se descartan.",
            "**Validación:** se comprueba que las dimensiones coincidan, que no haya valores "
            "negativos donde no se permiten y que el modelo sea estable.",
            "**Cálculo:** se ejecuta el algoritmo correspondiente.",
            "**Presentación:** se genera el informe con encabezados, tablas y explicaciones.",
            "**Error:** si algo falla, se muestra un cuadro de diálogo con el mensaje y no se "
            "modifica el resultado anterior.",
        ]
    )
    m.p(
        "Si el resultado anterior era de otro conjunto de datos, el panel conserva lo último que "
        "se calculó correctamente hasta que la nueva ejecución termina. Esto evita perder trabajo "
        "por un error de captura."
    )
