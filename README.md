<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&width=435&height=30&lines=COMPONENT+DB+PROJECT" alt="Typing SVG" /></a>
-----------------------------------------
This is the code for preparing data for information and reference database from modern electronic component database.

**File descriprion:**
- <ins>main.py:</ins> selection of all unique technical specifications and all unique manufacturers from json files with parsed books (folder /json)
- <ins>divide_title.py:</ins> making a json with a list of all ECBs in the following form:
{
"ekbName": "ECB name",
"tuName": ["First", "Second", ...],
"ManufacturerName": also a list of manufacturers in text
}
The elements are divided into files by title and each file lies in a folder with the name of the book
in which the corresponding elements were.
- <ins>divide_params.py:</ins> 

<ins><em>Libraries and modules used:</em></ins> os, re, sys, json
