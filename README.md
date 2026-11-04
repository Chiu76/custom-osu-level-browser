## Introduction

Custom level browser for the game osu! with advanced filtering and grouping functionalities.

## Current features

Imports beatmaps, scores, and collections from a local osu!stable install.

Filter and sort beatmaps by their scores (example: acc>94, grade=S). Each beatmap has its "top score" attached to it for query purposes, users can choose criteria for which score gets attached (best accuracy, latest score, more options later).

Perform set operations between groupings (collections, hardcoded groupings such as OD): 
 - right click a grouping to select it as "Source"
 - left click a different grouping to select it as a "Grouping"
 => leads to showing only the intersection of the two groupings

Multiple selected sources and groupings are supported.

## Planned features

- lazer support, mcosu support
- import all beatmaps and scores the user has ever set
- beatmap pack support
- custom star rating: aim/tapping/reading values per beatmap, normalized aim/tapping values (treating each map as if it's the same speed)
- custom tapping difficulty measures based on time between triples/bursts/streams

## Setup

Under backend/, create .env file based on .env.example, add path to osu!stable instance under OSU_DIRECTORY.

## Commands
Backend:
    uv sync
    python -m src.common.exec_full_import recreate_db
    uv run fastapi dev
Frontend:
    python -m http.server 3000