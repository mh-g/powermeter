# powermeter

Parses IEC 62056-21 data and stores it in a RRD tool database. The RRD database needs to have the following columns: "paid", "excess", and "delta".

"paid" contains the information from the "1.8.0" sentence (i. e. power that was taken from the grid)

"excess" contains the information from the "2.8.0" sentence (i. e. power that was put into the grid)

"delta" contains "paid" - "excess" (i. e. the difference between taken and put for a certain period)

Notice: For longer periods, there may be both "paid" and "excess" data for the same time slice.

Depends / tested on:
- Python 3.7.3
- pyserial 3.4
- rrdtool 0.1.15

I obtain the raw data using https://github.com/mh-g/Arduino-iec62056-21

Graphical outputs are done with e.g.:

<code>rrdtool graph /tmp/power.png --start now-12h --end now DEF:p=/localdata/powermeter.rrd:paid:MAX CDEF:prev_p=PREV\(p\) CDEF:time_p=p,POP,TIME CDEF:prevtime_p=PREV\(time_p\) CDEF:p_derivate=p,prev_p,-,time_p,prevtime_p,-,/ AREA:p_derivate#ff0000:"Verbrauch" VDEF:last_p=p,LAST "GPRINT:last_p:Summe\: %.4lf kWh" VDEF:paid_max=p_derivate,MAXIMUM "GPRINT:paid_max:Spitze\: %lf" DEF:e_unsigned=/srv/dev-disk-by-label-DISK1/localdata/powermeter.rrd:excess:MAX CDEF:e=e_unsigned,-1,* CDEF:prev_e=PREV\(e\) CDEF:time_e=e,POP,TIME CDEF:prevtime_e=PREV\(time_e\) CDEF:e_derivate=e,prev_e,-,time_e,prevtime_e,-,/ AREA:e_derivate#00ff00:"erzeugt" VDEF:last_e=e,LAST "GPRINT:last_e:Summe\: %.4lf kWh" VDEF:excess_min=e_derivate,MINIMUM GPRINT:excess_min:"Spitze\: %lf" --width 720 --height 360</code>

(720 x 360 pixels, 12h history, paid in red above x-axis, excess in green below x-axis, some stats below the plot)
