# Multithreaded Word Frequency Counter (Multiprocessing Version)

## Lab Overview

This project demonstrates how to use **multiprocessing** in Python to perform concurrent processing on a large text file. The program:

- Accepts a text file and the number of segments (`N`) as input.
- Splits the file into `N` segments (by word count).
- Launches one **process per segment** to count word frequencies.
- Displays a **progress bar** while processing.
- Consolidates all word frequencies and saves the result to `output.txt`.

---

## 📁 Contents

The `.zip` file should contain the following files:

- main.py - the file to run the program
- input.txt # Example input text file
- README.md #This instruction file

---

## 🖥️ System Requirements

- Python 3.6 or higher
- Terminal or command prompt
- Internet connection (only to install dependencies, if needed)

---

## 📦 Setup Instructions

### 1. Install Required Python Package

Open your terminal (or command prompt) and run:

```bash
pip install tqdm
```

---

## How to Run the program (example)
python3 main.py input.txt 4
