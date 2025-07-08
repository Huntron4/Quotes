## Run
`python3 Quote.py {-h | -themes | -authors}  {-a name} {-t name} {-s filename}`  

### Parameters:
- `-h` => print help
- `-themes` => list themes 
- `-authors` => list authors

#### Selectors:  
- `-a name` => list selected author quotes
- `-t name` => list selected theme quotes
- `-s filename` => name of saved **.csv** file

### Defects
1. Console print is used purely to have overview over quotes and its themes and authors. To read whole (longer) quotes, consider saving it into `your_filename.csv`.  
2. Processing and filtering might take longer time due to nature of data procesing libraries (which were the main goal to use un this project). So the optimalized (*or fastest*) approach is not used on purpose. 



## Possible future expansions:
- choose which page/s should be loaded 
- choose max number of quotes listed
- support for different file types
- graphic user interface