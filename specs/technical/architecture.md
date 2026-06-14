# reflex-rosencharts — Technical Design Document

## Metadata

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **PRD Relacionado** | [../prd/reflex-rosencharts-prd.md](../prd/reflex-rosencharts-prd.md) |
| **API Spec Relacionado** | [../api/component-api-v1.md](../api/component-api-v1.md) |

---

## 1. Contexto

rosencharts es un conjunto de 43 componentes React escritos en TypeScript (`.tsx`) que usan **D3.js**
para los cálculos de escalas/paths y **Tailwind CSS** para el estilo. No es un paquete npm: se
distribuye como código para copiar y pegar, con **datos hardcodeados** dentro de cada componente y
un helper local `ClientTooltip.tsx` (usado por 29 de las 43 gráficas) que renderiza el tooltip con
`createPortal` de `react-dom`.

Reflex permite **envolver componentes React locales**: con `rx.asset(...)` copia el archivo fuente al
frontend generado y, declarando `library = f"$/public{ruta}"` y `tag`, expone el componente como una
clase `rx.Component` con props tipados. El reto técnico central es triple: (1) **parametrizar** los
TSX para que reciban datos por props en lugar de tenerlos hardcodeados, (2) **integrar Tailwind** en
el pipeline de build de Reflex, y (3) manejar el **tooltip con portales** (SSR) correctamente.

Este documento define el patrón repetible de port, la estructura del proyecto y las decisiones clave.

## 2. Objetivos Técnicos

- **Correctitud:** cada gráfica portada debe ser visualmente equivalente a su original con los mismos datos.
- **Repetibilidad:** una "receta" por categoría que un contribuidor pueda seguir mecánicamente.
- **Mantenibilidad:** wrappers Python pequeños y aislados; TSX parametrizados versionados junto al wrapper; cobertura de tests > 70% del Python.
- **Operabilidad:** la demo app sirve como banco de pruebas visual (una página por gráfica).

## 3. Arquitectura Propuesta

### 3.1 Diagrama de Alto Nivel

```
┌──────────────────────┐      ┌──────────────────────────┐      ┌───────────────────────┐
│  App Reflex (Python) │      │  reflex_rosencharts (pkg) │      │  Frontend generado     │
│  rx.State + páginas   │────▶│  funciones de componente  │────▶│  (.web): React + D3    │
│  data: list[dict]     │ data │  rx.Component + rx.asset   │ TSX  │  + Tailwind + Portales │
└──────────────────────┘      └──────────────────────────┘      └───────────────────────┘
         │ props (data, color, height)                                   │ render SVG/DIV
         └───────────────────────────────────────────────────────────────┘
```

### 3.2 Componentes

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| Wrappers Python | Python 3.13 / Reflex `rx.Component` | Declarar `library/tag`, props tipados, event handlers; función pública por gráfica |
| TSX parametrizados | TypeScript / React / D3 | Render de la gráfica recibiendo `props` (datos, color, dimensiones) |
| Helper `ClientTooltip` | TSX / react-dom | Tooltip por portal, compartido por 29 gráficas |
| Integración Tailwind | Plugin Tailwind de Reflex | Procesar clases utilitarias usadas por los TSX |
| Demo app / galería | Reflex | Una página de ejemplo por gráfica (la "carpeta examples") |
| Empaquetado | `reflex component` / `uv` / Hatch | Build y publicación del custom component |

### 3.3 Flujo de Datos

**Flujo: render de una gráfica**
```
1. La página llama rxc.line_chart(data=State.sales)
2. El wrapper Python crea el rx.Component con la prop `data` (rx.Var) y demás props
3. Reflex copia el TSX local al frontend (rx.asset, shared=True) y genera el import desde $/public
4. En el cliente, React monta el componente TSX y pasa `data` como prop
5. D3 calcula escalas y paths a partir de `data`
6. Se renderiza SVG/DIV con clases Tailwind; ClientTooltip monta el tooltip vía portal en hover
```

