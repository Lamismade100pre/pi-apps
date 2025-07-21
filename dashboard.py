import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import (
    df_hoy, df_semana_actual, df_mes_actual, df_año_actual,
    df_mes_pasado_enero, df_mes_pasado_febrero, df_mes_pasado_marzo,
    df_mes_pasado_abril, df_mes_pasado_mayo, df_mes_pasado_junio
)

# --- Dataframes ---
df_hoy = df_hoy
df_semana_actual = df_semana_actual
df_mes_actual = df_mes_actual
df_año_actual = df_año_actual

# --- Totals ---
total_hoy_nuevo = df_hoy['Nuevo'].sum()
total_hoy_guiones = df_hoy['Guiones'].sum()

total_semana_actual_nuevo = df_semana_actual['Nuevo'].sum()
total_semana_actual_guiones = df_semana_actual['Guiones'].sum()

total_mes_actual_nuevo = df_mes_actual['Nuevo'].sum()
total_mes_actual_guiones = df_mes_actual['Guiones'].sum()

total_año_actual_nuevo = df_año_actual['Nuevo'].sum()
total_año_actual_guiones = df_año_actual['Guiones'].sum()

# --- KPIs ---
fig_kpis = make_subplots(
    rows=1, cols=4,
    specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
    vertical_spacing=0.2
)

fig_kpis.add_trace(go.Indicator(
    mode="number",
    value=total_hoy_nuevo,
    title={"text": "<b>Hoy (Nuevo)</b>", "font": {"size": 16}},
    number={'font': {'size': 40, 'color': '#2ca02c'}},
), row=1, col=1)

fig_kpis.add_trace(go.Indicator(
    mode="number",
    value=total_semana_actual_nuevo,
    title={"text": "<b>Semana Actual (Nuevo)</b>", "font": {"size": 16}},
    number={'font': {'size': 40, 'color': '#2ca02c'}},
), row=1, col=2)

fig_kpis.add_trace(go.Indicator(
    mode="number",
    value=total_mes_actual_nuevo,
    title={"text": "<b>Mes Actual (Nuevo)</b>", "font": {"size": 16}},
    number={'font': {'size': 40, 'color': '#2ca02c'}},
), row=1, col=3)

fig_kpis.add_trace(go.Indicator(
    mode="number",
    value=total_año_actual_nuevo,
    title={"text": "<b>Año Actual (Nuevo)</b>", "font": {"size": 16}},
    number={'font': {'size': 40, 'color': '#2ca02c'}},
), row=1, col=4)

fig_kpis.update_layout(
    title_text="<b>Resumen de Productividad (Diseños Nuevos)</b>",
    title_x=0.5,
    title_font_size=24,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#333',
    height=250
)

# --- Designer Ranking (Current Month) ---
df_mes_actual_sorted = df_mes_actual.sort_values(by='Nuevo', ascending=False)
fig_ranking_nuevo = go.Figure(go.Bar(
    x=df_mes_actual_sorted['Nuevo'],
    y=df_mes_actual_sorted['Diseñador'],
    orientation='h',
    marker_color='#1f77b4',
    text=df_mes_actual_sorted['Nuevo'],
    textposition='auto'
))
fig_ranking_nuevo.update_layout(
    title_text="<b>Ranking de Diseñadores por Productividad (Mes Actual)</b>",
    title_x=0.5,
    xaxis_title="Diseños Nuevos",
    yaxis_title="Diseñador",
    yaxis={'categoryorder':'total ascending'},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(240, 240, 240, 0.95)',
    font_color='#333',
    height=600
)

df_mes_actual_sorted_guiones = df_mes_actual.sort_values(by='Guiones', ascending=False)
fig_ranking_guiones = go.Figure(go.Bar(
    x=df_mes_actual_sorted_guiones['Guiones'],
    y=df_mes_actual_sorted_guiones['Diseñador'],
    orientation='h',
    marker_color='#d62728',
    text=df_mes_actual_sorted_guiones['Guiones'],
    textposition='auto'
))
fig_ranking_guiones.update_layout(
    title_text="<b>Ranking de Diseñadores por Errores (Mes Actual)</b>",
    title_x=0.5,
    xaxis_title="Guiones (Errores)",
    yaxis_title="Diseñador",
    yaxis={'categoryorder':'total ascending'},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(240, 240, 240, 0.95)',
    font_color='#333',
    height=600
)

# --- Monthly Trend ---
monthly_data = {
    'Enero': df_mes_pasado_enero,
    'Febrero': df_mes_pasado_febrero,
    'Marzo': df_mes_pasado_marzo,
    'Abril': df_mes_pasado_abril,
    'Mayo': df_mes_pasado_mayo,
    'Junio': df_mes_pasado_junio
}

monthly_summary = {
    'Mes': [],
    'Total Nuevo': [],
    'Total Guiones': []
}

for month, df in monthly_data.items():
    monthly_summary['Mes'].append(month)
    monthly_summary['Total Nuevo'].append(df['Nuevo'].sum())
    monthly_summary['Total Guiones'].append(df['Guiones'].sum())

