# reflex-rosencharts — Diseño de ejecución (port de las 43 gráficas)

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo (con Claude) |
| **Fecha** | 2026-06-14 |
| **Estado** | Aprobado (brainstorming) |
| **Specs base** | [PRD](../../specs/prd/reflex-rosencharts-prd.md) · [Tech Design](../../specs/technical/architecture.md) · [API](../../specs/api/component-api-v1.md) · [Data Model](../../specs/data-model/chart-data-schemas.md) · [Plan](../../specs/plans/implementation-plan.md) |

> La **arquitectura** (wrapping con `rx.asset` + `library="$/public..."`, parametrización de datos,
> Tailwind, tooltip/SSR) ya está fijada en los specs SDD. Este documento define el **cómo se ejecuta**
> el port de las 43 gráficas en una sesión, con TDD y verificación.

## 1. Decisiones de la sesión (aprobadas)

| Decisión | Valor |
|---|---|
| **Alcance** | Las **43 gráficas** completas + galería demo |
| **Metodología** | **TDD** en todo el layer Python (red → green → refactor por gráfica) |
| **Ejecución** | Receta probada en el piloto por el dev principal → **workflow multi-agente** por familias para las 42 restantes |
| **Verificación** | Tests pytest verdes + `reflex run` compila la galería + **capturas Playwright** vs `reference/` |

## 2. Principio rector

No se abanican agentes sobre una receta no comprobada. Primero se prueba el camino completo
(Tailwind + D3 + ClientTooltip + wrapping + demo) sobre **1 gráfica piloto** y se verifica que
**compila y renderiza**; recién entonces se paraleliza el resto.

## 3. Etapas

### Etapa A — Fundación + piloto (secuencial, verificado, TDD)

1. Portar `ClientTooltip.tsx` al paquete como helper compartido; wrapper NoSSR (usa `createPortal`).
2. Resolver Tailwind V4: asegurar que las clases de los TSX se escaneen/generen. Definir **safelist**
   para clases dinámicas que llegan por prop (p. ej. `stroke-fuchsia-400`, paletas).
3. Declarar la dependencia npm **`d3`** en el wrapper (`lib_dependencies`).
4. **TDD `line_chart`** (piloto): test primero (existe, importable, `.create(data=...)` → `rx.Component`
   con `tag`/`library`/props correctos, default = ejemplo) → TSX parametrizado + wrapper Python → verde.
5. Montar la **galería demo** (sidebar por familia, tarjeta + snippet por gráfica) con el piloto y
   **verificar que `reflex run` / export compila** sin errores TSX/Tailwind.

**Gate de salida de A:** `rxc.line_chart()` renderiza idéntico al original; tests verdes; compila.

### Etapa B — Fan-out de las 42 restantes (workflow multi-agente por familia)

- Pipeline por familia: line (resto), area, bar, pie/donut, scatter, treemap, radar, other.
- Cada agente recibe: la **receta probada** (de la Etapa A), el TSX de referencia y el esquema de datos.
  Porta su gráfica **siguiendo TDD** (test → wrapper + TSX parametrizado → verde), aislada en su módulo,
  y la re-exporta.
- Las familias corren en paralelo (todas dependen sólo de la fundación).

### Etapa C — Integración + verificación

- Recolectar wrappers; correr **suite pytest completa** (verde, cobertura Python > 70%).
- Completar la galería con las 43; **verificar que la app compila** (`reflex run`/export) sin errores.
- **Capturas Playwright** de cada gráfica para comparar contra `reference/` (auditoría de paridad visual
  por familia).

## 4. Estructura de archivos (Tech Design §5.1)

```
reflex_rosencharts/components/<familia>/<name>.tsx   # TSX parametrizado (default = ejemplo)
reflex_rosencharts/components/<familia>/<name>.py    # wrapper rx.Component + función pública
reflex_rosencharts/components/helpers/ClientTooltip.tsx + .py
reflex_rosencharts/__init__.py                       # re-export de las 43 funciones
reflex_rosencharts/reflex_rosencharts.py             # galería demo
tests/test_imports.py                                # smoke: todas importables
tests/test_<familia>.py                              # TDD por familia (render/props)
```

## 5. Receta de port por gráfica (TDD)

```
RED   → test_<familia>.py: la función existe, es importable, .create(data=...) construye
         un rx.Component con tag/library/props correctos; default reproduce el ejemplo.
GREEN → 1. Copiar reference/.../<n>_<Name>.tsx → components/<fam>/<name>.tsx
         2. Reemplazar datos hardcodeados por prop `data` (default = ejemplo original)
         3. Ajustar import del helper a la ruta local
         4. Escribir wrapper Python (rx.asset, library, tag, props tipados; NoSSR si usa portal)
         5. Re-exportar en components/<fam>/__init__.py y en reflex_rosencharts/__init__.py
         6. Añadir página/tarjeta de ejemplo en la galería
REFACTOR → limpiar manteniendo verde.
```

## 6. Riesgos y mitigaciones (de la sesión)

| Riesgo | Mitigación |
|---|---|
| Tailwind V4 no genera clases dinámicas por prop | Safelist en config; probado en piloto antes del fan-out |
| Hidratación por portales (tooltip) | `NoSSRComponent` / dynamic import en gráficas con tooltip |
| Agentes divergen de la receta | Receta probada y verificada en Etapa A antes del fan-out; cada agente la recibe literal |
| Paridad visual difícil de auto-verificar | Capturas Playwright vs `reference/`; revisión final manual con la demo |

## 7. Definición de Done (global)

- [ ] 43 wrappers Python + TSX parametrizados, re-exportados.
- [ ] Tests pytest verdes (TDD), cobertura Python > 70%.
- [ ] Galería demo con las 43 (tarjeta + snippet) y `reflex run` compila.
- [ ] Capturas Playwright de las 43 vs `reference/`.
