
# Hand Dashboard ReadMe

##Goal:

1. Collect all the data from services I use regularly. 
2. Visualize & Analyze to find meaningful & actionable information to make life better
3. Have compelling *story* to show others about myself


# RoadMap
 
## Milestone 1.0

Have a functioning site that connects to a few APIs, store & visualize that information. 

### Major Features:

* Create new user & basic account management
* Ability to connect to APIs (Fitbit, 4sq, GitHub, Readmill, Twitter)
* API for getting data to JS SDK (? - do I need this, I think I do, otherwise it wouldn't be 'sdk')
* Basic dashboard that uses a javascript SDK for visualziations
* 3 basic visualizations
* 1 basic 'analysis'

### Doesn't have

* Automatic API data grabs
* public dashboards (can only view own stuff)
* only get main data from APIs (e.g. tweets for twitter, not followers etc)

### Steps

1. Create a general User blueprint & model (done)
2. Create a general frontend blueprint (done)
3. (Python) Connect to a few APIs in manner that will be easy to expand/replicate (almost done, need to see if I can DRY better)
4. (Python) Sketch out ideas for user/api models and structure of those
5. (Python) Get basic user profile information from all APIs
6. (Python) Create initial prototype for 1 API (fitbit) for how to grab, process, and store data (manually)
7. (Python) Build internal API for the first set of data
8. (JS) Sketch out ideas for how SDK will interact with data, containter, etc
9. (JS) Build structure of JS interface (probably backbone, require, etc)
10. (JS) Create template for SDK (WTF does this mean?) 
11. (JS) Get first (very basic) visualization built
12. (??) Finish any loose ends with first prototype API stuff
13. (Python) Build grabber, processors, and stores for other APIs
14. (Python) Build internal APIs for rest of APIs
15. (JS) Flesh out SDK stuff based on other APIs
16. (JS) Build the 3 basic visualizations
17. (Python/JS) Figure out interesting analysis that could be done & best method for doing "analysis" - e.g. will this be available to the SDK (I guess they could do whatever they want with the right data).
18. (Python/JS) Do the analysis
19. (JS) Viz the analysis, if necessary
20. 20 seems like a good number to stop at. Touch up stuff?

### Questions/Issues

* Should I create API specific models or generic model (i.e. for weight, do I want to store it in a FitBit associated model or create a weight model that can get info from fitbit or others)?
    * The generic seems like it would be better for most things, if possible. But for something like twitter that seems silly. So maybe its case by case? But how do I translate from the API's to the generic models. And where do those models go? Under the user I guess... Ya that would make sense.
* Manual updating or automatic for this milestone? When I tried to figure out celery before it was a complete roadblock.
* Need to do research a bit on javascript SDKs and what exactly those are supposed to look like. And how to build one exactly. I can look at DECK, kind of. And maybe Ona has something up. Otherwise, I am sure there are examples somewhere. 
    * Basic idea of SDK: Module can access data via API, give easy way of doing that. Then just some information on size and layout so we can make things fluid. Does it need anything else? Way to auto update data? No idea what else...
* ???

## References/Motivations

http://blog.kirigin.com/personal-analytics
http://blog.chocol.it/2013/06/08/personal-api/
http://x.naveen.com/post/51808692792/a-personal-api
http://api.fxcardi.com/ and http://fxcardi.com/
http://www.erikbernacchi.com/
http://busterbenson.com/