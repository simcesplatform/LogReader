# API

The reader implements the following API described below. This API definition is a work in progress. It is based on uncertain assumptions about the way the data would be used, what is the message data structure in particular how timeseries are stored, and what are the query capabilities of the MongoDB database where messages are stored. Changes in these assumptions may require changes to the API definition.

The following notation is used to document request parameters and members of JSON objects in response and request bodies:

- name (data type, parameter type, required): description

- name: parameter or json member name
- data type: value data type such as string, integer or ISO datetime
- parameter type: Only for request parameters either in the URL path or in the URL query parameters
- required: Indicates that the parameter or JSON member is required. If this keyword is not present the parameter or member is optional. This is not used with response JSON where all members can be assumed to be present.
- description: Explain the purpose of the parameter or JSON member.

## Get simulations

method: GET  
path: /simulations

Returns a list of simulation runs the message database has messages for.

### Request parameters

- fromDate (ISO datetime, query): Return simulation runs which have started on or after the given date.
- toDate (ISO datetime, query) Return simulation runs that have been started before the given date.

### Response

List of simulation runs with the following information available about every run.

- simulationId (string): The id of the simulation.
- name (string): A human friendly name for the simulation.
- description (string): A longer description of the simulation run meant for humans.
- startTime (ISO datetime): The real wordl start time of the simulation run.
- endTime (ISO datetime): The real world end time of the simulation run.
- epoch (integer): Number of epochs in the simulation run.
- process (string[]): List of names of processes participating in the simulation run.

### Notes

Name and description are just a idea that seems good but of course they then would have to be provided when the simulation is created and some how communicated to the database process. List of process names would also be nice to get somewhere though the logger process can also just keep a record of processes it gets messages from and then save them to the database when the simulation is done. If there can be a lot of processes it might not make sense to list them here. Would we need other ways to search for runs for example some kind of categorization or tagging system. We could also have a concept like simulation author or owner i.e. person or (persons?) who created the simulation. This would help people to find their simulations.

## Get simulation

method: GET  
path: /simulations/{simulationId}

Returns general information about the given simulation run.

### Request parameters

- simulationId (string, path, required): The id of a simulation run.

### Response

Information about the given simulation run with the same contents as in each get simulations response item.

### Notes

Could also give more detailed information if we have it. For example list of topics used in the simulation run could be included here . As the response is defined now this API endpoint is not necessary since the same information can be obtained from the get simulations response assuming that the processes list will be there.

## Get messages for simulation run

method: GET  
path: /simulations/{simulationId}/messages

Returns messages from the given simulation run. Without parameters returns all messages. Parameters allow filtering in various ways.

### Request parameters

- simulationId (string, path, required): Id of the simulation run messages are fetched from.
- startEpoch (integer, query): Return messages published on or after the given epoch. Not applicable if epoch, fromSimDate or toSimDate are used.
- endEpoch (integer, query): Return messages posted on or before the given epoch. Not applicable if the epoch, fromSimDate or toSimDate are used.
- epoch (integer, query): return messages posted during the given epoch. Not applicable if fromSimDate, toSimDate endEpoch or startEpoch are used.
- fromSimDate (ISO datetime, query): Return messages starting from the epoch that includes the given date. Not applicable if fromEpoch, epoch or toEpoch are used.
- toSimDate (ISO datetime, query): Return messages until the epoch that includes the given date. Not applicable if fromEpoch, epoch or toEpoch are used.
- process (string, query): Return messages that have been published by the given processes i.e. messages whose source is the given process. Value is a comma separated list of process ids.
- topic (string, query): Return messages published to the given topic. Supports the same notation that is used when subscribing to the topics i.e. the same wildcard mechanism including the * and # characters.
- onlyWarnings: (boolean, query): If true only messages that include warnings are returned. If false messages with and without warnings are both returned. False is the default behaviour if this parameter is not used.

### Response

List of messages as they have been saved into the database including the message metadata.

### Notes

Depending on how exactly the db querying works it might not be possible to emulate the topic based filtering so that it fully supports how the subscribing  works. So topic filtering may be more limited than now promised here.

Should there be options for limiting what part of messages are returned. Current idea is return everything i.e. the metadata in the db and the message contents as is.

## Get simple timeseries for simulation

method: GET  
path: /simulations/{simulationId}/timeseries

Returns timeseries data constructed from given attributes of messages that meet the given time, topic and process based filtering conditions.

### Request parameters

