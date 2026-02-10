
# Data-Driven Decision Tool

**Interactive Python tool for multi-criteria decision-making and scenario analysis.**

---

## Overview

This project is an **interactive decision-making tool** implemented in Python. It allows users to compare multiple alternatives based on customizable criteria and weights, calculates normalized scores, ranks the options, and highlights the optimal choice. Additionally, it includes a visual ranking of alternatives for clear interpretation.

The tool demonstrates **analytical thinking, data-driven decision making, scenario analysis, and practical programming skills**. It can be applied to real-world scenarios such as supplier selection, project prioritization, or investment decisions.

---

## Features

- Input **any number of alternatives** and evaluation criteria.
- Specify if **higher or lower values are better** for each criterion.
- Assign **custom weights** to criteria reflecting strategic priorities.
- Normalizes data and calculates **weighted scores**.
- Outputs a **ranked list of alternatives**.
- Visualizes results using a simple **bar chart**.

---

## How to run (local)

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```
### 2) Run (interactive)
```bash
python -m decision_tool.cli
```
## Project structure

- `src/decision_tool/core.py` — scoring, normalization and ranking logic  
- `src/decision_tool/cli.py` — interactive command-line interface  
- `tests/` — unit tests for the core logic
  ## Requirements
- Python 3.10+
