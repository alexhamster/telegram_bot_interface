import pytest
from collections import namedtuple

@pytest.fixture(scope='module')
def get_message():
    message = {'content_type': 'text', 'message_id': 1002, 'from_user': {'id': 193586211, 'is_bot': False, 'first_name':
        'Александр', 'username': 'superuser', 'last_name': None, 'language_code': 'ru'}, 'date': 1591014702,
               'chat': {'type':
                            'private', 'last_name': None, 'first_name': 'Александр', 'username': 'superuser',
                        'id': 193586211, 'title': None,
                        'all_members_are_administrators': None, 'photo': None, 'description': None, 'invite_link': None,
                        'pinned_message':
                            None, 'sticker_set_name': None, 'can_set_sticker_set': None}, 'forward_from': None,
               'forward_from_chat': None,
               'forward_from_message_id': None, 'forward_signature': None, 'forward_date': None,
               'reply_to_message': None,
               'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': '/start some 123',
               'entities': [],
               'caption_entities': None, 'audio': None, 'document': None,
               'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None,
               'contact': None,
               'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None,
               'new_chat_members': None,
               'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None,
               'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None,
               'migrate_to_chat_id':
                   None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None,
               'successful_payment': None,
               'connected_website': None,
               'json': {'message_id': 1002, 'from': {'id': 193586211, 'is_bot': False, 'first_name':
                   'Александр', 'username': 'superuser', 'language_code': 'ru'},
                        'chat': {'id': 193586211, 'first_name': 'Александр',
                                 'username': 'superuser', 'type': 'private'}, 'date': 1591014702,
                        'text': '/start some 123',
                        'entities': [{'offset': 0,
                                      'length': 6, 'type': 'bot_command'}]}}

    return message

