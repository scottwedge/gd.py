from .utils.indexer import Index as i
from .song import Song
from .user import User
from .comment import Comment
from .authclient import AuthClient
from .abstractuser import AbstractUser
from .level import Level
from .message import Message
from .iconset import IconSet
from .friend_request import FriendRequest
from .utils.converter import Converter
from .utils.crypto.coders import Coder
from .utils.mapper import mapper_util
from .utils.types import MessagePrivacyType, FriendRequestPrivacyType, CommentPrivacyType, StatusLevelType
import base64 as b64

class class_converter:

    def SongConvert(to_parse):
        s = to_parse #I feel more confident with shorter variables
        dl_link = (s[i.SONG_URL]).replace('%3A', ':').replace('%2F', '/')
        return Song(
            name = s[i.SONG_TITLE],
            author = s[i.SONG_AUTHOR],
            _id = int(s[i.SONG_ID]),
            size = float(s[i.SONG_SIZE]),
            size_mb = f'{s[i.SONG_SIZE]} MB',
            links = [
                f'https://www.newgrounds.com/audio/listen/{s[i.SONG_ID]}',
                dl_link
            ]
        )
        
    def UserConvert(to_parse):
        s = to_parse #as I said, shorter variables are more comfortable
        pm_policy = s[i.USER_PRIVATE_MESSAGE_POLICY]
        dm = MessagePrivacyType(int(pm_policy))
        friend_req_policy = s[i.USER_FRIEND_REQUEST_POLICY]
        fr_rq = FriendRequestPrivacyType(int(friend_req_policy))
        youtube = s[i.USER_YOUTUBE]
        if youtube == '':
            yt = None
        if youtube != '':
            yt = f'https://www.youtube.com/channel/{youtube}'
        r = s[i.USER_ROLE]
        stat = StatusLevelType(int(r))
        rnk = s[i.USER_GLOBAL_RANK]
        if rnk == '': #check if it works like that
            rank = None
        if rnk != '':
            rank = int(rnk)
        twitter = s[i.USER_TWITTER]
        if twitter == '':
            twt = None
            twt_link = None
        if twitter != '':
            twt = '@' + twitter
            twt_link = f'https://twitter.com/{twt}'
        twitch = s[i.USER_TWITCH]
        if twitch == '':
            twch = None
            twch_link = None
        if twitch != '':
            twch = twitch
            twch_link = f'https://twitch.tv/{twch}'
        comment_policy = s[i.USER_COMMENT_HISTORY_POLICY]
        comment = CommentPrivacyType(int(comment_policy))
        #redo a bit (for easier interaction, and not all elements are yet implemented)
        return User(
            name = s[i.USER_NAME], id = int(s[i.USER_PLAYER_ID]),
            stars = int(s[i.USER_STARS]), demons = int(s[i.USER_DEMONS]),
            secret_coins = int(s[i.USER_SECRET_COINS]), user_coins = int(s[i.USER_USER_COINS]),
            cp = int(s[i.USER_CREATOR_POINTS]), diamonds = int(s[i.USER_DIAMONDS]),
            role = stat, global_rank = rank,
            account_id = int(s[i.USER_ACCOUNT_ID]), youtube = yt, 
            twitter = [twt, twt_link], twitch = [twch, twch_link],
            messages = dm, friend_requests = fr_rq, comments = comment,
            icon_setup = IconSet(
                main_icon = int(s[i.USER_ICON]),
                color_1 = int(s[i.USER_COLOR_1]),
                color_2 = int(s[i.USER_COLOR_2]),
                main_icon_type = int(s[i.USER_ICON_TYPE]),
                has_glow_outline = bool(int(s[i.USER_GLOW_OUTLINE])^1),
                icon_cube = int(s[i.USER_ICON_CUBE]),
                icon_ship = int(s[i.USER_ICON_SHIP]),
                icon_ball = int(s[i.USER_ICON_BALL]),
                icon_ufo = int(s[i.USER_ICON_UFO]),
                icon_wave = int(s[i.USER_ICON_WAVE]),
                icon_robot = int(s[i.USER_ICON_ROBOT]), 
                icon_spider = int(s[i.USER_ICON_SPIDER])
            )
        )
    
    def LevelConvert(to_parse):
        s = to_parse
        pass #I'll finish soon
    
    def MessageConvert(to_parse, to_parse_2, auth_client):
        s = to_parse
        cases = {0: 'normal', 1: 'sent'}
        type_of = cases.get(int(s[i.MESSAGE_INDICATOR]))
        useful_dict = {
            'name': s[i.MESSAGE_SENDER_NAME],
            'id': int(s[i.MESSAGE_SENDER_ID]),
            'account_id': int(s[i.MESSAGE_SENDER_ACCOUNT_ID])
        }
        user_1, user_2 = [class_converter.AbstractUserConvert(elem) for elem in [useful_dict, to_parse_2]]
        return Message(
            id = int(s[i.MESSAGE_ID]),
            timestamp = s[i.MESSAGE_TIMESTAMP],
            subject = b64.b64decode(mapper_util.normalize(s[i.MESSAGE_SUBJECT])).decode(),
            is_read = True if (s[i.MESSAGE_IS_READ] is '1') else False,
            author = user_1 if (type_of is 'normal') else user_2,
            recipient = user_2 if (type_of is 'normal') else user_1,
            type = type_of,
            retrieved_from = auth_client
        )

    def RequestConvert(to_parse, to_parse_2, auth_client):
        s = to_parse
        cases = {0: 'normal', 1: 'sent'}
        type_of = cases.get(int(s[i.REQUEST_INDICATOR]))
        useful_dict = {
            'name': s[i.REQUEST_SENDER_NAME],
            'id': int(s[i.REQUEST_SENDER_ID]),
            'account_id': int(s[i.REQUEST_SENDER_ACCOUNT_ID])
        }
        user_1, user_2 = [class_converter.AbstractUserConvert(elem) for elem in [useful_dict, to_parse_2]]
        return FriendRequest(
            id = int(s[i.REQUEST_ID]),
            timestamp = s[i.REQUEST_TIMESTAMP],
            body = b64.b64decode(mapper_util.normalize(s[i.REQUEST_BODY])).decode(),
            is_read = False if (s[i.REQUEST_STATUS] is '1') else True,
            author = user_1 if (type_of is 'normal') else user_2,
            recipient = user_2 if (type_of is 'normal') else user_1,
            type = type_of,
            retrieved_from = auth_client
        )

    def AuthClientConvert(to_parse):
        s = to_parse
        return AuthClient(
            name = s['username'],
            password = s['password'],
            encodedpass = Coder().encode0(type='accountpass', string=s['password']),
            accountid = int(s['accountid']),
            id = int(s['userid'])
        )
    
    def CommentConvert(to_parse, ret_from, to_parse_2):
        s = to_parse
        return Comment(
            body = b64.b64decode(mapper_util.normalize(s[i.COMMENT_BODY])).decode(),
            rating = int(s[i.COMMENT_RATING]),
            timestamp = s[i.COMMENT_TIMESTAMP],
            id = int(s[i.COMMENT_ID]),
            type = int(s[i.COMMENT_TYPE]),
            level_id = int(s.get(i.COMMENT_LEVEL_ID, 0)),
            level_percentage = int(s.get(i.COMMENT_LEVEL_PERCENTAGE, -1)),
            author = class_converter.AbstractUserConvert(to_parse_2),
            retrieved_from = ret_from #!
        )
    
    def AbstractUserConvert(to_parse):
        s = to_parse
        return AbstractUser(
            name = s['name'], id = s['id'], account_id = s['account_id']
        )

#woop >.>