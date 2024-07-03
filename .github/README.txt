EModelDB. Database of empirical substitution models of protein evolution
Iglesias-Rivas, Paula, Del Amparo, Roberto,  Arenas, Miguel.

Substitution models of evolution describe the relative rates of fixation of mutations and can be useful to predict relevant evolutionary
events, such as resistance mutations in protein drug targets, along an evolutionary history.

This database was created as a necessity to comprise at least the most relevants models as well as their classification. 
It contains different documents such as the database (models.db), the folder with the matrices (data),
the code to create the database (dbesmpm.py) and the graphical interface to manage the database (interface_database_esmpm.py). 

The dbesmpm.py file for the creation of the database is not necessary for the functioning of the interface, 
it is merely informative about how it was created. It is important to note that, in case you want 
to run this script, it is necessary to pay attention to the directory where the 'data' folder is located.

The graphical interface works thanks to the models.db file. As a requirement, it is necessary to have
Python installed and the libraries associated with the code, which are indicated at the beginning of the code.  

The interface can be executed from Python as well as from PowerSell by putting from the folder containing the files "python3 interface_database_esmpm.py". Once the interface is executed, a window appears with all the models present in the database together with other
characteristics such as: the date, author(s), a link to the article, the taxonomic group to which the model is
addressed and comments that were considered necessary to be made.  The models can be filtered according to these
characteristics, for example in case we only want the models of a specific taxonomic group.

To view the matrix, just double click on the desired model, a window will open and will allow you to download
the matrix. You can also download it without doing this, by selecting it and clicking on the download button. 

To open the hyperlink you have to select the model and then click the right mouse button.

If you have any questions, please send an email to:

p.rivas@udc.es
