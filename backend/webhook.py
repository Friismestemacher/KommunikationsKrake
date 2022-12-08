import random  # generates random chips for me
from flask import request  # makes a flask app and serves it to a specified port

# import all background intent_logic functionality
from intent_logic import collect_accessibility_needs, map_bedarf_for_db, order_events_by_interest, show_full_event_list

# import the response functionality
from response_func import button_response, chip_response, chip_w_context_response, chip_w_two_context_response, \
    event_detail_response, event_response, event_schedule_response, image_response, text_response, \
    chip_w_three_context_response

# import functionality to read out variables from gdf
from retrieve_from_gdf import retrieve_bedarf, retrieve_event_id, retrieve_event_index, \
    retrieve_found_events, \
    retrieve_interests, whether_searched_events
# import the database functions
from sb_db_request import get_event_schedule, get_event_title, get_full_event_list, get_timeframe_event_list, \
    get_next_event
from video_builder import make_video_array
from smalltalk import give_smalltalk
from glossary import give_glossary
from team import give_team
from faq import give_faq
from feedback import give_feedback
from send_yagmail import send_mail
from calendar_events import create_ics
from datetime import datetime, timedelta
import yagmail


def handle_intent(intent_name):
    """
    Handle the webhook request.
this is the main intent switch function. All intents that use the backend must be routed here.
    param intent_name: the name given in the dialogflow interface
    :return: None
    """
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
        # return {'fulfillmentText': f'Webhook : Der Webhook funktioniert. {datetime.now()}'}
        # return chip_response(chips=['Der', 'Webhook', 'funktioniert'])
        # return image_response(url = 'https://github.com/arontaupe/KommunikationsKrake/blob/'
        #                            '262cd82afae5fac968fa1d535a87d53cd99b9048/backend/sources/fa/a.png?raw=true')

        return text_response(text='Das Backend ist ansprechbar',
                             dgs_videos_bot=make_video_array(titles=['3', '2', '1']))
        # return context_response(session_id=session_id, context='mycontext', variable_name='variable1',
        #                        variable='value1')
        # return image_response(
        #    url='https://github.com/arontaupe/KommunikationsKrake/blob/262cd82afae5fac968fa1d535a87d53cd99b9048/backend/sources/fa/a.png?raw=true')

    elif intent_name == 'script.accessibility.select':
        return chip_response(text='Viele Veranstaltungen sind barrierefrei.\r\n'
                                  'Du kannst auswählen:\r\n'
                                  'Welche Form von Barrierefreiheit brauchst Du?\r\n'
                                  'Dann zeige ich dir nur Veranstaltungen an.\r\n'
                                  'Diese Veranstaltungen sind barrierefrei für Dich.\r\n'
                                  'Welche Form von Barrierefreiheit brauchst Du?\r\n',
                             chips=['Ich brauche keine Barrierefreiheit',
                                    'Ich suche Veranstaltungen in einfacher Sprache',
                                    'Ich habe eine Sehbehinderung',
                                    'Ich habe eine Hörbehinderung',
                                    'Ich habe eine Gehbehinderung'
                                    # 'Ich suche eine Veranstaltung ohne schnelle, blinkende Lichter.
                                    # Und ohne laute, plötzliche Geräusche.'
                                    ],
                             dgs_videos_bot=make_video_array(['A5']),
                             dgs_videos_chips=make_video_array(['RC14', 'RC15', 'RC16', 'RC17', 'RC18']))

    elif intent_name == 'accessibility.select - collect':
        return collect_accessibility_needs(parameters=parameters,
                                           num_contexts=num_contexts,
                                           output_contexts=output_contexts,
                                           session_id=session_id)

    elif intent_name == 'script.interest.select.start':
        # here we are done with collecting the accessibility and have to store it for further use
        prev_selection_bedarf = None
        for i in range(num_contexts):
            if 'save_bedarf' in output_contexts[i]['name']:
                prev_selection_bedarf = output_contexts[i]['parameters']['prev_selection_bedarf']

        return chip_w_context_response(
            text='Ich möchte dir Veranstaltungen empfehlen.\r\n'
                 'Veranstaltungen, die gut zu dir passen.\r\n'
                 'Dazu muss ich dich erstmal kennenlernen.\r\n'
                 'Ich befrage dich zu Deinen Interessen.\r\n'
                 'Du kannst immer mit Ja, mit Nein, oder mit Egal antworten.',
            chips=["Weiter: Frage 1"],
            session_id=session_id,
            context='final_accessibility',
            variable_name='final_accessibility',
            variable=prev_selection_bedarf,
            dgs_videos_bot=make_video_array(['A7']),
            dgs_videos_chips=make_video_array(['RC21'])
        )

    elif intent_name == 'script.interest.collect':
        try:
            interest_1 = parameters.get('interest_1')
            interest_2 = parameters.get('interest_2')
            interest_3 = parameters.get('interest_3')
            interest_4 = parameters.get('interest_4')
            interest_5 = parameters.get('interest_5')
            interest_6 = parameters.get('interest_6')
            interest_7 = parameters.get('interest_7')
            interest_8 = parameters.get('interest_8')
            interest_9 = parameters.get('interest_9')
        except Exception as e:
            print("Exception when trying to access the interests:script.interest.collect %s\n" % e)
            return text_response('Ich bekomme keine Interessen gesagt')

        while interest_1 == '':
            return chip_response(text='1. Aussage: \r\n'
                                      'Menschliche Körper faszinieren mich.',
                                 chips=["Ja", "Nein", "Ist mir egal"],
                                 dgs_videos_bot=make_video_array(['A8']),
                                 dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4']))
        while interest_2 == '':
            return chip_w_context_response(text='2. Aussage: \r\n'
                                                'Mich interessieren Lebenswege, die nicht ganz normal verlaufen.',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_1',
                                           variable_name='interest_1',
                                           variable=interest_1,
                                           dgs_videos_bot=make_video_array(['A9']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        while interest_3 == '':
            return chip_w_context_response(text='3. Aussage: \r\n'
                                                'Ich beschäftige mich gerne mit Ritualen.\r\n'
                                                'Zum Beispiel: Ich zünde eine Kerze für jemanden an.',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_2',
                                           variable_name='interest_2',
                                           variable=interest_2,
                                           dgs_videos_bot=make_video_array(['A10']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        while interest_4 == '':
            return chip_w_context_response(text='4. Aussage: \r\n'
                                                'Ich mag Poetisches. \r\n'
                                                'Zum Beispiel: Schöne Musik. '
                                                'Oder: Schöne Bilder.',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_3',
                                           variable_name='interest_3',
                                           variable=interest_3,
                                           dgs_videos_bot=make_video_array(['A11']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        while interest_5 == '':
            return chip_w_context_response(text='5. Aussage: \r\n'
                                                'Ich sehne mich nach einer guten Zukunft.',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_4',
                                           variable_name='interest_4',
                                           variable=interest_4,
                                           dgs_videos_bot=make_video_array(['A12']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        while interest_6 == '':
            return chip_w_context_response(text='6. Aussage: \r\n'
                                                'Ich interessiere mich für die Frage:\r\n'
                                                'Welche Themen sind in unserer Gesellschaft gerade wichtig? \r\n'
                                                'Worüber wird gerade gesprochen?',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_5',
                                           variable_name='interest_5',
                                           variable=interest_5,
                                           dgs_videos_bot=make_video_array(['A13']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        while interest_7 == '':
            return chip_w_context_response(text='7. Aussage: \r\n'
                                                'Ich bin gerne draußen unterwegs und mag Natur.',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_6',
                                           variable_name='interest_6',
                                           variable=interest_6,
                                           dgs_videos_bot=make_video_array(['A14']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        while interest_8 == '':
            return chip_w_context_response(text='8. Aussage: \r\n'
                                                'Ich möchte nur zuhören.\r\n'
                                                'Ich möchte nicht selbst bei etwas mitmachen müssen.',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_7',
                                           variable_name='interest_7',
                                           variable=interest_7,
                                           dgs_videos_bot=make_video_array(['A16']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        while interest_9 == '':
            return chip_w_context_response(text='9. Aussage: \r\n'
                                                'Ich möchte nicht so viel nachdenken. \r\n'
                                                'Ich will lieber etwas Lustiges sehen.',
                                           chips=["Ja", "Nein", "Ist mir egal"],
                                           session_id=session_id,
                                           context='interest_8',
                                           variable_name='interest_8',
                                           variable=interest_8,
                                           dgs_videos_bot=make_video_array(['A15']),
                                           dgs_videos_chips=make_video_array(['AC1', 'AC2', 'AC4'])
                                           )
        else:
            return chip_w_context_response(text='Danke für deine Antworten.',
                                           session_id=session_id,
                                           context='interest_9',
                                           variable_name='interest_9',
                                           variable=interest_9,
                                           dgs_videos_bot=make_video_array(['RC20']),
                                           dgs_videos_chips=make_video_array(['RC21b']),
                                           chips=['Weiter zu den Veranstaltungstipps']
                                           )

    elif intent_name == 'teach.fingeralhabet':
        try:
            fa_letter = parameters.get('FA-Zeichen')
            if fa_letter == '':
                chips = random.sample(
                    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 5)
                chips.append('Mehr Buchstaben vorschlagen')
                return chip_response(text='Na klar.\r\n'
                                          'Welchen Buchstaben möchtest du denn lernen?\r\n'
                                          'Gib einen Buchstaben ein.\r\n'
                                          'Ich zeige ihn dir.\r\n',
                                     chips=chips,
                                     dgs_videos_bot=make_video_array(['Finger1'])
                                     )
            folder = 'https://github.com/arontaupe/KommunikationsKrake/blob/' \
                     '262cd82afae5fac968fa1d535a87d53cd99b9048/backend/sources/fa/'
            return image_response(url=str(folder) + str(fa_letter) + '.png?raw=true',
                                  chips=['Ich möchte noch einen Buchstaben lernen',
                                         'Zurück zum Hauptmenü'],
                                  dgs_videos_bot=make_video_array(['Finger1']),
                                  dgs_videos_chips=make_video_array(['Finger2', 'AC7'])
                                  )
        except Exception as e:
            print("Exception when trying to access fa_letter: %s\n" % e)
            return text_response('Mir sind leider die Bilder ausgegangen.')

    elif intent_name == 'script.time.select':
        # here we are making the database call and see whether we need to filter further
        bedarf = None
        codes = None
        try:
            bedarf = retrieve_bedarf(output_contexts=output_contexts)
            codes = map_bedarf_for_db(bedarf=bedarf)
        except Exception as e:
            print("Exception when trying to access Accessibilities: %s\n" % e)
        if bedarf:
            print(f'Accessibilites: {bedarf}')
        if codes:
            print(f'Accessibility Codes: {codes}')

        entries = 50  # the number that decides how many events get called per round
        # page = retrieve_page_cache(output_contexts=output_contexts)  # page = index of the call batch
        page = 1

        event_count, events, titles, ids = get_full_event_list(accessibility=codes, page=page, entries=entries)
        print(f'Event_count: {event_count}')

        # obsolete, only used when chunking instead of caching
        # while less events than stated in event_count are present, make another call
        # if page var is lost, the second clause catches it
        while entries * page < event_count and len(events) <= event_count:
            _, events_cache, _, ids_cache = retrieve_found_events(output_contexts=output_contexts)
            if events_cache is None:
                pass  # do nothing when no cache is present, just hand over the caught events
            else:
                event_list = list(events.values())
                event_list.extend(list(events_cache.values()))
                # rename keys
                events = dict(zip(list(range(len(event_list))), event_list))
            page += 1
            return chip_w_two_context_response(text='Das sind viele Vorschläge. \r\n '
                                                    'Ich muss nochmal suchen.',
                                               chips=['Finde mehr Veranstaltungstipps'],
                                               session_id=session_id,
                                               context='events_found',
                                               variable_name='events_found',
                                               variable=events,
                                               lifespan=5,
                                               context_2='page_cache',
                                               variable_name_2='page_cache',
                                               variable_2=page,
                                               dgs_videos_bot=make_video_array(['E1']),
                                               dgs_videos_chips=make_video_array(['RC21b']),
                                               )

        if events:
            try:
                interests = retrieve_interests(output_contexts=output_contexts)
            except Exception as e:
                print("Exception when trying to access Interests: %s\n" % e)
            event_count, events, titles, ids = order_events_by_interest(interests=interests,
                                                                        event_count=event_count,
                                                                        events=events)
        if events and event_count:
            if event_count > 5:
                text = 'Ich habe sehr viele Veranstaltungen für dich gefunden. ' \
                       'Möchtest du ein bestimmtes Datum auswählen?',
                chips = ['Ja: Zeitraum auswählen',
                         "Nein: alle Empfehlungen anzeigen"
                         ]
                dgs_videos_bot = make_video_array(['A17'])
                dgs_videos_chips = make_video_array(['RC22', 'RC23'])
            else:
                text = 'Okay, hier kommt mein Tipp für dich! \r\n' \
                       'Ich kann dir mehr zu einer Veranstaltung erzählen oder eine andere Veranstaltung vorschlagen'
                chips = ["Zeig mir die Veranstaltungen",
                         'Zeig mir endlich die Veranstaltungen!'
                         ]
                dgs_videos_bot = make_video_array(['A19'])
                dgs_videos_chips = make_video_array(['RC27a'])
            return chip_w_context_response(text=text,
                                           chips=chips,
                                           session_id=session_id,
                                           context='events_found',
                                           variable_name='events_found',
                                           variable=events,
                                           lifespan=150,
                                           dgs_videos_bot=dgs_videos_bot,
                                           dgs_videos_chips=dgs_videos_chips
                                           )
        else:
            return chip_response(text='Ich habe leider keine Veranstaltungen mit deinen Barrierefreiheiten gefunden',
                                 chips=['Barrierefreiheit angeben', 'Zurück zum Hauptmenü'],
                                 dgs_videos_bot=make_video_array(['A18b']),
                                 dgs_videos_chips=make_video_array(['RC13', 'AC7'])
                                 )

    elif intent_name == 'script.time.filter':
        return chip_response(text='Das wird spannend! Ich kann dir nun: '
                                  'alle Veranstaltungen, die noch bevorstehen oder '
                                  'Veranstaltungen in den nächsten 5 Tagen suchen',
                             chips=['Nur zukünftige Veranstaltungen',
                                    'Veranstaltungen in den nächsten 5 Tagen'],
                             dgs_videos_bot=make_video_array(['A18']),
                             dgs_videos_chips=make_video_array(['RC25', 'RC26'])
                             )

    elif intent_name == 'script.time.filter.future':
        try:
            # here we are making the database call and see whether we need to filter further
            bedarf = retrieve_bedarf(output_contexts)
            interests = retrieve_interests(output_contexts=output_contexts)
            codes = map_bedarf_for_db(bedarf=bedarf)
            event_count, events, titles, ids = get_timeframe_event_list(accessibility=codes)
            event_count, events, titles, ids = order_events_by_interest(interests=interests, event_count=event_count,
                                                                        events=events)

            text = f'Okay, hier kommt mein heißer Tipp an noch stattfindenden Veranstaltungen für dich! ',
            chips = ["Zeig mir die Veranstaltungen"]
            return chip_w_context_response(text=text,
                                           chips=chips,
                                           session_id=session_id,
                                           context='events_found',
                                           variable_name='events_found',
                                           variable=events,
                                           lifespan=150,
                                           dgs_videos_bot=make_video_array(['A19']),
                                           dgs_videos_chips=make_video_array(['RC27a'])
                                           )
        except Exception as e:
            print("Exception when trying to access upcoming events: %s\n" % e)
            return chip_response(
                text='Ich habe leider einen Fehler in meinen Berechnungen gemacht, kannst du das nochmal sagen?',
                chips=['Zeig mir alle zukünftigen Veranstaltungen', "Zeig mir alle Veranstaltungen"])

    elif intent_name == 'script.time.filter.nextdays':
        try:
            num_next_days_filter = int(parameters.get('num_next_days_filter'))
            bedarf = retrieve_bedarf(output_contexts=output_contexts)
            interests = retrieve_interests(output_contexts=output_contexts)
            codes = map_bedarf_for_db(bedarf=bedarf)
            event_count, events, titles, ids = get_timeframe_event_list(num_days=num_next_days_filter,
                                                                        accessibility=codes)
            event_count, events, titles, ids = order_events_by_interest(interests=interests, event_count=event_count,
                                                                        events=events)

            if event_count > 0:
                text = f'Okay, hier sind die Veranstaltungen in den nächsten {num_next_days_filter} Tagen für dich'
                chips = ["Zeig mir die Veranstaltungen"]
                return chip_w_context_response(text=text,
                                               chips=chips,
                                               session_id=session_id,
                                               context='events_found',
                                               variable_name='events_found',
                                               variable=events,
                                               lifespan=150,
                                               dgs_videos_chips=make_video_array(['RC27a'])
                                               )
            else:
                return chip_response(
                    text=f'In den nächsten {num_next_days_filter} Tagen habe ich keine Events gefunden.\r\n'
                         f'Möchtest du deine Suche vergrößern?',
                    chips=[f'Suche Veranstaltungen in den nächsten {num_next_days_filter + 7} Tagen',
                           'Zeig mir alle Veranstaltungen'],
                    # dgs_videos_chips=make_video_array(['RC27a'])
                )
                return
        except Exception as e:
            print("Exception when trying to access num_event_filter: %s\n" % e)
            return chip_response(
                text='Ich habe leider nicht verstanden, wie viele Tage ich dir anzeigen soll.',
                chips=["Zeig mir alle Veranstaltungen"],
                dgs_videos_chips=make_video_array(['RC27a'])
            )

    elif intent_name == 'script.event.menu':
        return show_full_event_list(output_contexts=output_contexts, session_id=session_id)

    elif intent_name == 'script.event.menu - send_as_mail - consent':
        consent = parameters.get('consent')
        while consent == 'undefined':
            return chip_response(text='Um eine E-Mail senden zu können, brauche ich dein Einverständnis. \r\n'
                                      'Deine Adresse zählt zu den persönlichen Daten.\r\n'
                                      'Deine Mail-Adresse wird dabei an Google weitergeleitet. \r\n'
                                      'Google darf die Adresse dann genau wie alle deine Eingaben\r\n'
                                      'als Trainings-Daten verwenden und speichern.\r\n'
                                      'Bei Sommerblut wird deine Adresse nicht gespeichert.\r\n'
                                      'Gibst du dein Einverständnis?\r\n'
                                      'Bitte antworte mit Ja oder Nein.\r\n',
                                 chips=['Ja', 'Nein'])

    elif intent_name == 'script.event.menu - send_as_mail - consent - no':
        return chip_response(text='Okay, dann kann Ich dir leider keine Email senden.\r\n'
                                  'Möchtest du etwas anderes tun?\r\n',
                             chips=['Gib mir eine weitere Empfehlung',
                                    'Ich möchte mehr zur Veranstaltung wissen'],
                             dgs_videos_chips=make_video_array(['RC28', 'RC29']))

    elif intent_name == 'script.event.menu - send_as_mail - consent - yes':
        mail_addr = parameters.get('mail_addr')

        while mail_addr == '':
            return chip_response(text='Okay, dann brauche ich deine E-Mail Adresse.\r\n'
                                      'Gib sie einfach unten ein.\r\n'
                                      'Achte auf die korrekte Schreibweise.\r\n',
                                 chips=['Ich will doch keine Email angeben', ],
                                 )

        event_count, events, titles, ids = retrieve_found_events(output_contexts)
        if events is None:
            event_count, events, titles, ids = get_full_event_list(page=1, entries=50)
        print(f'{ids=}')

        if events is None:
            return chip_response(
                text='Ich habe leider keine Events gespeichert. \r\n'
                     'Ich konnte die E-Mail nicht senden.\r\n',
                chips=['Barrierefreiheit angeben'])

        prefix = mail_addr.split('@')[0]
        event_index = (int(retrieve_event_index(output_contexts)) + (event_count - 1)) % event_count

        title = titles[event_index]
        event_id = ids[event_index]
        print(f'{event_id=}')
        url = 'https://www.sommerblut.de/ls/veranstaltung/' + str(int(event_id))

        for e in range(event_count):
            e_idx = str(e)
            event = events[e_idx]
            if event.get('id') == event_id:
                title = event.get('title', None)
                subtitle = event.get('subtitle', None)
                duration = event.get('duration', None)
                if duration:
                    duration = int(duration)
                location = event.get('location', None)
                address = event.get('address', None)
                short_description = event.get('short_description', None)
                price = event.get('price_vvk', None)
                if price:
                    price = int(price)
                image = event.get('event_images', None)
                artist_name = event.get('artist_name', None)
                ticket_link = event.get('ticket_link', None)
                next_date = min_date = max_date = None
                if event.get('next_date'):
                    next_date = event['next_date']
                if event.get('min_date'):
                    min_date = event['min_date']
                if event.get('max_date'):
                    max_date = event['max_date']

        if next_date:
            start = datetime.strptime(next_date, '%Y-%m-%dT%H:%M:%S%z')
            end = datetime.strptime(next_date, '%Y-%m-%dT%H:%M:%S%z') + timedelta(
                minutes=(int(duration if duration else 60)))

        else:
            start = datetime.strptime(min_date, '%Y-%m-%dT%H:%M:%S%z')
            end = datetime.strptime(max_date, '%Y-%m-%dT%H:%M:%S%z')

        start_str = datetime.strftime(start, 'Beginn am %d.%m.%Y um %M:%S%z Uhr')
        end_str = datetime.strftime(end, 'bis zum %d.%m.%Y um %M:%S%z Uhr')

        create_ics(name=title,
                   desc=f'{subtitle if subtitle else ""} \r\n'
                        f'{short_description if short_description else ""} \r\n'
                        f'{url if url else ""}',
                   dtstart=start,
                   dtend=end,
                   organizer=artist_name if artist_name else "",
                   location=f'{location if location else ""}{address if address else ""}')

        default = 'Hier fehlt mir eine Info, schau lieber auf der Webseite nach.'

        contents = f"Hallo liebe:r {prefix},\r\n" \
                   f"Du hast dich beim Sommerblut-Festival für {title} interessiert.\r\n" \
                   f"Hier nun ein paar weitere Infos dazu:\r\n \r\n" \
                   f"{subtitle if subtitle else ''}\r\n" \
                   f"Künstler:in: {artist_name if artist_name else default}\r\n" \
                   f"{short_description if short_description else ''}\r\n" \
                   f"{start_str} {end_str}\r\n" \
                   f"Ort: {location if location else default}\r\n" \
                   f"{address if address else ''}\r\n" \
                   f"Preis in Euro: {price if price else default} \r\n" \
                   f"Hier buchen: {ticket_link if ticket_link else default}\r\n" \
                   f"Mehr Informationen: {url if url else default}\r\n" \
                   f"Ich freue mich, dass du mich besucht hast.\r\n" \
                   f"Komm mich gern wieder besuchen.\r\n \r\n" \
                   f"Dein Ällei\r\n"

        send_mail(TO=mail_addr,
                  subject=f'Ällei grüßt und schickt eine Einladung zu {title}',
                  contents=contents,
                  attachments=[f'events/{title}.ics'])

        return chip_response(text=f'Cool! ich habe gerade eine E-Mail an {mail_addr} gesendet.\r\n'
                                  f'Was möchtest du nun tun?\r\n',
                             chips=['Zeig mir weitere Veranstaltungen',
                                    'Erzähl mir einen Witz'],
                             )

    elif intent_name == 'script.event.menu - send_as_mail - consent - withdrawn':
        return chip_response(text=f'Okay, Ich habe deine Einwilligung gelöscht.\r\n'
                                  f'Du wirst keine E-Mail erhalten.\r\n'
                                  f'Was möchtest du nun tun?\r\n',
                             chips=['Zeig mir weitere Veranstaltungen',
                                    'Erzähl mir einen Witz'],
                             )

    elif intent_name == 'script.event.details':
        event_id = None
        try:
            event_id = retrieve_event_id(output_contexts=output_contexts)
        except Exception as e:
            print("Exception when trying to access event_id: %s\n" % e)

        if not whether_searched_events(output_contexts=output_contexts):
            if event_id:
                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung?\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit',
                                                      'Programmtext',
                                                      'Coronasituation',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf Sommerblut.de',
                                                      'Zurück: Ich habe eine andere Frage'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id',
                                               dgs_videos_bot=make_video_array(['AC20']),
                                               dgs_videos_chips=make_video_array(
                                                   ['RC30', 'RC31', 'RC32', 'RC33', 'RC34', 'RC3'])
                                               )

        try:
            event_count, events, titles, ids = retrieve_found_events(output_contexts)
            if event_id and events is not None:
                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung?\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit',
                                                      'Programmtext',
                                                      'Coronasituation',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf Sommerblut.de',
                                                      'Zurück: Veranstaltungs-empfehlungen'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id',
                                               dgs_videos_bot=make_video_array(['AC20']),
                                               dgs_videos_chips=make_video_array(
                                                   ['RC30', 'RC31', 'RC32', 'RC33', 'RC34', 'RC34b'])
                                               )
            elif event_id != 0 and events is None:
                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung?\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit',
                                                      'Programmtext',
                                                      'Coronamaßnahmen',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf sommerblut.de',
                                                      'Zurück: Ich habe eine Frage'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id',
                                               dgs_videos_bot=make_video_array(['AC20']),
                                               dgs_videos_chips=make_video_array(
                                                   ['RC30', 'RC31', 'RC32', 'RC33', 'RC34', 'RC34b'])
                                               )

            elif events is not None:
                next_event_index = int(retrieve_event_index(output_contexts))
                if next_event_index == event_count:
                    event_index = event_count - 1
                else:
                    event_index = next_event_index - 1

                event_id = events[str(event_index)]['id']

                return chip_w_context_response(session_id=session_id,
                                               text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                    '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                    '2. Worum geht es genau in der Veranstaltung?\r\n'
                                                    '3. Wie handhabt ihr Corona?\r\n'
                                                    '4. Wo und Wann findet sie statt?\r\n',
                                               chips=['Barrierefreiheit',
                                                      'Programmtext',
                                                      'Coronamaßnahmen',
                                                      'Datum und Ort',
                                                      'Zeig mir die Veranstaltung auf sommerblut.de',
                                                      'Zurück: Veranstaltungs-empfehlungen'],
                                               variable_name='event_id',
                                               variable=event_id,
                                               context='event_id',
                                               dgs_videos_bot=make_video_array(['AC20']),
                                               dgs_videos_chips=make_video_array(
                                                   ['RC30', 'RC31', 'RC32', 'RC33', 'RC34', 'RC34b'])
                                               )
            else:
                return chip_response(
                    text='Ich habe leider keine Veranstaltungen gespeichert. '
                         'Hast du schon deinen Zugänglichkeitsbedarf angegeben?',
                    chips=['Zugänglichkeit auswählen', 'Interessen angeben'])

        except Exception as e:
            print("Exception when trying to access event details and event_id: %s\n" % e)

    elif intent_name == 'script.event.menu.previous':
        event_count, events, titles, ids = retrieve_found_events(output_contexts)
        if events is None:
            return chip_response(
                text='Ich habe leider keine Events gespeichert. '
                     'Hast du schon deinen Zugänglichkeitsbedarf angegeben?',
                chips=['Zugänglichkeit auswählen',
                       'Interessen angeben'])

        next_event_index = event_index = int(retrieve_event_index(output_contexts))
        display_num = 1
        if event_count == 1:
            return chip_w_context_response(session_id=session_id,
                                           context='event_index',
                                           variable_name='event_index',
                                           variable=next_event_index,
                                           text='Ich habe dir nun alle ausgewählten Veranstaltungen gezeigt. '
                                                'Was möchtest du nun tun?',
                                           chips=['Zeig mir die Veranstaltungen noch einmal',
                                                  'Zurück zum Hauptmenü'],
                                           dgs_videos_bot=make_video_array(['A19b']),
                                           dgs_videos_chips=make_video_array(['RC29b', 'AC7']))
        if event_index == 0:
            event_index = event_count - 2
            next_event_index = event_index + 1
        elif event_index == 1:
            event_index = event_count - 1
            next_event_index = event_index + 1
        else:
            event_index = event_index - 2
            next_event_index = event_index + 1

        if event_index == 0:
            chips = ['Zeig mir das nächste Event',
                     'Mehr zur Veranstaltung']
            dgs_videos_chips = make_video_array(['RC28', 'RC29'])
        else:
            chips = ['Zeig mir die letzte Empfehlung nochmal',
                     'Gib mir eine weitere Empfehlung',
                     'Mehr zur Veranstaltung']
            dgs_videos_chips = make_video_array(['RC27', 'RC28', 'RC29'])
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
            chips=chips,
            dgs_videos_chips=dgs_videos_chips
        )
    elif intent_name == 'script.event.details - location':
        event_id = retrieve_event_id(output_contexts)
        event_count, events, titles, ids = retrieve_found_events(output_contexts=output_contexts)
        location = address = 'Für die Veranstaltung ist leider kein Ort eingetragen.'
        if event_id and events:
            for e in range(event_count):
                if events[str(e)].get('id') == event_id:
                    location = events[str(e)].get('location')
                    address = events[str(e)].get('address')
                    title = events[str(e)].get('title')

        return chip_response(
            text=f'Hier ist der Veranstaltungsort von {title}: \r\n'
                 f'{location}\r\n'
                 f'Die Adresse lautet: {address}\r\n',
            chips=['Zurück zu den Einzelheiten zur Veranstaltung'],
            # dgs_videos_chips=make_video_array(['RC34c']),
            # dgs_videos_bot=make_video_array([f'{title}_Lang'])
        )


    elif intent_name == 'script.event.details - linkout':
        event_id = retrieve_event_id(output_contexts)
        url = 'https://www.sommerblut.de/ls/event/' + str(event_id)
        button_text = 'Link zum Event'
        return button_response(url=url, button_text=button_text, chips=['Zurück: Veranstaltungsdetails'])

    elif intent_name == 'script.event.details - program':
        event_id = retrieve_event_id(output_contexts)
        event_count, events, titles, ids = retrieve_found_events(output_contexts=output_contexts)
        program_content = 'Ich habe leider keine Programmbeschreibung gefunden'
        title = 'der Veranstaltung'
        if event_id and events:
            for e in range(event_count):
                if events[str(e)].get('id') == event_id:
                    program_content = events[str(e)].get('program_content')
                    title = events[str(e)].get('title')
        return chip_response(
            text=f'Hier ist der Programmtext von {title}: \r\n'
                 f'{program_content}',
            chips=['Zurück zu den Einzelheiten zur Veranstaltung'],
            dgs_videos_chips=make_video_array(['RC34c']),
            dgs_videos_bot=make_video_array([f'{title}_Lang']))

    elif intent_name == 'script.event.details - corona':
        event_id = retrieve_event_id(output_contexts)
        event_count, events, tittles, ids = retrieve_found_events(output_contexts=output_contexts)
        health_infection_notice = ' Ich konnte leider keine Infos zum Coronaschutz finden \r\n'
        title = 'der Veranstaltung'
        if event_id and events:
            for e in range(event_count):
                if events[str(e)].get('id') == event_id:
                    if events[str(e)].get('health_infection_notice') is not None:
                        health_infection_notice = events[str(e)].get('health_infection_notice')
                    title = events[str(e)].get('title')
        return chip_response(
            text=f'Diese Corona-Regeln gelten bei {title}: \r\n'
                 f'{health_infection_notice}\r\n'
                 f'Möchtest du weitere Informationen zur Veranstaltung?',
            chips=['Zurück zu den Einzelheiten zur Veranstaltung'],
            dgs_videos_chips=make_video_array(['RC34c']),
            dgs_videos_bot=make_video_array([f'{title}_Corona'])
        )

    elif intent_name == 'script.event.details - accessibility':
        event_id = retrieve_event_id(output_contexts)
        event_count, events, titles, ids = retrieve_found_events(output_contexts=output_contexts)
        accessible_other = 'Ich konnte leider keine Infos zur Barrierefreiheit finden\r\n'
        title = 'der Veranstaltung'
        if event_id and events:
            for e in range(event_count):
                if events[str(e)].get('id') == event_id:
                    if events[str(e)].get('accessible_other') is not None:
                        accessible_other = events[str(e)].get('accessible_other')
                    title = events[str(e)].get('title')
        return chip_response(
            text=f'Das sind die Barriere-Informationen bei {title}: \r\n'
                 f'{accessible_other}\r\n'
                 f'Möchtest du weitere Informationen zur Veranstaltung?',
            chips=['Zurück zu den Einzelheiten zur Veranstaltung',
                   'Ich brauche Unterstützung bei der Veranstaltung. Mit wem kann ich Kontakt aufnehmen?',
                   'Zu welchen Zeiten kann ich die Veranstaltung besuchen?'],
            dgs_videos_bot=make_video_array([f'{title}_Barri']),
            dgs_videos_chips=make_video_array(['RC34c', 'RC34d', 'RC36'])

        )

    elif intent_name == 'script.event.details - schedule':
        event_id = retrieve_event_id(output_contexts)
        event_count, events, titles, ids = retrieve_found_events(output_contexts=output_contexts)
        if event_id and events:
            for e in range(event_count):
                e_idx = str(e)
                text = ''
                if events[e_idx].get('id') == event_id:
                    duration = title = location = price = image = None
                    if events[e_idx].get('title'):
                        title = events[e_idx].get('title')
                        text += f'{title} \r\n \r\n'
                    if events[e_idx].get('duration'):
                        duration = int(events[e_idx].get('duration'))
                        text += f' Dauer: {duration} Minuten. \r\n '
                    if events[e_idx].get('location'):
                        location = events[e_idx].get('location')
                        text += f'Ort: {location}. \r\n'
                    if events[e_idx].get('address'):
                        address = events[e_idx].get('address')
                        text += f'Adresse: {address}. \r\n'
                    if events[e_idx].get('price_vvk'):
                        price = int(events[e_idx].get('price_vvk'))
                        text += f'Preis: {price} Euro. \r\n'
                    if events[e_idx].get('event_images'):
                        image = events[e_idx].get('event_images')

                    return event_detail_response(duration=duration,
                                                 title=title,
                                                 location=location,
                                                 price=price,
                                                 image=image,
                                                 text=text,
                                                 chips=['Zurück zu den Einzelheiten zur Veranstaltung',
                                                        'Hauptmenü',
                                                        'Zu welchen Zeiten kann ich die Veranstaltung besuchen?'],
                                                 # dgs_videos_bot=make_video_array(),
                                                 dgs_videos_chips=make_video_array(['RC34c', 'AC7', 'RC36'])
                                                 )
        else:
            return chip_response(
                text='Irgendwie habe ich wohl die Veranstaltungsnummer vergessen, versuch es doch noch einmal.',
                chips=['Zurück zur Übersicht der Veranstaltungen',
                       'Zurück zu den Einzelheiten zur Veranstaltung', 'Hauptmenü'],
                dgs_videos_chips=make_video_array(['AC7']),
            )

    elif intent_name == 'script.event.details.showSchedule':
        event_id = int(retrieve_event_id(output_contexts))
        play_count, plays = get_event_schedule(event_id)
        event_title = get_event_title(event_id)

        if play_count == 0:
            return chip_response(text=f'Titel der Veranstaltung: {event_title} \r\n'
                                      f'Die Veranstaltung ist bereits vorüber.',
                                 chips=['Zurück zu den Einzelheiten zur Veranstaltung',
                                        'Zurück zur Übersicht der Veranstaltungen'],
                                 dgs_videos_chips=make_video_array(['RC34c', 'RC34b'])
                                 )
        return event_schedule_response(play_count,
                                       plays,
                                       text=f'Titel der Veranstaltung: {event_title} \r\n',
                                       chips=['Ich möchte online ein Ticket kaufen',
                                              'Ich möchte ein Ticket am Telefon kaufen',
                                              'Ich möchte Tickets an der Theaterkasse kaufen',
                                              'Zurück zu den Einzelheiten zur Veranstaltung',
                                              'Zurück zur Übersicht der Veranstaltungen'],
                                       dgs_videos_chips=make_video_array(['RC37', 'RC38', 'RC39', 'RC34c', 'RC34b'])
                                       )

    elif intent_name == 'script.random_event':
        entries = 50
        page = 1
        event_count, events, titles, ids = get_full_event_list(page=page, entries=entries)
        if events:
            title = random.sample(titles, 1)
            event_title = title[0]

            idx = titles.index(event_title)
            event_id = ids[idx]
            return chip_w_three_context_response(session_id=session_id,
                                                 text=f'Ich habe dir die Veranstaltung {event_title} gefunden.\r\n'
                                                      'Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                      '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                      '2. Worum geht es genau in der Veranstaltung? \r\n'
                                                      '3. Wie handhabt ihr Corona?\r\n'
                                                      '4. Wo und Wann findet sie statt?\r\n',
                                                 chips=['Barrierefreiheit',
                                                        'Programmtext',
                                                        'Coronamaßnahmen',
                                                        'Datum und Ort',
                                                        'Zeig mir die Veranstaltung auf Sommerblut.de',
                                                        'Zurück: Ich habe eine Frage'],
                                                 variable_name='event_id',
                                                 variable_name_2='events_found',
                                                 variable=event_id,
                                                 variable_2=events,
                                                 context='event_id',
                                                 context_2='events_found',
                                                 context_3='scripteventdetails-followup',
                                                 dgs_videos_bot=make_video_array(['AC20']),
                                                 dgs_videos_chips=make_video_array(
                                                     ['RC30', 'RC31', 'RC32', 'RC33', 'RC34'])
                                                 )
        else:
            return chip_response(text='FEHLER! ich habe keine Events gefunden',
                                 chips=['Zurück zum Hauptmenü',
                                        'Ich habe eine Frage',
                                        'Team von Ällei kontaktieren'],
                                 dgs_videos_chips=make_video_array(['F2']),
                                 # dgs_videos_bot=make_video_array(['A23']),
                                 )

    elif intent_name == 'faq.event':
        entries = 50
        page = 1
        event_count, events, titles, ids = get_full_event_list(page=page, entries=entries)

        # obsolete, only necessary for chunked and not cached responses
        while entries * page < event_count:
            _, events_cache, _, ids_cache = retrieve_found_events(output_contexts=output_contexts)
            if events_cache is not None:
                event_list = list(events.values())
                event_list.extend(list(events_cache.values()))
                # rename keys
                events = dict(zip(list(range(len(event_list))), event_list))

            page += 1
            return chip_w_two_context_response(text='Das sind viele Veranstaltungen. \r\n'
                                                    'Ich muss nochmal suchen.',
                                               chips=['Finde mehr Veranstaltungen'],
                                               session_id=session_id,
                                               context='events_found',
                                               variable_name='events_found',
                                               variable=events,
                                               lifespan=3,
                                               context_2='page_cache',
                                               variable_name_2='page_cache',
                                               variable_2=page
                                               )

        # get final list of events
        # event_count, events, titles, ids = retrieve_found_events(output_contexts=output_contexts)

        if events:
            event_title = parameters.get('event_title')
            if event_title == '':
                chips = random.sample(titles, 5)
                chips.append('Mehr Veranstaltungen vorschlagen')
                return chip_response(text='Du kannst den Namen der Veranstaltung in das Textfeld unten eingeben. '
                                          'Oder eine von unten wählen:',
                                     chips=chips,
                                     dgs_videos_chips=make_video_array(['F2']),
                                     # dgs_videos_bot=make_video_array(['A23']),
                                     )
            else:
                idx = titles.index(event_title)
                event_id = ids[idx]
                return chip_w_two_context_response(session_id=session_id,
                                                   text='Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                        '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                        '2. Worum geht es genau in der Veranstaltung? \r\n'
                                                        '3. Wie handhabt ihr Corona?\r\n'
                                                        '4. Wo und Wann findet sie statt?\r\n',
                                                   chips=['Barrierefreiheit',
                                                          'Programmtext',
                                                          'Coronamaßnahmen',
                                                          'Datum und Ort',
                                                          'Zeig mir die Veranstaltung auf Sommerblut.de',
                                                          'Zurück: Ich habe eine Frage'],
                                                   variable_name='event_id',
                                                   variable_name_2='events_found',
                                                   variable=event_id,
                                                   variable_2=events,
                                                   context='event_id',
                                                   context_2='events_found',
                                                   dgs_videos_bot=make_video_array(['AC20']),
                                                   dgs_videos_chips=make_video_array(
                                                       ['RC30', 'RC31', 'RC32', 'RC33', 'RC34'])
                                                   )

    elif intent_name == 'script.tickets.sale':
        return button_response(url='https://t.rausgegangen.de/tickets/shop/sommerblut-2022',
                               button_text='Rausgegangen Ticketshop',
                               text='Hier geht es zum Ticketshop von Sommerblut.',
                               chips=['Zeig mir die Veranstaltung auf Sommerblut.de',
                                      'Zurück zu den Einzelheiten zur Veranstaltung'])

    elif intent_name == 'fallback.default':
        return chip_response(text='Vielleicht habe ich Dich nicht richtig verstanden.\r\n'
                                  'Kannst du das noch einmal anders sagen?',
                             chips=['Zurück zum Hauptmenü',
                                    'Ich habe eine Frage',
                                    'Team von Ällei kontaktieren'],
                             dgs_videos_bot=make_video_array(['E2']),
                             dgs_videos_chips=make_video_array(['AC7', 'RC3', 'Feedback1']),
                             )
    elif 'smalltalk' in intent_name:
        return give_smalltalk(intent_name)

    elif 'faq' in intent_name:
        return give_faq(intent_name)

    elif 'feedback' in intent_name:
        return give_feedback(intent_name)

    elif 'glossary' in intent_name:
        return give_glossary(intent_name, parameters, output_contexts)

    elif 'team.sommerblut' in intent_name:
        return give_team(intent_name, parameters, output_contexts)

    elif intent_name == 'script.welcome':
        return chip_response(
            text='Hi! \r\n'
                 'Mein Name ist Ällei! \r\n'
                 'Schön, dass du hier bist. \r\n'
                 'Suchst Du nach Informationen über das Sommerblut Festival? \r\n'
                 'Ich kann Dir helfen. \r\n'
                 'Bist du das erste mal hier? \r\n'
                 'Dann schau dir gern das Einführungs-Video an.\r\n',
            chips=['Einführungsvideo', 'Einführungsvideo in leichter Sprache', 'Kenne ich schon: Hauptmenü',
                   'Ich habe eine Frage'],
            dgs_videos_bot=make_video_array(['A1']),
            dgs_videos_chips=make_video_array(['RC1a', 'RC1b', 'RC2', 'RC3']))

    elif intent_name == 'script.bot.introvideo':
        ls_video = parameters.get('ls_video')
        if ls_video == 'JA':
            return chip_response(
                text='Video: Wie funktioniert der Chatbot und was kann er alles:',
                chips=['Weiter zum Hauptmenü'],
                # dgs_videos_bot=None,
                dgs_videos_chips=make_video_array(['RC4', 'AC7']),
                content_videos=make_video_array(['Intro_Video_LS']))

        return chip_response(
            text='Video: Wie funktioniert der Chatbot und was kann er alles:',
            chips=['Weiter zum Hauptmenü'],
            # dgs_videos_bot=None,
            dgs_videos_chips=make_video_array(['RC4', 'AC7']),
            content_videos=make_video_array(['Intro_Video']))

    elif intent_name == 'script.main_menu':

        _, events, titles, ids = get_full_event_list(page=1, entries=50)

        return chip_w_context_response(
            text='Okay, worauf hast du jetzt Lust?\r\n'
                 'Ich kann dir zum Beispiel noch mehr über mich erzählen.\r\n'
            # 'Und über künstliche Intelligenz.\r\n'
                 'Oder ich berate dich, welche Veranstaltung dir gefallen wird.\r\n',
            chips=[  # 'Video: Ällei und KI',
                # 'Video: Ällei und KI in Leichter Sprache',
                'Ich habe eine Frage'
                'Veranstaltungsberatung',
                'Mehr über Sommerblut erfahren',
                'Mehr über Ällei erfahren',
                'Kontaktmöglichkeiten zum Sommerblut-Team'],
            context='events_found',
            variable_name='events_found',
            variable=events,
            lifespan=50,
            session_id=session_id,
            dgs_videos_bot=make_video_array(['A2']),
            dgs_videos_chips=make_video_array(['RC3', 'RC6', 'RC7', 'E1', 'E1']))
   
    elif intent_name == 'script.about_bot':

        _, events, titles, ids = get_full_event_list(page=1, entries=50)

        return chip_w_context_response(
            text='Sehr gerne. \r\n' 
                 'Ich habe einen eigenen Blog, in dem ihr viel über mich lesen könnt!\r\n'
            chips=['Blog in einem neuen Fenster öffnen'
                'Erzähl mir einen Witz',
                'Team von Ällei kontaktieren',
                'Mehr über das Sommerblut erfahren'],
            context='events_found',
            variable_name='events_found',
            variable=events,
            lifespan=50,
            session_id=session_id,
            dgs_videos_bot=make_video_array(['A2']),
            dgs_videos_chips=make_video_array(['E1', 'E1', 'Feedback1', 'RC7']))
    
    elif intent_name == 'script.about_bot - linkout':
        url = 'https://www.sommerblut.de/de/logbuch1'
        button_text = 'Link zum Blog von Ällei'
        return button_response(url=url, button_text=button_text, chips=['Zurück: Hauptmenü'])

    elif intent_name == 'script.bot_theme_input':
        ls_video = parameters.get('ls_video')
        if ls_video == 'JA':
            return chip_response(text='Hier wird ein Video gezeigt:\r\n'
                                      ' "Barrierefreiheit im digitalen Raum"\r\n'
                                      'Dieses Video ist leider noch nicht verfügbar.',
                                 chips=['Mehr über Sommerblut erfahren',
                                        'Ich habe eine Frage',
                                        'Veranstaltungsberatung'],
                                 dgs_videos_bot=make_video_array(['E1']),
                                 # content_videos=make_video_array(['E1']),
                                 dgs_videos_chips=make_video_array(['RC7', 'RC3', 'RC6'])
                                 )

        return chip_response(
            text='Hier wird ein Video gezeigt:\r\n '
                 '"Barrierefreiheit im digitalen Raum"\r\n'
                 'Dieses Video ist leider noch nicht verfügbar.',
            chips=['Mehr über Sommerblut erfahren',
                   'Ich habe eine Frage',
                   'Veranstaltungsberatung'],
            # dgs_videos_bot=make_video_array(['A2']),
            content_videos=make_video_array(['E1']),
            dgs_videos_chips=make_video_array(['RC7', 'RC3', 'RC6'])
        )

    elif intent_name == 'script.play_sb_video':
        return chip_response(
            text='Video: Was ist Sommerblut?',
            chips=['Weiter zur Themenvorstellung'],
            content_videos=make_video_array(['SB_Intro']),
            dgs_videos_chips=make_video_array(['AC6'])
        )

    elif intent_name == 'script.sb_theme.play_video':
        return chip_response(
            text='Hier ist ein Video zum Thema "Mach mal neu". ',
            chips=['Weiter zum Bedarfsfilter'],
            content_videos=make_video_array(['SB_Theme']),
            dgs_videos_chips=make_video_array(['RC13'])
        )

    elif intent_name == 'script.sb_intro':
        return chip_response(
            text='Das Sommerblut gibt es nun schon seit mehr als 20 Jahren. Hier ist ein Video. '
                 'Es erzählt dir mehr über das Festival.',
            chips=['Video anschauen: Was ist Sommerblut',
                   'Vorstellung überspringen'],
            dgs_videos_bot=make_video_array(['A3a']),
            dgs_videos_chips=make_video_array(['RC8', 'AC6'])
        )

    elif intent_name == 'script.sb_theme_intro':
        return chip_response(
            text='Alles klar.\r\n '
                 'Beim Sommerblut gibt es ganz unterschiedliche Veranstaltungen.\r\n'
                 'Dieses Jahr ist unser Motto "Mach mal neu".\r\n'
                 'Soll ich dir dazu mehr erzählen?',
            chips=['Video: Mehr zum Thema "Mach mal Neu"',
                   'Nein, weiter zur Veranstaltungsberatung'],
            dgs_videos_bot=make_video_array(['A4']),
            dgs_videos_chips=make_video_array(['RC11', 'RC12'])
        )

    elif intent_name == 'script.next_event':
        entries = 50
        page = 1
        _, events, _, _ = get_full_event_list(page=page, entries=entries)
        if events:
            event_title, event_id, next_date = get_next_event()
            if next_date:
                return chip_w_three_context_response(session_id=session_id,
                                                     text=f'Als nächstes findet {event_title} statt.\r\n'
                                                          f'Beginn ist {next_date}.\r\n'
                                                          'Was möchtest du mehr wissen über die Veranstaltung?\r\n'
                                                          '1. Ist die Veranstaltung barrierefrei?\r\n'
                                                          '2. Worum geht es genau in der Veranstaltung? \r\n'
                                                          '3. Wie handhabt ihr Corona?\r\n'
                                                          '4. Wo und Wann findet sie statt?\r\n',
                                                     chips=['Barrierefreiheit',
                                                            'Programmtext',
                                                            'Coronamaßnahmen',
                                                            'Datum und Ort',
                                                            'Zeig mir die Veranstaltung auf Sommerblut.de',
                                                            'Zurück: Ich habe eine Frage'],
                                                     variable_name='event_id',
                                                     variable_name_2='events_found',
                                                     variable=event_id,
                                                     variable_2=events,
                                                     context='event_id',
                                                     context_2='events_found',
                                                     context_3='scripteventdetails-followup',
                                                     dgs_videos_bot=make_video_array(['AC20']),
                                                     dgs_videos_chips=make_video_array(
                                                         ['RC30', 'RC31', 'RC32', 'RC33', 'RC34'])
                                                     )
        else:
            return chip_response(text='FEHLER! ich habe keine Events gefunden',
                                 chips=['Zurück zum Hauptmenü',
                                        'Ich habe eine Frage',
                                        'Team von Ällei kontaktieren'],
                                 dgs_videos_chips=make_video_array(['F2']),
                                 # dgs_videos_bot=make_video_array(['A23']),
                                 )
