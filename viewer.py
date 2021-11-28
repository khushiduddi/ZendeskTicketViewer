import requests
from datetime import datetime

# User cache to maintain a cache of the names the users to reduce API hits
user_cache = {}

# Credentials for API
username = 'kduddi2@illinois.edu!'
token = 'Pxi91Dr5ywN8NJTFPtvnbhOzNcQJWpixCoyrbJYw'

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
	url = f"https://zcctesla.zendesk.com/api/v2/users/{user_id}.json"

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


def load_tickets():
	"""This method fetches all tickets from zcctesla.zendesk.com"""
	# Set the request parameters
	url = 'https://zcctesla.zendesk.com/api/v2/tickets.json'

	# Do the HTTP get request
	response = requests.get(url, auth=(username + "/token", token))

	# Check for HTTP codes other than 200
	if response.status_code != 200:
		print('Status:', response.status_code, 'Problem with the request. Exiting. Please try again later or check your credentials')
		exit()

	# Decode the JSON response into a dictionary and use the data
	data = response.json()
	tickets = data['tickets']
	return tickets


def main():
	"""Main method for interactive viewing ticket list and ticket information"""
	tickets = load_tickets()
	PAGE = 25
	user_input = ""
	start = 0
	while user_input.lower() not in ("q", "x"):
		# print next 25
		if not user_input.isdigit():
			display_page(tickets, start, PAGE)
		# ask user for input
		user_input = input("Press N-next, P-previous, ID-view ticket and Q-quit: ")
		user_input = user_input.lower()
		if user_input == "p":
			start = 0 if (start < PAGE) else (start - PAGE)
		elif user_input.isdigit():
			t = find_ticket(tickets, int(user_input))
			if t == None:
				print("The ID you entered is not valid")
			else:
				display_ticket(t)
		else:
			# next page
			start = start if (start >= len(tickets)-PAGE) else (start + PAGE)


# run main if run as a program
if __name__ == "__main__":
	main()

# end of program