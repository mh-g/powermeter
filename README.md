# powermeter

Parses IEC 62056-21 data and stores it in a RRD tool database.
The RRD database needs to have the following columns: "paid", "excess", and "delta".
"paid" contains the information from the "1.8.0" sentence (i. e. power that was taken from the grid)
"excess" contains the information from the "2.8.0" sentence (i. e. power that was put into the grid)
"delta" contains "paid" - "excess" (i. e. the difference between taken and put for a certain period)

Notice: For longer periods, there may be both "paid" and "excess" data for the same time slice.

I obtain the raw data using https://github.com/mh-g/Arduino-iec62056-21
