**Description:** Documentation for `Quote.py`(*V2.0*) file.

# Run
Start the program as:
<pre>python3 Quote.py</pre>  
Usage of program through Graphic User Interface (**GUI**) should be intuitive and shouldn't need further guidance.

# Implementation
File `Quote.py`(*V2.0*)  is updated version of program in file (*currently named as*) `Quote_V1.py`. The previous version was runned purely trough "Command line" (**Cl**) with optional use of **Cl parameters**. It's documentation was also renamed and is available [here](./V1_README.md).
 
## Program structure 
The program could be semmantically separated into few functions and sections. 
- Libraries
- **scrape** (function)   
- **filterAuthor** (function)  
- **filterTheme** (function) 
- **reset** (function) 
- **save** (function)  
- GUI pattern

## Sections
### Libraries
In this section of code were imported **important** libraries for execution and proper function of this program.  
Imported libraries include:   
`resources`, `bs4` (submodule: `BeautifulSoup`) - web scraping  
`pandas` - data processing and filtration  
`tkinter` (*submodules*: `ttk`,`messagebox`) for **GUI**  

### Scrape
This function perform "**Web scraping**" (*load and processing of data extracted from some web page*). Uses `resources` library to download whole web page. Then, with module `BeautifulSoup`, is this page split into elements and *wanted* informations and content from this elements is extracted. Finally, data is formated and stored using `pandas` library. At the start and end of this function are sections for **GUI** elements update, to insist user knowledge about processes running at the background.

### Filter Author and Theme
Functions `filterAuthor` and `filterTheme` are executed on change of *theme* and *author* selectors. They are named not really intuitively, due to paradox that *selection of theme* causes change in *available authors* and *Vice versa*.  
Basic logic is filtering available authors for selected theme, and available themes for selected author. Both of this parameters result in finnal number of quotes corresponding to selectors.

### Reset
This function resets all filters, and reloads all data extracted from website.   
Its pupose is to end infinite loop created by selecting first *Author* or *Theme*, due to what it only shows option (inside selectors) matching with other selector.

### Save
This function at first check all needed inputs and data to evaluate if saving has meaning. Its behaviour is displayed trough information, warning and error messages from `messagebox` module.  
If all conditions are satisfied, it exports data into file type and name selected by user.

### Graphic User Interface
Last section creates pattern for **GUI**. Define its elements and structure. Specify which functions should be called based on which event etc. It's designed by GUI *best practise* that "*Every action which user does should manifest as change at the screen"


# Sources
### Disclaimer: 
Final content downloaded from this program execution is **not** property of *code author*. All quotes are downloaded from [quotes.toscrape.com](https://quotes.toscrape.com/page/) website. Program is meant to **load, process, filter** and **save** data from this website.

### Artificial Inteligence
During creation and testing of this program was used  [Microsoft Copilot](https://copilot.microsoft.com/) *LLM*. "**AI**" served for **educational**, **text editing** and **refactoring** purposes. 