Same parameters as in get simulation messages are used except onlyWarnings. In addition the following parameters are used:

- attrs (string, query, required) Comma separated list of names of message attributes whose values are assumed to be time series and which are then included to the timeseries response. It is possible to refer deeper into the message structure using the dot notation for example foo.bar.
- format (string, query): Determines the response format. Possible values are csv and json. If this parameter is not used json is used as the default value.

### Response

json

A JSON object with the following members:

- timeIndex (timeIndex[]): List of time index objects that indicate the timestamp for the data. For example if a timeindex object is the fifth item in the timeindex list then it has the time for the fifth attribute value in each value list. If there is no value for an attribute for a corresponding timeIndex value, the value will be nul.
- {topic} (topicData): For each topic there is timeseries data a member named after the topic. The value is a topicDATa object.

timeIndex object

- timestamp (ISO datetime): Indicates the simulation time for the corresponding data. 
- epoch (integer): Indicates the epoch for the corresponding data.

TopicData object

- {processName} (processData): For each process the timeseries has values for in the given topic a member where processName is replaced with the id of the process. The value is then processData object.

processData object

- {attr}: For each message attribute a member where attr is replaced with the attribute name. The value is then list of attribute values from the messages. Depending on the data it can be a single value like a number or more complex data structure.

csv

csv data with the following column titles and colun value data types

- epoch (integer): Number of the epoch the data in the row is from.
- timestamp (iso datetime): Simulation timestamp for the data in the row.
- {topic}:{processname}.{attr}: For each topic, process and message attribute the timeseries contains data for there is a column for it with a title consisting of the topic, process and attribute names. If there is no data for the row at a certain time then the column has an empty cell.

### Usage example 1

note: For simplicity this is based on a imaginary simulation with one hour epochs and just two data items an half hour apart per epoch. In reality one horu long epoch would probably have more data.

Get the charge state percentage for batteries batter1 and battery2 between 12:00 and 14:00 on 1st January 2020 in simulation with id 2020-06-10T10:00:00Z in the JSON format. This assumes that there is a batteryState topic and that the message there contains a chargePercentage attribute. During the two epochs covered in the query then the batteries have reported their status in each epoch and both status report messages have contained a timeseries for the charge percentage with two items.

#### request

    GET /simulations/2020-06-10T10:00:00Z/timeseries?process=battery1,battery2&topic=batteryState&attrs=chargePercentage&fromSimDate=2020-01-01T12:00:00Z&toSimDate=2020-01-01T14:00:00Z

#### Response

```
{
    "timeIndex": [
        {
            "epoch": 50,
            "timestamp": "2020-01-01T12:00:00Z"
        },
        {
            "epoch": 50,
            "timestamp": "2020-01-01T12:30:00Z"
        },
        {
            "epoch": 51,
            "timestamp": "2020-01-01T13:00:00Z"
        },
        {
            "epoch": 51,
            "timestamp": "2020-01-01T13:30:00Z"
        }
    ],
    "batteryState": {
        "battery1": {
            "chargePercentage": [
                90,
                88,
                87,
                91
            ]
        },
        "battery2": {
            "chargePercentage": [
                40,
                42,
                45,
                48
            ]
        }
    }
}
```

### Usage example 2

Same as example 1 except the timeseries data is requested in the csv format.

#### Request

    GET /simulations/2020-06-10T10:00:00Z/timeseries?process=battery1,battery2&topic=batteryState&attrs=chargePercentage&fromSimDate=2020-01-01T12:00:00Z&toSimDate=2020-01-01T14:00:00Z&format=csv

#### Response

```
epoch, timestamp, batteryState:battery1.chargePercentage, batteryState:battery2.chargePercentage
50, 2020-010-01T12:00:00Z, 90, 40
50, 2020-010-01T12:30:00Z, 88, 42
51, 2020-010-01T13:00:00Z, 87, 45
51, 2020-010-01T14:00:00Z, 91, 48
```

## Get complex timeseries

method: POST  
path: /simulations/{simulationId}/timeseries

Allows the building of more complex timeseries that consist of data from different kinds of messages.

### Request parameters

- simulationId (string, path, required): Id of the simulation run messages are fetched from.

Request body

A JSON object with the following members:

