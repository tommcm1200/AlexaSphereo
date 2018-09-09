"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""


from __future__ import print_function
import urllib3

# HOST_NAME = os.environ['HOST_NAME'] + ".ngrok.io"
HOST_NAME = "048708e1.ngrok.io"

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Sphero Alexa Skill"
    speech_output =  "Entering the Sphero Alexa Skill. " \
            "With this skill, you can control your Sphero through voice. Super Cool, Eh?" \
            "Let's jump into it! " \
            "I'm programed with 3 colors, Red, Green, Blue. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What color would you like your Sphero to change to?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Sphereo Skill. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

        
def set_Sphero_connect_in_session(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    print("Connecting Sphero")

    http = urllib3.PoolManager()
    r = http.request('POST', 'http://048708e1.ngrok.io/sphero/connect')
    print(r.status)
    reprompt_text = "What would you like to do now?"
    speech_output = "Ok. Connecting Sphero. Sphero should become a solid color. " + reprompt_text

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_Sphero_color_in_session(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    uColor = intent['slots']['color']['value']
    print("SpheroColor: " + uColor)
    arr = ['blue', 'green', 'red']

    reprompt_text = "What would you like to do now?"

    requestPath = '/sphero/color/'+uColor
    print(HOST_NAME)
    print(requestPath)

    try:
        arr.index(uColor)
        
        http = urllib3.PoolManager()
        request_url = 'http://'+HOST_NAME+requestPath
        print("Making HTTP request", request_url)
        r = http.request('POST', request_url)
        print(r.status)
            
        speech_output = "Ok. Changing to "+uColor+". Nice. You changed the color. " + reprompt_text
    except:
        print("Invalid Color")
        speech_output = "Sorry, I can't do "+uColor+"yet. Choose Red, Green or Blue."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_Sphero_move_in_session(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    requestedShape = intent['slots']['shape']['value']
    print("SpheroMove: " + requestedShape)

    reprompt_text = "What would you like to do now?"
    speech_output = "Ok. Sphero moving in a "+requestedShape+". " + reprompt_text

    requestPath = '/sphero/shape/'+requestedShape

    http = urllib3.PoolManager()
    request_url = 'http://'+HOST_NAME+requestPath
    print("Making HTTP request", request_url)
    r = http.request('POST', request_url)
    print(r.status)

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SpheroConnect":
        return set_Sphero_connect_in_session(intent, session)
    elif intent_name == "SpheroColor":
        return set_Sphero_color_in_session(intent, session)
    elif intent_name == "SpheroMove":
        return set_Sphero_move_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    
    
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
