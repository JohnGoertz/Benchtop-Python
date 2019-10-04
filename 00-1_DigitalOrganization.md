# 00.1: Digital Organization for Benchtop Scientists

This guide aims to help you achieve some level of sanity when it comes to the digital world of your lab life. First, I'll describe what I believe should be the guiding philosophy of your digital organization (and your science, more generally): reproducibility. Everything else in this guide is intended to help you achieve that goal, from the seemingly trivial concept of how to arrange your files to the more complex task of releasing your work into the wild for anyone to play with.

This guide is meant to be followed in order, but not necessarily all at once. I've tried to write sections in order of importance so that even if you only read the first two or three and ignore the rest you'll be better off than where you started. I suggest you approach it in an iterative way, adopting one or two guidelines at a time then moving on to the rest once you're comfortable with the workflow.

Hopefully you find this useful!

## Philosophy of Reproducibility

I believe the central philosophy of your scientific recordkeeping, and of your scientific pursuits in general, should be *reproducibility*. If you've discovered something, done an experiment and gotten a result, but no one else can find the same thing, what good is it? The raw data and step-by-step analysis method are at least as important as the figures in a publication.

Everything that's needed to reproduce any analysis, figure, or table you produce should be contained within a single folder. That way, when a colleague asks to see how you did it, or when you need to re-format the figure for publication, or when you are just trying to remember how you got that answer six months ago, it takes you less than sixty seconds to gather everything you need, rather than hours or days. 

It's important to remember that while the tools here do serve the larger philosophic goal of Open Science, but they're largely for your own good. Consistently following a simple file organization scheme will help you track down old data or code should you need it again. Performing analysis in Jupyter Notebooks will encourage you to talk through your approach and keep all of your code and figures together in one document, so you can remind yourself *why* you did it this way six months from now. Keeping your code under version control with git and syncing it to Github will save you from the inevitable "It used to work and then I changed something that broke it but I don't know how to get back to where it was!". It will take some effort to get comfortable with this workflow, as well as some discipline to maintain it, but if you do I hope it will bring some sanity to your digital lab life.

## Functions, scripts, notebooks, oh my!

First, a note on how I organize my code itself. I like to one file (a Jupyter notebook, more on that later) dedicated to each experiment, titled something to the effect of "processJG027.ipynb". This should be (relatively) minimal, containing only code that is specific to that experiment. If there's a bit of code that I reuse accross multiple experiments that goes in a function contained in a separate module (which is just a ".py" file that only contains function definitions). This "utility code" can be generic (saving figures, setting default plot parameters, etc), which case it goes in the "myUtils.py" module, or instrument-specific (importing data, fitting specific curves), in which case it goes something like "processQuantStudio.py". The processing code then calls functions from these modules.

Functions allow your code to be more modular, making it easier and faster to use for future analyses, but they are harder to test out than directly writing out the commands. I usually prototype segments in a notebook or script, then *refactor* them into functions and move them to a utility module later. For example, if you need to fit the same curve to lots of samples, write a function to process a single sample and return the fit parameters. Your process code can then loop over all your samples and gather their outputs together.

## Directory Structure

The core component of digital organization is, well, how you organize your files. As an experimentalist, there are several types of files I have for every experiment: calculations of reaction volumes and dilutions, raw instrument data (potentially from multiple instruments), code to process this specific experiment, "utility" code that I use pieces of for multiple experiments, the results (typically figures), and a lab notebook entry that brings it all together.

Before I get into how keep these organized *now*, let me first explain how I *used to* structure everything, and why that slowly drove me to anxiety. I had all my data in one folder, ordered by date I started the experiment. My "lab notebook" was in OneNote, with similar date ordering but divided into different project sections. Some experiment-specific code was stored next to the data, as were the resulting figures, but some "utility" code such as functions for plotting or processing that I used over and over were in an entirely different folder. This utility code folder was shared across the lab, and we periodically updated the code to fix bugs or add capabilities.

This all felt like a very natural system, but problems eventually arose. It was sometimes difficult to find the data folder that corresponded to a specific notebook entry, because I might have accidentaly put different dates for each (date started planning the experiment vs date actually performing it). The reverse was hard too, because the "project" I envisioned the experiment belonging to at the time might have morphed into something else six months later, or I might simply have forgotten which project I put it under. Repeating my own analysis was difficult too: because the utility code had been updated in the time since, it often didn't work the same way anymore. Plus, if that code referenced some file elsewhere in my computer, it may have moved since and I would have to hunt it down (this sort of problem might be insurmountable for someone else trying to reproduce your results).

This has led me to my current "everything contained in a single folder" approach. There's no ambiguity as to the connection between data and notebook entry, and the code will always work because it won't have changed since I ran the experiment. Here's how it works. The parent folder for each experiment is simply my initials followed by sequential numbering. All of the necessary files go in an appropriate subfolder, as shown below.

