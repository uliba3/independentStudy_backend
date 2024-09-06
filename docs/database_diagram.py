import os
import sys

# Set the current working directory as the parent directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath('..'))

from sqlalchemy_schemadisplay import create_schema_graph
from app.db.session import metadata, engine

# Create the graph
graph = create_schema_graph(metadata=metadata,
    show_datatypes=True,
    show_indexes=False,
    rankdir='LR',
    concentrate=False,
    engine=engine
)

# Output the graph
graph.write_png('database_diagram.png')