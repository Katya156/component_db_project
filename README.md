<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&width=435&height=30&lines=COMPONENT+DB+PROJECT" alt="Typing SVG" /></a>
-----------------------------------------
This is the code for preparing data for information and reference database from modern electronic component database.

<h3>File descriprion</h3>
<h4><ins>main.py</ins></h4> 
Selection of all unique technical specifications and all unique manufacturers from json files with parsed books (folder /json).

The result is stored in tu.txt and mf.txt files.
<h4><ins>divide_title.py</ins></h4>
Making a json with a list of all ECBs in the following form:
<code>
{
"ekbName": "ECB name",  
"tuName": ["First", "Second", ...],  
"ManufacturerName": also a list of manufacturers in text  
}
</code>
The elements are divided into files by title and each file lies in a folder with the name of the book in which the corresponding elements were.

The result is stored in the /data folder.
<h4><ins>divide_params.py</ins></h4>
Here is a section setting (new_parser_settings folder), which column corresponds to which Parameter Id. 
You need to make a program that will create such a file:
<code>
[
{"{"Name": "Lari 1",
"Parameters":
{
"5": ["the first value of the split parameter", "the second value of the split parameter", ..],
...}
},
...
]
</code>
Such files should be for for each category, both with names and technical specifications, but the template files are given per section (the gap between the two subtitle).

The result is stored in the /data_params folder.

<ins><em>Libraries and modules used:</em></ins> os, re, sys, json
