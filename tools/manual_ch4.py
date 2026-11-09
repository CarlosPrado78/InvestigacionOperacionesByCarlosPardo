"""Capítulos 12 y 13, y apéndices del manual."""

from __future__ import annotations

from pathlib import Path

from manual_style import MUTED, Manual


def add_chapters(m: Manual, assets: Path) -> None:
    # =====================================================================
    # 12. FLUJO DE TRABAJO
    # =====================================================================
    m.h1("12. Flujo de trabajo y buenas prácticas")
    m.lead(
        "Resolver el modelo es solo una parte del trabajo. Un informe de Investigación de "
        "Operaciones convincente explica el problema, justifica el modelo, presenta la solución y "
        "la interpreta en el contexto de la decisión. Este capítulo reúne recomendaciones para "
        "lograrlo."
    )

    m.h2("12.1 Del enunciado al modelo")
    m.p(
        "El primer paso es traducir el texto del problema a variables, objetivo y restricciones. "
        "Estas palabras suelen indicar la estructura del modelo:"
    )
    m.table(
        ["Expresión del enunciado", "Elemento del modelo", "Ejemplo"],
        [
            ["«maximizar», «mayor ganancia», «máximo beneficio»", "Función objetivo de maximización", "Max Z = 3x1 + 5x2"],
            ["«minimizar», «menor costo», «menor tiempo»", "Función objetivo de minimización", "Min C = 4x1 + 2x2"],
            ["«como máximo», «no más de», «disponible»", "Restricción <= (recurso limitado)", "x1 + 2x2 <= 10"],
            ["«al menos», «como mínimo», «debe cubrir»", "Restricción >= (requerimiento)", "x1 + x2 >= 8"],
            ["«exactamente», «debe ser igual»", "Restricción =", "x1 + x2 = 5"],
            ["«por unidad», «por hora», «por tonelada»", "Coeficiente unitario", "3 horas por unidad"],
            ["«cada agente debe…», «una tarea por persona»", "Asignación uno a uno", "Matriz de asignación"],
            ["«llegan… por hora», «se atienden… por hora»", "Tasas λ y μ de colas", "λ = 12, μ = 15"],
        ],
        widths=[6.2, 5.6, 4.6],
        caption="Palabras clave del enunciado y su traducción al modelo.",
    )
    m.p("Antes de abrir la aplicación, responda por escrito:")
    m.bullets(
        [
            "¿Cuáles son las variables de decisión y en qué unidades se expresan?",
            "¿Qué se quiere maximizar o minimizar?",
            "¿Qué recursos o requisitos generan restricciones?",
            "¿Los datos son determinísticos o probabilísticos?",
            "¿Qué supuestos simplifican el problema y deben declararse?",
        ]
    )

    m.h2("12.2 Lista de verificación antes de resolver")
    m.table(
        ["Verificación", "Sí / No"],
        [
            ["Los datos están en las mismas unidades (horas, días, pesos, unidades).", "☐"],
            ["No se usaron comas como separador decimal.", "☐"],
            ["Todas las filas de una matriz tienen la misma cantidad de columnas.", "☐"],
            ["La cantidad de ofertas coincide con las filas y la de demandas con las columnas.", "☐"],
            ["Las restricciones usan <=, >= o = correctamente.", "☐"],
            ["Las variables son no negativas y el modelo lo refleja.", "☐"],
            ["En colas, λ y μ están en la misma base de tiempo y el sistema es estable.", "☐"],
            ["En Markov, cada fila de P suma 1.", "☐"],
            ["En PERT, cada predecesor existe y no hay ciclos.", "☐"],
            ["En inventarios, D, S, H y B son anuales y positivos.", "☐"],
            ["Se eligió el módulo adecuado para el tipo de problema.", "☐"],
            ["Se guardó una copia del informe antes de cambiar los datos.", "☐"],
        ],
        widths=[15.0, 1.4],
        aligns=["l", "c"],
        caption="Lista de verificación rápida antes de presionar «Resolver».",
    )

    m.h2("12.3 Estructura recomendada de un informe")
    m.p("Un informe claro suele contener estas secciones:")
    m.steps(
        [
            "**Título y datos generales:** nombre del trabajo, autor, curso, fecha y versión de la aplicación.",
            "**Planteamiento del problema:** contexto, decisión que se debe tomar y objetivos.",
            "**Variables y modelo:** definición de variables, función objetivo, restricciones y supuestos.",
            "**Datos y fuentes:** de dónde provienen los números y qué unidades tienen.",
            "**Solución:** resultado óptimo, tablas principales y una captura o descripción del desarrollo.",
            "**Interpretación:** qué significa la solución en el contexto real, no solo el valor numérico.",
            "**Análisis de sensibilidad:** qué cambia si varía un parámetro o una restricción.",
            "**Conclusiones y recomendaciones:** decisión propuesta y limitaciones.",
            "**Anexos:** informes .txt completos, tablas auxiliares y cálculos adicionales.",
        ]
    )
    m.callout(
        "tip",
        "El valor de una solución está en su interpretación",
        [
            "Un informe que solo dice «Z = 36» es incompleto. Explique qué representan x1 y x2, qué "
            "restricciones están activas, qué recursos sobran y qué decisión se recomienda. Si el "
            "modelo es académico, indique los supuestos y las limitaciones.",
        ],
    )

    m.h2("12.4 Cómo comparar escenarios")
    m.p(
        "La comparación de escenarios es una de las aplicaciones más útiles de la suite. Para que "
        "sea válida, cambie **un parámetro a la vez** y registre los resultados en una tabla."
    )
    m.table(
        ["Escenario", "Cambio", "Resultado que debe registrar"],
        [
            ["Base", "Datos originales", "Solución óptima, Z y holguras."],
            ["Demanda +10 %", "Multiplicar la demanda por 1.10", "Nuevo costo, pedidos por año, Q*."],
            ["Capacidad +1", "Aumentar una unidad un recurso", "Nuevo Z y variables activas."],
            ["Tasa de llegada +20 %", "Aumentar λ en colas", "ρ, Lq, Wq, P(espera)."],
            ["Plazo más exigente", "Reducir T en PERT", "Probabilidad de cumplimiento."],
        ],
        widths=[3.8, 6.0, 6.6],
        first_col_bold=True,
        caption="Plantilla para un análisis de escenarios.",
    )
    m.p(
        "Guarde cada escenario con un nombre distinto (por ejemplo, `simplex_base.txt`, "
        "`simplex_capacidad_mas_1.txt`) y conserve una tabla resumen en su documento principal."
    )

    m.h2("12.5 Organización de archivos")
    m.p("Una estructura simple evita pérdidas de información:")
    m.code(
        [
            "Trabajo_IO/",
            "├── 01_enunciado/",
            "├── 02_datos/",
            "├── 03_informes/",
            "│   ├── metodo_grafico.txt",
            "│   ├── simplex.txt",
            "│   └── transporte.txt",
            "├── 04_escenarios/",
            "└── 05_presentacion/",
        ],
        caption="Estructura sugerida para organizar un trabajo.",
    )
    m.bullets(
        [
            "Use nombres descriptivos y sin caracteres especiales problemáticos.",
            "Conserve el archivo .txt original: es la evidencia del cálculo.",
            "No sobrescriba el informe base; cree una copia para cada escenario.",
            "Incluya en el informe la fecha y la versión de la aplicación.",
        ]
    )

    m.h2("12.6 Uso académico y ética")
    m.p(
        "La aplicación es una herramienta de cálculo y aprendizaje. Para usarla correctamente en "
        "un trabajo académico:"
    )
    m.bullets(
        [
            "**Cite la herramienta** si las normas de su curso lo requieren: «Cálculos realizados con "
            "Investigación de Operaciones By Carlos Pardo, versión 1.0».",
            "**Presente el desarrollo**, no solo el resultado. Incluya las tablas o el informe .txt.",
            "**Explique los supuestos** y las limitaciones del modelo.",
            "**Verifique** al menos un resultado con un cálculo manual o con otro método.",
            "**No presente datos inventados** como si fueran reales; indique la fuente o el carácter ilustrativo.",
        ]
    )
    m.callout(
        "warning",
        "La responsabilidad de la decisión es humana",
        [
            "La aplicación no conoce el contexto, la calidad de los datos ni las restricciones "
            "políticas u operativas que no se modelaron. Use los resultados como insumo para "
            "decidir, no como una respuesta automática.",
        ],
    )

    # =====================================================================
    # 13. SOLUCIÓN DE PROBLEMAS
    # =====================================================================
    m.h1("13. Solución de problemas y preguntas frecuentes")
    m.lead(
        "Esta sección reúne los inconvenientes más comunes al instalar, abrir o usar la aplicación, "
        "y explica cómo interpretar los mensajes de error. Si el problema persiste, al final se "
        "indica qué información conviene recopilar para reportarlo."
    )

    m.h2("13.1 La aplicación no abre en macOS")
    m.steps(
        [
            "Confirme que está ejecutando la aplicación desde una carpeta local, no desde el ZIP ni "
            "desde una unidad de red.",
            "Haga **clic derecho → Abrir** sobre el archivo .app y confirme **Abrir**.",
            "Abra **Terminal** y quite el atributo de cuarentena: `xattr -dr com.apple.quarantine "
            "\"/ruta/Investigación de Operaciones By Carlos Pardo.app\"`.",
            "Verifique la firma con `codesign --verify --deep --strict \"/ruta/App.app\"`. Si falla, "
            "vuelva a descomprimir el ZIP original.",
            "Si su Mac tiene un procesador distinto al del paquete, solicite la compilación "
            "correspondiente (Intel o Apple Silicon).",
            "Reinicie el Finder o el equipo si el icono aparece bloqueado.",
        ]
    )
    m.callout(
        "warning",
        "No mueva archivos dentro del paquete .app",
        [
            "El archivo .app es un paquete: si mueve archivos internos o lo edita con el Finder, la "
            "firma se rompe y macOS puede impedir su ejecución. Para cambiar el nombre visible, "
            "use el Finder sobre el paquete completo, no sobre su contenido.",
        ],
    )

    m.h2("13.2 La aplicación no abre en Windows")
    m.table(
        ["Síntoma", "Causa probable", "Solución"],
        [
            ["SmartScreen bloquea el inicio", "Ejecutable sin firma comercial.", "Más información → Ejecutar de todas formas."],
            ["El antivirus lo pone en cuarentena", "Falso positivo de PyInstaller.", "Restaure el archivo y añada una exclusión."],
            ["Error «no es una aplicación Win32 válida»", "Paquete de 32 bits en un sistema de 64 bits o descarga corrupta.", "Descargue de nuevo el .exe de 64 bits."],
            ["Se abre una ventana negra y se cierra", "Falta una biblioteca del sistema o el archivo está dañado.", "Vuelva a descargar; ejecute desde una carpeta local."],
            ["Windows Defender elimina el archivo", "Heurística de detección.", "Restaure y excluya la carpeta de la aplicación."],
        ],
        widths=[5.4, 5.4, 5.6],
        caption="Problemas de inicio en Windows.",
    )

    m.h2("13.3 Errores de datos")
    m.p(
        "La mayoría de los mensajes de error indican la línea o el campo que debe corregirse. "
        "Esta tabla resume los más frecuentes:"
    )
    m.table(
        ["Mensaje", "Módulo", "Qué hacer"],
        [
            ["«No se pudo interpretar un número»", "Todos", "Revise la línea indicada; use punto decimal y elimine letras o símbolos."],
            ["«Todas las filas… deben tener la misma cantidad de columnas»", "Matrices", "Cuente las columnas de la primera fila y complete las demás."],
            ["«Debe ingresar al menos una restricción»", "Gráfico / Simplex", "Escriba al menos una línea con coeficientes, operador y valor."],
            ["«Se esperaban N coeficientes, un operador y el valor»", "Simplex", "Ajuste la cantidad de coeficientes al número de variables."],
            ["«Operador no válido»", "Gráfico / Simplex", "Use <=, >= o =."],
            ["«La oferta debe tener un valor por cada fila»", "Transporte", "Escriba una oferta por fila."],
            ["«La demanda debe tener un valor por cada columna»", "Transporte", "Escriba una demanda por columna."],
            ["«La fila N suma X; cada fila debe sumar 1»", "Markov", "Ajuste las probabilidades de esa fila."],
            ["«La distribución inicial debe tener el mismo tamaño»", "Markov", "Escriba una probabilidad por estado."],
            ["«La actividad X tiene un predecesor desconocido»", "PERT", "Corrija el nombre o agregue la actividad que falta."],
            ["«Hay un ciclo en las dependencias»", "PERT", "Revise el orden lógico de las actividades."],
            ["«La tasa de producción p debe ser mayor que la demanda D»", "Inventarios", "Corrija p o D; el EPQ requiere p > D."],
        ],
        widths=[7.0, 3.4, 6.0],
        caption="Mensajes de error más frecuentes y su solución.",
    )

    m.h2("13.4 El resultado no es el esperado")
    m.table(
        ["Situación", "Posibles causas", "Cómo verificar"],
        [
            ["Z es distinto al cálculo manual", "Coeficiente mal escrito, variable omitida o coma decimal.", "Sustituya la solución en el modelo original."],
            ["El modelo resulta infactible", "Restricciones contradictorias o desigualdades invertidas.", "Grafique las restricciones o pruebe con un subconjunto."],
            ["El modelo resulta no acotado", "Falta una restricción o el sentido de optimización es incorrecto.", "Revise si todas las variables tienen límites."],
            ["La cola da valores negativos o infinitos", "λ ≥ cμ en un modelo infinito.", "Aumente la capacidad de servicio o reduzca la llegada."],
            ["Markov no converge", "Más de una clase recurrente o cadena periódica.", "Revise la estructura de la matriz y las clases."],
            ["PERT da una probabilidad muy baja", "El plazo T es menor que la duración esperada.", "Aumente T o revise las estimaciones."],
            ["El EOQ parece muy grande", "D y H están en unidades de tiempo distintas.", "Convierta ambos a la misma base."],
        ],
        widths=[4.6, 6.4, 5.4],
        caption="Diagnóstico de resultados inesperados.",
    )

    m.h2("13.5 Problemas de visualización")
    m.table(
        ["Síntoma", "Causa", "Solución"],
        [
            ["El gráfico no se dibuja", "La ventana es muy pequeña o el modelo no se ha resuelto.", "Amplíe la ventana y presione Resolver."],
            ["Las tablas se ven cortadas", "El panel de resultados tiene desplazamiento horizontal.", "Use la barra inferior o amplíe la ventana."],
            ["Las letras se ven pequeñas", "Resolución alta con escalado del sistema.", "Ajuste el zoom del sistema o maximice la ventana."],
            ["El texto no se copia", "Se intentó copiar desde un campo deshabilitado.", "Seleccione el texto del panel de resultados."],
        ],
        widths=[5.0, 5.8, 5.6],
        caption="Problemas de visualización y su solución.",
    )

    m.h2("13.6 Preguntas frecuentes")
    m.table(
        ["Pregunta", "Respuesta"],
        [
            ["¿Necesito internet para usarla?", "No. La aplicación funciona completamente sin conexión y no envía datos."],
            ["¿Puedo usarla en Linux?", "El código fuente es compatible con Python y Tkinter, pero no se distribuye un paquete oficial para Linux."],
            ["¿Dónde se guardan mis datos?", "Solo en la memoria mientras la aplicación está abierta. Los informes se guardan únicamente cuando usted presiona «Guardar .txt»."],
            ["¿Puedo resolver variables enteras?", "No. Los módulos de programación lineal trabajan con variables continuas. No hay programación entera."],
            ["¿Por qué el método gráfico solo acepta dos variables?", "Porque representa el problema en el plano. Para más variables use Simplex."],
            ["¿Los resultados se redondean?", "Se muestran con hasta seis decimales; los cálculos internos usan precisión de punto flotante."],
            ["¿Puedo cambiar el idioma?", "La interfaz y los informes están en español."],
            ["¿Cómo actualizo la aplicación?", "Reemplace el archivo .app o .exe por la versión nueva. No hay instalador ni migración de datos."],
            ["¿Puedo incluir los resultados en un trabajo?", "Sí. Guarde el .txt, inclúyalo como anexo y cite la herramienta si corresponde."],
            ["¿Por qué la app pide confirmación de seguridad?", "Porque no está notarizada por Apple ni firmada con un certificado comercial. Es normal en aplicaciones académicas."],
            ["¿Qué hago si se cierra inesperadamente?", "Guarde su trabajo con frecuencia, anote los datos y el mensaje, y reporte el problema con la información de la sección 13.7."],
        ],
        widths=[5.8, 10.6],
        first_col_bold=True,
        caption="Preguntas frecuentes sobre la aplicación.",
    )

    m.h2("13.7 Cómo reportar un problema")
    m.p("Si necesita ayuda, recopile esta información antes de escribir:")
    m.bullets(
        [
            "Sistema operativo y versión (por ejemplo, macOS 15.1 o Windows 11 23H2).",
            "Modelo de computador y tipo de procesador (Intel, Apple Silicon, AMD).",
            "Versión de la aplicación (1.0) y si es el paquete de macOS o el .exe de Windows.",
            "Módulo y pestaña donde ocurrió el problema.",
            "Datos exactos que introdujo (puede adjuntar el informe .txt o una captura).",
            "Mensaje de error completo, si aparece.",
            "Pasos que reprodujeron el problema.",
        ]
    )
    m.callout(
        "tip",
        "Adjunte el informe",
        [
            "Si el problema ocurre después de resolver, adjunte el archivo .txt generado con "
            "«Guardar .txt». Contiene los datos y los resultados, y permite reproducir el caso "
            "con exactitud.",
        ],
    )

    # =====================================================================
    # APÉNDICES
    # =====================================================================
    m.h1("Apéndice A. Formatos de entrada")
    m.lead(
        "Esta hoja de referencia resume el formato exacto de los datos de cada módulo. Puede "
        "imprimirla y tenerla junto al computador."
    )
    m.table(
        ["Módulo", "Campo", "Formato", "Ejemplo"],
        [
            ["Método gráfico", "Función objetivo", "Dos coeficientes separados", "`3 5`"],
            ["Método gráfico", "Restricciones", "a1 a2 operador valor", "`3 2 <= 18`"],
            ["Simplex", "Función objetivo", "n coeficientes", "`3 5`"],
            ["Simplex", "Restricciones", "n coeficientes, operador, valor", "`1 0 <= 4`"],
            ["Transporte", "Costos", "Una fila por origen", "`8 6 10 9`"],
            ["Transporte", "Oferta / demanda", "Listas separadas por espacios", "`35 50 40`"],
            ["Transporte", "Nombres", "Separados por comas", "`Planta 1, Planta 2`"],
            ["Asignación", "Matriz", "Filas = agentes", "`9 2 7 8`"],
            ["Colas", "λ, μ, c, K, σ", "Números; c y K enteros", "`2` · `3` · `2`"],
            ["Markov", "Matriz P", "Filas que suman 1", "`0.7 0.2 0.1`"],
            ["Markov", "Distribución inicial", "n probabilidades", "`1 0 0`"],
            ["Markov", "Pasos", "Entero ≥ 0", "`3`"],
            ["PERT / CPM", "Actividad", "Nombre, opt., prob., pes., predecesores", "`A, 2, 4, 6, -`"],
            ["Inventarios", "Parámetros", "Números positivos", "`1200` · `50` · `2`"],
        ],
        widths=[3.0, 4.0, 5.6, 3.8],
        caption="Resumen de formatos de entrada por módulo.",
    )
    m.callout(
        "tip",
        "Regla de oro",
        [
            "Si un campo admite varios valores, sepárelos con espacios. Si admite varias líneas, "
            "use una línea por fila, restricción o actividad. Nunca use comas como separador decimal.",
        ],
    )

    m.h1("Apéndice B. Glosario")
    m.lead(
        "Términos que aparecen en los informes y en la teoría. La definición está orientada al uso "
        "práctico dentro de la aplicación."
    )
    m.table(
        ["Término", "Definición"],
        [
            ["Actividad", "Tarea de un proyecto con duración y predecesores. En PERT se identifica con un nombre único."],
            ["Aperiódica", "Cadena de Markov cuyo período es 1; no tiene ciclos obligatorios."],
            ["Asignación", "Problema de parear agentes con tareas uno a uno al mínimo costo o máximo beneficio."],
            ["Costo de oportunidad (Δ)", "En transporte, diferencia entre el costo real de una celda y el costo implícito u + v. Si es negativa, conviene mejorar."],
            ["Costo de mantener (H)", "Costo anual de conservar una unidad en inventario."],
            ["Costo de ordenar (S)", "Costo fijo de emitir y recibir un pedido."],
            ["CPM", "Método de ruta crítica con duraciones determinísticas."],
            ["Degeneración", "Situación en la que una solución básica tiene menos celdas positivas de las necesarias; se completa con ceros."],
            ["EOQ", "Cantidad económica de pedido que minimiza el costo total de ordenar y mantener."],
            ["EPQ", "Cantidad económica de producción; considera producción y consumo simultáneos."],
            ["ES / EF", "Inicio y fin más tempranos de una actividad."],
            ["Estado absorbente", "Estado del que la cadena no puede salir; su probabilidad de permanencia es 1."],
            ["Estado estacionario", "Distribución de probabilidad que no cambia al aplicar la matriz de transición."],
            ["Función objetivo", "Expresión que se maximiza o minimiza en un modelo de optimización."],
            ["Holgura", "Margen de retraso de una actividad sin afectar la duración del proyecto: LS − ES."],
            ["Infactible", "Modelo sin ninguna solución que cumpla todas las restricciones."],
            ["Irreducible", "Cadena en la que todos los estados se comunican entre sí."],
            ["L, Lq", "Número esperado de clientes en el sistema y en la cola, respectivamente."],
            ["λ (lambda)", "Tasa media de llegadas por unidad de tiempo."],
            ["LS / LF", "Inicio y fin más tardíos de una actividad sin retrasar el proyecto."],
            ["Matriz de transición (P)", "Matriz cuyas entradas p_ij son las probabilidades de pasar del estado i al j."],
            ["MODI", "Método de optimización del transporte basado en potenciales u y v."],
            ["No acotado", "Modelo en el que la función objetivo puede mejorar indefinidamente."],
            ["Óptimo alternativo", "Más de una solución con el mismo valor óptimo."],
            ["P0", "Probabilidad de que el sistema de colas esté vacío."],
            ["PERT", "Técnica de evaluación y revisión de proyectos con duraciones probabilísticas."],
            ["Período", "Máximo común divisor de los tiempos de retorno a un estado."],
            ["ρ (rho)", "Utilización del sistema: λ/(cμ) en colas."],
            ["Recesivo", "Sinónimo de transitorio: estado del que se puede salir y no se regresa con probabilidad 1."],
            ["Recurrente", "Estado al que se regresa con probabilidad 1."],
            ["Ruta crítica", "Secuencia de actividades con holgura cero que determina la duración del proyecto."],
            ["Simplex", "Algoritmo iterativo para resolver programación lineal."],
            ["Transporte", "Modelo de distribución desde orígenes a destinos al mínimo costo."],
            ["Variable artificial", "Variable auxiliar que permite iniciar el simplex cuando no hay base factible evidente."],
            ["Variable de holgura", "Variable que mide el recurso no utilizado en una restricción <=."],
            ["Variable de exceso", "Variable que mide el exceso sobre el mínimo en una restricción >=."],
            ["W, Wq", "Tiempo esperado en el sistema y en la cola."],
        ],
        widths=[4.4, 12.0],
        first_col_bold=True,
        caption="Glosario de términos usados en la aplicación.",
    )

    m.h1("Apéndice C. Fórmulas de referencia")
    m.lead(
        "Resumen de las fórmulas que utiliza la aplicación. Las variables se definen en cada "
        "módulo; aquí se presentan para consulta rápida."
    )
    m.table(
        ["Módulo", "Fórmula"],
        [
            ["Programación lineal", "Optimizar Z = Σ c_j x_j sujeto a Σ a_ij x_j (<=, >=, =) b_i; x_j ≥ 0."],
            ["Método gráfico", "El óptimo de un PL con región acotada se alcanza en un vértice."],
            ["Simplex", "Costo reducido: c_j − z_j; entra la variable con mejor costo reducido."],
            ["Transporte", "Min Σ_i Σ_j c_ij x_ij; sujeto a Σ_j x_ij = oferta_i y Σ_i x_ij = demanda_j."],
            ["MODI", "u_i + v_j = c_ij en celdas básicas; Δ_ij = c_ij − (u_i + v_j)."],
            ["Asignación", "Min Σ_i c_i,σ(i), con σ una permutación de las tareas."],
            ["M/M/1", "ρ = λ/μ; L = ρ/(1−ρ); Lq = ρ²/(1−ρ); W = 1/(μ−λ); Wq = λ/[μ(μ−λ)]."],
            ["M/M/1/K", "P0 = (1−ρ)/(1−ρ^(K+1)); Pn = P0ρ^n; λ_ef = λ(1−P_K)."],
            ["M/M/c", "ρ = λ/(cμ); Lq = P0(cρ)^cρ/[c!(1−ρ)²]; Wq = Lq/λ."],
            ["M/G/1", "Lq = (ρ² + λ²σ²)/[2(1−ρ)]; Wq = Lq/λ."],
            ["Little", "L = λ_ef W; Lq = λ_ef Wq."],
            ["Markov", "π^(n) = π^(0)P^n; π = πP con Σπ = 1."],
            ["Absorción", "N = (I−Q)^(−1); tiempos esperados = N·1; probabilidades = N·R."],
            ["PERT", "te = (a + 4m + b)/6; Var = ((b−a)/6)²."],
            ["Ruta crítica", "Holgura = LS − ES; crítica si holgura = 0."],
            ["Probabilidad PERT", "z = (T − μ_proyecto)/σ_proyecto; P(T ≤ T) = Φ(z)."],
            ["EOQ", "Q* = √(2DS/H); CT = DS/Q + HQ/2."],
            ["EOQ con faltantes", "Q* = √(2DS(H+B)/(HB)); F = QH/(H+B)."],
            ["EPQ", "Q* = √(2DS/[H(1−D/p)]); inventario máximo = Q(1−D/p)."],
        ],
        widths=[3.8, 12.6],
        first_col_bold=True,
        caption="Formulario resumido de los métodos incluidos.",
    )

    m.h1("Apéndice D. Ficha técnica y compilación")
    m.lead(
        "Información para docentes, desarrolladores y personas que necesiten reconstruir los "
        "ejecutables o verificar el funcionamiento interno."
    )
    m.h2("D.1 Arquitectura")
    m.table(
        ["Aspecto", "Detalle"],
        [
            ["Lenguaje", "Python 3.10 o superior."],
            ["Interfaz", "Tkinter / ttk, sin dependencias externas en tiempo de ejecución."],
            ["Motor de cálculo", "Paquete `orlib/` con un módulo por técnica."],
            ["Pruebas", "Suite de pruebas unitarias con `unittest` (33 pruebas)."],
            ["Empaquetado", "PyInstaller: `.app` en macOS y `.exe` de un solo archivo en Windows."],
            ["Firma macOS", "Firma ad hoc; no notarizada."],
            ["Distribución", "ZIP para macOS y .exe para Windows; también código fuente."],
        ],
        widths=[4.2, 12.2],
        first_col_bold=True,
        caption="Ficha técnica de la aplicación.",
    )

    m.h2("D.2 Estructura del proyecto")
    m.code(
        [
            "InvestigacionOperaciones/",
            "├── main.py                 interfaz y pestañas",
            "├── ui.py                   componentes y estilos",
            "├── orlib/",
            "│   ├── graphic.py          método gráfico",
            "│   ├── simplex.py          simplex de dos fases",
            "│   ├── transport.py        transporte y MODI",
            "│   ├── assignment.py       algoritmo húngaro",
            "│   ├── queues.py           modelos de cola",
            "│   ├── markov.py           cadenas de Markov",
            "│   ├── pert.py             PERT / CPM",
            "│   └── inventory.py        EOQ y EPQ",
            "├── tests/test_orlib.py     pruebas unitarias",
            "├── build_macos.sh         compilación macOS",
            "├── build_windows.bat      compilación Windows",
            "└── .github/workflows/      compilación automática",
        ],
        caption="Estructura de archivos del proyecto.",
    )

    m.h2("D.3 Compilación")
    m.p("En macOS, desde la carpeta del proyecto:")
    m.code(["./build_macos.sh"], caption="Genera la aplicación y el ZIP para macOS.")
    m.p("En Windows, con Python instalado:")
    m.code(["build_windows.bat"], caption="Genera el ejecutable de Windows.")
    m.p("Para ejecutar las pruebas:")
    m.code(
        ["python -m unittest discover -s tests -v"],
        caption="Ejecuta la suite de pruebas del motor de cálculo.",
    )
    m.callout(
        "info",
        "Compilación automática",
        [
            "El repositorio incluye un flujo de trabajo de GitHub Actions que compila macOS y "
            "Windows en cada push. Los artefactos quedan disponibles en la sección **Actions** "
            "del repositorio.",
        ],
    )

    m.h1("Apéndice E. Índice de ejemplos")
    m.lead(
        "Todos los ejemplos se pueden reproducir con el botón «Ejemplo» de cada pestaña. Esta "
        "tabla indica dónde encontrar la explicación detallada."
    )
    m.table(
        ["Módulo", "Ejemplo", "Sección"],
        [
            ["Método gráfico", "Max Z = 3x1 + 5x2 con tres restricciones", "4.4"],
            ["Simplex", "El mismo modelo, con tablas de dos fases", "5.5"],
            ["Transporte", "3 plantas y 4 centros, costo mínimo 1020", "6.5"],
            ["Asignación", "4 agentes y 4 tareas, costo mínimo 13", "7.5"],
            ["Colas", "M/M/1 con λ = 2 y μ = 3", "8.6"],
            ["Colas", "M/M/c con λ = 8, μ = 3 y c = 3", "8.7"],
            ["Markov", "Tres estados, P³ y estado estable", "9.4"],
            ["Markov", "Cadena con un estado absorbente", "9.6"],
            ["PERT / CPM", "Cuatro actividades, ruta A → C → D", "10.5"],
            ["Inventarios", "EOQ básico con D = 1200, S = 50, H = 2", "11.5"],
            ["Inventarios", "EOQ con faltantes (B = 8)", "11.6"],
            ["Inventarios", "EPQ con p = 2000", "11.7"],
        ],
        widths=[3.6, 9.6, 3.2],
        first_col_bold=True,
        caption="Índice de ejemplos resueltos en el manual.",
    )

    m.h1("Apéndice F. Historial de versiones")
    m.table(
        ["Versión", "Fecha", "Cambios principales"],
        [
            ["1.0", "Noviembre de 2026", "Primera versión completa: ocho módulos, ejemplos, informes .txt, paquetes para macOS y Windows y manual de usuario."],
        ],
        widths=[2.4, 4.4, 9.6],
        caption="Historial de versiones de la aplicación y del manual.",
    )

    m.p(
        "Este manual se generó para la versión 1.0 de la aplicación. Si la interfaz cambia en una "
        "versión posterior, consulte el README del proyecto o la nota de la versión.",
        space_before=10,
        italic=True,
        color=MUTED,
        size=8.5,
    )
