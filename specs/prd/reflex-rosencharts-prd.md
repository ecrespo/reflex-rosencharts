# reflex-rosencharts

## Product Requirements Document (PRD)

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **Reviewers** | — |
| **Última actualización** | 2026-06-14 |

---

## 1. Resumen Ejecutivo

`reflex-rosencharts` es un **custom component de Reflex** que porta la librería de gráficas
[rosencharts](https://github.com/Filsommer/rosenCharts) (43 componentes React/TSX construidos con
D3.js y Tailwind CSS) al ecosistema **Reflex**, permitiendo a desarrolladores Python construir
dashboards y visualizaciones sin escribir JavaScript.

Está dirigido a desarrolladores Python que usan Reflex y necesitan gráficas modernas, ligeras y
estéticas. Resuelve el problema de que rosencharts hoy solo es consumible como "copy-paste" de
TSX dentro de proyectos React/Next.js; este port expone cada gráfica como una función Python
(`rxc.line_chart(...)`, `rxc.donut_chart(...)`, etc.) con props tipados y datos pasados desde el
estado de la aplicación.

## 2. Contexto y Problema

### 2.1 Situación Actual
- rosencharts es una colección de 43 componentes `.tsx` (no es un paquete npm) que el usuario
  copia y pega en su proyecto React, instalando `d3` y `@types/d3` manualmente.
- Cada componente trae **datos hardcodeados** y clases **Tailwind** para el estilo.
- 29 de las 43 gráficas dependen de un helper local `ClientTooltip.tsx` (usa `react-dom` / `createPortal`).
- No existe ninguna forma de usar estas gráficas desde Python/Reflex.

### 2.2 Problema
Los desarrolladores de Reflex no tienen acceso a estas gráficas. Las opciones nativas de Reflex
(recharts, plotly) tienen una estética distinta. Reescribir 43 gráficas D3 a mano en cada proyecto
es costoso y propenso a errores.

### 2.3 Oportunidad
Reflex soporta **wrapping de componentes React locales** (`rx.asset` + `library="$/public..."`).
Empaquetando los TSX de rosencharts como componentes locales y exponiéndolos como clases
`rx.Component`, se obtiene una librería reutilizable, instalable vía `pip`/`uv`, que cubre las 8
familias de gráficas con un único API Python coherente.

## 3. Usuarios Objetivo

### Persona 1: Desarrollador Python / Reflex
- **Descripción:** Construye aplicaciones web data-driven en Python con Reflex.
- **Necesidad principal:** Insertar gráficas atractivas pasando datos desde `rx.State`.
- **Frecuencia de uso:** Diaria durante desarrollo de dashboards.
- **Nivel técnico:** Medio/Alto en Python, bajo/nulo en React/D3.

### Persona 2: Data Scientist / Analista
- **Descripción:** Crea prototipos de visualización y reportes internos.
- **Necesidad principal:** Gráficas listas para usar con poca configuración.
- **Frecuencia de uso:** Semanal.
- **Nivel técnico:** Medio en Python, bajo en frontend.

### Persona 3: Contribuidor de la librería
- **Descripción:** Mantiene/extiende el port.
- **Necesidad principal:** Un patrón claro y repetible para portar cada gráfica.
- **Frecuencia de uso:** Eventual.
- **Nivel técnico:** Alto en Python y React.

## 4. Objetivos y Métricas de Éxito

### 4.1 Objetivos del Proyecto

| Objetivo | Métrica | Target | Plazo |
|---|---|---|---|
| Cobertura de gráficas | % de gráficas portadas de las 43 | 100% | Fin Fase 7 |
| Ejemplos de uso | Cada gráfica con un ejemplo ejecutable en la demo app | 43/43 | Fin Fase 7 |
| Paridad visual | Diferencia visual aceptable vs. original (revisión por captura) | ≥ 95% similar | Por gráfica |
| Publicación | Paquete instalable (`pip install reflex-rosencharts`) | Publicado en PyPI | Fase 8 |

