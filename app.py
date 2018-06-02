import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
Date_stops = Base.classes.date_stops
Gender_stops = Base.classes.gender_stops
Race_stops = Base.classes.race_stops
County_stops = Base.classes.county_stops
Gender_crashes = Base.classes.gender_crashes
Race_crashes = Base.classes.race_crashes
County_crashes = Base.classes.county_crashes

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


@app.route("/stops_by_date")
def stops_by_date():

    results = session.query(Date_stops).all()

    total_by_date = []

    for row in results:
        totals = {}

        totals["date"] = row.date
        totals["stops_2010"] = row.stops_2010
        totals["stops_2011"] = row.stops_2011
        totals["stops_2012"] = row.stops_2012
        totals["stops_2013"] = row.stops_2013
        totals["stops_2014"] = row.stops_2014
        totals["stops_2015"] = row.stops_2015

        total_by_date.append(totals)

    return jsonify(total_by_date)


@app.route("/stops_by_race")
def stops_by_race():

    stop_results = session.query(Race_stops).all()
    census_results = session.query(Demographics).all()

    total_by_race = []

    for row in stop_results:
        totals = {}

        totals["year"] = row.year
        totals["asian_stops"] = row.asian
        totals["black_stops"] = row.black
        totals["hispanic_stops"] = row.hispanic
        totals["other_stops"] = row.other
        totals["white_stops"] = row.white

        total_by_race.append(totals)

    for year in total_by_race:
        for row in census_results:
            if year["year"] == str(row.year):
                year["asian_pop"] = row.asian
                year["black_pop"] = row.black
                year["hispanic_pop"] = row.hispanic
                year["other_pop"] = row.pacific_islander + row.other_race
                year["white_pop"] = row.white

    return jsonify(total_by_race)


@app.route("/stops_by_gender")
def stops_by_gender():

    stop_results = session.query(Gender_stops).all()
    census_results = session.query(Demographics).all()

    total_by_gender = []

    for row in stop_results:
        totals = {}

        totals["year"] = row.year
        totals["male_stops"] = row.male
        totals["female_stops"] = row.female

        total_by_gender.append(totals)

    for year in total_by_gender:
        for row in census_results:
            if year["year"] == str(row.year):
                year["male_pop"] = row.male
                year["female_pop"] = row.female

    return jsonify(total_by_gender)


@app.route("/stops_by_county")
def stops_by_county():

    results = session.query(County_stops).all()

    total_by_county = []

    for row in results:
        totals = {}

        totals["county"] = row.county
        totals["stops_2010"] = row.stops_2010
        totals["stops_2011"] = row.stops_2011
        totals["stops_2012"] = row.stops_2012
        totals["stops_2013"] = row.stops_2013
        totals["stops_2014"] = row.stops_2014
        totals["stops_2015"] = row.stops_2015

        total_by_county.append(totals)

    return jsonify(total_by_county)

@app.route("/crashes_by_race")
def crashes_by_race():

    crash_results = session.query(Race_crashes).all()
    census_results = session.query(Demographics).all()

    total_by_race = []

    for row in crash_results:
        totals = {}

        totals["year"] = row.year
        totals["native_american_crashes"] = row.native_american
        totals["asian_crashes"] = row.asian
        totals["black_crashes"] = row.black
        totals["hispanic_crashes"] = row.hispanic
        totals["other_crashes"] = row.other
        totals["white_crashes"] = row.white

        total_by_race.append(totals)

    for year in total_by_race:
        for row in census_results:
            if year["year"] == str(row.year):
                year["native_american_pop"] = row.native_american
                year["asian_pop"] = row.asian
                year["black_pop"] = row.black
                year["hispanic_pop"] = row.hispanic
                year["other_pop"] = row.pacific_islander + row.other_race
                year["white_pop"] = row.white

    # Since there's no census population data for 2017 and 2018, remove those dicts from the list
    total_by_race = [x for x in total_by_race if not (("2017" == x.get('year')) or ("2018" == x.get("year")))]


    return jsonify(total_by_race)

@app.route("/crashes_by_gender")
def crashes_by_gender():

    crash_results = session.query(Gender_crashes).all()
    census_results = session.query(Demographics).all()

    total_by_gender = []

    for row in crash_results:
        totals = {}

        totals["year"] = row.year
        totals["male_crashes"] = row.male
        totals["female_crashes"] = row.female

        total_by_gender.append(totals)

    for year in total_by_gender:
        for row in census_results:
            if year["year"] == str(row.year):
                year["male_pop"] = row.male
                year["female_pop"] = row.female

    # Since there's no census population data for 2017 and 2018, remove those dicts from the list
    total_by_gender = [x for x in total_by_gender if not (("2017" == x.get('year')) or ("2018" == x.get("year")))]

    return jsonify(total_by_gender)

