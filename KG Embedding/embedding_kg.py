from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
import pandas as pd

# Carregar KG (arquivo de triplas)
df = pd.read_csv(
    "../Dataset/MetaQA/kb.txt", 
    sep="|",
    header = None,
    encoding = "utf-8"
    )

tf = TriplesFactory.from_labeled_triples(df.values)

result = pipeline(
    model='ComplEx',
    training=tf,
    testing=tf,
    validation=tf,
    model_kwargs=dict(embedding_dim=200),
    training_kwargs=dict(num_epochs=100),
)