### 4.2 Objetivos de Usuario

| Objetivo del Usuario | Indicador |
|---|---|
| Insertar una gráfica en < 5 líneas Python | Snippet en README por gráfica |
| Pasar datos desde el estado sin tocar JS | Todas las gráficas aceptan `data` como prop |
| Theming consistente (claro/oscuro) | Soporte de dark mode vía Tailwind |

## 5. Alcance

### 5.1 In Scope (Incluido)
- [ ] Port de las **43 gráficas** en 8 familias: area (4), bar (12), line (8), pie/donut (8), scatter (4), treemap (3), radar (2), other (2).
- [ ] Parametrización de **datos** (sustituir los datos hardcodeados por props alimentados desde Python).
- [ ] Port del helper `ClientTooltip` (requerido por 29 gráficas).
- [ ] Integración de **Tailwind CSS** en el build de Reflex.
- [ ] Una **demo app** (`reflex_rosencharts/reflex_rosencharts.py`) con una página de ejemplo por gráfica (la "carpeta examples").
- [ ] Documentación: README + docstrings + página de galería.
- [ ] Empaquetado como custom component de Reflex publicable.

### 5.2 Out of Scope (Excluido)
- Crear gráficas nuevas que no existan en rosencharts — sólo se portan las existentes.
- Backends de datos, autenticación o persistencia — la librería sólo renderiza.
- Animaciones/interacciones no presentes en el original.
- Versionar/parchear D3 más allá de lo necesario para renderizar.

### 5.3 Futuras Consideraciones
- Exportar gráficas a PNG/SVG.
- Tematización por tokens (paletas configurables) en lugar de clases Tailwind fijas.
- Soporte de streaming/actualización en tiempo real de datos.

## 6. Requisitos Funcionales

### RF-001: Renderizar cada gráfica como componente Reflex
- **Descripción:** El sistema debe exponer cada una de las 43 gráficas como una función Python que retorna un `rx.Component`.
- **Actor:** Desarrollador Python.
- **Precondiciones:** `reflex-rosencharts` instalado; Tailwind habilitado.
- **Flujo principal:**
  1. El desarrollador importa `reflex_rosencharts as rxc`.
  2. Llama a `rxc.<grafica>(data=...)` dentro de una página Reflex.
  3. Reflex compila el TSX local y renderiza la gráfica.
- **Postcondiciones:** La gráfica se muestra con los datos provistos.
- **Prioridad:** `MUST`

### RF-002: Alimentar datos desde el estado
- **Descripción:** Cada gráfica debe aceptar su dataset vía prop `data` (y props específicos) tipados con `rx.Var`.
- **Actor:** Desarrollador Python.
- **Flujo principal:** El dato vive en `rx.State`; al cambiar, la gráfica se re-renderiza.
- **Prioridad:** `MUST`

### RF-003: Tooltips interactivos
- **Descripción:** Las gráficas que en el original usan `ClientTooltip` deben mostrar el mismo tooltip al hacer hover.
- **Precondiciones:** Helper `ClientTooltip` portado y disponible.
- **Prioridad:** `SHOULD`

### RF-004: Ejemplo ejecutable por gráfica
- **Descripción:** El sistema debe incluir una página de ejemplo por gráfica en la demo app, replicando el "example" del repo original.
- **Prioridad:** `MUST`

### RF-005: Soporte de dark mode
- **Descripción:** Las gráficas deben respetar las variantes `dark:` de Tailwind como en el original.
- **Prioridad:** `SHOULD`

### RF-006: Props de estilo/tamaño
- **Descripción:** Cada gráfica debe permitir ajustar dimensiones y, donde aplique, colores/paleta.
- **Prioridad:** `COULD`

## 7. Requisitos No Funcionales

### Rendimiento
- El tiempo de compilación incremental de Reflex no debe degradarse notablemente; las gráficas son componentes ligeros (D3 en cliente).
- El render inicial de una página con una gráfica debe ser < 1s en local.

