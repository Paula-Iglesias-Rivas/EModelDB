### EModelDB ###
A database of empirical substitution models of protein evolution.

Paula Iglesias-Rivas, Roberto Del Amparo, Javier A Cabaleiro, Miguel Arenas

Substitution models of evolution describe the relative rates of fixation of mutations and are traditionally used in phylogenetics.
EModelDB is a database of empirical substitution models of protein evolution, including those based on phylogenetic and score matrices, and it includes their classification according to several filters. 

EModelDB is distributed with several files, including the database itself (models.db) and the folder with the matrices of the empirical substitution models (data) and, the graphical user interface (interface_EModelDB.py). 

The interface can be executed either remotely by accessing the following link:
https://emodeldb.streamlit.app/
or locally.
 
As a requirement to run the interface locally, it is necessary to have Python (https://www.python.org/downloads/) and Streamlit installed and the libraries associated with the code (indicated at the beginning of the code).
If they are not installed, the installation can be performed in the Linux command line through the following commands,
````bash
pip install pandas
pip install streamlit
 ````

Next, the graphical user interface can be executed from the command line by typing at the folder containing the code files,
````bash
streamlit run interface_EModelDB.py
````

Once the interface is executed, a window should appear displaying the database and the characteristics of every models (publication year, author(s), reference including link to the publication, taxonomic group, informative comments and a dropdown menu to preview the matrix). The models can be filtered according to some of these characteristics.

To download the matrix (or matrices), just select the desired model/s and click on the download button shown at the bottom or click Select All and the download button.


The framework is distributed under the General Public License (GPL), which is also distributed.


For any questions, please contact us through paula.iglesias.rivas@uvigo.es

### Disclaimer

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version (at your option) of the License. This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place – Suite 330, Boston, MA 02111-1307, USA.

