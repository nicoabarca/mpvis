import pandas as pd
import mpvis

# Load event log
dron_event_log_path = "mesa_ayuda.csv"

# Read event log
dron_event_log = pd.read_csv(dron_event_log_path, sep=";")

# Verificar columnas
dron_event_log['Fin'] = pd.to_datetime(dron_event_log['Fin'], format='%Y-%m-%d %H:%M:%S')
dron_event_log['Inicio'] = pd.to_datetime(dron_event_log['Inicio'], format='%Y-%m-%d %H:%M:%S')

# CORREGIDO: Key es el formato requerido por pm4py/mpvis
# Value es el nombre real de la columna en tu CSV
dron_event_log_format = {
    "case:concept:name": "ID Caso",           # Corregido: era "Case ID"
    "concept:name": "Actividad",              # Corregido: era "Activity" 
    "time:timestamp": "Fin",                  # Corregido: era "Complete"
    "start_timestamp": "Inicio",              # Corregido: era "Start"
    "resource": "Ejecutor",                   # Corregido: era "Resource"
    # "cost:total": "Cost",                   # No tienes columna de costo, comentado
}

# Format event log
formatted_event_log = mpvis.log_formatter(
    log=dron_event_log, log_format=dron_event_log_format
)

# Manual log grouping of activities
# Las actividades a agrupar deben usar los nombres exactos de tu CSV
activities_to_group = [
    # Aquí deberías poner los nombres exactos que aparecen en 'Nombre Actividad'
    # Por ejemplo, si quieres agrupar algunas actividades del proceso de drones
]

# Solo ejecutar si hay actividades para agrupar
if activities_to_group:
    manual_grouped_event_log = mpvis.preprocessing.manual_log_grouping(
        log=formatted_event_log,
        activities_to_group=activities_to_group,
        group_name="Grouped activities",
    )
else:
    manual_grouped_event_log = formatted_event_log

# Prune the log based on the top variants
pruned_event_log = mpvis.preprocessing.prune_log_based_on_top_variants(
    log=formatted_event_log, k=3
)

# MPDFG Functions
# Discover Multi-Perspective DFG
(multi_perspective_dfg, start_activities, end_activities) = (
    mpvis.mpdfg.discover_multi_perspective_dfg(
        log=formatted_event_log,
        calculate_frequency=True,
        calculate_time=True,
        calculate_cost=False,  # Cambiado a False porque no tienes columna de costo
        frequency_statistic="absolute-activity",
        time_statistic="mean",
        # cost_statistic="mean",  # Comentado porque no hay costos
    )
)

# Filter Multi-Perspective DFG by activities
activities_filtered_multi_perspective_dfg = mpvis.mpdfg.filter_multi_perspective_dfg_activities(
    percentage=1,
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    sort_by="frequency",
    ascending=True,
)

# Filter Multi-Perspective DFG by paths
paths_filtered_multi_perspective_dfg = mpvis.mpdfg.filter_multi_perspective_dfg_paths(
    percentage=1,
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    sort_by="frequency",
    ascending=True,
)

# Get Multi-Perspective DFG string
multi_perspective_dfg_string = mpvis.mpdfg.get_multi_perspective_dfg_string(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=False,  # Cambiado a False
    cost_currency="USD",
    rankdir="TD",
    diagram_tool="graphviz",
    arc_thickness_by="time"  # Ejemplo de uso del nuevo parámetro
)

# View Multi-Perspective DFG
mpvis.mpdfg.view_multi_perspective_dfg(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=False,  # Cambiado a False
    arc_thickness_by="time"  # Ejemplo de uso del nuevo parámetro
)

