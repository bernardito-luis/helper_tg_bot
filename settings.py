import json


BOT_KEY = ''
PROXY = {}

# MENTION_IT = ""
# MENTION_MANAGERS = ""
# MENTION_ALL = ""
# with open('usernames.json', encoding='utf8') as f:
#     mentions = json.load(f)
#     mention_string = list()
#     mention_string.append(' '.join(['@{}'.format(u) for u in mentions['it']['usernames']]))
#     for first_name, user_id in mentions['it']['without_usernames'].items():
#         mention_string.append('<a href="tg://user?id={}">{}</a>'.format(user_id, first_name))
#     MENTION_IT = ' '.join(mention_string)
#     mention_string = list()
#     mention_string.append(' '.join(['@{}'.format(u) for u in mentions['managers']['usernames']]))
#     for first_name, user_id in mentions['managers']['without_usernames'].items():
#         mention_string.append('<a href="tg://user?id={}">{}</a>'.format(user_id, first_name))
#     MENTION_MANAGERS = ' '.join(mention_string)
#     MENTION_ALL = '{} {}'.format(MENTION_IT, MENTION_MANAGERS)

try:
    from local_settings import *
except ImportError:
    pass
