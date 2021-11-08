# MDM3-TRL
Importing DataSets
    Bus Location Data set
        getLocationData / getLocationDataAtTimes
            Gets the location data from the open data for a particular operator, operator is given by the datafeed ID. This can be found on the gov open data website
        SaveLocationData
            Saves the latitude and longitude of the live location data for each 5 second live bus data update over a set period of time.
        getLineIds
            Loads the saved live location data, output as a dataframe
        VisualiseLocationData
            Out of use - been replaced by visualise with maps
        VisualiseWithMaps
            Displays a selection of buses on the map
    Timetables
        getTimetableData
        ImportTimetableDatav.2
            Gets the timetable data in a dictionary
    Bus Stops
        getStopLocations
            Gets the locations of the bus stops
        ReadPKL
    Traffic
        getTrafficGates
            Imports pairs of coordinates for the start and end of each bus gate

Methods
    anprCameraRoutes
        Plot the route of the gate
    getBusTraffic
        Get speed of bus through a gate and compare it to the average speed