# Save Multi-Perspective DFG
mpvis.mpdfg.save_vis_multi_perspective_dfg(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    file_name="multi_perspective_dfg_time",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=False,  # Cambiado a False
    diagram_tool="graphviz",
    arc_thickness_by="time"  # Ejemplo de uso del nuevo parámetro
)
# Quiero generar las imagenes MPDFG pero con arc_thickness_by="frequency" and arc_thickness_by="none"
# Save Multi-Perspective DFG with arc thickness by frequency
mpvis.mpdfg.save_vis_multi_perspective_dfg(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    file_name="multi_perspective_dfg_frequency",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=False,  # Cambiado a False
    diagram_tool="graphviz",
    arc_thickness_by="frequency"  # Cambiado a frequency
)               
# Save Multi-Perspective DFG with arc thickness by none
mpvis.mpdfg.save_vis_multi_perspective_dfg(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    file_name="multi_perspective_dfg_none",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=False,  # Cambiado a False
    diagram_tool="graphviz",
    arc_thickness_by="none"  # Cambiado a none
)

# MDDRT Functions
# Descubre el Multi-Dimensional DRT usando el event log formateado
# multi_dimensional_drt = mpvis.mddrt.discover_multi_dimensional_drt(
#     log=formatted_event_log,
#     calculate_time=True,
#     calculate_cost=False,        # No hay columna de costo en el CSV
#     calculate_quality=True,
#     calculate_flexibility=True,
#     group_activities=False,
#     show_names=False,
# )

# Obtiene el string de la visualización del Multi-Dimensional DRT
# multi_dimensional_drt_string = mpvis.mddrt.get_multi_dimensional_drt_string(
#     multi_dimensional_drt=multi_dimensional_drt,
#     visualize_time=True,
#     visualize_cost=False,        # No hay columna de costo en el CSV
#     visualize_flexibility=True,
#     visualize_quality=True,
#     node_measures=["total", "consumed", "remaining"],
#     arc_measures=["avg", "min", "max"],
# )

# Muestra la visualización del Multi-Dimensional DRT
# mpvis.mddrt.view_multi_dimensional_drt(
#     multi_dimensional_drt=multi_dimensional_drt,
#     visualize_time=True,
#     visualize_cost=False,        # No hay columna de costo en el CSV
#     visualize_flexibility=True,
#     visualize_quality=True,
#     node_measures=["total", "consumed", "remaining"],
#     arc_measures=["avg", "min", "max"],
#     format="svg",
# )

# Guarda la visualización del Multi-Dimensional DRT en un archivo SVG
# mpvis.mddrt.save_vis_multi_dimensional_drt(
#     multi_dimensional_drt=multi_dimensional_drt,
#     file_path="multi_dimensional_drt.svg",
#     visualize_time=True,
#     visualize_cost=False,        # No hay columna de costo en el CSV
#     visualize_flexibility=True,
#     visualize_quality=True,
#     node_measures=["total", "consumed", "remaining"],
#     arc_measures=["avg", "min", "max"],
#     format="svg",
# )

# Discover Multi-Dimensional DRT
print("Discovering Multi-Dimensional DRT...")
drt = mpvis.mddrt.discover_multi_dimensional_drt(
    log=formatted_event_log,
    calculate_time=True,
    calculate_cost=True,
    calculate_quality=True,
    calculate_flexibility=True,
    group_activities=False,
    show_names=False,
)

# Visualize with arc measures to see colored text
print("Generating visualization with colored arc text...")
print("Colors used:")
print("  - Time metrics (Service Time, Lead Time): Orange/Red (#FF6B35)")
print("  - Cost metrics: Green (#4CAF50)")
print("  - Quality metrics (Rework): Blue (#2196F3)")
print("  - Flexibility metrics (Optional): Purple (#9C27B0)")
print()

# View the DRT with arc measures enabled
mpvis.mddrt.view_multi_dimensional_drt(
    multi_dimensional_drt=drt,
    visualize_time=True,
    visualize_cost=True,
    visualize_quality=True,
    visualize_flexibility=True,
    node_measures=["total", "consumed", "remaining"],
    arc_measures=["avg", "min", "max"],  # This enables arc text with colors!
    format="svg",
)

# Save the visualization
print("Saving visualization to file...")
mpvis.mddrt.save_vis_multi_dimensional_drt(
    multi_dimensional_drt=drt,
    file_path="mddrt_colored_arcs.svg",
    visualize_time=True,
    visualize_cost=True,
    visualize_quality=True,
    visualize_flexibility=True,
    node_measures=["total"],
    arc_measures=["avg", "min", "max"],
    format="svg",
)