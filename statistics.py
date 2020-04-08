import json
from typing import Dict

import requests


punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
               '\\', '|', '=', '+', '‒', '–', '—', '―', '(', ')', '*', '~', '&']


class MessageBoardAPIWrapper:
    """
    Wrapper around the messageboard API

    http://localhost:8080/api/
    """
    response = requests.get('http://localhost:8080/api/messages')

    def __init__(self):
        self.response = requests.get('http://localhost:8080/api/messages').json()

    def num_messages(self) -> int:
        """
        Returns the total number of messages.
        """
        #Try to return the length of the response object
        try:
            return len(self.response)
        except Exception as e:
            raise e
        else:
            raise NotImplementedError

    def most_common_word(self) -> str:
        """
        Returns the most frequently used word in messages.
        """
        try:
            word_list = []
            for result in self.response:
                for word in result['content'].split():
                    # This checks if the first letter of the word is in the 
                    # punctuation_list. If it is, the function replaces the letter 
                    # with an empty string.
                    if word[0] in punctuation_list:
                        word = word.replace(word[0], '')
                    # This checks if the last letter of the word is in the 
                    # punctuation_list. If it is, the function replaces the letter 
                    # with an empty string.
                    elif word[-1] in punctuation_list:
                        word = word.replace(word[-1], '')
                    word_list.append(word.lower())
            return max(set(word_list), key = word_list.count)

        except Exception as e:
            raise e
        else:
            raise NotImplementedError

    def avg_num_words_per_sentence(self) -> float:
        """
        Returns the average number of words per sentence.
        """
        try:
            content = []
            words_per_sentence = []
            for result in self.response:
                content.append(result['content'])
            content = "".join(content).split('.')
            for sentence in content:
                words_per_sentence.append(len(sentence.split()))
            avg_num = sum(words_per_sentence) / len(words_per_sentence)
            return int(round(avg_num, 0))

        except Exception as e:
            raise e
        else:
            raise NotImplementedError

    def avg_num_msg_thread_topic(self) -> Dict[str, float]:
        """
        Returns the average number of messages per thread, per topic.
        """
        raise NotImplementedError

    def _as_dict(self) -> dict:
        """
        Returns the entire messageboard as a nested dictionary.
        """
        raise NotImplementedError

    def to_json(self) -> None:
        """
        Dumps the entire messageboard to a JSON file.
        """
        with open("messageboard.json", "w") as f:
            f.write(json.dumps(self._as_dict(), indent=4))


def main():
    """
    Returns information about the messageboard application
    """

    messageboard = MessageBoardAPIWrapper()

    print(f"Total number of messages: {messageboard.num_messages()}")
    print(f"Most common word: {messageboard.most_common_word()}")
    print(
        f"Avg. number of words per sentence.:"
        f"{messageboard.avg_num_words_per_sentence()}"
    )
    # print(
    #     f"Avg. number of messages per thread, per topic.:"
    #     f"{messageboard.avg_num_msg_thread_topic()}"
    # )

    # messageboard.to_json()
    # print("Message Board written to `messageboard.json`")
    return


if __name__ == "__main__":
    main()
