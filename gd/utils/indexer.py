class Index:
	#All indexes for gd levels
	LEVEL_ID = '1'
	LEVEL_NAME = '2'
	LEVEL_DESCRIPTION = '3'
	LEVEL_DATA = '4'
	LEVEL_VERSION = '5'
	LEVEL_CREATOR_ID = '6'
	LEVEL_DIFFICULTY = '9'
	LEVEL_DOWNLOADS = '10'
	LEVEL_AUDIO_TRACK = '12'
	LEVEL_GAME_VERSION = '13'
	LEVEL_LIKES = '14'
	LEVEL_LENGTH = '15'
	LEVEL_IS_DEMON = '17'
	LEVEL_STARS = '18'
	LEVEL_FEATURED_SCORE = '19'
	LEVEL_IS_AUTO = '25'
	LEVEL_PASS = '27'
	LEVEL_UPLOADED_TIMESTAMP = '28'
	LEVEL_LAST_UPDATED_TIMESTAMP = '29'
	LEVEL_ORIGINAL = '30'
	LEVEL_SONG_ID = '35'
	LEVEL_COIN_COUNT = '37'
	LEVEL_COIN_VERIFIED = '38'
	LEVEL_REQUESTED_STARS = '39'
	LEVEL_IS_EPIC = '42'
	LEVEL_DEMON_DIFFICULTY = '43'
	LEVEL_OBJECT_COUNT = '45'
    #all indexes for songs
	SONG_ID = '1'
	SONG_TITLE = '2'
	SONG_AUTHOR = '4'
	SONG_SIZE = '5'
	SONG_URL = '10'
    #all indexes for users
	USER_NAME = '1'
	USER_PLAYER_ID = '2'
	USER_STARS = '3'
	USER_DEMONS = '4'
	USER_CREATOR_POINTS = '8'
	USER_ICON = '9'
	USER_COLOR_1 = '10'
	USER_COLOR_2 = '11'
	USER_SECRET_COINS = '13'
	USER_ICON_TYPE = '14'
	USER_GLOW_OUTLINE = '15'
	USER_ACCOUNT_ID = '16'
	USER_USER_COINS = '17'
	USER_PRIVATE_MESSAGE_POLICY = '18'
	USER_FRIEND_REQUEST_POLICY = '19'
	USER_YOUTUBE = '20'
	USER_ICON_CUBE = '21'
	USER_ICON_SHIP = '22'
	USER_ICON_BALL = '23'
	USER_ICON_UFO = '24'
	USER_ICON_WAVE = '25'
	USER_ICON_ROBOT = '26'
	USER_GLOW_OUTLINE_2 = '28'
	USER_GLOBAL_RANK = '30'
	USER_ICON_SPIDER = '43'
	USER_TWITTER = '44'
	USER_TWITCH = '45'
	USER_DIAMONDS = '46'
	USER_DEATH_EFFECT = '47'
	USER_ROLE = '49'
	USER_COMMENT_HISTORY_POLICY = '50'
	#all indexes for messages
	MESSAGE_ID = '1'
	MESSAGE_SENDER_ACCOUNT_ID = '2'
	MESSAGE_SENDER_ID = '3'
	MESSAGE_SUBJECT = '4'
	MESSAGE_BODY = '5'
	MESSAGE_SENDER_NAME = '6'
	MESSAGE_TIMESTAMP = '7'
	MESSAGE_IS_READ = '8'
	MESSAGE_INDICATOR = '9' #like, when it's "1" - the message is sent TO MESSAGE_SENDER (if that makes sense)
	#all indexes for comments
	COMMENT_LEVEL_ID = '1'
	COMMENT_BODY = '2'
	COMMENT_RATING = '4'
	COMMENT_ID = '6'
	COMMENT_TIMESTAMP = '9'
	COMMENT_LEVEL_PERCENTAGE = '10'
	COMMENT_TYPE = 'TYPE'
	#all indexes for friend requests (at least all I need lol)
	REQUEST_SENDER_NAME = '1'
	REQUEST_SENDER_ID = '2'
	REQUEST_SENDER_ACCOUNT_ID = '16'
	REQUEST_ID = '32'
	REQUEST_BODY = '35'
	REQUEST_TIMESTAMP = '37'
	REQUEST_STATUS = '41'
	REQUEST_INDICATOR = 'TYPE'