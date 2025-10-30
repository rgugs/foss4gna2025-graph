import pandas as pd
from pyvis.network import Network

COLORS = [
    '#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#06b6d4',
    '#f97316', '#14b8a6', '#6366f1', '#84cc16', '#f43f5e', '#a855f7'
]

def read_csv(input_csv):
    """Load CSV into a pandas DataFrame."""
    return pd.read_csv(input_csv, encoding='latin-1')

def get_track_colors(tracks, colors):
    """Return color mapping for track categories."""
    if len(colors) < len(tracks):
        raise ValueError(f"Not enough colors for all tracks.")
    colors_needed = colors[:len(tracks)]
    return dict(zip(tracks, colors_needed))

def create_network():
    """Create and configure a pyvis Network object."""
    net = Network(height='800px', width='100%', bgcolor='#222222', font_color='white')
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=200)
    # net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08, damping=0.4, overlap=0)
    return net

def add_track_nodes(net, track_colors):
    """Add track category nodes to the network."""
    for track, color in track_colors.items():
        net.add_node(
            track, 
            label=track, 
            shape='box', 
            color=color, 
            size=30,
            font={'size': 16}, 
            title=track
        )

def add_tag_nodes(net, df, track_colors):
    """Add unique tag nodes to the network with matching track colors."""
    # Collect all unique tags from Tag1, Tag2, Tag3 columns
    all_tags = set()
    for col in ['Tag1', 'Tag2', 'Tag3']:
        if col in df.columns:
            tags = df[col].dropna()
            # Filter out empty strings and NaN values
            tags = tags[tags.astype(str).str.strip() != '']
            all_tags.update(tags.unique())
    
    print(f"Found {len(all_tags)} unique tags: {sorted(all_tags)}")
    
    # Add tag nodes with diamond shape and matching track colors
    for tag in all_tags:
        # Get the color for this tag from track_colors
        # Tags should match the same track name's color
        tag_color = track_colors.get(tag, '#64748b')  # Default to gray if not found
        
        net.add_node(
            f"tag_{tag}",  # Prefix to distinguish from track nodes
            label=tag,
            shape='diamond',  # Unique shape for tags
            color=tag_color,
            size=20,
            font={'size': 12},
            title=f"Tag: {tag}"
        )

def add_session_nodes(net, df):
    """Add session nodes and edges to the network."""
    for idx, row in df.iterrows():
        session_id = f"session_{idx}"
        title_text = f"{row['Session Title']}\nDate: {row['Date']}\nType: {row['Type']}"
        label = row['Session Title'][:30] + '...' if len(row['Session Title']) > 30 else row['Session Title']
        
        # Different shapes for different types
        shape = 'triangle' if row['Type'] == 'Workshop' else 'dot'
        
        net.add_node(
            session_id,
            label=label,
            title=title_text,
            color='#bdc3c7',
            size=15,
            shape=shape,
            date=row['Date'],
            type=row['Type'],
            track=row['Tracks']
        )
        
        # Connect to primary track
        net.add_edge(session_id, row['Tracks'], color='#95a5a6')
        
        # Connect to tag nodes
        for tag_col in ['Tag1', 'Tag2', 'Tag3']:
            if tag_col in df.columns and pd.notna(row[tag_col]):
                tag_value = str(row[tag_col]).strip()
                if tag_value and tag_value != '':
                    tag_node_id = f"tag_{tag_value}"
                    # Use a different color/style for tag connections
                    net.add_edge(session_id, tag_node_id, color='#64748b', dashes=True)

def prepare_filter_data(df):
    """Prepare filter options from the dataframe."""
    filter_data = {
        'dates': sorted(df['Date'].unique().tolist()),
        'types': sorted(df['Type'].unique().tolist()),
        'tracks': sorted(df['Tracks'].unique().tolist())
    }
    
    # Add tags to filter data
    all_tags = set()
    for col in ['Tag1', 'Tag2', 'Tag3']:
        if col in df.columns:
            tags = df[col].dropna()
            # Filter out empty strings
            tags = tags[tags.astype(str).str.strip() != '']
            all_tags.update(tags.unique())
    
    filter_data['tags'] = sorted(list(all_tags))
    print(f"Filter data tags: {filter_data['tags']}")
    
    return filter_data