```bash
JG027
├── JG027 Competitive Amplification 500uM Probes.docx
├── Calculations
│   └── JG027 Dilutions and Plate Layout.xlsx
├── Code
│   ├── Utils
│   │   ├── myUtils.py
│   │   └── processQuantStudio.py
│   └── processJG027.ipynb
├── Data
│   ├── JG026 TMCC1 Competitor Efficiency.xls
│   └── JG027 TMCC1 Competition.xls
└── Results
    ├── Logistic Growth-Drift Fit Parameters.png
    ├── Logistic Growth-Drift Fit Parameters.svg
    ├── Un-Competitive Amplification Efficiencies.png
    └── Un-Competitive Amplification Efficiencies.svg
```

Have utility code that you use for multiple experiments? Copy and paste it to every one of those experiments. (Using git/Github will provide a more elegant and powerful way to reuse code this way, as I get into below, but practically speaking it's little different than copy-pasting.) The analysis scripts and modules you'll write are probably very small files; that "processQuantStudio.py" contains nearly 1000 lines of code and comes in at a whopping 35 KB. For most experimental scientists this will be the case, there's no need to be stingy with disc space when you have hundreds of gigabytes or more at your disposal. Same goes with data. Need to reference data from another experiment? Copy and paste it along with the new data. The JG### experiment-naming scheme makes it clear that's what you're doing, and unless the data is hi-res images or movies the storage overhead is minimal. If your data is very large, it's probably best to process each fileset individually to extract only the lightweight data you need to compare directly, then copy that around as necessary.

Keeping everything self-contained like this has the additional advantage that everything can be linked together in your code via short *relative* paths. An *absolute* path specifies where a file is by its explicit location on the drive, something like `C:\User\John\Documents\Research\ELN\JG027\Data`. This is not only cumbersome to read and write, it's fragile: if I change the name of the "ELN" folder to "Lab Notebook", the link becomes broken and I have to rename it in the code too. A *relative* path specifies where a file is in relation to the current folder. If my current folder is `Code`, then I can refer to the `Data` folder simply as `../Data`, because `../` means "go up one folder". I can get to `myUtils.py` with `./Utils/myUtils.py` (the `./` means "this current folder" and is actually somewhat unnecessary).

My "myUtils.py" module has the following Python function that I can call from my "processJG027" notebook to store all these relative paths into variables:

```python
import pathlib as pl
import os

def setupPath():
    # Path to the file calling this function (e.g., processJG027.ipynb)
    code_pth = pl.Path(os.getcwd())
    
    # Path to the "JG###" folder
    base_pth = code_pth.parent
    
    data_pth = base_pth / 'Data'
    rslt_pth = base_pth / 'Results'
    
    return code_pth, base_pth, data_pth, rslt_pth
```

This structure also makes it easy to call functions from my utility modules `myUtils.py` and `processQuantStudio.py` within my analysis notebook. The imports for `processJG027.ipynb` include:

```python
from Utils import myUtils as mypy
from Utils import processQuantStudio as pQS
```

so I can then call `paths = mypy.setupPath()` to gather the relevant addresses.

I'd suggest keeping a template folder named something like "JG###" that contains empty Calculations/Code/Data/Results folders, and maybe a template .docx file for the notebook entry itself, so you can just copy/paste and rename for each new experiment. But hey, we're coders, right? There's got to be a way to make the computer do all that arduous work for us, right? At the bottom of this file I've put a small `bash` function that will automatically do all that for you, as well as some initial git commands (more on that in Part 2 of this guide). 

## Jupyter Notebooks

The concept of organizing code in "notebooks" (be they Jupyter or RMarkDown) as opposed to purely scripts and modules (or, *shudder*, Excel files) has been gaining in popularity. Traditional scripts are meant to be executed from beginning to end, perhaps spitting out graph after graph along the way. It's possible to introduce some interactivity so a user can play with certain settings on the fly, but doing so takes quite a bit of code in its own right. Furthermore, annotating the code to describe what you're doing and why is done via in-line "comments", but these comments lend themselves to terse explanations and make it difficult to depict things like equations. Notebooks allow you to keep the outputs of your analysis side-by-side with the code that generated it, facilitate more thorough explanations, and enable interactivity. 

Notebooks organize code into "blocks" or "cells" with the output of each displayed directly below. These cells can be executed individually, in order from beginning to end, or in any order you choose. The underlying Python/R "environment" or "kernel" interprets the code as if you had entered it line-by-line into a command window. This makes it easy to focus on one part of your code, tweaking and re-running it in isolation without having run everything. Be warned, though, there are dangers that come with this freedom. If you run code stored in a cell, then delete that cell, you don't *undo* the commands; if you changed a variable it's still changed but now you can't see what you did to it. The same goes with running cells out of order. If you run all your cells top-to-bottom, then go back and re-run a cell near the top, it might not behave the same because some of its variables were changed by cells lower down in the notebook. This can be really confusing, so be aware of it as you write your code: in later code blocks, try not to change variables used by earlier blocks. If all else fails, you can always "Restart kernel and run all cells". This clears the memory of all variables and code called so far, starting fresh as if you had opened it for the first time. It's a good idea to do this before considering a notebook "complete" to ensure everything's still cohesive.

Notebook cells can also contain formatted text instead of executable code. This text is in the very simple and elegant *markdown* format (like this document). You can include headers, bulletted/numbered lists, highlighted code snippets, and even equations written in LaTeX. For a complete list of Markdown formatting tools, go here. Math is inserted inline between single dollar signs `$...$` or you can put an equation on its own line with double dollar signs `$$...$$`; for an intro to writing equations in LaTeX (pronounced lah-tek), go __[here](https://en.wikibooks.org/wiki/LaTeX/Mathematics)__ or look at __[this cheatsheet](http://tug.ctan.org/info/undergradmath/undergradmath.pdf)__. The point of markdown cells is to give you the freedom to talk naturally about your code, so you should try to talk through what your code is doing and why as thoroughly as possible. Justifying your choices will help make you more certain of them, and your future self (and others) will thank you for the clarity.

Finally, notebooks make it easy to make your code interactive. Perhaps you want to see how a result changes as you vary some parameter in the analysis. Jupyter allows you to change values with sliders or other tools and updates the result automatically. Again, though, be careful with this power. In the spirit of reproducibility, don't rely on the user setting the correct values each time the notebook is run; if you want to retain interactivity, at least set the default values to what you deem "correct".

***
# Summary

Hopefully this has been a useful starting point for how to organize the digital side of your experiments. It all stems from a philosophy of reproducibility, ensuring you or others can replicate your results at any time in the future. This requires a file structure that is easy to remember and easy to maintain, one that keeps all the necessary pieces in one self-contained place. Writing data analysis in notebooks makes it clear how the code relates to our figures and outputs while encouraging natural descriptions of *why* each bit of code looks the way it does.

In Part 2 of this guide I'll discuss how I use git and Github to bring this all together. These tools provide an elegant platform for keeping track of changes made to code, reusing code, and sharing it with others.

***
## Postscript: Managing this from the terminal

If you write code regularly, you might benefit from getting familiar with how to navigate with the "terminal", using a command-line interface rather than a graphical one. This can make some operations much faster than doing them manually. If you're on a Mac or Linux machine, you already have a bash terminal at your disposal. If you're on Windows, I'd recommend steering clear of the "command prompt" and instead installing Windows Subsystem for Linux (WSL), specifically Ubuntu. It's relatively painless to set up, and it gives you access to a full-fledged Linux environment on your Windows computer. This is particularly important if you have to run software packages that require Linux (I'm glaring at you, __[Nupack](http://www.nupack.org)__).

__[Here's](https://linuxhint.com/install_ubuntu_windows_10_wsl/)__ a good guide on how to go about getting set up with WSL. You'll really only need to know a couple commands, primarily just `cd` to move around your directories and `ls` to view all the files in your current directory. Once you launch the Ubuntu terminal in Windows, your default directory is a special Linux internal folder that will more or less look empty; type `cd /mnt/c/Users/<your Windows username>` to find your files.

As promised, here's how to get the bash terminal to set up a new experiment folder for you.

* `nano ~/.bashrc`
* Navigate to the bottom of the file, then paste in the following. Replace all the "JG"s, and while you're welcome to use mine, you probably want to replace the URL for the utils repo with your own (more on that in part 2).
```bash
  alias myeln='cd /mnt/c/path/to/your/experiments/'

  function mkELN ()
  {
        myeln
        entry="JG$(ls | grep -e ^JG[0-9]*$ | sort -r | head -1 | awk -v FPAT="[0-9]+" '{printf "%03d\n", $NF+1}')"
        
        mkdir $entry
        
        cd $entry
        
        mkdir Code/
        mkdir Data/
        mkdir Results/
        cp -r ../Templates/* ./
        cp ../Templates/.gitignore ./
        mv JGXXX.docx $entry".docx"
        
        git init
        touch $entry"_README.md"
        
        git add $entry"_README.md"
        git lfs track "Results/**"
        git lfs track "*.xls*"
        git add .gitattributes
        git add .gitignore
        
        git commit -m "Initialize "$entry
        
        git remote add utils https://github.com/johngoertz/PythonUtils
        git subtree add utils master --prefix=Code/Utils/ --squash
        
        cd Code/
        touch "process"$entry.ipynb        
}
```
* Press Ctrl-o to save the file
* Press Ctrl-x to leave nano
* Type `. ~/.bashrc` to re-run the bashrc file

You're all set! Now if you want to get to the folder with all your experiments just type `myeln`. When you want to make a new experiment folder, all it takes is `mkELN`.