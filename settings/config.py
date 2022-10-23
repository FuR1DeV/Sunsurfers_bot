import os
from dotenv import load_dotenv
from emoji import emojize

load_dotenv()

VERSION = '0.0.1'
AUTHOR = 'Vasiliy Turtugeshev'

HOST = os.getenv('HOST')
POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
DATABASE = os.getenv('DATABASE')

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = str(os.getenv('ADMIN_ID')).split(',')

KEYBOARD = {
    'DASH': emojize(':minus:'),
    'OM': emojize(':om:'),
    'FOLDED_HANDS': emojize(':folded_hands:'),
    'NAZAR_AMULET': emojize(':nazar_amulet:'),
    'YIN_YANG': emojize(':yin_yang:'),
    'SMILING_FACE_WITH_SUNGLASSES': emojize(':smiling_face_with_sunglasses:'),
    'WAVING_HAND': emojize(':waving_hand:'),
    'SUNRISE': emojize(':sunrise:'),
    'BUST_IN_SILHOUETTE': emojize(':bust_in_silhouette:'),
    'HAMMER_AND_PICK': emojize(':hammer_and_pick:'),
    'SOS_BUTTON': emojize(':SOS_button:'),
    'MONEY_BAG': emojize(':money_bag:'),
    'OUTBOX_TRAY': emojize(':outbox_tray:'),
    'INBOX_TRAY': emojize(':inbox_tray:'),
    'ON!_ARROW': emojize(':ON!_arrow:'),
    'EX_QUEST_MARK': emojize(':exclamation_question_mark:'),
    'PENCIL': emojize(':pencil:'),
    'DOLLAR': emojize(':dollar_banknote:'),
    'ID_BUTTON': emojize(':ID_button:'),
    'CLIPBOARD': emojize(':clipboard:'),
    'INFORMATION': emojize(':information:'),
    'WRENCH': emojize(':wrench:'),
    'BAR_CHART': emojize(':bar_chart:'),
    'DOWNWARDS_BUTTON': emojize(':downwards_button:'),
    'UPWARDS_BUTTON': emojize(':upwards_button:'),
    'CROSS_MARK': emojize(':cross_mark:'),
    'CHECK_MARK_BUTTON': emojize(':check_mark_button:'),
    'TELEPHONE': emojize(':telephone_receiver:'),
    'GREEN_CIRCLE': emojize(':green_circle:'),
    'RED_CIRCLE': emojize(':red_circle:'),
    'BLUE_CIRCLE': emojize(':blue_circle:'),
    'WHITE_CIRCLE': emojize(':white_circle:'),
    'A_BUTTON': emojize(':A_button_(blood_type):'),
    'B_BUTTON': emojize(':B_button_(blood_type):'),
    'INPUT_LATIN_LETTERS': emojize(':input_latin_letters:'),
    'WORLD_MAP': emojize(':world_map:'),
    'SUN': emojize(':sun:'),
    'RIGHT_ARROW': emojize(':right_arrow:'),
    'LEFT_ARROW': emojize(':left_arrow:'),
    'UP!_BUTTON': emojize(':UP!_button:'),
    'MINUS': emojize(':minus:'),
    'RIGHT_ARROW_CURVING_LEFT': emojize(':right_arrow_curving_left:'),
}

COUNTRIES = {
    'Thailand': emojize(':Thailand:'),
    'India': emojize(':India:'),
    'Vietnam': emojize(':Vietnam:'),
    'Philippines': emojize(':Philippines:'),
    'Georgia': emojize(':Georgia:'),
    'Indonesia': emojize(':Indonesia:'),
    'Nepal': emojize(':Nepal:'),
    'Morocco': emojize(':Morocco:'),
    'Turkey': emojize(':Turkey:'),
    'Mexico': emojize(':Mexico:'),
    'SriLanka': emojize(':Sri_Lanka:'),
    'Albania': emojize(':Albania:'),
}