**Flujo de error / degradación:**
```
1. data vacío → el TSX hace early-return de un contenedor vacío (sin throw)
2. Esquema inesperado → fallo de tipado en compilación Reflex (no llega al runtime)
3. Fallo de Tailwind (clase no generada) → degradación visual, sin crash
4. Portal/SSR → componentes con portal se montan client-side (NoSSR/dynamic) para evitar errores de hidratación
```

## 4. Decisiones de Diseño

### DD-001: Estrategia de wrapping — componentes locales vs. publicar un npm intermedio

- **Decisión:** Envolver los TSX como **componentes locales** con `rx.asset` + `library="$/public..."`.
- **Contexto:** rosencharts no es un paquete npm; sus componentes son TSX sueltos con datos embebidos.
- **Alternativas evaluadas:**

| Opción | Pros | Contras |
|---|---|---|
| **A. Componentes locales (`rx.asset`) (elegida)** | Sin publicar npm; el TSX viaja con el paquete Python; control total para parametrizar | Hay que parametrizar cada TSX; gestión de assets/CSS |
| B. Publicar un paquete npm `rosencharts-react` y wrappear por `library` | Wrapping "estándar" por nombre de paquete | Mantener y publicar un npm extra; build step; fuera de alcance |
| C. Reescribir cada gráfica en Python puro (sin React/D3) | Sin dependencia JS | Enorme esfuerzo; pierde paridad visual; reinventa D3 |

- **Justificación:** La opción A da paridad visual con el original con el mínimo de infraestructura y mantiene todo dentro del paquete Python.
- **Consecuencias:** El paquete incluye los `.tsx` parametrizados como assets; se versiona JS dentro del paquete Python.

### DD-002: Parametrización de datos

- **Decisión:** Refactorizar cada TSX para que los datos hardcodeados pasen a ser una **prop** (`data`, y props específicos por gráfica), con defaults que reproduzcan el ejemplo original.
- **Contexto:** RF-002 exige alimentar datos desde `rx.State`.
- **Consecuencias:** Cada TSX gana un default de datos = el dataset del ejemplo original, de modo que `rxc.line_chart()` sin args reproduce el example.

### DD-003: Tailwind en Reflex

- **Decisión:** Habilitar el plugin Tailwind de Reflex y declarar el contenido de los TSX para que sus clases se generen. Spike en Fase 1.
- **Alternativas:** (a) Tailwind plugin (elegida); (b) CSS pre-compilado adjunto por `rx.asset` (más frágil con clases dinámicas).
- **Consecuencias:** Se mantiene la estética Tailwind original sin reescribir estilos.

### DD-004: Tooltip / SSR

- **Decisión:** Portar `ClientTooltip` una sola vez como helper compartido; las gráficas que lo usan se montan client-side (dynamic import / `NoSSRComponent`) si aparecen errores de hidratación.
- **Consecuencias:** Tooltips idénticos al original; coste de SSR nulo para esas gráficas.

### DD-005: Mapeo de nombres y "_DIV"

- **Decisión:** Nombre Python semántico en `snake_case`, eliminando el sufijo `_DIV` (técnica de render, no parte del API). Documentar la técnica en docstring.
- **Consecuencias:** API limpia y predecible; la técnica de render queda como detalle interno.

## 5. Patrones y Convenciones

### 5.1 Estructura del Código

```
reflex-rosencharts/
├── specs/                          # Especificaciones SDD (este conjunto)
├── reference/rosencharts/          # Código original TSX (solo lectura, referencia)
├── reflex_rosencharts/
│   ├── __init__.py                 # Re-exporta todas las funciones públicas
│   ├── reflex_rosencharts.py       # Demo app / galería (páginas de ejemplo)
│   └── components/
│       ├── helpers/
│       │   ├── ClientTooltip.tsx   # helper portado (parametrizado si aplica)
│       │   └── __init__.py
│       ├── area/
│       │   ├── area_chart.tsx      # TSX parametrizado
│       │   ├── area_chart.py       # wrapper rx.Component + función pública
│       │   └── __init__.py
│       ├── bar/  line/  pie/  scatter/  treemap/  radar/  other/
│       └── __init__.py
├── tests/
│   ├── test_imports.py             # smoke: todas las funciones importables
│   └── test_components.py          # render/props por gráfica
├── rxconfig.py
├── pyproject.toml
└── README.md
```

