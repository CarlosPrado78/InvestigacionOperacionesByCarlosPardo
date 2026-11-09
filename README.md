# Investigación de Operaciones By Carlos Pardo

Aplicación de escritorio para **resolver, presentar y explicar** problemas clásicos de
Investigación de Operaciones. Funciona sin internet y guarda los resultados en un informe
de texto.

Incluye ejemplos precargados en todas las pestañas y muestra el **desarrollo de los
algoritmos**, no solo la respuesta final.

## Módulos incluidos

| Módulo | Qué resuelve |
|---|---|
| **Método gráfico** | Programación lineal con 2 variables: región factible, vértices, recta objetivo y solución óptima. |
| **Simplex** | Dos fases, restricciones `<=`, `>=`, `=`, maximizar/minimizar, tablas iteración por iteración. |
| **Transporte** | Esquina noroeste, costo mínimo, Vogel y optimización MODI (`u`, `v`), con balanceo automático. |
| **Asignación** | Algoritmo húngaro para minimizar costos o maximizar beneficios, incluye matrices rectangulares. |
| **Teoría de colas** | `M/M/1`, `M/M/1/K`, `M/M/c`, `M/M/c/K` y `M/G/1`: ρ, P0, L, Lq, W, Wq, P(espera), rechazo y distribución. |
| **Cadenas de Markov** | `P^n`, distribución tras `n` pasos, estado estable, clases, periodicidad, absorción y tiempos esperados. |
| **PERT / CPM** | Tiempos esperados, ES/EF/LS/LF, holguras, ruta crítica y probabilidad de cumplir un plazo. |
| **Inventarios** | EOQ básico, EOQ con faltantes y lote de producción EPQ. |

## Ejecutables

### macOS (ya compilado)

El proyecto incluye la aplicación lista para usar:

```
dist/Investigación de Operaciones By Carlos Pardo.app
```

1. Abra `dist/Investigación de Operaciones By Carlos Pardo.app` con doble clic.
2. Si macOS muestra el aviso de “desarrollador no identificado”, haga **clic derecho →
   Abrir** la primera vez. También puede ejecutar:

```bash
xattr -dr com.apple.quarantine "dist/Investigación de Operaciones By Carlos Pardo.app"
```

Para volver a compilarla:

```bash
./build_macos.sh
```

El resultado se genera en `dist/Investigación de Operaciones By Carlos Pardo.app` y también
se crea `dist/Investigación de Operaciones By Carlos Pardo (macOS).zip` para compartirla.
Si va a enviarla a otra persona, use el ZIP: al descomprimirlo se conserva la firma ad hoc
de la aplicación.

### Windows (.exe)

PyInstaller **no puede compilar para Windows desde macOS**: el `.exe` debe generarse en
Windows. Hay dos formas sencillas:

**Opción A — desde un PC Windows**

1. Instale Python 3.11 o superior desde <https://www.python.org/downloads/windows/>.
   Marque la opción **Add python.exe to PATH** (el instalador oficial incluye Tkinter).
2. Copie la carpeta del proyecto al PC.
3. Ejecute `build_windows.bat` con doble clic.
4. El ejecutable queda en `dist\Investigación de Operaciones By Carlos Pardo.exe`.

**Opción B — GitHub Actions (genera macOS y Windows automáticamente)** ✅ *en uso*

Repositorio: <https://github.com/CarlosPrado78/InvestigacionOperacionesByCarlosPardo>

El proyecto incluye `.github/workflows/build.yml`, que se ejecuta solo con cada *push*:

1. Vaya a **Actions → Construir ejecutables**.
2. Al terminar, descargue los dos artefactos:
   - `InvestigacionOperacionesByCarlosPardo-macOS` → `Investigación de Operaciones By Carlos Pardo (macOS).zip`
   - `InvestigacionOperacionesByCarlosPardo-Windows` → `Investigación de Operaciones By Carlos Pardo.exe`

Los artefactos se conservan **90 días** (hay que iniciar sesión en GitHub para descargarlos).

### Ejecutar desde el código fuente

Requiere Python 3.11+ con Tkinter (el instalador oficial de python.org lo incluye).

```bash
python3 main.py
```

En Windows: `run_windows.bat` o `py -3 main.py`.

## Uso rápido

1. Abra la pestaña del tipo de problema.
2. Presione **Ejemplo** para cargar un caso resuelto y ver el formato esperado.
3. Edite los datos.
4. Presione **Resolver** (también funciona `Cmd+Enter` en macOS o `Ctrl+Enter` en Windows).
5. Revise el desarrollo y la interpretación.
6. Use **Guardar .txt** para exportar el informe.

## Manual de usuario

El manual completo está en Word:

```
docs/Manual de Usuario - Investigación de Operaciones By Carlos Pardo.docx
```

Detalle, para cada módulo, el uso de todos los campos, un ejemplo resuelto, la
interpretación de los resultados, los errores frecuentes y ejercicios propuestos. Incluye
la tabla de contenidos, la guía de instalación y las notas de compilación.

Para regenerarlo desde el código (figuras y tablas incluidas):

```bash
.venv-build/bin/python tools/generate_manual.py
```

Requiere `python-docx` y `pillow`:

```bash
.venv-build/bin/pip install python-docx pillow
```

