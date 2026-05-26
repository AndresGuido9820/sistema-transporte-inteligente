from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORT = ROOT / "report" / "blog_post.md"

COLABS = {
    "Demanda": "https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/01_prediccion_demanda.ipynb",
    "Conduccion": "https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/02_clasificacion_conduccion.ipynb",
    "Recomendacion": "https://colab.research.google.com/github/AndresGuido9820/sistema-transporte-inteligente/blob/main/notebooks/03_recomendacion_destinos.ipynb",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9áéíóúñü]+", "-", text)
    return text.strip("-")


def inline_markdown(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', text)
    return text


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    in_ul = False
    in_table = False
    table_rows: list[list[str]] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_ul() -> None:
        nonlocal in_ul
        if in_ul:
            output.append("</ul>")
            in_ul = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table or not table_rows:
            return
        headers = table_rows[0]
        body = table_rows[1:]
        output.append("<table><thead><tr>")
        output.extend(f"<th>{inline_markdown(cell)}</th>" for cell in headers)
        output.append("</tr></thead><tbody>")
        for row in body:
            output.append("<tr>")
            output.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
            output.append("</tr>")
        output.append("</tbody></table>")
        in_table = False
        table_rows = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped == "---":
            flush_paragraph()
            flush_ul()
            flush_table()
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_ul()
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if set("".join(cells)) <= {"-", ":", " "}:
                in_table = True
                continue
            in_table = True
            table_rows.append(cells)
            continue
        flush_table()
        if stripped.startswith("#"):
            flush_paragraph()
            flush_ul()
            level = min(len(stripped) - len(stripped.lstrip("#")), 3)
            title = stripped[level:].strip()
            output.append(f'<h{level} id="{slugify(title)}">{inline_markdown(title)}</h{level}>')
        elif stripped.startswith("- "):
            flush_paragraph()
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            output.append(f"<li>{inline_markdown(stripped[2:])}</li>")
        else:
            paragraph.append(stripped)

    flush_paragraph()
    flush_ul()
    flush_table()
    return "\n".join(output)


STYLE = """
:root { color-scheme: light; --ink:#172026; --muted:#5c6873; --line:#d9e0e7; --blue:#1f5eff; --green:#0a7a5f; --amber:#a86200; --bg:#f5f7fa; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--bg); line-height: 1.55; }
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.wrap { max-width: 1120px; margin: 0 auto; padding: 28px 20px 56px; }
.topbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-bottom: 34px; }
.brand { font-weight: 800; letter-spacing: .2px; }
.nav { display: flex; flex-wrap: wrap; gap: 12px; font-size: 14px; }
.hero { display: grid; grid-template-columns: 1.05fr .95fr; gap: 28px; align-items: center; padding: 42px 0 34px; border-bottom: 1px solid var(--line); }
.hero h1 { margin: 0; max-width: 850px; font-size: clamp(34px, 5vw, 60px); line-height: 1.02; letter-spacing: 0; }
.hero p { margin: 18px 0 0; max-width: 680px; color: var(--muted); font-size: 18px; }
.badge { display: inline-flex; margin-bottom: 14px; color: var(--green); font-weight: 700; font-size: 14px; }
.kpis { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
.kpi { border: 1px solid var(--line); background: white; border-radius: 8px; padding: 14px; }
.kpi strong { display: block; font-size: 22px; }
.hero-visual { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 18px; box-shadow: 0 14px 36px rgba(23,32,38,.08); }
.route-chart { height: 178px; display: flex; align-items: end; gap: 8px; padding: 14px 8px 8px; border-bottom: 1px solid var(--line); }
.route-chart i { flex: 1; min-width: 10px; border-radius: 5px 5px 0 0; background: linear-gradient(180deg, #2f6fff, #11a87d); }
.route-chart i:nth-child(2n) { background: linear-gradient(180deg, #f6a531, #e06d2f); }
.visual-caption { display: flex; justify-content: space-between; gap: 12px; margin-top: 12px; color: var(--muted); font-size: 13px; }
.visual-caption strong { color: var(--ink); display: block; font-size: 16px; }
.grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin-top: 28px; }
.card { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 18px; min-height: 230px; display: flex; flex-direction: column; }
.card h2 { margin: 0 0 8px; font-size: 21px; }
.card p { margin: 0 0 12px; color: var(--muted); }
.card ul { padding-left: 18px; margin: 0 0 16px; color: var(--muted); }
.card-top { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
.icon { width: 42px; height: 42px; border-radius: 8px; display: grid; place-items: center; font-weight: 900; color: white; background: var(--blue); }
.icon.green { background: var(--green); }
.icon.amber { background: var(--amber); }
.mini-bars { display: flex; align-items: end; gap: 5px; height: 46px; margin: 6px 0 14px; }
.mini-bars i { flex: 1; border-radius: 4px 4px 0 0; background: #c9d8ff; }
.mini-bars i:nth-child(2n) { background: #afe3d2; }
.mini-bars i:nth-child(3n) { background: #ffd69a; }
.button { display: inline-flex; align-items: center; justify-content: center; min-height: 38px; padding: 8px 12px; margin-top: auto; border-radius: 6px; background: var(--blue); color: white; font-weight: 700; }
.button:hover { text-decoration: none; background: #174bd0; }
.section { margin-top: 34px; }
.panel { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 22px; }
.section h2 { margin: 0 0 10px; }
.pipeline { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 16px; }
.step { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 16px; position: relative; }
.step span { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; background: #edf3ff; color: var(--blue); font-weight: 800; margin-bottom: 10px; }
.step h3 { margin: 0 0 6px; font-size: 17px; }
.step p { margin: 0; color: var(--muted); font-size: 14px; }
.evidence { display: grid; grid-template-columns: 1.15fr .85fr; gap: 16px; align-items: stretch; }
.shot { background: white; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
.shot img { display: block; width: 100%; height: 100%; max-height: 310px; object-fit: cover; object-position: top left; background: #eef3f8; }
.metric-list { display: grid; gap: 10px; }
.metric { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 14px; }
.metric b { display: flex; justify-content: space-between; gap: 12px; margin-bottom: 8px; }
.meter { height: 8px; border-radius: 999px; overflow: hidden; background: #e8edf3; }
.meter i { display: block; height: 100%; background: linear-gradient(90deg, var(--blue), var(--green)); }
.links-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.ghost { background: white; color: var(--blue); border: 1px solid var(--line); }
.ghost:hover { background: #edf3ff; }
.report { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 28px; }
.report h1 { font-size: 36px; line-height: 1.12; margin-top: 0; }
.report h2 { margin-top: 34px; border-top: 1px solid var(--line); padding-top: 22px; }
.report table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
.report th, .report td { border: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; }
.report th { background: #eef3f8; }
code { background: #edf1f5; padding: 2px 5px; border-radius: 4px; }
@media (max-width: 820px) { .hero, .grid, .pipeline, .evidence { grid-template-columns: 1fr; } .kpis { grid-template-columns: 1fr; } .topbar { align-items: flex-start; flex-direction: column; } }
"""


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>{body}</body>
</html>
"""


def build_index() -> str:
    colab_cards = [
        (
            "Predicción de demanda",
            "Pronóstico de pasajeros por ruta para los próximos 30 días.",
            ["Variables temporales", "Comparación real vs. predicción", "Tabla operativa futura"],
            COLABS["Demanda"],
        ),
        (
            "Clasificación de conducción",
            "Clasificador de imágenes para comportamientos distractivos.",
            ["Matriz de confusión", "Probabilidades por clase", "Prueba con imagen nueva"],
            COLABS["Conduccion"],
        ),
        (
            "Recomendación de destinos",
            "Recomendador personalizado basado en historial de usuarios.",
            ["Precision@K y Recall@K", "Top destinos", "Explicación por similitud"],
            COLABS["Recomendacion"],
        ),
    ]
    cards_html = []
    icons = [("01", ""), ("02", "green"), ("03", "amber")]
    mini_heights = [
        [35, 52, 44, 68, 82, 74, 91, 63],
        [82, 46, 68, 38, 58, 77, 51, 64],
        [43, 61, 54, 80, 69, 88, 76, 58],
    ]
    for index, (title, description, bullets, url) in enumerate(colab_cards):
        bullet_html = "".join(f"<li>{html.escape(item)}</li>" for item in bullets)
        icon_text, icon_class = icons[index]
        bars = "".join(f'<i style="height:{height}%"></i>' for height in mini_heights[index])
        cards_html.append(
            f"""<article class="card">
  <div class="card-top">
    <h2>{html.escape(title)}</h2>
    <span class="icon {icon_class}">{icon_text}</span>
  </div>
  <p>{html.escape(description)}</p>
  <div class="mini-bars" aria-hidden="true">{bars}</div>
  <ul>{bullet_html}</ul>
  <a class="button" href="{url}">Abrir en Colab</a>
</article>"""
        )
    hero_bars = "".join(f'<i style="height:{height}%"></i>' for height in [46, 63, 58, 81, 69, 92, 77, 88, 74, 96, 84, 90])
    body = f"""
<main class="wrap">
  <header class="topbar">
    <div class="brand">Sistema Inteligente de Transporte</div>
    <nav class="nav">
      <a href="reporte.html">Reporte técnico</a>
      <a href="https://github.com/AndresGuido9820/sistema-transporte-inteligente">Repositorio</a>
    </nav>
  </header>
  <section class="hero">
    <div>
      <span class="badge">Herramientas ejecutables en Google Colab</span>
      <h1>Predicción, clasificación visual y recomendación para una empresa de transporte</h1>
      <p>La entrega separa las herramientas de trabajo del reporte técnico. Cada Colab se puede ejecutar de forma independiente y termina con una sección de uso lista para demostrar.</p>
    </div>
    <aside class="hero-visual" aria-label="Resumen visual del sistema">
      <div class="route-chart" aria-hidden="true">{hero_bars}</div>
      <div class="visual-caption">
        <span><strong>Demanda</strong>Pronóstico por ruta</span>
        <span><strong>Seguridad</strong>Clasificación visual</span>
        <span><strong>Usuarios</strong>Top destinos</span>
      </div>
    </aside>
  </section>
  <section class="section kpis">
    <div class="kpi"><strong>3</strong><span>herramientas Colab independientes</span></div>
    <div class="kpi"><strong>30 días</strong><span>de pronóstico futuro por ruta</span></div>
    <div class="kpi"><strong>7 pruebas</strong><span>validación automática del flujo</span></div>
  </section>
  <section class="grid">
    {''.join(cards_html)}
  </section>
  <section class="section">
    <h2>Flujo de la solución</h2>
    <div class="pipeline">
      <div class="step"><span>1</span><h3>Datos</h3><p>Series por ruta, imágenes de conducción e historial usuario-destino.</p></div>
      <div class="step"><span>2</span><h3>Modelos</h3><p>Regresión temporal, clasificador visual y filtrado colaborativo.</p></div>
      <div class="step"><span>3</span><h3>Métricas</h3><p>MAE/RMSE, accuracy/F1 y Precision@K/Recall@K.</p></div>
      <div class="step"><span>4</span><h3>Uso</h3><p>Colabs ejecutables, demo web y reporte técnico publicado.</p></div>
    </div>
  </section>
  <section class="section evidence">
    <figure class="shot">
      <img src="assets/app_demanda.png" alt="Vista de predicción de demanda en la herramienta web">
    </figure>
    <aside class="metric-list">
      <div class="metric"><b><span>Demanda</span><span>MAPE 8.24%</span></b><div class="meter"><i style="width:78%"></i></div></div>
      <div class="metric"><b><span>Visión</span><span>F1 0.448</span></b><div class="meter"><i style="width:45%"></i></div></div>
      <div class="metric"><b><span>Recomendación</span><span>Recall@5 1.00</span></b><div class="meter"><i style="width:100%"></i></div></div>
      <div class="metric"><b><span>Reporte</span><span>GitHub Pages</span></b><div class="meter"><i style="width:100%"></i></div></div>
    </aside>
  </section>
  <section class="section panel">
    <h2>Reporte aparte</h2>
    <p>El reporte técnico se mantiene como una página independiente con resumen ejecutivo, metodología, desarrollo por módulo, resultados, ética, conclusiones, anexos y bibliografía.</p>
    <div class="links-row">
      <a class="button" href="reporte.html">Ver reporte técnico</a>
      <a class="button ghost" href="assets/app_demanda.png">Ver captura</a>
      <a class="button ghost" href="datasets_reales.md">Fuentes de datos</a>
    </div>
  </section>
</main>
"""
    return page("Herramientas - Sistema Inteligente de Transporte", body)


def build_report() -> str:
    body = f"""
<main class="wrap">
  <header class="topbar">
    <div class="brand">Reporte Técnico</div>
    <nav class="nav">
      <a href="./">Herramientas</a>
      <a href="https://github.com/AndresGuido9820/sistema-transporte-inteligente">Repositorio</a>
    </nav>
  </header>
  <article class="report">
    {markdown_to_html(REPORT.read_text(encoding="utf-8"))}
  </article>
</main>
"""
    return page("Reporte tecnico - Sistema Inteligente de Transporte", body)


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    (DOCS / "index.html").write_text(build_index(), encoding="utf-8")
    (DOCS / "reporte.html").write_text(build_report(), encoding="utf-8")


if __name__ == "__main__":
    main()
