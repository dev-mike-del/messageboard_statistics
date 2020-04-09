import unittest

import requests

from statistics import MessageBoardAPIWrapper


class TestMessageBoardAPIWrapper(unittest.TestCase): 
      
    def setUp(self): 
        self.topics = requests.get('http://localhost:8080/api/topics').json()
        self.threads = requests.get('http://localhost:8080/api/threads').json()
        self.messages = requests.get('http://localhost:8080/api/messages').json()
        self.messageboard = MessageBoardAPIWrapper()

    def test_num_messages(self):
        i = 0
        for x in self.messages:
            i += 1 
        self.assertEqual( self.messageboard.num_messages(), i) 
        self.assertFalse(self.messageboard.num_messages() == 0)


if __name__ == '__main__': 
    unittest.main()