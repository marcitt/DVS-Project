# DVS-Project
Visual Systems Coursework Submission

## Project Description

The overall aim of this mini project is to create a structured representation of GUI elements using screenshots.
These structured representations can be provided to accessibility tools e.g. screen-readers.

This aims to support accessibility in applications that may not supply accessibility data through other means such as metadata or tags or in cases where some GUI data is not provided.

I hope to extend some of the findings from this mini project into my master's project which aims to use natural language processing to support accessibility agents.

(This project is primarily focused on extracting meaningful GUI representations from design softwares e.g. Figma and Illustrator as this is the scope of my master's project)

---

The aims are to create the processing pipeline and then demonstrate the usage in a particular accessibility context
e.g. my initial plan was to demonstrate how this could be used for head-tracking to enable

## Setup Instructions

1. Clone repo 

2. Setup virtual environment using `requirements.txt`

3. The key analysis is contained in `gui-analysis-notebook.ipynb` - all of the results should be visible in the notebook so the code does not need to be run.

4. To run the eye-tracking application you must allow the program access to certain accessibility tools to allow it to control the mouse - I included a demo video of the code working so this program doesn't need to be set up.


I usually use conda to setup projects and run notebooks:
```
conda create -n dvs_project python=3.11
conda activate dvs_project
pip install -r requirements.txt

```

## Key Features
All of key findings and notes are available in `gui-analysis-notebook.ipynb` but they have been summarised below:

### GUI Analysis features
- Canvas detection - using canny edge detection + sorting.

- Extraction of key GUI icons using  - using thresholding, morphological operations and connected components analysis.

- GUI icon segmentation - segmenting icons into key regions e.g. toolbar vs aside etc. using k-means, which can help give accessibility tools more context about where to find a tool e.g. the pen is likely to be in the toolbar and layers are likely to be in the aside panel. 

- GUI icon labelling - using SIFT to match identified icons with an existing database of icons.

- Tested more generalisable approach with a VLM approach - however this was not very successful.

### Eye-tracking
- Captures current screen and then applies the GUI analysis to extract bounding boxes for key icons
- Applies general eye-tracking referenced from: https://github.com/ProgrammingHero1/eye_controlled_mouse
- Proposed a new concept of "eye-snapping" inspired by this paper on "voice-snapping": https://dl.acm.org/doi/10.1145/3532106.3533452
Voice Snapping: Inclusive Speech Interaction Techniques for Creative Object Manipulation

Here I wanted to introduce the idea of eye-snapping e.g. when the cursor approaches an icon - it will snap to the GUI icon.
The goal here is to help users who may have difficulty with stable movement or precision - addressing some of the existing problems associated with eye-tracking systems. 

## Quick Video Demo
https://drive.google.com/file/d/18CXzTmuBRaIngzlLHF5UOiLpp2jIyEOJ/view?usp=sharing

## Contributions & Reflection
I worked independently on the project (no partner)


### Process / Design Decisions
I chose to work with Python as this is easy to integrate with my existing master's work which is primarily written in Python. Python is much easier to integrate with deep-learning toolkits, AI agents, APIs and accessibility tools as opposed to matlab. 

I created a small ipynb lab book for this project to test my experiments and track my progress: `gui-analysis-notebook.ipynb`

Then I created the eye tracking application to show how this GUI analysis toolkit might be used by real accessibility tools.

### What I have learnt
Analysis of very small, highly cropped images (e.g. icons) is difficult. SIFT and feature analysis can work quite well if icons are distinct enough, however many modern applications have very simplistic icon designs which are challenging for algorithms like SIFT to pick up as there not enough unique fetures.

Extracting general bounding boxes for icons works well! Connected component analysis is a strong tool for this.
After extracting centroids for icons - k-means clustering also works well for segmenting them into potential categories. 

### What I would develop further
- Further investigation on the deep-learning side of the project e.g. employing models like CLIP or fine-tuned VLMs - I did some initial testing in: `vlm-test.ipynb` but it wasn't very successful. 

- Testing out different matching algorithms beyond SIFT - looking at CNN features could be a place to start.

- Potentially adding smoothing to the eye-snapping application + live labelling