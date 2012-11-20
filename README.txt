TO RUN THE TESTS:
> python tests.py
"These tests cover the vectorization of movies, the knn core algorithm, and then finally the integration of both."

TO RUN THE PROGRAM:
> python rating_predictor.py classify_movies.json
----------------------------------------------------------------------------------------------------------------------------
CORE FILES:
knn.py: "The core knn algorithm, takes in a trained dict of movies, and then finally classifies a movie based on this trained data"
vectorization.py: "Takes in a json file, and formats and vectorizes it in such a way that it can be classified. Applies weights to vectors"
tests.py: "Tests over basic functionality"
rating_predictor.py: "Trains the data and executes the knn algorithm"
utils.py: "Reads json file from command line input"
----------------------------------------------------------------------------------------------------------------------------

Authors: Mohamed Sleem, Luis Perozo
