# documentation
# [here](https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html)
def lambda_handler(event, context):
    """ App entry point  """
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()


# ----- Response handlers -----

def on_launch(request, session):
    print("Session started")
    return response({}, response_plain_text("I'm launching"))

def on_intent(request, session):
    intent = Intent(request, session)
    intent = request['intent']
    if intent['name'] == 'testIntent':
        return response({}, response_plain_text("You successfully tested"
            + " the functionality!"))
    elif intent.name == 'exit':
        return exit_intent(request, session);
    else:
        return response({}, response_plain_text("This is an intent"))

# We can't send a response back on a session end
def on_session_ended(request, session):
    print("Session ended")

def response_plain_text(output, endSession = False):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endSession
    }

def response(attributes, response_obj):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': response_obj
    }

# Oh swag money, you're actually playing a cool song
class Intent():
    def __init__(self, request, session):
        self.request = request
        self.session = session

    @property
    def name(self):
        return self.request['intent']['name']

    def exit(self):
        return response({}, response_plain_text("Oh, hasthag finally", True))
