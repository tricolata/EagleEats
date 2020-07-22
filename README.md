# EagleEats
![](eagleseat/static/img/preview.png)

# Table of Contents
* [Setup and Installation](#setup-and-installation)
    * [Requirements](#requirements)
    * [Installation](#installation)
    * [Running](#running)
* [Documentation](#documentation)
    * [Environment Variables](#environment-variables)
    * [Data Storage and Exchange](#data-storage-and-exchange)
        * [Database Structure](#database-structure)
        * [Cart Structure](#cart-structure)

## Setup and Installation

### Requirements
* [Python](https://www.python.org/) version 3.7 or higher
* [Pip](https://pip.pypa.io/en/stable/installing/)

### Installation

#### Cloning
Clone and navigate to the repository:

```
   git clone https://github.com/yafetkubrom/csce-3444-project/
   cd csce-3444-project
```

#### Installing Packages
Install the required pip packages with the following command

`pip3 install -r requirements.txt`

### Running
First, `cd` into the `eagleseat` directory:

`cd eagleseat`

Then, start the flask server:

`python3 -m flask run`

## Documentation

### Environment Variables
Environment variables to be used during the program are to be stored in a `.env`
file inside of the `eagleseat` directory. An example file (`.env.example` ) is included.

If you would like to use the example file, run the following inside of the `eagleseat` directory:

`mv .env.example .env`

### Data Storage and Exchange
[]: # TODO: Write Data Storage and Exchange Documentation

#### Database Structure
[]: # TODO: Write Database Structure Documentation

#### Cart Structure
[]: # TODO: Write Cart Structure Documentation
