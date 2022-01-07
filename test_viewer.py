import viewer
import unittest

class TestZendeskViewer(unittest.TestCase) :
	# Set up tests by loading in tickets
	def setUp(self):
		self.tickets = viewer.load_tickets()

	# Test helper funtion find_ticket
	def test_TicketNotFound(self):
		self.assertEqual(viewer.find_ticket(self.tickets, 9999), None)
	def test_NegativeTicketID(self):
		self.assertEqual(viewer.find_ticket(self.tickets, -20), None)
	def test_ZeroTicketID(self):
		self.assertEqual(viewer.find_ticket(self.tickets, 0), None)
	def test_ValidNonZeroTicketID(self):
		self.assertNotEqual(viewer.find_ticket(self.tickets, 5), None)

	# Test format_time
	def test_FormatTimeWorking(self):
		self.assertEqual(viewer.format_time("2021-11-24T23:04:57Z"), "Wed Nov 24 23:04:57 2021")
	def test_FormatTimeNone(self):
		self.assertEqual(viewer.format_time(None), "--")
	def test_FormatTimeNotValid(self):
		self.assertEqual(viewer.format_time("9/30/2021 Last week"), "9/30/2021 Last week")
	
	# Test get_user
	def test_GetUserValid(self):
		self.assertEqual(viewer.get_user(1267642956750), "Khushi Duddi")
	def test_GetUserInvalid(self):
		self.assertEqual(viewer.get_user(999), 999)
	def test_GetUserZero(self):
		self.assertEqual(viewer.get_user(0), 0)
	def test_GetUserNegative(self):
		self.assertEqual(viewer.get_user(-1920308043), -1920308043)


# run main if run as a program
if __name__ == "__main__":
	unittest.main()

# end of program