df_monthly_summary = pd.DataFrame(monthly_summary)

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=df_monthly_summary['Mes'],
    y=df_monthly_summary['Total Nuevo'],
    mode='lines+markers',
    name='Diseños Nuevos',
    line=dict(color='#2ca02c', width=2),
    marker=dict(size=8)
))
fig_trend.add_trace(go.Scatter(
    x=df_monthly_summary['Mes'],
    y=df_monthly_summary['Total Guiones'],
    mode='lines+markers',
    name='Guiones (Errores)',
    line=dict(color='#d62728', width=2),
    marker=dict(size=8)
))
fig_trend.update_layout(
    title_text="<b>Tendencia Mensual de Productividad y Errores</b>",
    title_x=0.5,
    xaxis_title="Mes",
    yaxis_title="Cantidad",
    legend_title="Métrica",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(240, 240, 240, 0.95)',
    font_color='#333',
    height=500
)

# --- Effectiveness Ratio ---
df_mes_actual['Efectividad'] = df_mes_actual['Guiones'] / df_mes_actual['Nuevo']
df_mes_actual['Efectividad'] = df_mes_actual['Efectividad'].fillna(0).round(2) # Handle division by zero and round

df_efectividad_sorted = df_mes_actual.sort_values(by='Efectividad', ascending=True)

fig_efectividad = go.Figure(go.Bar(
    x=df_efectividad_sorted['Efectividad'],
    y=df_efectividad_sorted['Diseñador'],
    orientation='h',
    marker_color='#ff7f0e',
    text=df_efectividad_sorted['Efectividad'],
    textposition='auto'
))
fig_efectividad.update_layout(
    title_text="<b>Ratio de Efectividad (Guiones/Nuevo) - Mes Actual (Menor es Mejor)</b>",
    title_x=0.5,
    xaxis_title="Ratio de Efectividad",
    yaxis_title="Diseñador",
    yaxis={'categoryorder':'total descending'},
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(240, 240, 240, 0.95)',
    font_color='#333',
    height=600
)

# --- Top 5 Performers ---
top_5_productividad = df_mes_actual.nlargest(5, 'Nuevo')
top_5_efectividad = df_mes_actual[df_mes_actual['Nuevo'] > 0].nsmallest(5, 'Efectividad') # Exclude those with 0 new designs for fairness

fig_top_prod = go.Figure(data=[go.Table(
    header=dict(values=list(top_5_productividad.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[top_5_productividad.Diseñador, top_5_productividad.Nuevo, top_5_productividad.Guiones, top_5_productividad.Efectividad],
               fill_color='lavender',
               align='left'))
])
fig_top_prod.update_layout(title_text="<b>Top 5 - Mayor Productividad (Mes Actual)</b>", title_x=0.5)

fig_top_efec = go.Figure(data=[go.Table(
    header=dict(values=list(top_5_efectividad.columns),
                fill_color='lightcoral',
                align='left'),
    cells=dict(values=[top_5_efectividad.Diseñador, top_5_efectividad.Nuevo, top_5_efectividad.Guiones, top_5_efectividad.Efectividad],
               fill_color='lavender',
               align='left'))
])
fig_top_efec.update_layout(title_text="<b>Top 5 - Mejor Efectividad (Mes Actual)</b>", title_x=0.5)


# --- Averages ---
avg_nuevo = df_mes_actual['Nuevo'].mean()
avg_guiones = df_mes_actual['Guiones'].mean()

fig_avg = make_subplots(rows=1, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}]])
fig_avg.add_trace(go.Indicator(
    mode = "number",
    value = round(avg_nuevo, 2),
    title = {"text": "<b>Promedio de Diseños Nuevos (por diseñador)</b>"}
), row=1, col=1)
fig_avg.add_trace(go.Indicator(
    mode = "number",
    value = round(avg_guiones, 2),
    title = {"text": "<b>Promedio de Guiones (por diseñador)</b>"}
), row=1, col=2)
fig_avg.update_layout(title_text="<b>Promedios del Equipo (Mes Actual)</b>", title_x=0.5)


# --- Show figures ---
if __name__ == "__main__":
    # Create a single HTML file with all figures
    with open("dashboard.html", 'w') as f:
        f.write("<html><head><title>Dashboard de Productividad</title></head><body>")
        f.write("<h1 style='text-align: center;'>Dashboard de Estadísticas de Productividad</h1>")

        f.write(fig_kpis.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write("<hr>")
        f.write(fig_avg.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write(fig_ranking_nuevo.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write(fig_ranking_guiones.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write(fig_efectividad.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write(fig_top_prod.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write(fig_top_efec.to_html(full_html=False, include_plotlyjs=False))
        f.write("<hr>")
        f.write(fig_trend.to_html(full_html=False, include_plotlyjs=False))

        f.write("</body></html>")

    print("Dashboard guardado como dashboard.html")
