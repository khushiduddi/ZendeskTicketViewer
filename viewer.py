import requests
import sys
import json
from decouple import config
from datetime import datetime

# User cache to maintain a cache of the names the users to reduce API hits
user_cache = {}
# Tickets and pagination
tickets = []
next_page = ""
has_more = True
# Mode: Search or List
mode = 'list'
# Credentials for API
apibase = 'https://zcctesla1.zendesk.com/api/v2'
username = config('USERNAME')
token = config('TOKEN')

#Initialize global variables
def init(m='list'):
	"""This method initializes the global state"""
	global tickets, next_page, has_more, mode
	tickets = []
	next_page = ""
	has_more = True
	mode = m

# Processes command line arguments for importing tickets
def process_arg():
	"""This method processes command line arguments"""
	if (len(sys.argv) == 1):
		return
	if (len(sys.argv) != 3):
		print("Error processing arguments")
		print("Usage: python3 viewer.py [--import tickets.json]")
		exit()
	if (sys.argv[1] == "--import"):
		import_tickets(sys.argv[2])

# Imports tickets from a file
def import_tickets(filename):
	"""This method allows agents to import tickets from a file"""
	# Read the file
	try:
		f = open(filename)
	except IOError:
		print(f"Error: Cannot read file {filename}")
		return
	
	ticket_data = json.load(f)
	f.close()

	# Set the request parameters
	url = apibase + '/imports/tickets/create_many.json'

	# Do the HTTP get request
	response = requests.post(url, auth=(username + "/token", token), json=ticket_data)

	# Check for HTTP codes other than 200
	if response.status_code != 200:
		print('Status:', response.status_code, 'Problem with the request. Exiting. Please try again later or check your credentials')
		print("Response status code: ", response.status_code, " Response reason: ", response.reason, " Text: ", response.text)
		exit()


# Method displays a page of a certain number of tickets
def display_page(tickets, start, count):
	"""This method displays a page of count number of tickets from the start"""
	end = len(tickets) if (start+count > len(tickets)) else start + count
	for i in range(start, end):
		t = tickets[i]
		print(f"{t['id']} {t['subject']}")

# Method displays info of certain ticket
def display_ticket(t):
	"""This method displays information about a single ticket"""
	print("-----------------------------------------------------")
	print(f"Ticket ID: {t['id']}")
	requester = get_user(t['requester_id'])
	assignee = get_user(t['assignee_id'])
	print(f"Requester ID: {requester} \t Assignee ID: {assignee}")
	print(f"Status: {t['status']} \t Priority: {t['priority']}")
	created_at = format_time(t['created_at'])
	due_at = format_time(t['due_at'])
	print(f"Due at: {due_at} \t Created at: {created_at}")
	print(f"Subject: {t['subject']} \nDescription: {t['description']}")
	print("-----------------------------------------------------")
	

# Method finds ticket with certain id number
def find_ticket(tickets, ticket_id):
	"""This method returns a ticket based on a the id passed into the function"""
	for t in tickets:
		if t['id'] == ticket_id:
			return t
	return None

# Method displays time from Zendesk ticket is readable format
def format_time(str):
	"""This method returns the time from a Zendesk ticket in a human readable format using local format"""
	if (str == None):
		return "--"
	# Remove the last Z
	str = str.rstrip('Z')
	try:
		dt = datetime.fromisoformat(str)
	except:
		# Failure happened: most likely incorrect format. Return string
		return str
	return dt.strftime("%c")

# Method returns name for a requester or assignee from ID
def get_user(user_id):
	"""This method returns the name of the user from an ID for a requester or assignee"""
	if user_id in user_cache:
		return user_cache[user_id]

	# Set the request parameters
	url = f"{apibase}/users/{user_id}.json"

	# Do the HTTP get request
	response = requests.get(url, auth=(username + "/token", token))

	# Check for HTTP codes other than 200
	if response.status_code != 200:
		# API failed. Fall back to user id. Return user_id
		return user_id

	# Decode the JSON response into a dictionary and use the data
	data = response.json()
	user = data['user']
	user_cache[user_id] = user['name']
	return user['name']