> La tabla de contenidos es un campo automático de Word. La primera vez que abra el
> manual puede pedirle actualizarla: presione `F9` o haga clic derecho → **Actualizar
> campo**.

## Formatos de entrada

Use punto decimal (`2.5`) y separe valores con espacios o comas.

### Método gráfico

```
Función objetivo:  3 5          (Z = 3x1 + 5x2)
Restricciones:
1 0 <= 4
0 2 <= 12
3 2 <= 18
```

Las variables siempre son no negativas: `x1 >= 0`, `x2 >= 0`.

### Simplex

```
Función objetivo:  3 5
Restricciones:
1 0 <= 4
0 2 <= 12
3 2 <= 18
```

Cada restricción debe tener un coeficiente por variable, un operador y el valor.
Se admiten `<=`, `>=`, `=` y términos independientes negativos.

### Transporte

```
Matriz de costos:
8 6 10 9
9 12 13 7
14 9 16 5

Oferta:  35 50 40
Demanda: 45 20 30 30
```

Si la oferta y la demanda no coinciden, la aplicación agrega automáticamente una fila o
columna ficticia con costo cero. Para rutas prohibidas use un costo muy alto.

### Asignación

Una fila por agente y una columna por tarea:

```
9 2 7 8
6 4 3 7
5 8 1 8
7 6 9 4
```

### Colas

Seleccione el modelo e ingrese λ y μ. Según el modelo se habilitan `c`, `K` o `σ`.
Las unidades de tiempo de `W` y `Wq` son las mismas que las de `1/λ` y `1/μ`.

### Markov

Una fila por estado; cada fila debe sumar 1:

```
0.7 0.2 0.1
0.3 0.4 0.3
0.2 0.2 0.6
```

La distribución inicial y el número de pasos son opcionales.

### PERT / CPM

```
Nombre, optimista, probable, pesimista, predecesores
A, 2, 4, 6, -
B, 3, 5, 8, A
C, 4, 6, 9, A
D, 2, 3, 5, B, C
```

Use `-` cuando no hay predecesores. El plazo objetivo es opcional y sirve para calcular
`P(T ≤ plazo)`.

### Inventarios

- `D`: demanda anual.
- `S`: costo de ordenar.
- `H`: costo de mantener una unidad durante un año.
- `B`: costo de faltante por unidad y año (solo EOQ con faltantes).
- `p`: tasa anual de producción (solo EPQ; debe ser mayor que `D`).

## Estructura del proyecto

```
InvestigacionOperaciones/
├── main.py                  # Interfaz gráfica y pestañas
├── ui.py                    # Componentes, estilos y lectura de datos
├── orlib/
│   ├── simplex.py           # Simplex de dos fases
│   ├── graphic.py           # Método gráfico
│   ├── transport.py         # Transporte + MODI
│   ├── assignment.py        # Algoritmo húngaro
│   ├── queues.py            # Modelos de colas
│   ├── markov.py            # Cadenas de Markov
│   ├── pert.py              # PERT / CPM
│   └── inventory.py         # EOQ / EPQ
├── tests/test_orlib.py      # Pruebas del motor de cálculo
├── docs/
│   ├── Manual de Usuario - Investigación de Operaciones By Carlos Pardo.docx
│   └── assets/              # Figuras y capturas del manual
├── tools/                   # Generadores del manual (python-docx)
├── build_macos.sh           # Compilación para macOS
├── build_windows.bat        # Compilación para Windows
├── run_macos.sh             # Ejecutar desde el código
├── run_windows.bat
├── requirements-build.txt   # Solo PyInstaller
└── .github/workflows/build.yml
```

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

Las pruebas cubren los 9 módulos: optimalidad, infactibilidad, no acotamiento, casos
degenerados, balanceo, modelos de colas, cadenas periódicas y absorbentes, ruta crítica
y fórmulas de inventario.

## Notas y limitaciones

- **Programación lineal:** las variables son no negativas (`x >= 0`), como en la
  formulación estándar de los cursos.
- **Método gráfico:** solo 2 variables.
- **Transporte:** el modelo es lineal con costos por unidad; para rutas prohibidas use
  un costo suficientemente grande.
- **Colas:** se implementan modelos clásicos con llegadas/servicios exponenciales
  (excepto `M/G/1`, que usa la fórmula de Pollaczek-Khinchine).
- **Markov:** tiempo discreto, cadena finita y homogénea.
- **PERT:** la probabilidad usa la aproximación normal sobre la ruta crítica.
- **Firma de código:** el `.app` se firma de forma local (ad hoc), no está notarizado.
  En Windows, SmartScreen puede pedir confirmación: **Más información → Ejecutar de
  todos modos**.

## Solución de problemas

**La app de macOS no abre.** Use clic derecho → Abrir, o quite la cuarentena con el
comando `xattr` mostrado arriba.

**Windows no reconoce `py`.** Instale Python desde python.org y marque “Add python.exe to
PATH”; luego ejecute `build_windows.bat` de nuevo.

**Error al compilar en macOS.** Verifique que `python3 -c "import tkinter"` funcione. Si
usa Homebrew, instale `python-tk` o use el Python oficial de python.org.

**Los resultados muestran `—`.** Significa que el dato no aplica al modelo seleccionado.

---

Hecho para apoyar cursos, tareas y presentaciones de Investigación de Operaciones.
