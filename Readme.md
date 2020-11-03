# Qomma first implementation
## How to run
Project can be init by the command in command line:  
```
python qomma/main.py {path_to_folder_with_csv_files}
```
or 
```
python3 qomma/main.py {path_to_folder_with_csv_files}
```
in some cases.
Test drivers.csv file placed in csv folder, so you can simply run:
```
python3 qomma/main.py ../csvs/
```
For now, it supports only CSV files.
  
To run tests:
```
python -m unittest discover tests
```
or
```
python3 -m unittest discover tests
```
  
## Description
**You can find more description for each method and class in specific files. There, I will describe only general 
approach of this app.**  
  
As you know from **How to run** section, to run this project, you need to use main.py. It's an entry point to the app.  
Main.py has function `qomma.main()`, and initiation for it at the end of the file. Actually, `qomma.main()` function 
implements Dependency Injection pattern, and allows us to manipulate with dependencies in future - create interfaces, 
change implementation by changing the specific class, etc. Although, it gives us an ability to test separate 
classes without the necessity to implement all relations.  
Although, `qomma.main.py` implements argparse - native Python package to work with command line.  
As was mentioned in the task, there are plans to support other file formats, so I implemented 
`qomma.Readers.ReaderFactory` class, which is responsible for finding a right Reader for each file.  
I implemented only `qomma.Readers.CSVReader` class (acts as a Repository pattern) and decided to not go with creation of 
`ReaderInterface`. It can be easy implemented in the future, on next steps of the project. It will be more clear, which 
file types are we going to support. Of course, tests will be less complicated as well.  
In `qomma.Handlers.PathHandler` class, I used `try/except` construction, which is supposed to handle exception, produced 
by `qomma.ReaderFactory` class. As there might be some other files in the folder, I chose to simpy pass them and do not 
rise any error.  
`qomma.Domain` package contains all business logic, that we are going to have. Is supposed to be changed in the future, 
while new features are going to be implemented. It is separated from Infrastructure layer, and does not depend on 
changes there. So, it will work with other types of files in the future.
`qomma.Domain.Database` is an Aggregate Entity of this domain. It has relations with `qomma.Database.Query`, as a 
container for query attributes, and Table (list of Tables). Each table itself represents each CSV file, that was found 
on the stage of app initiation.  
I decided to go with regular expression to parse query string. I found this approach more flexible for future changes.  
Domain model might and should be extended. I have just used a simplified version, with plans to extend it later. So that
some methods of `Database` entity may migrate to specific entities, and code structure may become simplified a bit then.  
I tried to cover code with tests as much as I could.  
`qomma.Domain.Database` is highly bounded with `Query` and `Table` entities, so that I decided to not go with mocking 
all methods in `Query` and `Table` while testing `qomma.Domain.Database`. I used mock from case to case in this 
particular case. It allowed to simplify tests for `qomma.Domain.Database` a bit and save time for this test challenge.   
I stuck with extending test cases for `qomma.Controllers.Controller`, especially with multiple user inputs. 
Unfortunately, I did not found a suitable solution for this case.