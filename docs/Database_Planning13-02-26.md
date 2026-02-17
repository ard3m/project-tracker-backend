Project Tracker - Database Planning



This document contains notes on the planning of the app features and early drafts of the database tables.

------------------------------------



What does the app do in its 'final form'?

&nbsp;	

The app lets users:

&nbsp;		- Create a number of different 'jobs/projects' (date created, created by, status, completed/closed/cancelled by)

&nbsp;		- Add 'tasks' for each task (date created, created by, status, completed/closed/cancelled by)

&nbsp;			○ Tasks can be expanded to display more context and larger photos for selection. (tempted to make it look like OneNote here though that would be difficult, most likely it will be more dot points with photos.)

&nbsp;			

&nbsp;		- Add images to be stored in 'Job' and/or 'tasks' (upload date, uploaded by, archive status?

&nbsp;		- Each job has a: 

&nbsp;			○ 'access and egress' section where notes can be added, such as: "back entry is for vehicle loading only, no pedestrian access". (date edited, edited by) \[include images?]

&nbsp;			○ 'VIP names and contacts' section, such as: forklift driver=Robert 0478 927 123, Plumber contact=David 0421 385 476 (upload date, uploaded by, date edited, edited by) \[we don’t want people to be afraid of uploading for fear of exposing themselves - ensure that things can be deleted with only ADMIN access to app history).

&nbsp;			○ 'Materials and Equipment' section. Containing headings with subheadings such as: Waterproofing ; Silicone sausages ; location: inside toolbox on level 3, quantity/amount: approx 25 tubes.

&nbsp;			○ 'documentation' containing site plans, safety data sheets, technical data sheets, helpful emails?, other.

&nbsp;	

&nbsp;	



This is a first draft on the SCHEMAs for the individual tables:



&nbsp;	1. Project

&nbsp;		- \*Project\_id INT \[primary key]

&nbsp;		- Project\_name VARCHAR(30)

&nbsp;		- is\_active BOOLEAN

&nbsp;		- Address VARCHAR(320)

&nbsp;		- Updated\_at TIMESTAMP

&nbsp;		- Updated\_by VARCHAR(320)

&nbsp;	2. Task

&nbsp;		- \*Task\_id INT

&nbsp;		- ^Project\_id \[foreign key]

&nbsp;		- Task\_name VARCHAR(30)

&nbsp;		- Task\_description TEXT

&nbsp;		- is\_active BOOLEAN

&nbsp;		- Updated\_at TIMESTAMP

&nbsp;		- Updated\_by VARCHAR(320)

&nbsp;	3. Image

&nbsp;		- \*Image\_id INT

&nbsp;		- ^Project\_id \[foreign key] <----is this needed? For simplicity, probably yes.

&nbsp;		- Upload\_date TIMESTAMP

&nbsp;		- Uploaded\_by VARCHAR(320)

&nbsp;		- Archived\_by VARCHAR(320)

&nbsp;	4. Access\_Egress

&nbsp;		- \*^Project\_id INT \[foreign key as primary key] <-----beccause there is only 1 instance of 			access\_egress - its not like a 'task' where there are multiple.

&nbsp;		- Access\_Details TEXT

&nbsp;		- Updated\_at TIMESTAMP

&nbsp;		- Updated\_by VARCHAR(320)

&nbsp;	5. VIP\_contact

&nbsp;		- \*contact\_number INT(10)

&nbsp;		- ^Project\_id INT

&nbsp;		- Contact\_First\_name VARCHAR(50)

&nbsp;		- Contact\_Last\_name VARCHAR(50)

&nbsp;		- Updated\_at TIMESTAMP

&nbsp;		- Updated\_by VARCHAR(320)

&nbsp;	6. Materials

&nbsp;		- Material\_name

&nbsp;		- ^Project\_id INT

&nbsp;		- Material\_name VARCHAR(30)

&nbsp;		- Material\_description

&nbsp;		- Updated\_at TIMESTAMP

&nbsp;		- Updated\_by VARCHAR(320)

&nbsp;	7. Jobsite documentation

&nbsp;		- \*File\_name VARCHAR(30)

&nbsp;		- ^Project\_id INT

&nbsp;		- File\_type VARCHAR(10)

&nbsp;		- Updated\_at TIMESTAMP

&nbsp;		- Updated\_by VARCHAR(320)

&nbsp;	8. User

&nbsp;		- \*email VARCHAR(320)

&nbsp;		- Username VARCHAR(30)

&nbsp;		- Password CHAR(60)

&nbsp;		- First\_name VARCHAR(50)

&nbsp;		- Last\_name VARCHAR(50)

&nbsp;		- Last\_login\_time TIMESTAMP

&nbsp;	9. Account

&nbsp;		- \*Account\_id INT

&nbsp;		- User\_email VARCHAR(320)

&nbsp;		- Account\_name VARCHAR(30)

&nbsp;		- Account\_email VARCHAR(320)

&nbsp;		

&nbsp;	10. History\_Event (this will be added much later - not now, too much bloat.)

&nbsp;		- \*email VARCHAR(320)

&nbsp;		- Edited\_date TIMESTAMP

&nbsp;		

&nbsp;		\*\*Consider removing the date features. Overly complex and I cant quite figure it out right now.

&nbsp;		\*\*\*Simplified them instead so can be emboldened later.



These features can be added in their basic forms and expanded on later if need be, such as a 'due by' date for tasks to be a tracked data-point, which it currently is not and should not be present in the completed MVP/version 1

