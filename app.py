import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


#################################################
# Database Setup
#################################################
dbfile = os.path.join('speeding.sqlite')
engine = create_engine(f"sqlite:///{dbfile}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Crashes = Base.classes.crashes

# Create our session (link) from Python to the DB
session = Session(engine)
