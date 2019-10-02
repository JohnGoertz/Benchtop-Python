# 00: Digital Organization for Benchtop Scientists

This guide aims to help you achieve some level of sanity when it comes to the digital world of your lab life. First, I'll describe what I believe should be the guiding philosophy of your digital organization (and your science, more generally): reproducibility. Everything else in this guide is intended to help you achieve that goal, from the seemingly trivial concept of how to arrange your files to the more complex task of releasing your work into the wild for anyone to play with.

This guide is meant to be followed in order, but not necessarily all at once. I've tried to write sections in order of importance so that even if you only read the first two or three and ignore the rest you'll be better off than where you started. I suggest you approach it in an iterative way, adopting one or two guidelines at a time then moving on to the rest once you're comfortable with the workflow.

Hopefully you find this useful!

## Philosophy of Reproducibility

I believe the central philosophy of your scientific recordkeeping, and of your scientific pursuits in general, should be *reproducibility*. If you've discovered something, done an experiment and gotten a result, but no one else can find the same thing, what good is it? The raw data and step-by-step analysis method are at least as important as the figures in a publication.

Everything that's needed to reproduce any analysis, figure, or table you produce should be contained within a single folder. That way, when a colleague asks to see how you did it, or when you need to re-format the figure for publication, or when you are just trying to remember how you got that answer six months ago, it takes you less than sixty seconds to gather everything you need, rather than hours or days. 

It's important to remember that while the tools here do serve the larger philosophic goal of Open Science, but they're largely for your own good. Consistently following a simple file organization scheme will help you track down old data or code should you need it again. Performing analysis in Jupyter Notebooks will encourage you to talk through your approach and keep all of your code and figures together in one document, so you can remind yourself *why* you did it this way six months from now. Keeping your code under version control with git and syncing it to Github will save you from the inevitable "It used to work and then I changed something that broke it but I don't know how to get back to where it was!". It will take some effort to get comfortable with this workflow, as well as some discipline to maintain it, but if you do I hope it will bring some sanity to your digital lab life.

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

## Jupyter Notebooks

The concept of organizing code in "notebooks" (be they Jupyter or RMarkDown) as opposed to purely scripts and modules (or, *shudder*, Excel files) has been gaining in popularity. Traditional scripts are meant to be executed from beginning to end, perhaps spitting out graph after graph along the way. It's possible to introduce some interactivity so a user can play with certain settings on the fly, but doing so takes quite a bit of code in its own right. Furthermore, annotating the code to describe what you're doing and why is done via in-line "comments", but these comments lend themselves to terse explanations and make it difficult to depict things like equations. Notebooks allow you to keep the outputs of your analysis side-by-side with the code that generated it, facilitate more thorough explanations, and enable interactivity. 

Notebooks organize code into "blocks" or "cells" with the output of each displayed directly below. These cells can be executed individually, in order from beginning to end, or in any order you choose. The underlying Python/R "environment" or "kernel" interprets the code as if you had entered it line-by-line into a command window. This makes it easy to focus on one part of your code, tweaking and re-running it in isolation without having run everything. Be warned, though, there are dangers that come with this freedom. If you run code stored in a cell, then delete that cell, you don't *undo* the commands; if you changed a variable it's still changed but now you can't see what you did to it. The same goes with running cells out of order. If you run all your cells top-to-bottom, then go back and re-run a cell near the top, it might not behave the same because some of its variables were changed by cells lower down in the notebook. This can be really confusing, so be aware of it as you write your code: in later code blocks, try not to change variables used by earlier blocks. If all else fails, you can always "Restart kernel and run all cells". This clears the memory of all variables and code called so far, starting fresh as if you had opened it for the first time. It's a good idea to do this before considering a notebook "complete" to ensure everything's still cohesive.

Notebook cells can also contain formatted text instead of executable code. This text is in the very simple and elegant *markdown* format (like this document). You can include headers, bulletted/numbered lists, highlighted code snippets, and even equations written in LaTeX. For a complete list of Markdown formatting tools, go here. For an intro to writing equations in LaTeX (pronounced lah-tek), go here. The point of markdown cells is to give you the freedom to talk naturally about your code, so you should try to talk through what your code is doing and why as thoroughly as possible. Justifying your choices will help make you more certain of them, and your future self (and others) will thank you for the clarity.

Finally, notebooks make it easy to make your code interactive. Perhaps you want to see how a result changes as you vary some parameter in the analysis. Jupyter allows you to change values with sliders or other tools and updates the result automatically. Again, though, be careful with this power. In the spirit of reproducibility, don't rely on the user setting the correct values each time the notebook is run; if you want to retain interactivity, at least set the default values to what you deem "correct".

## Git(hub)

> _"My code was working but then I changed something and now it doesn't and I don't know how to get it back to working again!" - Every. Coder. Ever._

Git is the answer to this inevitable dilemma. Git and Github are powerful tools to help you keep track of the changes you make to your code, sync your code to the cloud so you and others can access it anywhere, and incorporate changes proposed by collaborators. Intended for developers writing open-source software, it can be difficult to translate these tools into a workflow adapted to experimental science. Here I'll describe my own system for doing just that.

First, I'll describe how to use git locally (on your computer, not the cloud) as a sort of lab notebook for your code. Next I'll talk about how to use the cloud service *Github* to host your code, keeping it private to yourself and a few collaborators or open for the whole world to see. Next, I'll show you how to use git "subtrees" to re-use utility code in a more elegant way than copy-pasting for every experiment. Finally, I'll work through a couple extra tools that make tracking binary files (e.g., Excel or Word documents, images) or Jupyter Notebooks easier to do.

### Version Control: A Lab Notebook for Code

#### Branching: A Safe Space to Experiment

### Remote Repositories: Sharing is Caring

#### Binder: Turning Your Code Into A Public Playground 

### Subtrees: Recycling Code

### Large File System: Tracking Raw Data

### Git and Jupyter Notebooks: Filters