@app.route("/crashes_by_county")
def crashes_by_county():

    results = session.query(County_crashes).all()

    total_by_county = []

    for row in results:
        totals = {}

        totals["county"] = row.county
        totals["crashes_2010"] = row.crashes_2010
        totals["crashes_2011"] = row.crashes_2011
        totals["crashes_2012"] = row.crashes_2012
        totals["crashes_2013"] = row.crashes_2013
        totals["crashes_2014"] = row.crashes_2014
        totals["crashes_2015"] = row.crashes_2015
        totals["crashes_2016"] = row.crashes_2016
        totals["crashes_2017"] = row.crashes_2017
        totals["crashes_2018"] = row.crashes_2018

        total_by_county.append(totals)

    return jsonify(total_by_county)


@app.route('/crashesPar')
def crashesPar():

    results = session.query(Crashes).order_by(func.random()).limit(150).all()

    cars = []
    map = []

    for row in results:
        crash_result = {}
        crash_result["crash_year"] = row.crash_year
        crash_result["speed_limit"] = row.speed_limit
        crash_result["person_age"] = row.person_age
        crash_result["crash_death_count"] = row.crash_death_count
        crash_result["crash_total_injury_count"] = row.crash_total_injury_count
        crash_result["crash_time"] = row.crash_time
        cars.append(crash_result)

    for row in results:
        mapData = {}
        mapData["city"] = row.city
        mapData["county"] = row.county
        mapData["crash_death_count"] = row.crash_death_count
        mapData["crash_severity"] = row.crash_severity
        mapData["crash_time"] = row.crash_time
        mapData["crash_total_injury_count"] = row.crash_total_injury_count
        mapData["crash_year"] = row.crash_year
        mapData["day_of_week"] = row.day_of_week
        mapData["latitude"] = row.latitude
        mapData["longitude"] = row.longitude
        mapData["manner_of_collision"] = row.manner_of_collision
        mapData["population_group"] = row.population_group
        mapData["road_class"] = row.road_class
        mapData["speed_limit"] = row.speed_limit
        mapData["weather_condition"] = row.weather_condition
        mapData["vehicle_color"] = row.vehicle_color
        mapData["person_age"] = row.person_age
        mapData["person_ethnicity"] = row.person_ethnicity
        mapData["person_gender"] = row.person_gender
        mapData["person_type"] = row.person_type
        map.append(mapData)

    return jsonify(cars, map)

@app.route('/wordList')
def wordList():

    results = session.query(County_crashes).all()
    crashcty = []

    for row in results:
        crash_result = {}
        crash_result["county"] = row.county

        if(row.crashes_2010 == None):
            row.crashes_2010 = 0

        elif(row.crashes_2011 == None):
            row.crashes_2011 = 0

        elif(row.crashes_2012 == None):
            row.crashes_2012 = 0

        elif(row.crashes_2013 == None):
            row.crashes_2013 = 0

        elif(row.crashes_2014 == None):
            row.crashes_2014 = 0

        elif(row.crashes_2015 == None):
            row.crashes_2015 = 0

        elif(row.crashes_2016 == None):
            row.crashes_2016 = 0

        crash_result["allCrash"] = row.crashes_2010 + row.crashes_2011 + row.crashes_2012 + row.crashes_2013 + row.crashes_2014 + row.crashes_2015 + row.crashes_2016
        crashcty.append(crash_result)

    return jsonify(crashcty)



@app.route("/example")
def example():
    return render_template("flask_plotly_example.html")

@app.route("/date_graph")
def date_graph():
    return render_template("date_graph_svg.html")

@app.route("/race_graph")
def race_graph():
    return render_template("race_graph.html")

@app.route("/gender_graph")
def gender_graph():
    return render_template("gender_graph.html")

@app.route("/crashes_gender_graph")
def crashes_gender_graph():
    return render_template("crashes_gender_graph.html")

@app.route("/crashes_race_graph")
def crashes_race_graph():
    return render_template("crashes_race_graph.html")


@app.route("/bubble")
def bubble():
    return render_template("bubble.html")

@app.route("/map_chart")
def map_chart():
    return render_template("map_chart.html")


if __name__ == "__main__":
    app.run(debug=True)
