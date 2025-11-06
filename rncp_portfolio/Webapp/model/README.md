Mission Recommendation System

This project provides a mission recommendation engine for medical/clinical environments.
It loads user preference data, computes similarities between users, and recommends the best-matched missions based on services, specialties, and work rhythms.

The system uses:

    Cosine similarity (pre-computed & cached)

    Jaccard similarity between users for mission scoring

    Database user data, cleaned using failsafes

    Configurable models and generators (services × specialties × rhythms)

📁 Project Structure
.
├── main.py
├── similarity.py
├── calculators.py
├── models.py
├── db_tools.py
├── model_cache.py
├── failsafes.py
├── refresher.py
├── file_system_tools.py
├── exceptions.py

File Overview
    main.py

        Main entry point.
        Contains the recommend() function which:

        Loads dataset & cosine similarity (via model_cache.py)

        Fetches user data from DB (db_tools.py)

        Cleans data with failsafes (failsafes.py)

        Computes recommendation scores (similarity.py)

        Returns sorted mission recommendations

    similarity.py

        Computes mission similarity & final mission scores.

        Includes:

            compute_mission_scores()

                Retrieves similar users using cosine similarity

                Computes Jaccard similarity between users

                Weights mission scores

                Returns missions sorted by relevance

    models.py

        Defines model structures used to generate all mission combinations:

        lists of services, specialties, and rythms

        functions to generate all mission tuples

        utility to cast or normalize data types

     calculators.py   

        Helper module for mission generation and conversions.

        Contains:

            mission tuple expansion (service × specialty × rhythm)

            utilities like cast_to_int() for data normalization

     db_tools.py

        Database interface.

        Loads DB connection variables via dotenv

        Fetches user preference data from MySQL

        Returns user row as a dict

     model_cache.py

        Handles all caching of heavy model objects:

        Loads dataset from .joblib

        Loads or generates cosine similarity matrix

        Saves results into cache folder

        Returns (data, cosine_sim)

        Useful to avoid recalculating similarity matrices every run.

     failsafes.py

        Provides default/fallback values when user data is incomplete.

        Includes:

            default service / specialty / rhythm vectors

            merges user data with fallback values

            ensures the model always receives valid inputs

     refresher.py

        Tool to rebuild training data:

        loads raw data from storage (GCS or local)

        generates full mission combinations

        builds a training dataset for similarity model

        saves the new dataset into the cache

        Used when new missions or users are added.

     file_system_tools.py

        File system abstraction (local or GCS):

        returns filesystem handler (GCSFS or local OSFS)

        used for reading/writing model files