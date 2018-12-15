The folder contains the experimentation python files.

-Aggregating_AC2.py: The python code for aggregating judgements from AC2 dataset using different algorithms in Algorithms folder

-item_model.py: Model for items which is labeled by crow workers.

-user_model.py: Model for crow worker.

-graph_builder.py: builder the relationship between items and workers, for example, assign the observed label for the corresponding item. For the item, record the workers who labeled it.

The aggregating algorithms will be applied to the built graph, which including the relations between items and workers.
