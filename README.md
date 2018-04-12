# org_to_anki

[![Build Status](https://travis-ci.org/c-okelly/org_to_anki.svg?branch=master)](https://travis-ci.org/c-okelly/org_to_anki) [![codecov](https://codecov.io/gh/c-okelly/org_to_anki/branch/master/graph/badge.svg)](https://codecov.io/gh/c-okelly/org_to_anki)

Python module to convert org files into Anki question decks.

Provides two command line scripts to upload org files and take new basic notes quickly.
 
Based on [AnkiConnect](https://ankiweb.net/shared/info/2055492159). An addon for Anki that provides a HTTP api for Anki.

## Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Comannd line scripts](#command-line-scripts)
4. [Org file syntax](#org-file-syntax)
5. [Parameters](#parameters)
6. [Running tests](#testing)
7. [Future features](#future-features)

## Requirements

1. Have the [Anki app](https://apps.ankiweb.net/) installed.
2. Installing the Anki plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159).

	i. For OSX users of anki-connect see [note for OSX users](https://foosoft.net/projects/anki-connect/#installation)
	
	ii. For Windows users of anki-connect see [notes for Windows users](https://foosoft.net/projects/anki-connect/#installation) 

## Installation

To install this module from source.

1. git clone https://github.com/c-okelly/org_to_anki
2. cd into the module directory
3. python3 setup.py install

## Command line scripts

### org_to_anki

```bash
org_to_anki
```
* Upload the default org file to Anki

```bash
org_to_anki /path/to/your/org/file.org
```
* Upload the specified file to Anki

### ankiq

* New questions are added to the default file stored at ~/orgNotes/quickOrgNotes.org
* This file is created by default if it does not already exist

```bash
ankiq
```
* Will start a Python input reply.
* Takes a questions and a series of anwers
* Empty line add a new question to the default org file

## Org file syntax

* Currently supports two different types of org files
* All questions and answers should start with an asterix
* All comment lines start with a \#
```org
# Line comments
* Question
** Answer
```

* Each org file will be converted into its own deck in Anki

### Global Parameters 

* Parameters to be inherited by all questions / decks should be specified at the top file.
* These will be overwritten by parameters lower down the tree.

```org
# Basic Example
# type=Basic

* Question
** Answer
* Second Question
# type=Basic (and reversed card)
** Second Answer
```

### Basic org file syntax

* Sample answer and question in org file

 ```org
 * What is the capital of Ireland?
 ** Dublin
 ```
 
### Topics file syntax

* Each topic will be turned into its own subdeck. The name of this deck is given by the first line. E.G Capitals cities and Spoken languages.
* Allows for a group of related topics to be managed in a single file.

* Sample answer and questions for topics org file.

 ```org
 * Capital cities
 ** What is the capital of Ireland?
 *** Dublin
 * Spoken languages
 ** What are the main spoken languages in Ireland?
 *** English
 *** Irish
 ```

### Parameters

* Supported parameter syntax.

1. Each line must start with a hashtag
```org 
# type=Basic
# type = Basic
```

* Currently supported parameters are questions type

1. Org file type
* By default all org files will be of basic type.
* If you want to use a topics layout must be specified at the top of the file.

```org
# Comment line
# fileType=topics

* Topics 1
** Questions 1
*** Answer 1
```

2. Question type. Used to set the type of the Anki note.
    i. Default value is Basic

```org
# type=Basic
# type=Basic (and reversed card)
```

#### Parameter inheritance

* Questions and decks will inhert parameters from parent Decks
* Parameters inhereted will not override existing parameters.

## Config values

* Config in project root contains all the default values for running
* Default org file is located at ~/orgNotes/quickOrgNotes.org
* Default anki-connect url is http://127.0.0.1:8765/

## Testing

A number of extra libraries are used in testing

* To run unittests 
``` bash
python3 setup.py nosetests
```

## Future features

* Check to see if note exists before sending to Anki
* Expanded support for different paramters types
* If you have a feature you would like to see please open an issue!
 
