# 00: Digital Organization for Experimental Analysis

This guide aims to help you achieve some level of sanity when it comes to the digital world of your lab life. First, I'll describe what I believe should be the guiding philosophy of your digital organization (and your science, more generally): reproducibility. Everything else in this guide is intended to help you achieve that goal, from the seemingly trivial concept of how to arrange your files to the more complex task of releasing your work into the wild for anyone to play with.

This guide is meant to be followed in order, but not necessarily all at once. I've tried to write sections in order of importance so that even if you only read the first two or three and ignore the rest you'll be better off than where you started. I suggest you approach it in an iterative way, adopting one or two guidelines at a time then moving on to the rest once you're comfortable with the workflow.

Hopefully you find this useful!

## Philosophy of Reproducibility

I believe the central philosophy of your scientific recordkeeping, and of your scientific pursuits in general, should be *reproducibility*. If you've discovered something, done an experiment and gotten a result, but no one else can find the same thing, what good is it? The raw data and step-by-step analysis method are at least as important as the figures in a publication.

Everything that's needed to reproduce any analysis, figure, or table you produce should be contained within a single folder. That way, when a colleague asks to see how you did it, or when you need to re-format the figure for publication, or when you are just trying to remember how you got that answer six months ago, it takes you less than sixty seconds to gather everything you need, rather than hours or days. 

It's important to remember that the tools here do serve the larger philosophic goal of Open Science, but they're largely for your own good. Consistently following a simple file organization scheme will help you track down old data or code should you need it again. Performing analysis in Jupyter Notebooks will encourage you to talk through your approach and keep all of your code and figures together in one document, so you can remind yourself *why* you did it this way six months from now. Keeping your code under version control with git and syncing it to Github will save you from the inevitable "It used to work and then I changed something that broke it but I don't know how to get back to where it was!". It will take some effort to get comfortable with this workflow, as well as some discipline to maintain it, but if you do I hope it will bring some sanity to your digital lab life.

## Directory Structure

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

## Jupyter Notebooks

## Git(hub)

### The answer to "I don't know why it stopped working!"

### Local Version Control: A Lab Notebook for Code

#### Branching: A Safe Space to Experiment

### Remote Repositories: Sharing is Caring

#### Binder: Turning Your Code Into A Public Playground 

### Large File System: Tracking Raw Data

### Subtrees: Recycling Code