- startEpoch (integer): Return timeserries on or after the given epoch. Not applicable if epoch, fromSimDate or toSimDate are used.
- endEpoch (integer): Return timeseries on or before the given epoch. Not applicable if the epoch, fromSimDate or toSimDate are used.
- epoch (integer): return  timeseries from the given epoch. Not applicable if fromSimDate, toSimDate, endEpoch or startEpoch are used.
- fromSimDate (ISO datetime): Return timeseries starting from the epoch that includes the given date. Not applicable if fromEpoch, epoch or toEpoch are used.
- toSimDate (ISO date): Return timeseries until the epoch that includes the given date. Not applicable if fromEpoch, epoch or toEpoch are used.
- format (string): Determines the response format. Possible values are csv and json. If this parameter is not used json is used as the default value.
- filters (filter[], required) List of filter objects used to filter messages from different topics, processes and attributes. At least one filter object is required.

filter object 

- process (string[]): Return timeseries about the given processes i.e. messages whose source is the given process. Value is list of process ids.
- topic (string): Return timeseries published to the given topic. Supports the same notation that is used when subscribing to the topics i.e. the same wildcard mechanism including the * and # characters.
- attrs (string[], required) List of names of message attributes whose values are assumed to be time series and which are then included to the timeseries response. It is possible to refer deeper into the message structure using the dot notation for example foo.bar.

### Usage example 1

Same kind of timeseries request as in usage example 1 of get simple timeseries.

#### Request

    POST /simulations/2020-06-10T10:00:00Z/timeseries

Request body

```
{
    "fromSimDate": "2020-01-01T12:00:00Z",
    "toSimDate": "2020-01-01T14:00:00Z",
    "filters": [
        {
            "process": [ "battery1", "battery2" ],
            "topic": "batteryState",
            "attrs": [ "chargePercentage" ]
        }
    ]
}
```

#### Response

Same as in usage example 1 of get simple timeseries.

### Usage example 2

Get the energy produced by all solar power plants and irradiance between 12:00 and 14:00 on 1st January 2020 for simulation run with id 2020-06-10T10:00:00Z in the csv format. Energy production is assumed to be published to topic production.solar in a message that has a energy attribute. Irradiance is assumed to be published to topic weather.current in message with attribute irradiance. There are two solar power plants in the simulation sol1 and sol2.

#### Request

    POST /simulations/2020-06-10T10:00:00Z/timeseries

Request body

```
{
    "fromSimDate": "2020-01-01T12:00:00Z",
    "toSimDate": "2020-01-01T14:00:00Z",
    "format": "csv",
    "filters": [
        {
            "topic": "production.solar",
            "attrs": [ "energy" ]
        },
        {
            "topic": "weather.current",
            "attrs": [ "irradiance" ]
        }
    ]
}
```

#### Response

Note: data values are just random numbers and do not mean anything sensible.

```
epoch, timestamp, weather.current:weatherDivinity.irradiance, production.solar:sol1.energy,  production.solar:sol2.energy
50, 2020-01-01T12:00:00, 100, 10, 8
50, 2020-01-01T12:30:00, 120, 11, 10
51, 2020-01-01T13:00:00, 115, 10, 9
51, 2020-01-01T13:30:00, 90, 7, 6
```

### Notes

These concern both of the timeseries end points. Generating the timeseries might take long if there is a lot of messages to be processed. This then may not be suitable for HTTP request and response since the wait time for the response may be long. Alternative solution is that these APIs just create a timeseries creation job. The response would then contain the id of the job. There would then be another API endpoint for querying by id the status of the job which can be in progress or finished. When the status is finished the actual timeseries response could then be fetched.

The simple and complex timeseries endpoints are kind of alternatives to each other. If the simple is all that is needed then the complex can be removed. If complex is required simple is not needed because complex can do both though simple can be kept just as a convenience. Idea in simple is that it would process just one type of message which can be published to multiple topics by multiple processes. Complex is then meant for processing and combining data from different kinds of messages.

## General notes

### Authentication and access control

The current plan seems to be to run this process on a web server accessible from the public internet or at least from TAU network. This requires then at least some kind of authentication and use of HTTPS to prevent outsider access. This could be HTTP basic authentication with user name and password or simple API access tokens in HTTP headers. It might also be required that not everybody with access to the service could access every simulation run's messages. In this case some kind of access control and permissions are required.

### Pagination

There probably can be a large number of messages and even after filtering the response could contain too many messages for one request. Same can be true even for simulation runs. Time based filtering could always be used to limit the number of returned items e.g. get messages for each day separately and not for the whole month at once. However a pagination feature could be also implemented. Requests would then have a limit parameter telling at most how many items can be returned, and offset telling from where to start. For example give me 100 messages starting from the 500th that the query would return.