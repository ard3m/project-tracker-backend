Test goal: Create Projects and tasks, and get them displayed in GET request.









1\. Open POST /projects 'Create Project'



&nbsp;	{

&nbsp;	  "name": "Commercial Rd"

&nbsp;	}

I hit execute.

&nbsp;	{

&nbsp;	  "name": "Albert St"

&nbsp;	}

I hit execute. A few times…



----



2\. Open /projects 'List Projects'



I hit execute.

Scrolled down to the response body:

&nbsp;	\[

&nbsp;	  {

&nbsp;	    "project\_id": 1,

&nbsp;	    "name": "Commercial Rd",

&nbsp;	    "created\_at": "2026-02-03T00:56:11.441867"

&nbsp;	  },

&nbsp;	  {

&nbsp;	    "project\_id": 2,

&nbsp;	    "name": "Albert St",

&nbsp;	    "created\_at": "2026-02-03T00:57:12.545133"

&nbsp;	  },

&nbsp;	  {

&nbsp;	    "project\_id": 3,

&nbsp;	    "name": "Albert St",

&nbsp;	    "created\_at": "2026-02-03T00:57:28.666362"

&nbsp;	  },

&nbsp;	  {

&nbsp;	    "project\_id": 4,

&nbsp;	    "name": "Albert St",

&nbsp;	    "created\_at": "2026-02-03T00:57:30.140525"

&nbsp;	  }

&nbsp;	]



So each time I hit execute, it created a new project.



----



3\. Open POST /tasks 'Create Task'

Here is the base 'try it' value:

&nbsp;	{

&nbsp;	  "project\_id": 0,

&nbsp;	  "title": "string",

&nbsp;	  "status": "Pending"

&nbsp;	}



Attempt to create multiple like this:

&nbsp;	{

&nbsp;	  "project\_id": 1,

&nbsp;	  "title": "Replace cracked tile in ensuite.",

&nbsp;	  "status": "Pending"

&nbsp;	}

&nbsp;	{

&nbsp;	  "project\_id": 1,

&nbsp;	  "title": "Grout laundry floor tiles.",

&nbsp;	  "status": "Complete"

&nbsp;	}

&nbsp;	{

&nbsp;	  "project\_id": 1,

&nbsp;	  "title": "Tile pantry splashback",

&nbsp;	  "status": "Canceled"

&nbsp;	}

&nbsp;	{

&nbsp;	  "project\_id": 2,

&nbsp;	  "title": "screed bathroom and ensuite shower bases",

&nbsp;	  "status": "Pending"

&nbsp;	}

&nbsp;	{

&nbsp;	  "project\_id": 4,

&nbsp;	  "title": "meet with Moira (owner) for onsite measure and quote",

&nbsp;	  "status": "Pending"

&nbsp;	}

I hit execute (once..)

Nex we'll try to list the tasks.



----



**4.** Open GET /tasks List Tasks

&nbsp;	Hit 'Execute'

Response is empty.

&nbsp;	\*so either the 'create tasks' is broken, or the 'list tasks' is broken.

&nbsp;		\*\*given that there are no parameters which must be entered for the 'list tasks' and its just an execute button, this tells me  the issue is probably in there.

&nbsp;		

(Before attempting to fix, I'll try out the other POST / 'create task' which uses the older code.)



----

&nbsp;		

5\. Open POST / Create Task

Submitted this:

&nbsp;	{

&nbsp;	  "project\_id": 1,

&nbsp;	  "title": "TEST TEST title",

&nbsp;	  "status": "TEST status TEST TEST TEST"

&nbsp;	}

&nbsp;	

----



6\. Open GET 'tasks List Tasks

&nbsp;	Hit Execute button.

&nbsp;		No result.



----



CONCLUSION:

'tasks' are not being stored in memory OR not being accessed from the GET request. Details above.'













