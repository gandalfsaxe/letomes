# NASA JPL SSD Horizons Web-Interface Settings

## Current Settings

Ephemeris Type [change] :  	OBSERVER
**Target Body [change] :  	 	Earth [Geocenter] [399]   OR   Mars [499]**
**Observer Location [change] :  	Sun (body center) [500@10]**
**Time Span [change] :  	Start=2019-01-01, Stop=3019-01-01, Step=1 d**
**Table Settings [change] : 	QUANTITIES=1,3,16-20,22,28,31,33,41; date/time format=BOTH; time digits=FRACSEC; angle format=DEG; extra precision=YES; CSV format=YES**
**Display/Output [change] : 	download/save (plain text file)**

_NOTE:_
year 2265 chosen due to the output lines are limited. Chosing e.g. 2019-3019 gave error:
`Projected output length (~365243) exceeds 90024 line max -- change step-size`

So we chose:
`2019+90024/365 = 2,265.64 = 2265`

It also turns out that Mars ephemerides [only goes](https://ssd.jpl.nasa.gov/eph_spans.cgi?id=A) to year 2500 Jan 04, in Horizon.

## Table Settings

See "Current Settings" above for enabled quantities. Many quantities are not used to included anyway due to being of potential interest.

NOTE the following quantities were `n.a.` even though they could've been of potential interest:
- 27.	Sun-Target radial & -vel pos. angle
- 36.	RA & DEC uncertainty
- 39.	Range & range-rate 3-sigmas

### Optional observer-table settings:
**date/time format : both   -- display date/time in year-month-day and/or Julian-day format  **
**time digits : fractional seconds (HH:MM:SS.SSS)   -- controls output precision of time  **
**angle format : decimal degrees   -- select RA/Dec output format  **
output units : km & km/s   -- units for most output quantities  
range units : astronomical units   -- units for range-type quantities  
refraction model : airless model (no refraction)   -- select atmospheric refraction model  
airmass cut-off :-- suppress output when airmass is greater than limit [1 to 38]  
elevation cutoff : [EMPTY]   (deg) -- suppress output when object elevation is less than limit [-90 to 90]  
solar elong. cut-off : [EMPTY] - [EMPTY]   (deg) -- suppress output when solar elongation is outside (min,max) range [0 to 180, min to 180]
hour angle cutoff : [EMPTY]   (h) -- suppress output when the local hour angle (LHA) exceeds value [0 to 12]  
angular rate cutoff : [EMPTY]   (arcsec/h) -- suppress output when the RA/Dec angular rate exceeds this value [0 to 100000]  
suppress range-rate : [UNCHECKED]   -- suppress range-rate for range/range-rate output  
skip daylight : [UNCHECKED]   -- suppress output during daylight  
**extra precision : [CHECKED]   -- output addition digits for RA/Dec quantities  **
RTS flag : [DISABLE]   -- output data only at target rise/transit/set (RTS)  
reference system : ICRF/J2000.0	 -- reference frame for geometric and astrometric quantities  
**CSV format : [CHECKED]   -- output data in Comma-Separated-Values (CSV) format  **
object page : [CHECKED]   -- include object information/data page on output  
