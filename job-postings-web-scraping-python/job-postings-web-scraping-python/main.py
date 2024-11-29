# Step 1: Import required libraries
from bs4 import BeautifulSoup
import csv
import dateparser
from datetime import date, timedelta
import requests

# Step 2: Generating a URL with a function
# You need to define a function that takes in one parameter: position
def generate_job_search_url(position):
	r"""
	Returns Finn.no url for the position
	"""
	base_url = "https://www.finn.no/job/fulltime/search.html?q={}"
	formatted_position = position.replace(' ', '+')
	url = base_url.format(formatted_position)
	return url

# Step 3: Extract the Job Data from a single job posting card
''' 
The function you define here will be responsible for extracting relevant information from each individual job posting card. 
For example, on Finn's job search results page, each job posting is typically displayed as a card containing information 
such as job title, company name, location, and a brief description. 
Your extract_job_data function will be designed to parse these cards and extract the desired information from them. 
You'll use BeautifulSoup to navigate the HTML structure of each job posting card and extract the relevant data. 
This function will then be called within the main function to process each job posting retrieved from the search results page.

Extract the desired data using a series of try/except blocks to protect the program and the provide the data with
known values in case some data is missing from the posting.
AttributeError clause handles situations where attributes or methods may not be available or accessible.
'''
def extract_job_data(posting):
	r"""
	Extracts job posting information as [job_title, company, location, description, job_date, is_deadline, job_type, link]
	"""
	try:
		job_title = posting.find("a", class_="sf-search-ad-link link link--dark hover:no-underline").text.strip()
	except AttributeError:
		job_title = "-Not found-"
	
	try:
		company = posting.find("div", class_="flex flex-col text-12").span.text.strip()
	except AttributeError:
		company = "-Not found-"
	
	try:
		location_and_date = posting.find("div", class_="pr-44 order-first space-x-16 text-12 text-gray-500").text.strip()
		info = location_and_date.split('|')
		if len(info) == 1:
			location = info[0]
			job_date = "-Not found-"
		elif len(info) == 2:
			job_date = info[0]
			if job_date.find("Ny i dag") >= 0:
				job_date = date.today()
			elif job_date.find("en dag siden") >= 0:
				job_date = date.today() - timedelta(days=1)
			elif job_date.find("2 dager siden") >= 0:
				job_date = date.today() - timedelta(days=2)
			else:
				job_date = dateparser.parse(job_date).strftime("%Y-%m-%d")
			
			# print(f"info[0] -> job_date: {info[0]} -> {job_date}")
			location = info[1]
		else:
			location = "-Not implemented-"
			job_date = "-Not implemented-"
	except AttributeError:
		location = "-Not found-"
		job_date = "-Not found-"

	try:
		deadline = posting.find("span", class_="text-red-600").text.strip()
		job_date = date.today()
		is_deadline = True
	except AttributeError:
		deadline = ""
		is_deadline = False
	
	try:
		description = posting.find("a", class_="sf-search-ad-link link link--dark hover:no-underline").text.strip()
	except AttributeError:
		description = "-Not found-"

	try:
		link = posting.find("a", class_="sf-search-ad-link link link--dark hover:no-underline")['href']
		if link.find("parttime") >= 0:
			job_type = "parttime"
		elif link.find("fulltime") >= 0:
			job_type = "fulltime"
		elif link.find("management") >= 0:
			job_type = "management"
	except AttributeError:
		link = "-Not found-"
		job_type = "-Not found-"

	try:
		position_count_div = posting.find("div", class_="flex flex-col text-12")
		position_count_spans = position_count_div.find_all("span")
		if len(position_count_spans) >= 2:
			position_count_text = position_count_spans[1].text.strip()
			position_count_array = position_count_text.split(' ')
			if len(position_count_array) >= 1:
				position_count = int(position_count_array[0])
			else:
				position_count = -1
		else:
			position_count = -2
	except AttributeError:
		position_count = -3
	
	return job_title, position_count, company, location, description, job_date, is_deadline, job_type, link

# Step 4: Define the main function
def main(position):
	# Set the headers for the HTTP request. A website may block requests from bots, so it's a good idea to set a user agent string.
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}

	# Construct the URL for the job search based on the job position and location using the function you created earlier.
	url = generate_job_search_url(position)
	print(url)

	# Send an HTTP request to the URL and retrieve the HTML code of the search results page.
	response = requests.get(url, headers=headers)
	
	if response.status_code == 200:
		# Parse the HTML code using BeautifulSoup and select the HTML elements that contain the job postings (hint: use the Beautiful Soup’s findall method).
		soup = BeautifulSoup(response.content, 'html.parser')
		job_postings = soup.find_all('div', class_='flex flex-col')

		# # Extract location's special url
		# location_value = ""
		# locations = soup.find("ul", class_="list u-ml16")
		# for li in locations.find_all("li"):
		# 	location_name = li.div.label.text.strip()
		# 	if location.lower() in location_name.lower():
		# 		location_value = li.div.label['for']
		# 		location_value = location_value.replace("location-", "")

		# Process each job postings to extract the relevant data
		job_data = []
		for posting in job_postings:
			data = extract_job_data(posting)
			job_data.append(data)
		
		# Save the data as a csv file
		with open('job_postings.csv', 'w', newline='', encoding='utf-8') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['Job Title', 'Position Count', 'Company', 'Location', 'Description', 'Date', 'Deadline', 'Job Type', 'Link'])
			writer.writerows(job_data)
		
		print("Job postings scraped successfully.")
	else:
		print("Failed to retrieve the webpage.")

# Call the main function with position parameter
main('data analyst')