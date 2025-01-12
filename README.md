# EModelDB
Database of empirical substitution models of protein evolution
Iglesias-Rivas, Paula, Del Amparo, Roberto,  Arenas, Miguel.

Substitution models of evolution describe the relative rates of fixation of mutations and can be useful to predict relevant evolutionary
events, such as resistance mutations in protein drug targets, along an evolutionary history.

This database was created as a necessity to comprise at least the most relevants models as well as their classification. 
It contains different documents such as the database (models.db), the folder with the matrices (data) and
the graphical interface to manage the database (interface_EModelDB.py). 

The data folder used  for the creation of the database is not necessary for the functioning of the interface, 
it is merely informative. 

The graphical interface works thanks to the models.db file. As a requirement, it is necessary to have
Python and Streamlit installed and the libraries associated with the code, which are indicated at the beginning of the code.  

The interface can be executed from the terminal by putting from the folder containing the files 
"streamlit run interface_EModelDB". Once the interface is executed, a window appears with all the models present in
the database together with other characteristics such as: the date, author(s), a link to the article, the taxonomic 
group to which the model is addressed and comments that were considered necessary to be made.  The models can be 
filtered according to these characteristics, for example in case we only want the models of a specific taxonomic group.

To dowload the matrix (or matrices), just select the desired model or models and click on the download button at the bottom of the interface.


Future updates to the database will involve adding new models and possibly modifying the schema to accommodate additional types of data 
relevant to protein evolution research. The interface will also undergo changes in order to make it more useful. 
If you have any questions, please send an email to:

paula.iglesias.rivas@uvigo.es

