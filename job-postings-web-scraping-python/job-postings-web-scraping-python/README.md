# Job Postings Web Scraping with Python & BeautifulSoup

## Summary

This Python script scrapes job postings from finn.no based on the specified job position. It provides an easy way to gather job listings matching specific criteria without the need for manual searching.

## Solution

The solution utilizes web scraping techniques with the BeautifulSoup library to extract job postings from the finn.no website. It allows users to input their desired job position and location, then retrieves relevant job listings from the website's search results page. The extracted data is saved to a CSV file for further analysis or reference.

## Approach

1. **Input Handling**: Prompt the user to input the desired job position.

2. **URL Generation**: Generate the search URL for finn.no based on the user input. The URL includes parameters for the job position.

3. **Web Scraping**: Use requests to fetch the HTML content of the search results page. Then, use BeautifulSoup to parse the HTML and extract relevant job posting information such as job_title, company, location, description, job_date, is_deadline, job_type, link.

4. **Data Processing**: Process the extracted job data and store it in a list or data structure.

5. **CSV Export**: Write the processed job data to a CSV file named job_postings.csv. Each row in the CSV file represents a single job posting, with columns for job_title, company, location, description, job_date, is_deadline, job_type, link.

## Dependencies

- requests
- BeautifulSoup
- csv
- datetime
- dateparser


