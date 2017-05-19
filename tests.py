from cakeipsum import Provider
import unittest

class testCakeipsum(unittest.TestCase):

	def test_return_a_paragraph_that_contains_at_leat_10_words(self):
		self.assertTrue(len(Provider.paragraph()) >= 10 )

	def test_return_a_word(self):
		self.assertTrue(len(Provider.word()) >= 1 )

	def test_return_sentences(self):
		self.assertTrue(len(Provider.sentences()) >= 1 )


if __name__ == '__main__':
    unittest.main()