# PACRR Neural Net Retrieval

## Introduction
---
This part contains our simple classifier that retrieves as many results as it can for re-ranking by the PACRR neural net.

This repository contains the IR folder which is the package that contains our "_src"_ folder. All of the code is found there.

## Main Class
---
Index - gets a String path to the data to index and IndexWriter. The data is read from “path” and formed into java objects via Gson’s fromJson function. The data is then indexed in the index by using Lucene’s IndexWriter and by iterating over each object and storing relevant fields. 
This function is to be called at the start of every run of the system to set up an index containing all given data.

Retrieve - gets a query and an IndexSearcher and returns any results for the query that were retrieved from the index. By using Lucene’s IndexSearcher.search function we can retrieve documents from the index by using the IndexSearcher’s configurations to define the retrieval method. We then extract the information from the retrieved docs and store them in objects, and return them.
This function is used to retrieve answers for queries from the index. As previously mentioned the retrieval method is defined by the index searcher.

Write_answers - gets a String path and a list of results to write to path. Using Gson’s toJson function we write the input list of answers to a json file. 
This function is used to write the result of the “Retrieve” function into a json file for later use.

Write_questions - gets to String paths, one for the input and one for the output. Using Gson’s fromJson we read the data from the input path and store it in objects. Then we extract the relevant information from the input and write it to the target file. 
This function was used to extract the questions from the yahoo database and then store them in a file to be used for testing.

Main_func - first we call the function “write_questions” if we need to generate a question file. Once we have a question file there is no need to generate a new one each time we run the code.
We then proceed to initialize parameters such as an index writer.
After we have finished initialization we proceed to open a directory where we want our index to be. Now we have everything that we need to open the index so we call “index”.
Now that we have an index we create an index reader and searcher.
Now we read the questions we need to answer from a text file. For each question we parse it and pass it to the “retrieve” function to get back a list of possible answers.
After we have gathered answers for all questions we can call “write_answers” to write the answers to a json file.
