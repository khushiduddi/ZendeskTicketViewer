# ZendeskTicketViewer

This is my ticket viewer for Zendesk's 2021 coding challenge. I created a CLI version where you can interactively look through all tickets and choose which ones you want to view the information for based on ticket ID. I used the Zendesk REST API as my backend.

## Scenario
The scenario I envisioned is that people working at zcctesla can use this ticket viewer to check on tickets to help customers. This program will be used by the support agents at the company. This will help them organize customer requests and complaints about their cars.

## Requirements
- Connect to the Zendesk API
- Request all the tickets for your account
- Display them in a list
- Display individual ticket details
- Page through tickets when more than 25 are returned

## Installation and Usage
In order to run the viewer, fetch the viewer.py code from github.
```
git clone https://github.com/khushiduddi/ZendeskTicketViewer.git
```
Run the viewer in terminal.
```
$ python3 viewer.py
```
While in the viewer, different keys invoke different actions:
- N for next page
- P for previous page
- ID Number of ticket to view ticket information
- Q to quit

## Unit Tests
In order to run tests, fetch the test_viewer.py code from github.
Run the tests on terminal.
```
$ python3 test_viewer.py
```

## Module Documentation
    viewer

## FUNCTIONS
    display_page(tickets, start, count)
        This method displays a page of count number of tickets from the start
    
    display_ticket(t)
        This method displays information about a single ticket
    
    find_ticket(tickets, ticket_id)
        This method returns a ticket based on a the id passed into the function
    
    load_tickets()
        This method fetches all tickets from zcctesla.zendesk.com
    
    main()
        Main method for interactive viewing ticket list and ticket information

## FILE
    github.com/khushiduddi/Zendesk/ZendeskTicketViewer/viewer.py
