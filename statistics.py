import json
from typing import Dict

import pandas as pd
import requests


punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
               '\\', '|', '=', '+', '‒', '–', '—', '―', '(', ')', '*', '~', '&']


class MessageBoardAPIWrapper:
    """
    Wrapper around the messageboard API

    http://localhost:8080/api/
    """

    def __init__(self):
        self.topics = requests.get('http://localhost:8080/api/topics').json()
        self.threads = requests.get('http://localhost:8080/api/threads').json()
        self.messages = requests.get('http://localhost:8080/api/messages').json()

    def num_messages(self) -> int:
        """
        Returns the total number of messages.
        """
        #Try to return the length of the response object
        try:
            return len(self.messages)
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
            for result in self.messages:
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
            for result in self.messages:
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
        try:
            num_of_topics = len(self.topics)
            num_of_threads = len(self.threads)
            df_threads = pd.DataFrame(self.threads)
            df_messages = pd.DataFrame(self.messages)

            i = 1
            results = {}
            while i <= num_of_topics:
                df_thread_sample = df_threads.loc[df_threads['topic'] == i]
                results[i] = df_thread_sample.id.to_string(index=False).split()
                i += 1

            for topic in results:
                value_list = []
                for thread in results[topic]:
                    df_message_sample = df_messages.loc[df_messages['thread'] == int(thread)]
                    value_list.append(len(df_message_sample))
                results[topic] = value_list
                value_list = round(sum(value_list) / len(value_list))
                results[topic] = value_list
            return round(sum(results.values()) / len(results.values()))    

        except Exception as e:
            raise e

    def _as_dict(self) -> dict:
        """
        Returns the entire messageboard as a nested dictionary.
        """
        try:
            results = {}
            for topic in self.topics:
                results[topic['title']] = {}
                for thread in self.threads:
                    if thread['topic'] == topic['id']:
                        results[topic['title']][thread['title']] = ''
                        message_list = []
                        for message in self.messages:
                            if message['thread'] == thread['id']:
                                message_list.append(message['content'])
                            results[topic['title']][thread['title']] = message_list
            return(results)


        except Exception as e:
            raise e

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
    print(
        f"Avg. number of messages per thread, per topic.:"
        f"{messageboard.avg_num_msg_thread_topic()}"
    )

    messageboard.to_json()
    print("Message Board written to `messageboard.json`")
    return


if __name__ == "__main__":
    main()
