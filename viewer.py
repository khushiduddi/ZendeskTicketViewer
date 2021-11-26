import requests
import datetime

# method displays a page of a certain number of tickets
def display_page(tickets, start, count):
	"""This method displays a page of count number of tickets from the start"""
	end = len(tickets) if (start+count > len(tickets)) else start + count
	for i in range(start, end):
		t = tickets[i]
		print(f"{t['id']} {t['subject']}")

# method displays info of certain ticket
def display_ticket(t):
	"""This method displays information about a single ticket"""
	print(f"Ticket ID: {t['id']}")
	print(f"Requester ID: {t['requester_id']} \t Assignee ID: {t['assignee_id']}")
	print(f"Status: {t['status']}")
	created_at = (t['created_at'])
	print(f"Due at: {t['due_at']} \t Created at: {created_at}")
	print(f"Subject: {t['subject']} \nDescription: {t['description']}")
	

# method finds ticket with certain id number
def find_ticket(tickets, ticket_id):
	"""This method returns a ticket based on a the id passed into the function"""
	for t in tickets:
		if t['id'] == ticket_id:
			return t
	return None

def load_tickets():
	"""This method fetches all tickets from zcctesla.zendesk.com"""
	# Set the request parameters
	url = 'https://zcctesla.zendesk.com/api/v2/tickets.json'
	user = 'kduddi2@illinois.edu'
	token = 'Pxi91Dr5ywN8NJTFPtvnbhOzNcQJWpixCoyrbJYw'

	# Do the HTTP get request
	response = requests.get(url, auth=(user + "/token", token))

	# Check for HTTP codes other than 200
	if response.status_code != 200:
		print('Status:', response.status_code, 'Problem with the request. Exiting.')
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