def load_tickets(recent=False):
	"""This method fetches all tickets from zcctesla.zendesk.com"""
	global next_page, tickets, has_more
	# Set the request parameters
	if (recent):
		url = f"{apibase}/tickets.json?page[size]=100&sort=-updated_at"
	else:
		url = f"{apibase}/tickets.json?page[size]=100"
	# Check if at the end of all tickets
	if (next_page == "" and not has_more):
		return tickets
	if (next_page != ""):
		url = next_page
	print("Loading tickets...")
	# Do the HTTP get request
	response = requests.get(url, auth=(username + "/token", token))

	# Check for HTTP codes other than 200
	if response.status_code != 200:
		print('Status:', response.status_code,' Text: ', response.text, 'Problem with the request. Exiting. Please try again later or check your credentials')
		exit()

	# Decode the JSON response into a dictionary and use the data
	data = response.json()
	tickets.extend(data['tickets'])
	has_more = data['meta']['has_more']
	if has_more:
		next_page = data['links']['next']
	else:
		next_page = ""
	return tickets

# Search through tickets using API
def search_tickets(search_str="", recent=False):
	global next_page, tickets, has_more
	url = f"{apibase}/search.json?query={search_str}"
	if (recent):
		# XXX SORT ASC HAS BUG: ids slightly out of order
		url += "&sort_by=updated_at&sort_order=asc"
	# Check if at the end of filtered tickets
	if (next_page == None and not has_more):
		return tickets
	if (next_page != ""):
		url = next_page

	response = requests.get(url, auth=(username + "/token", token))

	# Check for HTTP codes other than 200
	if response.status_code != 200:
		print('Status:', response.status_code,' Text: ', response.text, 'Problem with the request. Exiting. Please try again later or check your credentials')
		exit()
	
	data = response.json()
	# Remove non tickets from result 'result_type' != 'ticket'
	i = 0
	while i < len(data['results']):
		if data['results'][i]['result_type'] != 'ticket':
			data['results'].pop(i)
		else:
			i += 1

	tickets.extend(data['results'])
	next_page = data['next_page']
	has_more = (next_page != None) 
	return tickets


def main():
	"""Main method for interactive viewing ticket list and ticket information"""
	global mode
	process_arg()
	tickets = load_tickets()
	PAGE = 30
	user_input = ""
	start = 0
	while user_input.lower() not in ("q", "x"):
		# print next 25
		if not user_input.isdigit():
			display_page(tickets, start, PAGE)
		# ask user for input
		user_input = input("Press n-next, p-previous, id-view ticket, search <text>-search, list-get ticket list, recent-sort and q-quit: ")
		user_input = user_input.lower()
		if user_input == "p":
			start = 0 if (start < PAGE) else (start - PAGE)
		elif user_input.isdigit():
			t = find_ticket(tickets, int(user_input))
			if t == None:
				print("The ID you entered is not valid")
			else:
				display_ticket(t)
		elif user_input.startswith("search "):
			searched_str = user_input[7:]
			init('search')
			tickets = search_tickets(searched_str)
			start = 0
		elif user_input.startswith("list"):
			init('list')
			tickets = load_tickets()
			start = 0
		elif user_input.startswith("recent"):
			if mode == "list":
				init('list')
				tickets = load_tickets(True)
				start = 0
			else:
				init('search')
				tickets = search_tickets(searched_str, True)
				start = 0
		else:
			# Check if there is at least 1 full page left
			if (start + PAGE + PAGE >= len(tickets)):
				if mode == 'list':
					# Load more tickets from server
					tickets = load_tickets()
				else:
					tickets = search_tickets()
			if (start + PAGE < len(tickets)):
				start += PAGE
				


# run main if run as a program
if __name__ == "__main__":
	main()

# end of program