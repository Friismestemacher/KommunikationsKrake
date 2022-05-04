# import flask dependencies
import json  # make me interact with json
# use pretty printing for json responses
from pprint import pprint
import random

pprint('keep pprint')
# server functionality
from flask import Flask, request  # makes the thing ngrokable
# Import datetime class from datetime module

from datetime import datetime, timedelta

# import the response functionality
from response_func import image_response, chip_response, chip_w_context_response, event_response, text_response, \
    context_response, button_response, event_schedule_response, event_detail_response
# import functionality to read out variables from gdf
from retrieve_from_gdf import retrieve_bedarf, retrieve_found_events, retrieve_event_index, retrieve_event_id
# import the database functions
from sb_db_request import test_sb_db, get_accessibility_ids, get_full_event_list, get_event_schedule, get_event_title, \
    get_partial_event_list, get_upcoming_event_list, get_timeframe_event_list, get_all_titles_ids
from video_builder import make_video_array

# import all background intent_logic functionality
from intent_logic import collect_accessibility_needs, show_full_event_list, map_bedarf_for_db

# console should say 200 meaning we have a link to the SB_DB
test_sb_db()

# initialize the flask app
app = Flask(__name__)


@app.route('/')
def index():
    """
  default route, has text, so I can see when the app is running
    :return: Hello World
    """
    return 'Hello World! This is the running Webhook for Sommerblut. ' \
           'For the API please append /webhook to the current url'


