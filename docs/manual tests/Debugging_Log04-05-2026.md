Issue: the app gives an error when initiated via: uvicorn main:app --reload

===============

**Debugging log:**

===============

\----------

02/05/26

1\. Test the app: in windows terminal from the same folder main.py is located: python -c "import main"

&#x09;	Result:  ModuleNotFoundError: No module named 'exceptions'

Addressing the issue: 

&#x09;- There is no 'exceptions' file located in the /app folder where main.py lives. The file must be created/inserted there.

&#x09;- Also the import in main.py is: from exceptions import ErrorResponse

&#x09;I think it should be: from app.exceptions import ErrorResponse

&#x09;- There is a exceptions\_schema.py file inside the schemas folder. I think this is the file. I'll rename it 'exceptions.py' and move it to the /app folder.



\----------

2\. Test the app: in windows terminal from the same folder main.py is located: python -c "import main"

&#x09;	Result: 

&#x09;		  File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\routers\\account\_router.py", line 5, in <module>

&#x09;		    from app.database import get\_db

&#x09;		ModuleNotFoundError: No module named 'app'

Addressing the issue:

&#x09;- The command I was using: python -c "import main"

&#x09;	Is incorrect. It must instead be: python -c "import app.main"



\----------

3\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;	Result: 

&#x09;		 File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\main.py", line 11, in <module>

&#x09;		    from routers.account\_router import router as account\_router

&#x09;		ModuleNotFoundError: No module named 'routers'

Addressing the issue: 

&#x09;- The router import line: 

&#x09;from routers.account\_router import router as account\_router

&#x09;Should instead be:

&#x09;from app.routers.account\_router import router as account\_router

&#x09;- I will also correct the import paths for all routers and services to match this.



\----------

4\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;	Result:

&#x09;		File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\routers\\account\_router.py", line 5, in <module>

&#x09;		    from app.database import get\_db

&#x09;		ModuleNotFoundError: No module named 'app.database'

Addressing the issue:

&#x09;- The import found in account\_router.py is: 

&#x09;from app.database import get\_db

&#x09;Should instead be:

&#x09;from app.db.database import get\_db

&#x09;- I will change similar imports in all other router files to match this.

&#x09;- Also, looking into the app/db/database.py code

&#x09;	○  there is no 'get\_db' function or export. This is required.

&#x09;	○  database.py does not feature async functionality/structure like the rest of the system has been made.



\----------

03/05/26

5\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;	Result: 

&#x09;		File "C:\\Users\\laros\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sqlalchemy\\dialects\\postgresql\\asyncpg.py", line 1094, in import\_dbapi

&#x09;		    return AsyncAdapt\_asyncpg\_dbapi(\_\_import\_\_("asyncpg"))

&#x09;		                                    ^^^^^^^^^^^^^^^^^^^^^

&#x09;		ModuleNotFoundError: No module named 'asyncpg'

Addressing the issue:

&#x09;- asyncpg package has not been installed into the environment.

&#x09;- Installed it via terminal: pip install asyncpg



\----------

6\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;	Result: 

&#x09;		 File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\routers\\account\_router.py", line 6, in <module>

&#x09;		    from app.schemas.account import (

&#x09;		ModuleNotFoundError: No module named 'app.schemas.account'

Addressing the issue:

&#x09;- 'app.schemas.account' is not the correct path the router files require. It should be 'app.schemas.account\_schema'

&#x09;- I will refactor tall the service files to fix this same issue.



\----------	

7\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;	Result: 

&#x09;		File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\services\\account\_service.py", line 9

&#x09;		    async def create\_account(

&#x09;		IndentationError: unexpected indent

Addressing the issue:

&#x09;- Check over files for inappropriate indents and rectify.



\----------

8\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;Result: 

&#x09;	File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\services\\account\_service.py", line 42

&#x09;	    return row

&#x09;	    ^^^^^^^^^^

&#x09;	SyntaxError: 'return' outside function

Addressing the issue:

&#x09;- Move the 'return row' line to be inside the function. Check over other service files for similar issue.



\----------

04/05/26

9\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;Result:

&#x09;	File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\services\\account\_service.py", line 42

&#x09;	    return row

&#x09;	    ^^^^^^^^^^

&#x09;	SyntaxError: 'return' outside function

Addressing the issue:

&#x09;- Apparently this will happen if the indents in the function are not exactly the same. They may appear the same however 4 spaces =! 1 tab. I will replace each indentation in the function with exactly '1 tab' indentation.



\----------

10\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;Result:

&#x09;	File "C:\\Users\\laros\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sqlalchemy\\sql\\naming.py", line 127, in \_\_getitem\_\_

&#x09;	    raise KeyError(key)

&#x09;	KeyError: 'all\_column\_names'

Addressing the issue:

&#x09;- This seems to be an error with 'naming conventions' found in the app\\db\\database.py file

&#x09;- 'all\_column\_names' is not compatible with check constraints, some foreign keys/indexes/ect.

&#x09;- SQLAlchemy’s docs recommend using 'column\_0\_name' instead of 'all\_column\_names'.

&#x09;- I will replace this code: 

&#x09;	naming\_convention = {

&#x09;	    "ix": "ix\_\_%(table\_name)s\_\_%(all\_column\_names)s",

&#x09;	    "uq": "uq\_\_%(table\_name)s\_\_%(all\_column\_names)s",

&#x09;	    "ck": "ck\_\_%(table\_name)s\_\_%(constraint\_name)s",

&#x09;	    "fk": "fk\_\_%(table\_name)s\_\_%(all\_column\_names)s\_\_%(referred\_table\_name)s",

&#x09;	    "pk": "pk\_\_%(table\_name)s",

&#x09;	}

&#x09;	

&#x09;With this code:

&#x09;	naming\_convention = {

&#x09;	    "ix": "ix\_\_%(table\_name)s\_\_%(column\_0\_name)s",

&#x09;	    "uq": "uq\_\_%(table\_name)s\_\_%(column\_0\_name)s",

&#x09;	    "ck": "ck\_\_%(table\_name)s\_\_%(constraint\_name)s",

&#x09;	    "fk": "fk\_\_%(table\_name)s\_\_%(column\_0\_name)s\_\_%(referred\_table\_name)s",

&#x09;	    "pk": "pk\_\_%(table\_name)s",

&#x09;	}



\----------	

11\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;Result:

&#x09;	File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\models\\audit\_log.py", line 3

&#x09;	    from sqlalchemy import String, DateTime, ForeignKey, Integer, JSON,

&#x09;	                                                                        ^

&#x09;	SyntaxError: trailing comma not allowed without surrounding parentheses

Addressing the issue:

&#x09;- Delete comma at end of line 3 in \\app\\models\\audit\_log.py



\----------

12\. Test the app: in windows terminal from the same folder main.py is located: python -c "import app.main"

&#x09;Result:

&#x09;	File "C:\\Users\\laros\\Project-Tracker-Backend\\app\\routers\\account\_router.py", line 16, in <module>

&#x09;	    from app.dependencies.auth import get\_current\_user, get\_current\_account

&#x09;	ModuleNotFoundError: No module named 'app.dependencies'

Addressing the issue:

There is no such auth.py file. I must create it. Along with an '\_\_init\_\_' file, and put them both inside a folder labeled 'dependencies'.