### 5.2 Receta de port (patrón repetible por gráfica)

```
1. Copiar reference/rosencharts/<cat>/<n>_<Name>.tsx → reflex_rosencharts/components/<cat>/<name>.tsx
2. Reemplazar `let data = [...]` hardcodeado por `export function Name({ data = <default>, ... }) `
3. Ajustar imports del helper a la ruta local (./<...>/ClientTooltip)
4. Escribir el wrapper Python:
       path = rx.asset("./<name>.tsx", shared=True)
       class <Name>(rx.Component):           # o NoSSRComponent si usa portal
           library = f"$/public{path}"
           tag = "<Name>"; is_default = False
           data: rx.Var[list[<Schema>]] = rx.Var.create(<default>)
           # color/height/colors/event handlers según API Spec
       def <name>(**props) -> rx.Component: return <Name>.create(**props)
5. Re-exportar en components/<cat>/__init__.py y en reflex_rosencharts/__init__.py
6. Añadir página de ejemplo en la galería
7. Test: import + render; comparación visual por captura contra el original
```

### 5.3 Patrones Aplicados

| Patrón | Dónde | Por qué |
|---|---|---|
| Wrapper por componente | `components/<cat>/<name>.py` | Aislar cada gráfica, evolución independiente |
| Helper compartido | `components/helpers/` | DRY del tooltip (29 gráficas) |
| Defaults = ejemplo original | TSX parametrizados | `func()` sin args reproduce el example |
| Subpaquetes por familia | `components/<cat>/` | Organización y descubribilidad |

### 5.4 Manejo de Errores
- Sin excepciones de dominio (no hay backend). Los fallos relevantes son de **compilación** (tipos/imports) y de **estilo** (Tailwind). Política: data vacío ⇒ render vacío, nunca throw.

## 6. Seguridad

| Vector | Mitigación |
|---|---|
| Inyección por `data` en el DOM | D3/React escapan texto; no se inyecta HTML crudo |
| Dependencias JS (d3, react-dom) | Versiones fijadas; superficie mínima |
| Assets externos (logos/imágenes en variantes) | URLs controladas por el consumidor; documentar |

No se manejan datos sensibles ni credenciales: la librería sólo renderiza datos provistos por la app.

## 7. Observabilidad
- **Build:** errores de compilación TSX y de Tailwind visibles en consola de `reflex run`.
- **Runtime:** sin telemetría propia; el consumidor instrumenta su app.

## 8. Testing Strategy

| Nivel | Cobertura Target | Herramientas | Qué cubre |
|---|---|---|---|
| Unit (Python) | > 70% | pytest | Que cada función exista, sea importable y construya un `rx.Component` con props |
| Compilación | 100% gráficas | `reflex export`/build | Que cada TSX compile dentro de Reflex |
| Visual | 43/43 | Capturas (Playwright/manual) contra `reference/` | Paridad visual con el original |
| Smoke demo | 1 página/gráfica | Carga de la galería | Que cada ejemplo renderice sin error |

## 9. Plan de Migración / Rollout
- Desarrollo incremental por familias; cada familia mergea cuando sus gráficas compilan y tienen ejemplo.
- Publicación a PyPI sólo cuando las 43 estén portadas y la galería completa (gate de Fase 8).
- Versionado semántico; conservar licencia MIT y atribución a rosencharts.

## 10. Preguntas Abiertas
- [ ] ¿Tematización por tokens (paleta) en v1 o v2? — Owner: Ernesto
- [ ] ¿Qué gráficas requieren realmente `NoSSRComponent`? — confirmar en spike Fase 1
- [ ] ¿Publicar como "custom component" de Reflex (`reflex component`) o paquete plano? — Owner: Ernesto

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Versión inicial |
