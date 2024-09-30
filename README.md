<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&width=435&height=30&lines=COMPONENT+DB+PROJECT" alt="Typing SVG" /></a>
-----------------------------------------
This is the code for preparing data for information and reference database from modern electronic component database.

<h4>File descriprion:</h4>
<h5><ins>main.py</ins></h5> 
Selection of all unique technical specifications and all unique manufacturers from json files with parsed books (folder /json)
<h5><ins>divide_title.py:</ins></h5>
Making a json with a list of all ECBs in the following form:

{
"ekbName": "ECB name",  
"tuName": ["First", "Second", ...],  
"ManufacturerName": also a list of manufacturers in text  
}

The elements are divided into files by title and each file lies in a folder with the name of the book
in which the corresponding elements were.
<h5><ins>divide_params.py</ins></h5>

<ins><em>Libraries and modules used:</em></ins> os, re, sys, json
