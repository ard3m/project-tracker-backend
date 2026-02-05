Test goal: Perform fast-paced simple test to Create Tasks and List tasks.

1. Performed POST project request.
	Outcome: 200 OK

2. Performed GET project request.
	Outcome: 200 OK

3. Performed POST task request,
	Outcome: 500 Internal Server Error

Below displays key points of the server actions/debug log:


--(viewed in terminal)--
INFO:     127.0.0.1:55947 - "POST /projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:55947 - "GET /projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:55587 - "POST /tasks HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application

	----[many lines of file issues with pointers]----
	----[scrolled down and identified the key clue]----

pydantic_core._pydantic_core.ValidationError: 3 validation errors for TaskOut
project_id
Field required [type=missing, input_value={'task_id': 1, 'name': 'b..., 5, 5, 17, 20, 347675)}, input_type=dict]
For further information visit https://errors.pydantic.dev/2.12/v/missing
title
Field required [type=missing, input_value={'task_id': 1, 'name': 'b..., 5, 5, 17, 20, 347675)}, input_type=dict]
For further information visit https://errors.pydantic.dev/2.12/v/missing
status
Field required [type=missing, input_value={'task_id': 1, 'name': 'b..., 5, 5, 17, 20, 347675)}, input_type=dict]
For further information visit https://errors.pydantic.dev/2.12/v/missing


*this showed exactly where the issue was with: 
	-  project_id
	-  title
	-  status


CONCLUSION:

*these are in the CreateTask schemas - however none of the data supplied references them - so the 'shape' is always 'wrong'.

Actions to fix: I deleted them in TaskOut and TaskCreate sections of the task.py schema file.

I performed the same test again and it worked as intended.

Result seen in log:
INFO:     127.0.0.1:54878 - "GET /projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:52204 - "POST /projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:64801 - "GET /projects HTTP/1.1" 200 OK
INFO:     127.0.0.1:62345 - "POST /tasks HTTP/1.1" 200 OK
INFO:     127.0.0.1:50748 - "GET /tasks HTTP/1.1" 200 OK












