"We" are looking into the possibility to adopt a dog from a dog shelter "around here", so I wanted to see how the turnover of available dogs was, how many are adopted and especially how often dogs get returned. So I wrote a small Python script.

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
pip install -t layer/python/lib/python3.8/site-package -r ./requirements.txt
````

To deploy to AWS:
````
sls deploy --aws-profile <profilename>
````