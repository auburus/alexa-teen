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
    print("Indent requested")
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
