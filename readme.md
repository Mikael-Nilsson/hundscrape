# Checking the return rate of dog shelters

"We" are looking into the possibility to adopt a dog from a dog shelter "around here", so I wanted to see how the turnover of available dogs was, how many are adopted and especially how often dogs get returned. So I wrote a small Python script.

20210322: The timer trigger is now working, so now the script runs once a week, checking the current dog state. It works!

20210311: I got the process to work with a REST request to the present shelters and also succeeded in deployment to Azure. So the next step should be to schedule the run. Very nice :).

20210309: It hit me that selenium is unnessecary in this case, all the data is reachable with a simple REST GET. At the same time I've decided on Azure functions for this project, so I'll be changing that too.

20210204: Just realised I can't reasonably run chromedriver in a lambda, so I'll have to postpone the deploying to AWS for the time being. It s'x, but I guess it's like they say: back to the drawing board. In the meantime I'll simply have to run it manually and locally from time to time.

20210119: Got support for storing images and csvs on Dropbox

20210110: Refactorized code and got support for multiple shelters. So now I can get info on Hundstallet too, yey!

20201229: Created feature that 
* get the dog and id, save in csv for date. This lends the possibility to easier see if a dog has been adopted and then returned to the shelter. Example:
```
20201207,20201214,20201221,20201228
Atilla_1021,Atilla_1021,Albert_321,Atilla_1021,
Albert_321,Albert_321,Zipp_34,Albert_321
Zipp_34,,Zipp_34
```


[Next Steps]
* Some kind of scheduling could be nice
* Deploying the code to some serverless platform would be nice. 
* * That would require saving the files in some file cloud.

To install layer libs:
````
pipenv install
pipenv run pip install -t layer/python/lib/python3.7/site-package -r ./requirements.txt
````

To run locally:
````
pipenv run python src/main.py
````

### AWS
To deploy to AWS:
````
sls deploy --aws-profile <profilename>
````

### Azure
To install libs:
````
pipenv install
pipenv run pip freeze > requirements.txt
pipenv run pip install -t .python_packages/lib/site-packages -r ./requirements.txt
````

Run locally:
````
func start
````

To deploy to Azure:
````
func azure functionapp publish Hundscrape
````

Creating a new Azure app:
````
func init Hundscrape --python
cd Hundscrape
func new --name Hundscrape --template "HTTP trigger" --authlevel "anonymous"
az login
az group create --name <RESOURCE_GROUP> --location northeurope
az storage account create --name <STORAGE_NAME> --location northeurope --resource-group <RESOURCE_GROUP> --sku Standard_LRS
az functionapp create --resource-group <RESOURCE_GROUP> --consumption-plan-location northeurope --runtime python --runtime-version 3.7 --functions-version 3 --name Hundscrape --storage-account <STORAGE_NAME> --os-type linux
func azure functionapp publish Hundscrape
````