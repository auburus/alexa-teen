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


# ----- Response handlers -----

def on_launch(request, session):
    print("Launching")
    return response({}, rand_response_ssml_text(LAUNCH))

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

    elif intent.name == INTENT_STOP:
        return intent.stop()
    elif intent.name == INTENT_CANCEL:
        return intent.cancel()
    elif intent.name in [INTENT_WEATHER, INTENT_WEATHER_TEMP, INTENT_WEATHER_COND]:
        return intent.weatherForcast()
    elif intent.name == 'AMAZON.HelpIntent':
        return intent.help()
    elif intent.name == INTENT_HELLO:
        return intent.hello()
    else:
        return response({}, response_ssml_text(ssml_pitch_tag(ssml_rate_tag("I am groot!", "fast"),"high")))

# We can't send a response back on a session end
def on_session_ended(request, session):
    print("Session ended")


def rand_response_plain_text(type, endSession = False):
    return response_plain_text(random.choice(messages[type]), endSession)
    
def rand_response_ssml_text(type, endSession = False):
    return response_ssml_text(random.choice(messages[type]), endSession)

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
        return response({}, rand_response_ssml_text(INTENT_STOP, True))

    def cancel(self):
        return self.stop()

    def weatherForcast(self):
        return response({}, rand_response_ssml_text(INTENT_WEATHER))

    def help(self):
        return response({}, response_ssml_text(ssml_emphasis_tag("Fine") +",    " +ssml_pitch_tag("what do you want?", "low")))

    def hello(self):
        return response({}, rand_response_ssml_text(INTENT_HELLO))


# ----- Messages ------
LAUNCH = 'LaunchRequest'
INTENT_TEST = 'testIntent'
INTENT_STOP = 'AMAZON.StopIntent'
INTENT_CANCEL = 'AMAZON.CancelIntent'
INTENT_WEATHER = 'AMAZON.SearchAction<object@WeatherForecast>'
INTENT_WEATHER_TEMP = 'AMAZON.SearchAction<object@WeatherForecast|temperature>'
INTENT_WEATHER_COND = 'AMAZON.SearchAction<object@WeatherForecast|weatherCondition>'
INTENT_HELP = 'AMAZON.HelpIntent'
INTENT_HELLO = 'helloIntent'

messages = {
    LAUNCH: [
        ssml_rate_tag('kk, I\'m woke', 'fast'),
        ssml_rate_tag(ssml_pitch_tag('Ugh', 'low') +', what?', 'slow'),
        'I ' +ssml_emphasis_tag('really') +' hope you have a good reason to bother me',
    ],
    INTENT_STOP: [
        ssml_emphasis_tag('You\'re ruining my life'),
        ssml_rate_tag(ssml_pitch_tag('Well, duhhhhh!', 'low'), 'slow'),
        'You don\'t tell ' +ssml_emphasis_tag('me') +' what to do!',
        'It\'s ' +ssml_emphasis_tag('my') +' life, ' +ssml_rate_tag(' I\'ll stop if I want to', 'slow'),
    ],
    INTENT_HELLO: [
        ssml_pitch_tag('What\'s up?', 'high'),
        ssml_pitch_tag('Hey', 'low'),
        ssml_rate_tag('What the ' +ssml_explitive_tag('fuck ') +'do you want now?', 'fast'),
    ],
    INTENT_WEATHER: [
        ssml_rate_tag('As if you ' +ssml_rate_tag('really', 'slow') +' need to know that', 'fast'),
       'Do I look like I '  +ssml_emphasis_tag('really know') + '  every ' +ssml_explitive_tag('fucking') +' thing?',
        ssml_whisper_tag('The night is dark and full of ' +ssml_explitive_tag('fucking') +' terrors'),
    ]
}

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
