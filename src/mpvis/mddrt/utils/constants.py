GRAPHVIZ_STATE_NODE = '<table cellpadding="3" cellborder="1" cellspacing="0" border="0" style="rounded">{}</table>'

GRAPHVIZ_STATE_NODE_ROW = '<tr><td bgcolor="{}"><font face="arial" color="white">{}</font></td></tr>'

GRAPHVIZ_ACTIVITY = '<table cellpadding="0" cellborder="0" cellspacing="0" border="0" style="rounded">{}</table>'
GRAPHVIZ_ACTIVITY_DATA = '<tr><td bgcolor="snow"><font face="arial" color="black">{}</font></td></tr>'
GRAPHVIZ_ACTIVITY_DATA_COLORED = '<tr><td bgcolor="snow"><font face="arial" color="{}">{}</font></td></tr>'

# Arc text colors by dimension
ARC_TEXT_COLORS = {
    "time": "#FF6B35",        # Orange/Red for time metrics
    "cost": "#4CAF50",        # Green for cost metrics
    "quality": "#2196F3",     # Blue for quality (rework)
    "flexibility": "#9C27B0"  # Purple for flexibility (optional)
}
