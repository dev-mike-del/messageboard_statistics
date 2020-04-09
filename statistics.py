import json
from typing import Dict

import pandas as pd
import requests


# This list to remove any punctuation marks that may be in a string.
# This is used in MessageBoardAPIWrapper.most_common_word function
punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
               '\\', '|', '=', '+', '‒', '–', '—', '―', '(', ')', '*', '~', '&']


class MessageBoardAPIWrapper:
    """
    Wrapper around the messageboard API

    http://localhost:8080/api/
    """
    # Use the API endpoint urls to create variables that will be used through
    # out the MessageBoardAPIWrapper class.
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
            # Try to return the length of the message response object.
            # The length of the message response object will return the total
            # number of messages in the object.
            return len(self.messages)
        except Exception as e:
            raise e

    def most_common_word(self) -> str:
        """
        Returns the most frequently used word in messages.
        """ 
        try:
            # This list is for appending every word in every message.
            # We will include duplicated but they will be removed via
            # the set() function used the the return.
            word_list = []
            for message in self.messages:
                for word in message['content'].split():
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
                    # Now we add the lowercase word to our word_list variable
                    word_list.append(word.lower())
            # This returns the most common word in the word_list variable
            return max(set(word_list), key = word_list.count)

        except Exception as e:
            raise e

    def avg_num_words_per_sentence(self) -> float:
        """
        Returns the average number of words per sentence.
        """
        try:
            # The content variable will store every sentence from every message
            content = []
            # The words_per_sentence variable will store the length of every 
            # sentence from every message
            words_per_sentence = []
            for message in self.messages:
                # The message['content'] contains the message string.
                # Here we append the message string to the content variable.
                content.append(message['content'])
            # Split the contents variable into individual sentences
            content = "".join(content).split('.')
            for sentence in content:
                # Append the length of each sentence to the words_per_sentence
                # variable.
                words_per_sentence.append(len(sentence.split()))
            # Get the average of the values of the words_per_sentence 
            # variable. 
            avg_num = sum(words_per_sentence) / len(words_per_sentence)
            # Return the rounded average number of words per sentence
            return int(round(avg_num, 0))

        except Exception as e:
            raise e

    def avg_num_msg_thread_topic(self) -> Dict[str, float]:
        """
        Returns the average number of messages per thread, per topic.
        """
        try:
            # Using the pandas library, these two variables are
            # DataFrames of the threats and messages response objects.
            df_threads = pd.DataFrame(self.threads)
            df_messages = pd.DataFrame(self.messages)

            i = 1
            # The results variable will store values and be used to return 
            # the average number. 
            results = {}
            # This while loop is used to construct the results variable 
            # dictionary with the topic id(s) as the keys and thread id(s)
            # as the values.
            while i <= len(self.topics):
                df_thread_sample = df_threads.loc[df_threads['topic'] == i]
                results[i] = df_thread_sample.id.to_string(index=False).split()
                i += 1

            # This for loop is used to first replace the results values with 
            # the corrisponding number of messages per thread. Then, it uses
            # those values to return the rounded average.
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
            # This series of iterations is used to create a nested dictionary
            # that follows the pattern {topic1:{thread1:[messages], thread2:[messages]}}
            results = {}
            for topic in self.topics:
                # This set the main keys as the topic title.
                results[topic['title']] = {}
                for thread in self.threads:
                    if thread['topic'] == topic['id']:
                        # This adds the thread title as a key in the value dictionary .
                        results[topic['title']][thread['title']] = ''
                        message_list = []
                        for message in self.messages:
                            if message['thread'] == thread['id']:
                                message_list.append(message['content'])
                            # This sets the messages as the values for the 
                            # corrisponding thread keys.
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
