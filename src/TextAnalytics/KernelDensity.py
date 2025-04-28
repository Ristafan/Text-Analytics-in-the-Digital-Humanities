from textplot.text import Text
from textplot.graphs import Skimmer
from textplot.matrix import Matrix


# Load the text
text = Text.from_file("C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/bible.txt")

# View the number of tokens (excluding stopwords)
print(f"Number of tokens: {len([t for t in text.tokens if t is not None])}")

# Create a term matrix
matrix = Matrix()
matrix.index(text)

# Build the graph
graph = Skimmer()
graph.build(text, matrix, skim_depth=3)

# Draw the graph (spring layout)
graph.draw_spring()

# Save the graph to a GML file
#graph.write_gml("C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/bible.gml")
graph.write_graphml("C:/Users/marti/documents/Text-Analytics-in-the-Digital-Humanities/data/bible.graphml")

