import viewer
import unittest

class TestZendeskViewer(unittest.TestCase) :
	def setUp(self):
		self.tickets = viewer.load_tickets()

	def test_TicketNotFound(self):
		self.assertEqual(viewer.find_ticket(self.tickets, 9999), None)

	def test_NegativeTicketID(self):
		self.assertEqual(viewer.find_ticket(self.tickets, -20), None)

	def test_ZeroTicketID(self):
		self.assertEqual(viewer.find_ticket(self.tickets, 0), None)

	def test_ValidNonZeroTicketID(self):
		self.assertNotEqual(viewer.find_ticket(self.tickets, 5), None)

# run main if run as a program
if __name__ == "__main__":
	unittest.main()

# end of program