### Mantenibilidad
- Patrón de port **repetible y documentado** (una receta por tipo de gráfica).
- Cobertura de tests > 70% del código Python de wrappers.
- Cada wrapper en su propio módulo dentro de la familia correspondiente.

### Compatibilidad
- Python ≥ 3.10 (proyecto fijado a 3.13).
- Reflex ≥ 0.9.x.
- Navegadores evergreen (Chrome, Firefox, Safari, Edge).

### Observabilidad
- Errores de compilación de TSX deben ser visibles en la consola de Reflex.

## 8. Restricciones y Dependencias

### Restricciones Técnicas
- rosencharts **no es un paquete npm**: hay que tratar los TSX como **componentes locales** (`rx.asset`).
- Las gráficas usan **Tailwind**: requiere habilitar el plugin Tailwind de Reflex.
- `ClientTooltip` usa `react-dom`/`createPortal`: candidatas a `NoSSRComponent` donde sea necesario.
- Datos hardcodeados en cada TSX → refactor para recibir `props`.

### Restricciones de Negocio / Licencia
- rosencharts es **MIT**: el port debe conservar la atribución y licencia MIT.

### Dependencias Externas

| Dependencia | Tipo | Owner | Estado | Riesgo |
|---|---|---|---|---|
| Reflex (framework) | Runtime | reflex-dev | Estable | Bajo |
| D3.js | Runtime (npm) | d3 | Estable | Bajo |
| Tailwind CSS | Build | tailwindlabs | Estable | Medio (config en Reflex) |
| rosencharts (código fuente TSX) | Fuente | Filsommer | Estable | Bajo |
| react-dom (portales tooltip) | Runtime | Meta | Estable | Bajo |

## 9. User Stories

### Épica: Galería de gráficas en Python

**US-001:** Como desarrollador Reflex, quiero llamar `rxc.line_chart(data=mi_serie)`, para mostrar una línea sin escribir JS.
- Criterios de aceptación:
  - [ ] La función existe y acepta `data` tipado.
  - [ ] La gráfica renderiza igual que el ejemplo original.

**US-002:** Como analista, quiero una galería con todos los ejemplos, para elegir la gráfica adecuada.
- Criterios de aceptación:
  - [ ] La demo app lista las 43 gráficas con su ejemplo.

**US-003:** Como contribuidor, quiero una guía de port por tipo, para añadir gráficas siguiendo un patrón.
- Criterios de aceptación:
  - [ ] Tech Design documenta la receta de wrapping.

## 10. Wireframes / Mockups
- Galería: barra lateral con familias (Area, Bar, Line, Pie, Scatter, Treemap, Radar, Other) y, por cada una, tarjetas con la gráfica + snippet de código. Referencia visual: los archivos `reference/rosencharts/*`.

## 11. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Configuración de Tailwind en Reflex compleja | Media | Alto | Spike inicial en Fase 1; documentar config |
| Tooltips con portales no compatibles con SSR | Media | Medio | Usar `NoSSRComponent` / dynamic import |
| Refactor de datos rompe la estética | Media | Medio | Comparación por captura contra original |
| Cambios de versión de Reflex en su API de wrapping | Baja | Medio | Fijar versión de Reflex en pyproject |

## 12. Timeline Estimado

| Fase | Duración Estimada | Entregable |
|---|---|---|
| Spec & Design | 0.5 semana | Specs aprobados |
| Fundación (Tailwind + helper + patrón) | 1 semana | 1ª gráfica funcionando |
| Port por familias | 3-4 semanas | 43 gráficas + ejemplos |
| Demo/galería + docs | 1 semana | Galería navegable |
| Empaquetado y publicación | 0.5 semana | Paquete en PyPI |

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Versión inicial |

## Aprobaciones

| Rol | Nombre | Fecha | Estado |
|---|---|---|---|
| Owner | Ernesto Crespo | | ☐ Pendiente |
| Tech Lead | | | ☐ Pendiente |