def generate_filter_html(filter_data, template_path='template.html'):
    """Generate HTML for filter controls from template file."""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    date_options = ''.join(f'<option value="{d}">{d}</option>' for d in filter_data['dates'])
    type_options = ''.join(f'<option value="{t}">{t}</option>' for t in filter_data['types'])
    track_options = ''.join(f'<option value="{t}">{t}</option>' for t in filter_data['tracks'])
    tag_options = ''.join(f'<option value="{t}">{t}</option>' for t in filter_data['tags'])
    
    return template.replace('{date_options}', date_options) \
                   .replace('{type_options}', type_options) \
                   .replace('{track_options}', track_options) \
                   .replace('{tag_options}', tag_options)

def inject_controls(html_path, control_html):
    """Inject filter controls into the generated HTML."""
    with open(html_path, 'r', encoding='utf-8') as f:
        pyvis_html = f.read()
    
    # Extract CSS (between <style> and </style>)
    css_match = control_html[control_html.find('<style>'):control_html.find('</style>') + 8]
    
    # Extract legend and controls (between body opening and mynetwork div)
    body_start = control_html.find('<body>') + 6
    mynetwork_pos = control_html.find('<div id="mynetwork"></div>')
    controls_section = control_html[body_start:mynetwork_pos].strip()
    
    # Extract just the JavaScript code (without <script> tags)
    script_start = control_html.find('<script>') + 8
    script_end = control_html.find('</script>')
    script_code = control_html[script_start:script_end].strip()
    
    # Inject CSS into head (before </head>)
    pyvis_html = pyvis_html.replace('</head>', f'{css_match}\n</head>', 1)
    
    # Inject controls at the beginning of body (after <body>)
    pyvis_html = pyvis_html.replace('<body>', f'<body>\n{controls_section}\n', 1)
    
    # Find the existing script tag and inject our code at the end
    last_script_pos = pyvis_html.rfind('</script>')
    if last_script_pos != -1:
        pyvis_html = pyvis_html[:last_script_pos] + f'\n\n{script_code}\n' + pyvis_html[last_script_pos:]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(pyvis_html)

def generate_graph(csv_path, output_path):
    """Main function to generate the interactive graph."""
    # Load data
    df = read_csv(csv_path)
    
    # Remove rows with missing Tracks
    df = df.dropna(subset=['Tracks'])
    
    # Debug: Check what columns exist
    print(f"Columns in CSV: {df.columns.tolist()}")
    print(f"\nFirst few rows of Tag columns:")
    for col in ['Tag1', 'Tag2', 'Tag3']:
        if col in df.columns:
            print(f"{col}: {df[col].head()}")
            print(f"  Non-null count: {df[col].notna().sum()}")
            print(f"  Non-empty count: {(df[col].astype(str).str.strip() != '').sum()}")
        else:
            print(f"{col}: Column not found!")
    
    # Create network
    net = create_network()
    
    # Get unique tracks and colors
    tracks = sorted(df['Tracks'].unique())
    colors = get_track_colors(tracks, COLORS)
    
    # Add nodes and edges
    add_track_nodes(net, colors)
    add_tag_nodes(net, df, colors)  # Pass colors to tag nodes
    add_session_nodes(net, df)
    
    # Save initial graph
    net.save_graph(output_path)
    
    # Prepare and inject filter controls
    filter_data = prepare_filter_data(df)
    control_html = generate_filter_html(filter_data)
    inject_controls(output_path, control_html)
    
    print(f"Graph generated: {output_path}")
    print("This file can be embedded in Quarto or hosted on GitHub Pages.")
    print(f"\nAdded {len(filter_data['tags'])} unique tag nodes")

def main():
    """Entry point for the script."""
    csv_file = 'Output_Graph_Data_Tagged.csv'
    output_file = 'conference_graph.html'
    
    generate_graph(csv_file, output_file)

if __name__ == "__main__":
    main()