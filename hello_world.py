# documentation
# [here](https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html)
import random


# ----- Entry point -----
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

# ----- Messages ------
LAUNCH = 'LaunchRequest'
INTENT_TEST = 'testIntent'
INTENT_STOP = 'Amazon.StopIntent'
INTENT_CANCEL = 'Amazon.CancelIntent'
INTENT_WEATHER = 'AMAZON.SearchAction<object@WeatherForecast>'
INTENT_WEATHER_TEMP = 'AMAZON.SearchAction<object@WeatherForecast|temperature>'
INTENT_WEATHER_COND = 'AMAZON.SearchAction<object@WeatherForecast|weatherCondition>'
INTENT_HELP = 'Amazon.HelpIntent'
INTENT_HELLO = 'hello'

messages = {
    LAUNCH: [
        'kk, I\'m woke',
        'Ugh, what?',
        'I really hope you have a good reason to bother me',
    ],
    INTENT_HELLO: [
        'What\'s up?',
        'Hey',
        'What do you want now?',
    ],
}


# ----- Response handlers -----

def on_launch(request, session):
    print("Launching")
    return response({}, rand_response_plain_text(LAUNCH))

def on_intent(request, session):
    print("Intent received")
    intent = Intent(request, session)

    if intent.name == 'testIntent':
        return response({}, 
            response_ssml_text("You " +ssml_emphasis_tag("successfully") 
                + ssml_explitive_tag("tested") + " the " + ssml_whisper_tag("functionality!")
                + ssml_pitch_tag(" this is a low pitch ", "low")
                + ssml_rate_tag(" now I'm talking soooo slow ", "slow")
            )
        )

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
    elif intent.name == INTENT_HELLO:
        return intent.hello()
    else:
        return response({}, response_ssml_text(ssml_rate_tag("I am groot!"), "fast"))

# We can't send a response back on a session end
def on_session_ended(request, session):
    print("Session ended")


def rand_response_plain_text(type, endSession = False):
    return response_plain_text(random.choice(messages[type]), endSession)

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
        
def ssml_explitive_tag(output):
    return "<say-as interpret-as=\"expletive\">" + output +"</say-as>"

def ssml_emphasis_tag(output):
    return "<emphasis level=\"strong\">" + output +"</emphasis>"

def ssml_pitch_tag(output, pitch):
    return "<prosody pitch=\"" + pitch + "\">" + output +"</prosody>"

def ssml_rate_tag(output, rate):
    return "<prosody rate=\"" + rate + "\">" + output +"</prosody>"

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
        return response({}, response_ssml_text(ssml_whisper_tag("The night is dark and full of terrors")))

    def help(self):
        return response({}, response_ssml_text(ssml_emphasis_tag("Fine") +",    " +ssml_pitch_tag("what do you want?", "low")))

    def hello(self):
        return response({}, rand_response_plain_text(INTENT_HELLO))


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
