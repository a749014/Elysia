# Elysia`s core chat tools based on nltk.chat.utils
# developer : a749014
# For the perfect fearless Elysia♪

import random
import re
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
}


class Chat:
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections, key=len, reverse=True)
        return re.compile(
            r"\b({})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )

    def _wildcards(self, response, match):
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response

    def respond(self, Str):
        """
        Generate a response to the user input.

        :type Str: Str
        :param Str: The String to be mapped
        :rtype: Str
        """

        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.search(Str)#improve the accuracy a little bit

            # did the pattern match?
            if match:
                # resp = random.choice(response)  # pick a random response
                # Fix the bug that the response only show one word when it is a string or its length is 1
                if type(response)==str:
                    resp=response
                elif type(response)==list and len(response)<2:
                    resp=response[0]
                else:
                    resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                print(self.respond(user_input))
class Classifier():
    '''Based on NaiveBayesClassifier to improve the accuracy'''
    def __init__(self) -> None:
        pass
    def document_features(self,document:list):
        features = {}
        for word in document:
            features[word] = True
        return features
    def train_classifier(self,training_set:list):
        '''
        data format:[
            [question(str or list),answer(str)],
            .
            .
            .
        ]
        return data:a classifier trained by NaiveBayesClassifier'''
        # 自定义数据集
        data =training_set

        # 定义特征提取函数
        
        # 提取特征

        featuresets = [(self.document_features(d), c) for (d, c) in data]
        # print(featuresets)

        # 训练朴素贝叶斯分类器
        classifier = NaiveBayesClassifier.train(featuresets)

        return classifier

