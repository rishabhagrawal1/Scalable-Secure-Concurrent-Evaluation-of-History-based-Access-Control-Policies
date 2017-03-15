
=======INSTRUCTIONS=======

Project requires the installation of the stable version of DistAlgo and Python3.5 or above.

We have used "DistAlgo-1.0.0b17" and Python3.5 for the same

1) Extract the zip folder to the directory of your choice.
2) Follow instruction for Distalgo installations in README.md file of Distalgo. It is important to install distalgo to run program from the     directory of your choice
3 Go to the directory where the project is extracted and run below command
	"python3.5 -m da -f main.da"
   If needed create a softlink to /usr/bin/python3.5 folder to python3.5 as used in above command
4) By default this will run the default test file we specified (conf/conf1.json)
   In order to run the different testcase please provide the file path as 1st argument in command line
   Other test documents are available in conf folder.
5) Similarly to change the policy file please provide sys arg(2nd argument) policy/policy1.xml, for database (3rd argument)use  data/data1.json. For each test case in conf, a corresponding policy.xml and data.json are provided with similar numberings
6) Upon running the program, it generates main.da.log, special mechanism of logging is used, where each line of log startstimestamp and then has its DA Module name. for e.g a log from application.da will be like below:

[2016-10-16 20:53:50,724]Application[('localhost', 34222)]:INFO: Application: Application fetches next policy evaluation request #: 1

7) Each Application will read its quanta of Test cases based on the load distribution provided in configuration. 
   After each Application finishes its evaluation it will print a completion message.
   After each application prints the message ,user can press "Ctrl-c" to terminate the program.

=======MAIN FILES=======

Location of main files 
async_system is the root directory. It will be present at the location where zip file is extracted. 
In async_system below files are present 

"da" modules:

	async_system/src/application.da
	async_system/src/coordinator.da
	async_system/src/database.da
	async_system/src/main.da
	async_system/src/Worker.da

"py" modules:
	async_system/src/message.py
	async_system/config/config.py
	
"log" file:
	async_system/src/main.da.log

"json" file:
	async_system/conf/conf1.json
	async_system/data/data1.json

"xml" file:
	async_system/policy/policy1.xml



Module description:

main.da: 
	This is the master process which starts other processes(namely co ordinators, database, and applications but not workers), it also 	   takes care of individual config file reads and provides the respective processes with their init files(data1.json to database, 		policy.xml to applications, conf1.json to applications).This process also creates a list of coordinator processes.

application.da: 
	These processes 
	reads individual policy evaluation requests from conf1.json, as per the load distribution
	creates a unique Message object for each request and populates this object
	identify the subject co ordinator and forwards the request message to it.
	awaits the response from subject coordinators and provides the response and present it to output.
	
Coordinator.da: 
	These processes acts as both subject and resource co ordinators. They:
	receive requests from application as subject co ordinators,
	establish proper msg object and updates it with tentative updates for subject piggybacked
	for this it maintains 2 data structures, a list of active messages along with their possible tentative subject atttibutes and 		dependent requests and another list of tentative updates for each subject 
	activate workers and setup each worker
	generate a request for resource coordinator including tentative resource attributes piggybacked with message and await reply from 	  workers for policy evaluation. This too mkaintains data structures similar to subject attribute to store tentative updates and 		dependent requests
	Handle conflict detection for subject attributes using the list of tetnative attributes(detect and restart)
	Query Resource co ordinator for conflicts
	in case of no conflict update the DB with new values for the attributes
	To simulate the  DB Max and Min Latency, we are using sleep to postpone the writing of updated attributes to database
	we decided to use the sleep in application instead of Databse process to minimize its impact on all other evaluations
	Provide the evaluation result to application processes.


Worker.da: 
	These are the workers specific to co ordinator processes. They:
	receive request from Resource co ordinators,
	Request for Attributes from Database.
	Merge tentative attributes received in request message and remaining attributes fetched from database to create attribute set.
	For policy evaluation, it first establishes which policy matches the request by parsing the policy and available information in request
	evaluates decision based on available attributes and policy rule , creates 2 sets , updated attributes adn read attributes.
	forwards its decision along with above 2 sets of information to the respective subject co ordinator.
	
database.da: 
	This is  the database emulator that reads an entire json file (preinit config) to create an in-memory hash map of subject and resources.
	It supports 2 types of requests: Query and update
	for each query it responds back with fetched attributes(if available, none otherwise) to the process that generates the querry
	for each update  request it updates both the subject and resource attributes received in the request message.
	It returns failure if  Initial Json file is not a valid Json. 

message.py: T
	his process has a message class and all the communication between each node takes place using objects of the same class.
	This class is super rich in class memebers and provides Full API support to update all the members.
	We use two types of message objefcts, History based(e.g document) and DRM Based(e.g movies).
	This class provides support for  movement of attributes and associated values among processes and has below 3 helper classes for the same
	FromDBAttributes
	TentativeAttributes
	FromWorkerAttributes
	each attribute update travels through above class objects to finally become tentative and read attributes.
	The message object also contains parameters to store the respective worker and application for each request.
	This class generates unique timestamp for the request and also provides API to generates a unique ID for each request by application
	Further below tags are used for interaction between different types of processes(RPC):
	req_db_read :  read an attribute set from database
	reply_db_read: Database replies to a read query 
	req_db_write: request to dtabase to write/update an attribute set
	req_app:  Application generates a new request and forwards to Subject co ordinator
	req_sub: subject co ordinator generates this request to send to resource co ordinator
	req_res: resource co ordinator send request to worker
	reply_work: worker evaluates and sends to subject co ordiantor
	result_sub: subjet co ordinator creates final packet with evaluation result to send to application

  
test/conf<n>.json: 
	These are the files with sets of testcases, each file presents mixture of testcases to help display different features of the 		program. We provide 5 JSON file with different testcases. Details of testcases are present in testing.txt

main.da.log: 
	This contains all the logs generated by the program run and is a cumulative file(feature of distalgo -f flag)

======= BUGS AND LIMITATIONS======

1) TO simulate the effect of DB Latency we are using python time.sleep function in the respective subject co ordinator to delay sending the update request to database process.

2) In using logical clock, clk = rclk, we were facing issues, for a workaround, we are simply passing each await, and calling respective functionality in receive function based on msg tag. A clearer understanding of await and logical clock can fix this and we hope to do so by next iteration.

=======CONTRIBUTIONS=======

CONTRIBUTORS:
	Rishabh Agarwal
	Umesh Jain

The strategy to implement was discussed extensively between both the contributors.
All the modules are collective effort of both the contributors, every file contains some code which was written by both.


