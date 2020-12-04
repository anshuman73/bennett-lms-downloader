import requests
from bs4 import BeautifulSoup
import os
import urllib
from getpass import getpass
from tqdm import tqdm

import datetime

print('\n\nWe need to ask for you your LMS credentials to login into the LMS system as you so as to retrieve your courses:\n')
username = input('Enter your bennett username: ')
password = getpass('Enter your bennett password: ')

with open("logs.txt","a+") as file:
	datetime_object = datetime.datetime.now()
	file.write("\n\n"+str(datetime_object)+"\tBeginning run"+"\n")			


request_session = requests.Session()
login_request = request_session.post('https://lms.bennett.edu.in/login/index.php?authldap_skipntlmsso=1', data={'username': username, 'password': password, 'submit': ''}, verify=False)
login_history = login_request.history
login_history_length = len(login_history)

if login_history_length == 2:
	local_path = os.path.join(os.getcwd(), 'Bennett LMS Data')
	if not os.path.exists(local_path):
		os.makedirs(local_path)
	r = request_session.get('https://lms.bennett.edu.in/my/')

	soup = BeautifulSoup(r.content, 'html.parser')

	raw_courses = soup.find_all("div", class_="course-info-container")
	courses = {}

	for course in raw_courses:
		course_meta_data = course.find_all('h4', class_='media-heading')[0]
		courses[course_meta_data.find('a').text.strip()] = courses.get(course_meta_data.find('a').text.strip(), course_meta_data.find('a')['href'].strip())

	for course_name, course_link in courses.items():
		print(f'\n\n\nProcessing the course "{course_name}":\n\n')
		course_path = os.path.join(local_path, course_name.replace(':', ''))
		if not os.path.exists(course_path):
			os.makedirs(course_path)

		course_data = request_session.get(course_link, verify=False).content
		course_soup = BeautifulSoup(course_data, 'html.parser')
		resources = course_soup.find_all('li', class_='activity resource modtype_resource')
		count = 0
		for resource in tqdm(resources[::-1]):
			try:
				file_url = resource.find('div', class_='activityinstance').find('a')['href']
				file_req = request_session.get(file_url, stream=True, verify=False)
				file_name = urllib.parse.unquote(file_req.url.split('/')[-1])
				if(file_name.find('forcedownload')!=-1):
					file_name = file_name.strip("forcedownload=1")[:-1]
				try:
					online_size = int(file_req.headers['Content-Length'])
				except:
					count += 1
					continue
				file_path = os.path.join(course_path, file_name)
				if os.path.exists(file_path):
					local_size = os.path.getsize(file_path)
					if online_size == local_size:
						count += 1
						continue

				local_file = open(file_path, 'wb')
				for block in file_req.iter_content(512):
					if not block:
						break
					local_file.write(block)

				count += 1
			except Exception as e:
				datetime_object = datetime.datetime.now()
				print(datetime_object)
				print(str(e))
				with open("logs.txt","a+") as file:
					file.write(str(datetime_object)+"\n"+str(e)+"\n")			

	print('\n\n\nAll Done\n\nKeep studying !')

else:
	print('Invalild Login details ! Please close the window and re-run the program !')

input('Press Enter to exit')
