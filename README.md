### EModelDB ###
A database of empirical substitution models of protein evolution
Paula Iglesias-Rivas, Roberto Del Amparo, Javier A Cabaleiro, Miguel Arenas

Substitution models of evolution describe the relative rates of fixation of mutations and are traditionally used in phylogenetics.
EModelDB is a database of empirical substitution models of protein evolution, including those based on phylogenetic and score matrices, and it includes their classification according to several filters. 

EModelDB is distributed with several files, including the database itself (models.db) and the folder with the matrices of the empirical substitution models (data) and, the graphical user interface (interface_EModelDB.py). 

 
As a requirement, it is necessary to have Python and Streamlit installed and the libraries associated with the code (indicated at the beginning of the code).
If they are not installed, the installation can be performed in the Linux command line through the following commands,

pip install pandas

pip install streamlit


Next, the graphical user interface can be executed from the command line by typing at the folder containing the code files,
streamlit run interface_EModelDB.py


Once the interface is executed, you may click on the Local URL or Network URL, a window should appear displaying the database and the characteristics of every models (publication year, author(s), reference including link to the publication, taxonomic group and informative comments. The models can be filtered according to some of these characteristics.

To download the matrix (or matrices), just select the desired model/s and click on the download button shown at the bottom.


The framework is distributed under the General Public License (GPL), which is also distributed.


For any questions, please contact us through paula.iglesias.rivas@uvigo.es

