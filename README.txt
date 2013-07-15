Digvijay Singh, UNI: ds3161
Rohan Agrawal, UNI: ra2616

List of Files:-----------------------------------------------------------------------

qprober.py
root.txt
computers.txt
health.txt
sports.txt
run.sh

How to Run:--------------------------------------------------------------------------

1.Go to the directory ds3161-proj2 and type: 
python qprober.py <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>

2.Alternatively,you can run the program through our makefile 'run.sh' in the following way:
chmod +x run.sh
./run.sh <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>


Internal Design:---------------------------------------------------------------------

1.We store all the queries at level 0 (root) and level 1 (computers,sports,health) from the 4 files root.txt, computers.txt, health.txt and sports.txt in a dictionary named "rules", in which the category is the key and the queries associated with that catergory are its value. 

2.Then there is another dictionary "categories" which stores the parent child relationship of the categories in the form of key, value pairs in the dictionary (key is the parent and its value are its children)

3.The dictionary "covspec" stores the coverage and specificity for each category. The category name is the key while the value is 2 member list,first member being the coverage and the second member being the specificity,initialized to [0,0] (except the root whose specificity is 1, as defined in the research paper by Prof. Gravano)

4.The dictionary "cat_urls" stores the URLs of the document samples of each category in the classification (obtained from part 1 of the project)

5.1.We are storing our classifications in a list called "classif".The method by which we are doing so is : We start from a category (root initially) and give bing queries corresponding to that category. Side by side we store the top 4 URLs returned by each query  (to be used for the content summary) and also calculate the coverage and specificity, based on the metadata our composite query returned from bing. The formulae used are the same as given in the research paper.

5.2.Then if a particular category satisfies the condition on specificity and coverage threshold,we include it in our classification string (in "classif" dictionary) and continue searching in case the document can be categorized into more.

5.3.At each step we keep on adding our classification strings to the "classif" list. If in case after adding "root/health" we find that the database can be further classified into "root/health/diseases" , then we remove the previous string and append the new one (using our custom made my_append() function)

6.Moving onto part b of the project,we now iterate on each categort in the cat_urls dictionary and parse each of the URLs in their document samples (and hence tokenize,lowercase the text in them). We then count the document frequency of each word and produce it in the content summary of that category (if both parent and child are in the classification, then parent also contains the document samples of the child).
We do not go beyong "References" in the text and also ignore anything between [...]. We separate our words on the basis of ANY non english alphabet character.

NOTE### We have decided not to include multiple word information in the content summaries.

References:---------------------------------------------------------------------------

1. Christopher D. Manning, Prabhakar Raghavan, Hinrich Schütze: An Introduction to Information Retrieval, 2009.

2. Ipeirotis and Gravano: "Classification-Aware Hidden-Web Text Database Selection", ACM TOIS 2008.

3. Gravano, Ipeirotis, and Sahami: "QProber: A System for Automatic Classification of Hidden-Web Databases", ACM TOIS 2003.