def handle_intent(intent_name, req_json):
    """
    Handle the webhook request.
this is the main intent switch function. All intents that use the backend must be routed here.
    :param intent_name:
    :param req_json: the raw format from DF
    :return: None
    """
    print('Intent with backend_logic recognized')
    # build a request object
    req = request.get_json(force=True)
    # fetch action from json
    # action = req.get('queryResult').get('action')

    # fetch param from json
    parameters = req.get('queryResult').get('parameters')
    output_contexts = req.get('queryResult').get('outputContexts')
    num_contexts = len(output_contexts)
    session_id = req.get('session')
    # this is the session id given by dialogflow, it can be overridden to start a new session.
    # Then all data and variables will be lost.
    session_id_array = session_id.split("/")
    session_id = session_id_array[len(session_id_array) - 1]

    if intent_name == 'test.fulfillment':
        # several options for feature testing
        now = datetime.now()
        # return {'fulfillmentText': f'Webhook : Der Webhook funktioniert. {now}'}
        # return chip_response(chips=['Der', 'Webhook', 'funktioniert'])
        # return image_response(url = 'https://github.com/arontaupe/KommunikationsKrake/blob/262cd82afae5fac968fa1d535a87d53cd99b9048/backend/sources/fa/a.png?raw=true')

        return text_response(text='Das Backend ist ansprechbar',
                             dgs_videos_bot=make_video_array(titles=['3', '2', '1']))
        # return context_response(session_id=session_id, context='mycontext', variable_name='variable1',
        #                        variable='value1')
        # return image_response(
        #    url='https://github.com/arontaupe/KommunikationsKrake/blob/262cd82afae5fac968fa1d535a87d53cd99b9048/backend/sources/fa/a.png?raw=true')

    elif intent_name == 'script.accessibility.select':
        return chip_response(text='Viele Veranstaltungen sind barrierefrei Zugänglich. '
                                  'Wenn du magst, kannst du nun einen Bedarf wählen. '
                                  'Dann zeige ich dir nur Veranstaltungen an, bei denen dieser Bedarf erfüllt wird.',
                             chips=['Keinen Bedarf angeben',
                                    'Zugänglich in einfacher Sprache',
                                    'Zugänglich mit Seheinschränkung',
                                    'Zugänglich mit Höreinschränkungen',
                                    'Zugänglich mit Mobilitätseinschränkungen',
                                    'Zugänglich ohne intensive sensorische Reizungen'])

    elif intent_name == 'accessibility.select - collect':
        return collect_accessibility_needs(parameters=parameters,
                                           num_contexts=num_contexts,
                                           output_contexts=output_contexts,
                                           session_id=session_id)

    elif intent_name == 'script.interest.select.1':
        # here we are done with collecting the accessibility and have to store it for further use
        prev_selection_bedarf = None
        for i in range(num_contexts):
            if 'save_bedarf' in output_contexts[i]['name']:
                prev_selection_bedarf = output_contexts[i]['parameters']['prev_selection_bedarf']
                # print('Saving final Accessibility: ' + str(prev_selection_bedarf))
        return chip_w_context_response(
            text='Hier kannst du nun 9 Aussagen bewerten und ich suche dir danach eine passende Veranstaltung heraus. \r\n'
                 'Du kannst sie immer mit Ja, Nein, oder Ist mir Egal bewerten. \r\n'
                 'Erste Frage: \r\n'
                 'Ich finde menschliche Körper interessant.',
            chips=["Ja", "Nein", "Ist mir egal"],
            session_id=session_id,
            context='final_accessibility',
            variable_name='final_accessibility',
            variable=prev_selection_bedarf)

    elif intent_name == 'script.interest.select.1 - egal' or \
            intent_name == 'script.interest.select.1 - ja' or \
            intent_name == 'script.interest.select.1 - nein':
        interest_1 = parameters.get('interest_1')
        return chip_w_context_response(text='Soso, ' + interest_1 + ' also.',
                                       chips=["Weiter: Frage 2", "Menü"],
                                       session_id=session_id,
                                       context='interest_1',
                                       variable_name='interest_1',
                                       variable=interest_1)

    elif intent_name == 'script.interest.select.2':
        # here we are asking for interest_2
        return chip_response(text='Ich mag Biografien und Lebensgeschichten.',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.2 - egal' or \
            intent_name == 'script.interest.select.2 - ja' or \
            intent_name == 'script.interest.select.2 - nein':
        interest_2 = parameters.get('interest_2')
        return chip_w_context_response(text=interest_2 + ', interessant.',
                                       chips=["Weiter: Frage 3", "Menü"],
                                       session_id=session_id,
                                       context='interest_2',
                                       variable_name='interest_2',
                                       variable=interest_2)

    elif intent_name == 'script.interest.select.3':
        # here we are asking for interest_3
        return chip_response(text='Mich faszinieren Rituale',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.3 - egal' or \
            intent_name == 'script.interest.select.3 - ja' or \
            intent_name == 'script.interest.select.3 - nein':
        interest_3 = parameters.get('interest_3')
        return chip_w_context_response(text='Rituale eher so: ' + interest_3,
                                       chips=["Weiter: Frage 4", "Menü"],
                                       session_id=session_id,
                                       context='interest_3',
                                       variable_name='interest_3',
                                       variable=interest_3)

    elif intent_name == 'script.interest.select.4':
        # here we are asking for interest_4
        return chip_response(text='Poesie begeistert mich',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.4 - egal' or \
            intent_name == 'script.interest.select.4 - ja' or \
            intent_name == 'script.interest.select.4 - nein':
        interest_4 = parameters.get('interest_4')
        return chip_w_context_response(text=interest_4 + '? Poesie steckt überall.',
                                       chips=["Weiter: Frage 5", "Menü"],
                                       session_id=session_id,
                                       context='interest_4',
                                       variable_name='interest_4',
                                       variable=interest_4)

    elif intent_name == 'script.interest.select.5':
        # here we are asking for interest_5
        return chip_response(text='Ich verfolge aktuelles Zeitgeschehen und aktuelle Diskurse',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.5 - egal' or \
            intent_name == 'script.interest.select.5 - ja' or \
            intent_name == 'script.interest.select.5 - nein':
        interest_5 = parameters.get('interest_5')
        return chip_w_context_response(text=interest_5 + ', also ich finde Aktuelles wichtig',
                                       chips=["Weiter: Frage 6", "Menü"],
                                       session_id=session_id,
                                       context='interest_5',
                                       variable_name='interest_5',
                                       variable=interest_5)

    elif intent_name == 'script.interest.select.6':
        # here we are asking for interest_6
        return chip_response(text='Ich bin gerne Draußen unterwegs und mag Pflanzen.',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.6 - egal' or \
            intent_name == 'script.interest.select.6 - ja' or \
            intent_name == 'script.interest.select.6 - nein':
        interest_6 = parameters.get('interest_6')
        return chip_w_context_response(text=interest_6 + ', Ich merke, dass das wichtig ist.',
                                       chips=["Weiter: Frage 7", "Menü"],
                                       session_id=session_id,
                                       context='interest_6',
                                       variable_name='interest_6',
                                       variable=interest_6)

    elif intent_name == 'script.interest.select.7':
        # here we are asking for interest_7
        return chip_response(text='Ich lasse mich lieber berieseln als selber aktiv mitmachen zu müssen',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.7 - egal' or \
            intent_name == 'script.interest.select.7 - ja' or \
            intent_name == 'script.interest.select.7 - nein':
        interest_7 = parameters.get('interest_7')
        return chip_w_context_response(text='Dass du ' + interest_7 + ' klickst, sag ich deiner Mutter!',
                                       chips=["Weiter: Frage 8", "Menü"],
                                       session_id=session_id,
                                       context='interest_7',
                                       variable_name='interest_7',
                                       variable=interest_7)

    elif intent_name == 'script.interest.select.8':
        # here we are asking for interest_8
        return chip_response(text='Ich finde Utopien und Zukunftsvisionen interessant.',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.8 - egal' or \
            intent_name == 'script.interest.select.8 - ja' or \
            intent_name == 'script.interest.select.8 - nein':
        interest_8 = parameters.get('interest_8')
        return chip_w_context_response(text='Ich habe mir gemerkt, dass du ' + interest_8 + ' geantwortet hast.',
                                       chips=["Weiter: Frage 9", "Menü"],
                                       session_id=session_id,
                                       context='interest_8',
                                       variable_name='interest_8',
                                       variable=interest_8)

    elif intent_name == 'script.interest.select.9':
        # here we are asking for interest_9
        return chip_response(text='Ich möchte lieber etwas lustiges sehen, als nachdenklich gestimmt zu werden',
                             chips=["Ja", "Nein", "Ist mir egal"],
                             )

    elif intent_name == 'script.interest.select.9 - egal' or \
            intent_name == 'script.interest.select.9 - ja' or \
            intent_name == 'script.interest.select.9 - nein':
        interest_9 = parameters.get('interest_9')
        return chip_w_context_response(text=None,
                                       chips=["Weiter: Zeitselektor", "Menü"],
                                       session_id=session_id,
                                       context='interest_9',
                                       variable_name='interest_9',
                                       variable=interest_9)

    elif intent_name == 'teach.fingeralhabet':
        try:
            fa_letter = parameters.get('FA-Zeichen')
            folder = 'https://github.com/arontaupe/KommunikationsKrake/blob/262cd82afae5fac968fa1d535a87d53cd99b9048/backend/sources/fa/'
            return image_response(url=str(folder) + str(fa_letter) + '.png?raw=true',
                                  chips=['Noch ein Buchstabe', 'Menü'])
        except Exception as e:
            print("Exception when trying to access fa_letter: %s\n" % e)
            return text_response('Mir sind leider die Bilder ausgegangen.')

    elif intent_name == 'faq.sommerblut.team':
        return button_response(url='https://www.sommerblut.de/ls/ueber-uns/profil-team',
                               button_text='Das Team vom Sommerblut',
                               text=' Das Sommerblut hat ein ganz tolles Team. Du kannst sie hier finden',
                               chips=['Ich habe eine andere Frage', 'Zurück: Hauptmenü'])
    elif intent_name == 'script.time.select':
        # here we are making the database call and see whether we need to filter further
        bedarf = retrieve_bedarf(output_contexts)
        # interests = retrieve_interests()
        codes = map_bedarf_for_db(bedarf=bedarf)
        print(codes)
        event_count, events = get_full_event_list(accessibility=codes)
        if events and event_count:
            text = ''
            if event_count > 5:
                text = 'Ich habe mehr als 5 (' + str(
                    event_count) + ') Veranstaltungen gefunden, möchtest du nach Veranstaltungsdatum filtern?'
                chips = ["Nein: alle Empfehlungen anzeigen", 'Ja: Zeitraum auswählen']
            else:
                text = 'Okay, hier kommt mein heißer Tipp für dich! \r\n' \
                       'Ich kann dir mehr zu einer Veranstaltung erzählen oder eine andere Veranstaltung vorschlagen'
                chips = ["Zeig mir die Veranstaltungen"]
            return chip_w_context_response(text=text,
                                           chips=chips,
                                           session_id=session_id,
                                           context='events_found',
                                           variable_name='events_found',
                                           variable=events,
                                           lifespan=150
                                           )
        else:
            return chip_response(text='Ich habe leider keine Events mit deinen Zugänglichkeitsanforderungen gefunden',
                                 chips=['Weiter zum Veranstaltungstipp'])

    elif intent_name == 'script.time.filter':
        return chip_response(text='Das wird spannend! Ich kann dir nun: '
                                  'alle Veranstaltungen, die noch bevorstehen oder '
                                  'Veranstaltungen in den nächsten 5 Tagen suchen',
                             chips=['Nur zukünftige Veranstaltungen', 'Veranstaltungen in den nächsten 5 Tagen'])

    elif intent_name == 'script.time.filter.future':
        try:
            # here we are making the database call and see whether we need to filter further
            bedarf = retrieve_bedarf(output_contexts)
            # interests = retrieve_interests()
            codes = map_bedarf_for_db(bedarf=bedarf)
            event_count, events = get_upcoming_event_list(accessibility=codes)

            text = f'Okay, hier kommt mein heißer Tipp an noch stattfindenden Veranstaltungen für dich! ' \
                   f'Ich kann dir mehr zu einer Veranstaltung erzählen oder eine andere Veranstaltung vorschlagen'
            chips = ["Zeig mir die Veranstaltungen"]
            return chip_w_context_response(text=text,
                                           chips=chips,
                                           session_id=session_id,
                                           context='events_found',
                                           variable_name='events_found',
                                           variable=events,
                                           lifespan=150
                                           )
        except Exception as e:
            print("Exception when trying to access upcoming events: %s\n" % e)
            return chip_response(
                text='Ich habe leider einen Fehler in meinen Berechnungen gemacht, kannst du das nochmal sagen?',
                chips=['Zeig mir alle zukünftigen Veranstaltungen', "Zeig mir alle Veranstaltungen"])



    elif intent_name == 'script.time.filter.nextdays':
        try:
            num_next_days_filter = int(parameters.get('num_next_days_filter'))

            # here we are making the database call and see whether we need to filter further
            bedarf = retrieve_bedarf(output_contexts)
            # interests = retrieve_interests()
            codes = map_bedarf_for_db(bedarf=bedarf)

            event_count, events = get_timeframe_event_list(
                to_date=datetime.now() + timedelta(days=num_next_days_filter),
                accessibility=codes)

            text = f'Okay, hier sind die Veranstaltungen in den nächsten {num_next_days_filter} Tagen für dich'
            chips = ["Zeig mir die Veranstaltungen"]
            return chip_w_context_response(text=text,
                                           chips=chips,
                                           session_id=session_id,
                                           context='events_found',
                                           variable_name='events_found',
                                           variable=events,
                                           lifespan=150
                                           )
        except Exception as e:
            print("Exception when trying to access num_event_filter: %s\n" % e)
            return chip_response(
                text='Ich habe leider nicht verstanden, wie viele Tage ich dir anzeigen soll.',
                chips=["Zeig mir alle Veranstaltungen"])

    elif intent_name == 'script.event.menu':
        return show_full_event_list(output_contexts=output_contexts, session_id=session_id)

    elif intent_name == 'script.event.details':
        try:
            event_id = retrieve_event_id(output_contexts=output_contexts)
            event_count, events = retrieve_found_events(output_contexts)
            if event_id != 0 and events is not None:
                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit', 'Programmtext', 'Coronamaßnahmen',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf sommerblut.de',
                                                      'Zurück: Veranstaltungsübersicht'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id')
            elif event_id != 0 and events is None:
                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit', 'Programmtext', 'Coronamaßnahmen',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf sommerblut.de',
                                                      'Zurück: Ich habe eine Frage'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id')

            elif events is not None:
                next_event_index = int(retrieve_event_index(output_contexts))
                if next_event_index == event_count:
                    event_index = event_count - 1
                else:
                    event_index = next_event_index - 1

                event_id = events[str(event_index)]['id']
                print('entering last elif')
                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit', 'Programmtext', 'Coronamaßnahmen',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf sommerblut.de',
                                                      'Zurück: Veranstaltungsübersicht'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id')
            else:
                print('entering  else')
                return chip_response(
                    text='Ich habe leider keine Events gespeichert. Hast du schon deinen Zugänglichkeitsbedarf angegeben?',
                    chips=['Zugänglichkeit auswählen', 'Interessen angeben'])

        except Exception as e:
            print("Exception when trying to access event details and event_id: %s\n" % e)



    elif intent_name == 'script.event.menu.previous':
        event_count, events = retrieve_found_events(output_contexts)
        if events is None:
            print('no events')
            return text_response(text='Ich habe leider keine Events gespeichert')

        next_event_index = event_index = int(retrieve_event_index(output_contexts))
        display_num = 1
        if event_count == 1:
            return chip_w_context_response(session_id=session_id,
                                           context='event_index',
                                           variable_name='event_index',
                                           variable=next_event_index,
                                           text='Ich habe dir nun alle ausgewählten Events gezeigt. '
                                                'Was möchtest du nun tun?',
                                           chips=['Zurück: Hauptmenü', 'Zeig mir die Veranstaltungen noch einmal'])
        if event_index == 0:
            event_index = event_count - 2
            next_event_index = event_index + 1
        elif event_index == 1:
            event_index = event_count - 1
            next_event_index = event_index + 1
        else:
            event_index = event_index - 2
            next_event_index = event_index + 1

        print(event_index, next_event_index, event_count)
        if event_index == 0:
            chips = ['Zeig mir das nächste Event', 'Mehr zur Veranstaltung']
        else:
            chips = ['Zeig mir das letzte Event', 'Zeig mir das nächste Event', 'Mehr zur Veranstaltung']
        return event_response(
            text='Ich empfehle dir noch einmal die letzte Veranstaltung. '
                 'Ich kann dir dir mehr erzählen oder eine andere Veranstaltung vorschlagen',
            session_id=session_id,
            context='event_index',
            variable_name='event_index',
            variable=next_event_index,
            display_num=display_num,
            display_index=event_index,
            events=events,
            chips=chips
        )

    elif intent_name == 'script.event.details - linkout':
        event_id = retrieve_event_id(output_contexts)
        url = 'https://www.sommerblut.de/en/event/' + str(event_id)
        button_text = 'Link zum Event'
        return button_response(url=url, button_text=button_text, chips=['Zurück: Veranstaltungsdetails'])

    elif intent_name == 'script.event.details - program':
        event_id = retrieve_event_id(output_contexts)
        return chip_response(
            text='Du hast nach dem Programmtext der Veranstaltung gefragt.  TODO Event ID = ' + str(event_id),
            chips=['Zurück: Veranstaltungsübersicht', 'Zurück: Veranstaltungsdetails', 'Hauptmenü'])

    elif intent_name == 'script.event.details - corona':
        event_id = retrieve_event_id(output_contexts)
        return chip_response(
            text='Du hast nach dem Coronainfos der Veranstaltung gefragt.  TODO Event ID = ' + str(event_id),
            chips=['Zurück: Veranstaltungsübersicht', 'Zurück: Veranstaltungsdetails', 'Hauptmenü'])

    elif intent_name == 'script.event.details - accessibility':
        event_id = retrieve_event_id(output_contexts)
        return chip_response(
            text='Du hast nach den Barrierefreiheitsinfos der Veranstaltung gefragt. TODO Event ID = ' + str(event_id),
            chips=['Zurück: Veranstaltungsübersicht', 'Hauptmenü',
                   'Kontaktmöglichkeit für Zugänglichkeitsunterstützung'])

    elif intent_name == 'script.event.details - schedule':
        event_id = retrieve_event_id(output_contexts)
        event_count, events = retrieve_found_events(output_contexts=output_contexts)
        if event_id and events:
            for e in range(event_count):
                if events[str(e)].get('id') == event_id:
                    duration = int(events[str(e)].get('duration'))
                    title = events[str(e)].get('title')
                    location = events[str(e)].get('location')
                    price = int(events[str(e)].get('price_vvk'))
                    image = events[str(e)].get('event_images')
                    print(image)
                    return event_detail_response(duration=duration,
                                                 title=title,
                                                 location=location,
                                                 price=price,
                                                 image=image,
                                                 text=f'{title} dauert {duration} Minuten. \r\n '
                                                      f'Es findet statt an diesm Ort: {location}. \r\n'
                                                      f'Er kostet {price} Euro. \r\n'
                                                      f'(Event_ID: {event_id})',
                                                 chips=['Zurück: Veranstaltungsübersicht',
                                                        'Zurück: Veranstaltungsdetails', 'Hauptmenü',
                                                        'Liste der Spielzeiten anzeigen'])
        else:
            return chip_response(
                text='Irgendwie habe ich wohl die Veranstaltungsnummer vergessen, versuch es doch noch einmal.',
                chips=['Zurück: Veranstaltungsübersicht', 'Zurück: Veranstaltungsdetails', 'Hauptmenü'])

    elif intent_name == 'script.event.details.showSchedule':
        event_id = int(retrieve_event_id(output_contexts))
        play_count, plays = get_event_schedule(event_id)
        event_title = get_event_title(event_id)

        return event_schedule_response(play_count,
                                       plays,
                                       text=f'Titel der Veranstaltung: {event_title} \r\n'
                                            f'Veranstaltungs ID: {event_id}',
                                       chips=['Tickets online kaufen', 'Alternative Wege Tickets zu kaufen',
                                              'Zurück: Veranstaltungsübersicht', 'Zurück: Veranstaltungsdetails',
                                              'Hauptmenü']
                                       )

    elif intent_name == 'faq.contact.accessibility':
        return chip_response(text='Franziska hilft dir gerne bei Fragen rund um die Zugänglichkeit '
                                  'von Veranstaltungen weiter. '
                                  'Du kannst sie so erreichen: franziska.lammers@sommerblut.de '
                                  'oder per Telefon: 0221 – 29 49 91 34',
                             chips=['Zurück: Veranstaltungsdetails'])

    elif intent_name == 'faq.event':

        try:
            event_title = parameters.get('event_title')
            titles, ids = get_all_titles_ids()
            if len(event_title) != 0:
                idx = titles.index(event_title)
                event_id = ids[idx]

                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit', 'Programmtext', 'Coronamaßnahmen',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf sommerblut.de',
                                                      'Zurück: Ich habe eine Frage'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id')
            else:

                chips = random.sample(titles, 3)
                return chip_response(text='Du kannst den Namen der Veranstaltung in das Textfeld unten eingeben. '
                                          'Oder eine von unten wählen:',
                                     chips=chips)

        except Exception as e:
            print("Exception when trying to identify the event asked about-> faq.event: %s\n" % e)

    elif intent_name == 'faq.tickets.sale_location':
        return chip_response(
            text='An folgenden Orten können Tickets gekauft werden:\r\n'
                 'Theater·kasse am Neumarkt\r\n'
                 'Die Theater·kasse ist auf der Zwischen·ebene der U-Bahn-Station Neumarkt.\r\n '
                 'Die genaue Adresse ist:\r\n'
                 'Neumarkt, U-Bahn-Passage\r\n'
                 'Laden 12\r\n'
                 '50667 Köln, \r\n',
            chips=['Zeig mir die Veranstaltung auf Sommerblut.de', 'Zurück: Veranstaltungsdetails'])

    elif intent_name == 'faq.tickets.sale_phone':
        return button_response(url='tel:+4922142076000',
                               button_text='Direkt anrufen',
                               text='Du kannst die Tickets auch am Telefon bestellen.\r\n'
                                    'Unter der Telefonnummer 0221 42 07 6000.\r\n'
                                    'Aber Achtung:\r\n'
                                    'Am Telefon kann man die Tickets mit Kreditkarte bezahlen.\r\n',
                               chips=['Zeig mir die Veranstaltung auf Sommerblut.de', 'Zurück: Veranstaltungsdetails'])

    elif intent_name == 'script.tickets.sale':
        return button_response(url='https://t.rausgegangen.de/tickets/shop/sommerblut-2022',
                               button_text='Rausgegangen Ticketshop',
                               text='Hier geht es zum Ticketshop von Sommerblut.',
                               chips=['Zeig mir die Veranstaltung auf Sommerblut.de', 'Zurück: Veranstaltungsdetails'])

    elif intent_name == 'fallback.default':
        return chip_response(text='Ich bin nicht so sicher, ob ich dich richtig verstanden habe. '
                                  'Kannst du das noch einmal anders formulieren?',
                             chips=['Hauptmenü', 'Ich habe eine Frage'])

    elif intent_name == 'faq.bot.cando':
        return chip_response(
            text='Ich bin noch am lernen. Ich kann dir Veranstaltungen empfehlen und Fragen beantworten. '
                 'Hoffentlich kann ich bald auch so gut digital surfen wie du.',
            chips=['Hauptmenü', 'Ich habe eine Frage'])

    elif intent_name == 'faq.knowledge.chatbot':
        return chip_response(
            text='Ein Chatbot Ist eine Maschine, die sich mit dir unterhalten kann wie ein Mensch.',
            chips=['Zurück: Hauptmenü', 'Ich habe eine andere Frage'])

    elif intent_name == 'faq.knowledge.whoami':
        return chip_response(
            text='Ich bin Ällei, ein Chatbot. '
                 'Ich lebe auf der Website des Sommerblut Festivals. '
                 'Komm mich gern besuchen!',
            chips=['Zurück: Hauptmenü', 'Ich habe eine andere Frage'])

    elif intent_name == 'script.welcome':
        return chip_response(
            text='Hi! Mein Name ist Ällei! \r\n'
                 'Schön, dass du hier bist. \r\n'
                 'Ich kann dir helfen, Informationen über das Sommerblut Festival zu finden. \r\n'
                 'Bist du das erste mal hier? Dann schau dir gern das Einführungs-Video an. \r\n',
            chips=['Einführungsvideo', 'Kenne ich schon: Hauptmenü', 'Ich habe eine Frage'],
            dgs_videos_bot=make_video_array(['A1']),
            dgs_videos_chips=make_video_array(['RC1a', 'RC1b', 'RC2', 'RC3']))

    elif intent_name == 'script.bot.introvideo':
        return chip_response(
            text='Video: Wie funktioniert der bot und was kann er alles:',
            chips=['Weiter: Hauptmenü'],
            dgs_videos_bot=None,
            dgs_videos_chips=make_video_array(['RC4']))

    elif intent_name == 'script.main_menu':
        return chip_response(
            text='Okay, worauf hast du jetzt Lust?'
                 'Ich kann dir zum Beispiel noch mehr über mich und über künstliche Intelligenz erzählen.'
                 'Oder ich berate dich, welche Veranstaltung dir gefallen wird.',
            chips=['Video: Ällei und KI', 'Video: Ällei und KI in Leichter Sprache', 'Veranstaltungsberatung',
                   'Mehr über Sommerblut erfahren'],
            dgs_videos_bot=make_video_array(['A2']),
            dgs_videos_chips=make_video_array(['RC5a', 'RC5b', 'RC6', 'RC7']))

    elif intent_name == 'script.bot_theme_input':
        return chip_response(
            text='Hier wird ein Video gezeigt: "Barrierefreiheit im digitalen Raum"',
            chips=['Mehr über Sommerblut erfahren', 'Ich habe eine Frage', 'Veranstaltungsberatung'],
            # dgs_videos_bot=make_video_array(['A2']),
            # dgs_videos_chips=make_video_array(['RC5a', 'RC5b', 'RC6', 'RC7'])
        )

    elif intent_name == 'faq.sommerblut':
        return chip_response(
            text='Okay, was willst du über das Sommerblut wissen?',
            chips=['Festivalschwerpunkt 2022',
                   'Womit beschäftigt sich das Sommerblut?',
                   'Frage zur Barrierefreiheit',
                   'Wer steckt hinter dem Sommerblut?'],
            # dgs_videos_bot=make_video_array(['A2']),
            # dgs_videos_chips=make_video_array(['RC5a', 'RC5b', 'RC6', 'RC7'])
        )

    elif intent_name == 'faq.start':
        return chip_response(
            text='Alles klar. Du kannst die Frage unten in das Textfeld schreiben. '
                 'Oder du kannst aus einem Bereich auswählen:',
            chips=['Frage zu einer konkreten Veranstaltung', 'Frage zum Sommerblut allgemein',
                   'Frage zur Barrierefreiheit'
                   'Frage zu Ällei, dem Chatbot'],
            # dgs_videos_bot=make_video_array(['A2']),
            # dgs_videos_chips=make_video_array(['RC5a', 'RC5b', 'RC6', 'RC7'])
        )


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def update():
    """
Main listener to DF, will call handle_intent upon being activated
    :return: the response to DF
    """
    if request.method == 'POST':
        update = request.data.decode("utf8")
        update = json.loads(update)
        print("====================================== REQUEST.DATA ======================================")
        # pprint(update)
        response = handle_intent(update['queryResult']['intent']['displayName'], update)

        if response:
            print("====================================== RESPONSE.DATA ======================================")
            # pprint(response)

        return response
    else:
        return "Incorrect request format (/)"


# run the app 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

print("botserver started")
