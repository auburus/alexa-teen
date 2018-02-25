# documentation
# [here](https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html)
def lambda_handler(event, context):
    """ App entry point  """
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    else:
        print("BUG: request type wrong")
        print(event['request'])


# ----- Response handlers -----

def on_launch(request, session):
    print("Session started")
    return response({}, response_plain_text("kk, I'm woke"))

def on_intent(request, session):
    print("Intent recived")
    intent = Intent(request, session)

    if intent.name == 'testIntent':
        return response({}, response_ssml_text("You successfully tested the" + ssml_whisper_tag(" functionality!")))
    elif intent.name == 'AMAZON.StopIntent':
        return intent.stop()
    elif intent.name == 'AMAZON.CancelIntent':
        return intent.cancel()
    elif intent.name in ['AMAZON.SearchAction<object@WeatherForecast>',
            'AMAZON.SearchAction<object@WeatherForecast|temperature>', 
            'AMAZON.SearchAction<object@WeatherForecast|weatherCondition>']:
        return intent.weatherForcast()
    elif intent.name == 'AMAZON.HelpIntent':
        return intent.help()
    elif intent.name == 'hello':
        return intent.hello()
    else:
        return response({}, response_plain_text("I am groot!"))

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

def response_ssml_text(output, endSession = False):
    return {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" + output +"</speak>"
                },
            'shouldEndSession': endSession
            }
                        
def ssml_whisper_tag(output):
    return "<amazon:effect name=\"whispered\">" + output +"</amazon:effect>"
        
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


    def stop(self):
        return response({}, response_plain_text("Oh, hashtag finally", True))

    def cancel(self):
        return self.stop()

    def weatherForcast(self):
        return response({}, response_plain_text("The night is dark and full of terror"))

    def help(self):
        return response({}, response_plain_text("Fine, what do you want?", False))

    def hello(self):
        print("DEBUG: Hello request")
        print("DEBUG", self.request)
        print("DEBUG: Hello response")
        print("DEBUG", response({}, response_plain_text("Mehh")))
        return response({}, response_plain_text("Mehh"))


# test
if __name__ == "__main__":
    import sys

    intent_name = "AMAZON.CancelIntent"
    if len(sys.argv) >= 2:
        intent_name = sys.argv[1]

    event = {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "amzn1.echo-api.session.[unique-value-here]",
            "application": {
                "applicationId": "amzn1.ask.skill.[unique-value-here]"
            },
            "attributes": {
                "key": "string value"
            },
            "user": {
                "userId": "amzn1.ask.account.[unique-value-here]",
                "accessToken": "Atza|AAAAAAAA...",
                "permissions": {
                    "consentToken": "ZZZZZZZ..."
                    }
            }
        },
        "context": {},
        "request": {
            "type": "IntentRequest",
            "requestId": "string",
            "timestamp": "string",
            "dialogState": "string",
            "locale": "string",
            "intent": {
                "name": intent_name,
                "confirmationStatus": "string",
                "slots": {
                    "SlotName": {
                        "name": "string",
                        "value": "string",
                        "confirmationStatus": "string",
                        "resolutions": {
                            "resolutionsPerAuthority": [
                                {
                                    "authority": "string",
                                    "status": {
                                        "code": "string"
                                    },
                                    "values": [
                                        {
                                            "value": {
                                                "name": "string",
                                                "id": "string"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }
    }

    print(lambda_handler(event, {}))
