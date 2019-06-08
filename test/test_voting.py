import unittest
from . import fake_message
from foodflex.periods import voting


class TestVoteValidation(unittest.TestCase):

    def test_b(self):
        author = fake_message.FakeAuthor(1, "Will")
        message1 = fake_message.FakeMessage(author, ":b:")
        self.assertEqual(voting.check_vote(message1), True)

        message2 = fake_message.FakeMessage(author, "🅱️")
        self.assertEqual(voting.check_vote(message2), True)

if __name__ == '__main__':
    unittest.main()
