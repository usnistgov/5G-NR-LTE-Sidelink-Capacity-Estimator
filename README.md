# Introduction

This is the prototype for the Sidelink Capacity Tool

![Application Screenshot](preview-screenshot.png)

# Installation

## Requirements

* Python 3.6+
* Qt 5.9+ (charts, core, widgets)

## Create a virtual environment

```shell
python -m venv venv
source venv/bin/activate
```

## Install Dependencies

```shell
pip install -r requirements.txt
```

## Compile UI Files

```shell
pyside2-uic  main-window.ui > ui_mainwindow.py
```

## Run

```shell
python main.py
```
