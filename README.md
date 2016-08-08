# Tagged Point Cloud 

## Purpose

This is a JSON microformat for storing a collection of points in R^n
(a "cloud") and additional data related to the points in the form of
*attributes* and *tags*.

This format is an alternative to CSV (and its relatives) that is
adapted to a specific use case---point clouds in space where each
point is labeled with additional data.  It addresses the following
shortcomings of CSV for this application:

* While CSV is good for tabular data, it does not offer a standardized
  method to embed machine-readable metadata.

* For CSV files representing point clouds in space (e.g. cities on a
  2-dimensional map, stars in a galaxy, etc.), there are often
  additional columns containing attributes of the points separate from
  their locations (e.g. population of a city, brightness of a star).
  CSV does not have a standard way to distinguish between columns for 
  coordinates and those containing non-positional data.

* There is no easy way to embed named subsets of the rows in a CSV
  file, for example to indicate a region of interest.  Adding
  additional boolean "membership indicator" columns is one way to
  handle this, however it adds to the file size in proportion to the
  full dataset size, rather than in proportion to the size of the
  subset.


## Specification

The format is specified in doc/TPC.md.

## Library

A simple Python 3.x module to read and write this file format can be
found in `pytpc`.  A utility to convert CSV to TPC using this library
is also included there.

## Maintainer

David Dumas <david@dumas.io>
