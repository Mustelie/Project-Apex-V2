# Project-Apex-Vasquez
**Instructions to Run Code:**

Press the 'run' button and watch the magic happen.

**Resource Documentation:**

The News API was used to pull data on Mueller articles: https://newsapi.org/docs/endpoints/everything

NYT API was used to pull data on articles on Netanyahu: https://developer.nytimes.com/

Matplotlib was used to make the graphs: https://matplotlib.org/contents.html

**Code Documentation:**

1-7: Importing Libraries

8-14: Setting up the fixin's for some links.

16-25: Prepares a dictionary to search the News API for mentions of Mueller.

28-36: Retrieving and preparing data from the News API Mueller search.

38-48: Putting Mueller data into an SQL file.

54-73: Pulling Mueller data from database and counting how many news stories are from which sources, then writing this into a dictionary.

76-85: Using Mueller data to make a piechart of the top ten news stories.

88-103: Searches through 10 pages of a search of Netanyahu in the NYT API, adding data from each page into a SQL database.

105-125: Searches the News API for Netanyanu and adds this data into another database.

127-147: Calculates the number of Netanyahu stories in the News API results match stories from the NYT Netanyahu results.

149-155: Creates a pie chart of what percentage of the News API Netanyahu results were also in the NYT results.