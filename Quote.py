### File: Quote.py
### Author: Huntron4
### Description: Web scraper for filtering and saving quotes into csv file  
## Date: 04.07.2025
## Update: 
##       07.07.2025 - Added Graphic User Interface (GUI) and support for various filetypes


# Libraries
import tkinter as tk                  # GUI elements
from tkinter import ttk, messagebox   # advanced GUI elements
import requests, pandas as pd         # data mechanisms
from bs4 import BeautifulSoup         # data mechanisms


# Web scraping function
def scrape():
    # Initialization
    global log, f_log, themes, authors      # Global variables
    url_pattern = "https://quotes.toscrape.com/page/"
    page = 1
    all_quotes = []; themes = []; authors = []; 

    # GUI update
    but1.config(text="Processing")
    okno.update_idletasks()

    while True:
        url = url_pattern + str(page) + "/"
        response = requests.get(url)
        # End condition
        if response.status_code != 200:
            print("Ended on the page",page) 
            break

        ## Soup section
        soup = BeautifulSoup(response.text, "html.parser")
        
        #Iterate trough quotes
        noq = 0
        for quote in soup.select("div.quote"):
            text = quote.select_one(".text").text
            autor = quote.select_one(".author").text
            tags = quote.select(".tags a.tag")

            temy = ", ".join([tag.text for tag in tags])
            #save unique tags
            for tag in tags:
                if not tag.text in themes: themes.append(tag.text)        

            # Add quote to the list
            all_quotes.append([text, autor, temy])
            noq += 1

        # No more quotes
        if noq == 0: break
        page += 1

    ## Pandas section
    log = pd.DataFrame(all_quotes, columns=("Text","Author","Tags"))
    f_log = log

    # Process variables
    authors = list(log["Author"].unique())
    authors = sorted(authors); themes = sorted(themes)

    # GUI update
    but1.config(text="Start")
    but3.config(text="Save")
    out2.config(text="No filters selected")
    out3.config(text=f"{len(log)} quotes found")
    combo1.set("Pick author:")  # default text
    combo2.set("Pick theme:")  # default text
    combo3.set("Pick type of file:")  # default text
    combo1.config(values=authors)
    combo2.config(values=themes)
    okno.update_idletasks()
    messagebox.showinfo("Done", "Load and processing of data sucessfully done!")
    #End of "Scrape" function

# Function to reset all filters
def reset():
    global f_log, log, authors, themes
    f_log = log
    out2.config(text="No filters selected")
    out3.config(text=f"{len(f_log)} quotes found")
    combo1.set("Pick author:")  # default text
    combo2.set("Pick theme:")  # default text
    combo1.config(values=authors)
    combo2.config(values=themes)
    messagebox
    okno.update_idletasks()
    #End of "Reset" function

# Function filtering data and updates avabile author based on selected theme
def filterAuthor(event):
    global f_log, log
    s_author = combo1.get()     #selected author
    s_theme = combo2.get()      #selected theme

    # Filter based on theme
    filtered_by_theme = log[log["Tags"].str.contains(s_theme, na=False)]

    if s_author == "Pick author:":
        f_log = filtered_by_theme.reset_index(drop=True)
        auth = sorted(f_log["Author"].unique())
        out2.config(text=f'Filtered for "{s_theme}" theme')
    else:
        # Pre-filter from full log to ensure consistency
        f_log = filtered_by_theme[filtered_by_theme["Author"] == s_author].reset_index(drop=True)
        auth = sorted(filtered_by_theme["Author"].unique())
        out2.config(text=f'Filtered for "{s_author}" author and "{s_theme}" theme')

    # Update GUI components
    combo1.config(values=auth)
    out3.config(text=f"{len(f_log)} quotes found")
    okno.update_idletasks()
    #End of "filter_author" function


# Function filtering data and updates avabile author based on selected theme
def filterTheme(event):
    global f_log, log
    s_author = combo1.get()     #selected author
    s_theme = combo2.get()      #selected theme

    # Filtering by author
    if s_author != "Pick author:":
        filtered_by_author = log[log["Author"] == s_author]
        available_themes = sorted(set(tag for tags in filtered_by_author["Tags"].dropna() for tag in tags.split(", ")))
        combo2.config(values=available_themes)  # Actualiyation of themes
    else:
        combo2.config(values=sorted(set(tag for tags in log["Tags"].dropna() for tag in tags.split(", "))))

    # Filtering by author + theme
    if s_theme == "Pick theme:":
        f_log = log[log["Author"] == s_author].reset_index(drop=True)
        out2.config(text=f'Filtered for "{s_author}" author')
    else:
        filtered_by_theme = log[log["Tags"].str.contains(s_theme, na=False)]
        if s_author == "Pick author:":
            f_log = filtered_by_theme.reset_index(drop=True)
            out2.config(text=f'Filtered for "{s_theme}" theme')
        else:
            f_log = filtered_by_theme[filtered_by_theme["Author"] == s_author].reset_index(drop=True)
            out2.config(text=f'Filtered for "{s_author}" author and "{s_theme}" theme')

    out3.config(text=f"{len(f_log)} quotes found")
    okno.update_idletasks()
    #End of "filterTheme" function


