# Google News By SerpApi
This script utilizes the SerpApi library to perform a Google search and retrieve news articles related to a specific keyword within a specified date range. The script fetches news results using the SerpApi service and filters the results based on the provided date range. The filtered articles are then sorted based on their posted date.

### API Key
To use the script, you need an API key from SerpApi. The API key is assigned to the SERP_API_KEY variable at the beginning of the script. Replace "xxxxx" with your actual API key.

### Usage
The script provides a main function that can be called with the following parameters:

- keyword: The keyword to search for news articles. The default value is "DataForSEO".
- from_date: The start date of the date range in the format "YYYY-MM-DD".
- to_date: The end date of the date range in the format "YYYY-MM-DD".

To run the script, execute the following command:
```bash
python scrap_search_google_serpapi.py
```

The script will perform the Google search, retrieve the news articles, filter and sort them based on the date, and display the results. If there are any articles found, they will be saved in a CSV file named "google_search_results.csv" in the current directory.

