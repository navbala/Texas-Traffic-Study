import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template

app = Flask(__name__)

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
Demographics = Base.classes.demographics

# Create our session (link) from Python to the DB
session = Session(engine)

@app.route("/")
def index():

    """Return the homepage."""
    return render_template('index.html')


@app.route('/allcrashes')
def allCrashes():
    # Returning EVERYTHING from the Crashes table

    results = session.query(Crashes).all()

    all_crashes = []

    for row in results:
        crash_result = {}
        crash_result["id"] = row.id
        crash_result["crash_id"] = row.crash_id
        crash_result["agency"] = row.agency
        crash_result["city"] = row.city
        crash_result["county"] = row.county
        crash_result["crash_death_count"] = row.crash_death_count
        crash_result["crash_severity"] = row.crash_severity
        crash_result["crash_time"] = row.crash_time
        crash_result["crash_total_injury_count"] = row.crash_total_injury_count
        crash_result["crash_year"] = row.crash_year
        crash_result["day_of_week"] = row.day_of_week
        crash_result["latitude"] = row.latitude
        crash_result["longitude"] = row.longitude
        crash_result["manner_of_collision"] = row.manner_of_collision
        crash_result["population_group"] = row.population_group
        crash_result["road_class"] = row.road_class
        crash_result["speed_limit"] = row.speed_limit
        crash_result["weather_condition"] = row.weather_condition
        crash_result["vehicle_color"] = row.vehicle_color
        crash_result["person_age"] = row.person_age
        crash_result["person_ethnicity"] = row.person_ethnicity
        crash_result["person_gender"] = row.person_gender
        crash_result["person_type"] = row.person_type
        all_crashes.append(crash_result)

    return jsonify(all_crashes)



@app.route('/allcensus')
def allCensus():

    # Returning EVERYTHING from the demographics table

    results = session.query(Demographics).all()

    allDemo = []

    for row in results:
        demo_row = {}
        demo_row["id"] = row.id
        demo_row["year"] = row.year
        demo_row["total_population"] = row.total_population
        demo_row["male"] = row.male
        demo_row["female"] = row.female
        demo_row["age_under_5"] = row.age_under_5
        demo_row["age_5_to_9"] = row.age_5_to_9
        demo_row["age_10_to_14"] = row.age_10_to_14
        demo_row["age_15_to_19"] = row.age_15_to_19
        demo_row["age_20_to_24"] = row.age_20_to_24
        demo_row["age_25_to_34"] = row.age_25_to_34
        demo_row["age_35_to_44"] = row.age_35_to_44
        demo_row["age_45_to_54"] = row.age_45_to_54
        demo_row["age_55_to_60"] = row.age_55_to_60
        demo_row["age_60_to_64"] = row.age_60_to_64
        demo_row["age_65_to_74"] = row.age_65_to_74
        demo_row["age_75_to_84"] = row.age_75_to_84
        demo_row["age_85_and_over"] = row.age_85_and_over
        demo_row["white"] = row.white
        demo_row["black"] = row.black
        demo_row["native_american"] = row.native_american
        demo_row["asian"] = row.asian
        demo_row["pacific_islander"] = row.pacific_islander
        demo_row["other_race"] = row.other_race
        demo_row["hispanic"] = row.hispanic
        allDemo.append(demo_row)

    return jsonify(allDemo)


@app.route('/crashColumns')
def crashColumns():

    # Use Pandas to perform the sql query
    stmt = session.query(Crashes).statement
    df = pd.read_sql_query(stmt, session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns))


@app.route('/censusColumns')
def censusColumns():

    # Use Pandas to perform the sql query
    stmt = session.query(Demographics).statement
    df = pd.read_sql_query(stmt, session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns))



@app.route('/crashes2016')
def crashes2016():
    # Returning 2016 crashes only from the Crashes table

    results = session.query(Crashes).all()

    all_crashes = []

    for row in results:

        if row.crash_year == 2016:
            crash_result = {}
            crash_result["id"] = row.id
            crash_result["crash_id"] = row.crash_id
            crash_result["agency"] = row.agency
            crash_result["city"] = row.city
            crash_result["county"] = row.county
            crash_result["crash_death_count"] = row.crash_death_count
            crash_result["crash_severity"] = row.crash_severity
            crash_result["crash_time"] = row.crash_time
            crash_result["crash_total_injury_count"] = row.crash_total_injury_count
            crash_result["crash_year"] = row.crash_year
            crash_result["day_of_week"] = row.day_of_week
            crash_result["latitude"] = row.latitude
            crash_result["longitude"] = row.longitude
            crash_result["manner_of_collision"] = row.manner_of_collision
            crash_result["population_group"] = row.population_group
            crash_result["road_class"] = row.road_class
            crash_result["speed_limit"] = row.speed_limit
            crash_result["weather_condition"] = row.weather_condition
            crash_result["vehicle_color"] = row.vehicle_color
            crash_result["person_age"] = row.person_age
            crash_result["person_ethnicity"] = row.person_ethnicity
            crash_result["person_gender"] = row.person_gender
            crash_result["person_type"] = row.person_type
            all_crashes.append(crash_result)

    return jsonify(all_crashes)



if __name__ == "__main__":
    app.run(debug=True)
