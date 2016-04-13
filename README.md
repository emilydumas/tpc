== Tagged Point Cloud ==

This is a JSON data format for storing a collection of points in R^n
(a "cloud") and additional data related to the points in the form of
*attributes* and *tags*.

The format is specified in doc/TPC.md.

A python implementation of a library to read and write this file
format is planned.


An attribute is pair consisting of a string, the *attribute name*, and
a JSON object associated to each point in the cloud (collectively
these are the *attribute values*).  The attribute names used in a
given file are stored in a header.  The attribute values are stored
with the coordinates of the points in the cloud.

A tag is a pair consisting of a string, the *tag name*, and a subset
of the cloud, the *tag set*.  These are stored by associating to each
point in the cloud a list of tag names for which that point belongs to
the tag set.

