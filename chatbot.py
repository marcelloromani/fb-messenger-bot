import re
import nltk

class ChatBot:
    STATE_START = 0  # we haven't received any message yet
    STATE_WAIT_FOR_ORDER = 1
    STATE_GETTING_ORDER = 2

    # this should go into some sort of inventory class...
    available_items = [
        'pizza',
        'potatoes',
        'broccoli',
        'pasta',
        'burritos',
        'porridge',
    ]

    def __init__(self):
        self.state = self.STATE_START
        self.ordered_items = []

    def reply_to(self, msg):
        msg = msg.lower()
        tokens = nltk.word_tokenize(msg)
        print(tokens)
        tagged = nltk.pos_tag(tokens)
        print(tagged)

        if not set(["hi", "hello"]).isdisjoint(tokens):
            self.state = self.STATE_WAIT_FOR_ORDER
            self.ordered_items = []
            return "Hi, I'm Gina. What food do you want to order?"

        if self.state == self.STATE_START:
            return "Please say Hi"

        elif self.state == self.STATE_WAIT_FOR_ORDER:
            desired_items = []
            unwanted_items = []
            adj_noun = ""

            negation_active = False
            for x in tagged:
                print "analysing " + ', '.join(x)

                if x[1] == "RB" and x[0] in ['not', "n't", 'no']:
                    negation_active = True
                elif x[1] in ['JJ']:
                    adj_noun += x[0] + " "
                elif x[1] in ['NN', 'NNS']:
                    adj_noun += x[0]
                    if negation_active:
                        print "negation in place, not adding " + adj_noun
                        negation_active = False
                        unwanted_items.append(adj_noun)
                    else:
                        print "adding " + adj_noun
                        desired_items.append(adj_noun)
                    adj_noun = ""

            print "The user wants"
            print desired_items

            # check if we have all the items
            self.ordered_items = []
            response = ""
            for item in desired_items:
                if item in self.available_items:
                    self.ordered_items.append(item)
                else:
                    response += "Sorry, " + item + " is not available.\n"

            if len(self.ordered_items) > 0:
                response += "\nOk, I will get you " + ', '.join(self.ordered_items)
                self.state = self.STATE_GETTING_ORDER
            else:
                response = "Please tell me what you wnat to order!"

            return response
        elif self.state == self.STATE_GETTING_ORDER:
            return "Your " + ", ".join(self.ordered_items) + " is on the way. If you want something else please say 'Hi' again."
