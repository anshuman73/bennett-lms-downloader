import requests
from bs4 import BeautifulSoup
import os
import urllib
from selenium.webdriver import Chrome
from getpass import getpass
from time import sleep

print('\n\nAfter asking for your credentials, the software will run an automated chrome window to login into the LMS system as you, please do not close it !\n')
sleep(3)
username = input('Enter your bennett username: ')
password = getpass('Enter your bennett password: ')

driver = Chrome(os.getcwd() + '/' + 'chromedriver')
driver.get('http://lms.bennett.edu.in')
username_elem = driver.find_element_by_id('inputName')
username_elem.clear()
username_elem.send_keys(username)
password_elem = driver.find_element_by_id('inputPassword')
password_elem.clear()
password_elem.send_keys(password)
submit_button = driver.find_element_by_id('submit')
submit_button.click()

try:
	assert driver.current_url == 'http://lms.bennett.edu.in/my/'
	cookies = driver.get_cookies()
	cookie = cookies[0]['value']
	driver.close()
	local_path = os.getcwd() + '/' + 'Bennett LMS Data' + '/'
	if not os.path.exists(local_path):
		os.makedirs(local_path)

	request_session = requests.Session()

	request_session.cookies.set('MoodleSession', cookie)


	r = request_session.get('http://lms.bennett.edu.in/my/')

	soup = BeautifulSoup(r.content, 'html.parser')

	raw_courses = soup.find_all("div", class_="course-info-container")
	courses = {}

	for course in raw_courses:
		course_meta_data = course.find_all('h4', class_='media-heading')[0]
		courses[course_meta_data.find('a').text.strip()] = courses.get(course_meta_data.find('a').text.strip(), course_meta_data.find('a')['href'].strip())

	for course_name, course_link in courses.items():
		print(f'\n\n\nProcessing the course "{course_name}":\n\n')
		course_path = local_path + course_name + '/'
		if not os.path.exists(course_path):
			os.makedirs(course_path)

		course_data = request_session.get(course_link).content
		course_soup = BeautifulSoup(course_data, 'html.parser')
		resources = course_soup.find_all('li', class_='activity resource modtype_resource ')
		count = 0
		for resource in resources:
			file_url = resource.find('div', class_='activityinstance').find('a')['href']
			file_req = request_session.get(file_url, stream=True)
			file_name = urllib.parse.unquote(file_req.url.split('/')[-1])
			try:
				online_size = int(file_req.headers['Content-Length'])
			except:
				count += 1
				print('File ' + str(count) + ' not downloadable, skipping...')
				continue
			if os.path.exists(course_path + file_name):
				local_size = os.path.getsize(course_path + file_name)
				if online_size == local_size:
					print('File ' + str(count + 1) + ' of ' + str(len(resources)) + ' "' + file_name + '" already exists, skipping...')
					count += 1
					continue
			print('\nDownloading File ' + str(count + 1) + ' of ' + str(len(resources)) + ' "' + file_name + '" \t\tSize: ' + str(online_size / 1024) + ' KB')

			local_file = open(course_path + file_name, 'wb')
			for block in file_req.iter_content(512):
				if not block:
					break
				local_file.write(block)

			count += 1

	print('\n\n\nAll Done\n\nKeep studying !')
except AssertionError:
	driver.close()
	print('Invalild Login details ! Please close the window and re-run the program !')
except Exception as e:
	driver.close()
	print(f'Un-identified error {e} occured ! Please let the developer know the exact steps you made')
