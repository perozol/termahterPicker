TO RUN THE PROGRAM:
> mongod

On another terminal
> python server.py

----------------------------------------------------------------------------------------------------------------------------
CORE FILES:
classifies a movie based on this trained data"
knn.py: "The core knn algorithm, takes in a trained dict of movies, and then finally 
moviesearch.py: "Boolean retrieval search engine"
mv.json: "Data used to train classifier"
rating_predictor.py: "Trains the data and executes the knn algorithm"
serve.py: "Implementation of local server"
settings.py: "Establishes ports to use for server and database"
static: "Contains all the front end files: HTML, javascript, css, etc"
utils.py: "Reads json files and established db connection"
upcomingReleases.py: "Uses Rotten Tomatoes API to get movies coming out in theaters."
vectorization.py: "Takes in a json file, and formats and vectorizes it in such a way that it can be classified. Applies weights to vectors"


DEPENDENCIES:
ujson
stemming
pymongo
----------------------------------------------------------------------------------------------------------------------------

Authors: Mohamed Sleem, Luis Perozo
