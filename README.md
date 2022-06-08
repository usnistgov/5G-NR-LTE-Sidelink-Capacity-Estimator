![Application Screenshot](preview-screenshot.png)

# Introduction
This tool computes the expected link capacity (Mbit/s) for Sidelink considering 5G New Radio (NR) and Long Term Evolution (LTE) communication standards, as defined by the The 3rd Generation Partership Project (3GPP). Users can input the respective configuration paramenter and evaluate the resuling capcity.

The tool provides side-by-side chart plotting between NR and LTE Sidelink capacities for easy comparisson. Data and generated charts can be exported to be used outside the tool.

## New Radio (NR) Sidelink Capacity

## Long Term Evolution (LTE) Sidelink Capacity


# Installation Instructions

## Requirements

* Python 3.6+

## Create a virtual environment

```shell
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```shell
pip install -r requirements.txt
```

## Run

```shell
python main.py
```

# Development
Follow the [Installation](#installation) instructions above

## Compiling UI Files

### The Quick Way
There's a convenience script to run the following commands,
be sure virtual environment is activated.
```shell
./compile_ui.sh
```

### Manual

If the UI is updated, then the UI files need to be recompiled, run the
following in the virtual environment

```shell
pyside2-uic main-window.ui > ui_mainwindow.py
pyside2-uic csv_dialog.ui > ui_csvdialog.py
```
