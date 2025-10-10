GRAPHVIZ_STATE_NODE = '<table cellpadding="3" cellborder="1" cellspacing="0" border="0" style="rounded">{}</table>'

GRAPHVIZ_STATE_NODE_ROW = '<tr><td bgcolor="{}"><font face="arial" color="white">{}</font></td></tr>'

GRAPHVIZ_ACTIVITY = '<table cellpadding="0" cellborder="0" cellspacing="0" border="0" style="rounded">{}</table>'
GRAPHVIZ_ACTIVITY_DATA = '<tr><td bgcolor="snow"><font face="arial" color="black">{}</font></td></tr>'
GRAPHVIZ_ACTIVITY_DATA_COLORED = '<tr><td bgcolor="snow"><font face="arial" color="{}">{}</font></td></tr>'

# New table-based format for arc labels
GRAPHVIZ_ARC_TABLE = '<table border="0" cellborder="1" cellspacing="0" cellpadding="4">{}</table>'
GRAPHVIZ_ARC_HEADER = '<tr><td colspan="2" bgcolor="white"><font face="arial"><b>{}</b></font></td></tr>'
GRAPHVIZ_ARC_DIMENSION_HEADER = '<tr><td colspan="2" bgcolor="{}"><font face="arial" color="white"><b>{}</b></font></td></tr>'
GRAPHVIZ_ARC_DATA_ROW = '<tr><td bgcolor="white"><font face="arial">{}</font></td><td bgcolor="white"><font face="arial">{}</font></td></tr>'

# Arc text colors by dimension (for text coloring - legacy)
ARC_TEXT_COLORS = {
    "time": "#FF6B35",        # Orange/Red for time metrics
    "cost": "#4CAF50",        # Green for cost metrics
    "quality": "#2196F3",     # Blue for quality (rework)
    "flexibility": "#9C27B0"  # Purple for flexibility (optional)
}

# Background colors for dimension headers in table format
ARC_HEADER_BG_COLORS = {
    "time": "#FF6B35",        # Orange/Red background
    "cost": "#4CAF50",        # Green background
    "quality": "#2196F3",     # Blue background
    "flexibility": "#9C27B0"  # Purple background
}