# Function for saving data into a file
def save():
    global f_log
    fname = in1.get(); ftype = combo3.get()
    if fname != "" and ftype != "N/A" and ftype != "Pick type of file:":
        if "f_log" in globals() and len(f_log) != 0:
            filename = fname + "." + ftype
            if messagebox.askokcancel("Download",f"Do you want to download file: \n             \"{filename}\""):
                match ftype:
                    case "csv": f_log.to_csv(filename, index=False)
                    case "json": f_log.to_json(filename, orient="records", lines=True)
                    case "html": f_log.to_html(filename)
                    case "tex":
                        with open(filename, "w") as f:
                            f.write(f_log.to_latex(index=False))
                    case "pickle":
                        filename = fname + ".pkl"
                        f_log.to_pickle(filename)
                
                if not messagebox.askokcancel("Continue", f"File \"{filename}\" was sucessfully downloaded into local repository \n             Continue?"):
                    exit(50)
        else:
            messagebox.showerror("ERROR", "No data to download. \n Load data first!")
    else:
        messagebox.showwarning("Warning!", "Name or type of file is missing.")
    #End of "save" function



# GUI Pattern
okno = tk.Tk()
okno.title("Quotes")
okno.geometry("1200x900")

title = tk.Label(okno, text="QUOTES", font=("Helvetica", 32))
title.pack(pady=25)

## Description
desc1 = tk.Label(okno, text="This app gets quotes from website \"quotes.toscrape.com\" \nand enable its filtration by author or/and theme", font=("Helvetica", 20))
desc1.pack(pady=15)

## Button
but1 = tk.Button(okno, text="Start", command=scrape, font=("Helvetica", 20))
but1.pack(pady=10,)

## Separator line
sep1 = ttk.Separator(okno, orient="horizontal")
sep1.pack(fill="x", padx=10, pady=10)

## Button
but2 = tk.Button(okno, text="Reset filters", command=reset, font=("Helvetica", 20))
but2.pack(pady=10, )

frame = tk.Frame(okno)
frame.pack()

## Combobox options (author)
combo1 = ttk.Combobox(frame, values=["No data available","Run process first"], state="readonly", font=("Helvetica", 18),)
combo1.set("N/A")  # default text
combo1.bind("<<ComboboxSelected>>", filterTheme)
###+++++++++ (theme)
combo2 = ttk.Combobox(frame, values=["No data available","Run process first"], state="readonly", font=("Helvetica", 18))
combo2.set("N/A")  # default text
combo2.bind("<<ComboboxSelected>>", filterAuthor)
###==========
combo1.pack(side="left", pady=10, padx=20)
combo2.pack(side="right", pady=10, padx=20)


## Output log
out2 = tk.Label(okno, text="Nothing to filter", font=("Helvetica", 18))
out2.pack(pady=5)

## Output log
out3 = tk.Label(okno, text="0 quotes found", font=("Helvetica", 18))
out3.pack(pady=5)


## Separator line
sep2 = ttk.Separator(okno, orient="horizontal")
sep2.pack(fill="x", padx=10, pady=10)

frame2 = tk.Frame(okno)
frame2.pack()

## Description
desc2 = tk.Label(frame2, text="Choose name and pick file format", font=("Helvetica", 20))
desc2.pack(pady=15)

## Entry
in1 = tk.Entry(frame2, font=("Helvetica", 18), border=5)
in1.pack(side="left", padx=10, pady=10)

## Combobox options (author) 
ftype = ["csv", "json", "html", "tex", "pickle"]
combo3 = ttk.Combobox(frame2, values=ftype, state="readonly", font=("Helvetica", 18),)
combo3.set("N/A")  # default text
combo3.pack(side="right", padx=10, pady=10)

## Button
but3 = tk.Button(okno, text="Nothing to save", command=save, font=("Helvetica", 20))
but3.pack(pady=10)


okno.mainloop()








