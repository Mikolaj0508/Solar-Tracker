# Solar-Tracker

The above software is a part of our engineering project. The goal was to construct a physical model and software on the executive side (microcontroller) and microcomputer side for tracking a light source. An important aspect was the construction of a flexible solution based on a database.

## Microcontroller part

The following software has been prepared to create a simple interface to control small servos and perform electrical load measurements using the INA219 chip. 
Ultimately, the code was prepared for the Arduino UNO board, but even a smaller platform should handle it without any problems.

## Microcomputer part

The software for the microcomputer was written in Python and ran on the Raspbian environment. Key functionalities included communication with Arduino, saving and reading data from a SQLite database, and executing algorithms for optimizing electricity production.

## Installation

To set the things up, you have to do following steps:

Clone the project

```bash
  git clone https://github.com/Mikolaj0508/Solar-Tracker.git
```

Go to the project directory

```bash
  cd my-project
```
Activate virtual environment

```bash
  source env/bin/activate
```

Install all required packages

```bash
  pip install -r requirements.txt
```

## IMPORTANT

If you want to run this software, you need to properly configure it on all devices. This software cannot function independently.
