from gd.logging import get_logger
from gd.typing import Client, Comment, Level, LevelRecord, List, Optional, Tuple, Type, Union

from gd.abstractentity import AbstractEntity
from gd.abstractuser import AbstractUser
from gd.song import Song

from gd.errors import MissingAccess, NothingFound

from gd.api.editor import Editor

from gd.utils.converter import Converter
from gd.utils.enums import (
    DemonDifficulty,
    LevelDifficulty,
    CommentStrategy,
    LevelLength,
    TimelyType,
    LevelLeaderboardStrategy,
)
from gd.utils.indexer import Index
from gd.utils.parser import ExtDict
from gd.utils.text_tools import make_repr, object_split
from gd.utils.crypto.coders import Coder

log = get_logger(__name__)


def excluding(*args: Tuple[Type[BaseException]]) -> Tuple[Type[BaseException]]:
    return args


DEFAULT_EXCLUDE: Tuple[Type[BaseException]] = excluding(NothingFound)


class Level(AbstractEntity):
    """Class that represents a Geometry Dash Level.
    This class is derived from :class:`.AbstractEntity`.
    """

    def __repr__(self) -> str:
        info = {
            "id": self.id,
            "name": repr(self.name),
            "creator": self.creator,
            "version": self.version,
            "difficulty": self.difficulty,
        }
        return make_repr(self, info)

    def __str__(self) -> str:
        return str(self.name)

    @classmethod
    def official(cls, level_id: int, client: Optional[Client] = None) -> None:
        mapping = {
            # ID: (name, stars, difficulty, coins, length)
            1: ("Stereo Madness", 1, "easy", 3, 3),
            2: ("Back On Track", 2, "easy", 3, 3),
            3: ("Polargeist", 3, "normal", 3, 3),
            4: ("Dry Out", 4, "normal", 3, 3),
            5: ("Base After Base", 5, "hard", 3, 3),
            6: ("Cant Let Go", 6, "hard", 3, 3),
            7: ("Jumper", 7, "harder", 3, 3),
            8: ("Time Machine", 8, "harder", 3, 3),
            9: ("Cycles", 9, "harder", 3, 3),
            10: ("xStep", 10, "insane", 3, 3),
            11: ("Clutterfunk", 11, "insane", 3, 3),
            12: ("Theory of Everything", 12, "insane", 3, 3),
            13: ("Electroman Adventures", 10, "insane", 3, 3),
            14: ("Clubstep", 14, "easy_demon", 3, 3),
            15: ("Electrodynamix", 12, "insane", 3, 3),
            16: ("Hexagon Force", 12, "insane", 3, 3),
            17: ("Blast Processing", 10, "harder", 3, 3),
            18: ("Theory of Everything 2", 14, "easy_demon", 3, 3),
            19: ("Geometrical Dominator", 10, "harder", 3, 3),
            20: ("Deadlocked", 15, "easy_demon", 3, 3),
            21: ("Fingerdash", 12, "insane", 3, 3),
            1001: ("The Seven Seas", 1, "easy", 3, 3),
            1002: ("Viking Arena", 2, "normal", 3, 3),
            1003: ("Airborne Robots", 3, "hard", 3, 3),
            2001: ("Payload", 2, "easy", 0, 1),
            2002: ("Beast Mode", 3, "normal", 0, 2),
            2003: ("Machina", 3, "normal", 0, 2),
            2004: ("Years", 3, "normal", 0, 2),
            2005: ("Frontlines", 3, "normal", 0, 2),
            2006: ("Space Pirates", 3, "normal", 0, 2),
            2007: ("Striker", 3, "normal", 0, 2),
            2008: ("Embers", 3, "normal", 0, 1),
            2009: ("Round 1", 3, "normal", 0, 2),
            2010: ("Monster Dance Off", 3, "normal", 0, 2),
            3001: ("The Challenge", 3, "hard", 0, 1),  # well...
            4001: ("Press Start", 4, "normal", 3, 3),
            4002: ("Nock Em", 6, "hard", 3, 3),
            4003: ("Power Trip", 8, "harder", 3, 3),
        }
        translate = {
            1001: 22,
            1002: 23,
            1003: 24,
            3001: 25,
            2001: 26,
            2002: 27,
            2003: 28,
            2004: 29,
            2005: 30,
            2006: 31,
            2007: 32,
            2008: 33,
            2009: 34,
            2010: 35,
            4001: 36,
            4002: 37,
            4003: 38,
        }

        if level_id not in mapping:
            raise ValueError(f"Level ID [{level_id}] is not known to be official.")

        song_id, (name, stars, str_diff, coins, length) = (
            translate.get(level_id, level_id),
            mapping[level_id],
        )

        creator, song = (
            AbstractUser(client=client),
            Song.official(song_id, server_style=False, client=client),
        )
        is_demon = "demon" in str_diff

        if is_demon:
            difficulty = DemonDifficulty.from_value(str_diff)
        else:
            difficulty = LevelDifficulty.from_value(str_diff)

        return cls(
            id=level_id,
            name=name,
            description=f"Official Level: {name}",
            version=1,
            creator=creator,
            song=song,
            data="",  # XXX: maybe we can dump all official levels and load their data
            password=None,
            copyable=False,
            is_demon=is_demon,
            is_auto=(str_diff == "auto"),
            difficulty=difficulty,
            stars=stars,
            coins=coins,
            verified_coins=True,
            is_epic=False,  # XXX: are Rob's levels epic? ~ nekit
            original=True,  # would be fun if this was false haha
            low_detail_mode=False,
            downloads=0,
            rating=0,
            score=1,
            uploaded_timestamp="unknown",
            last_updated_timestamp="unknown",
            length=length,
            game_version=21,
            stars_requested=0,
            object_count=0,
            type=0,
            time_n=-1,
            cooldown=-1,
            client=client,
        )

    @classmethod
    def from_data(
        cls,
        data: ExtDict,
        creator: Union[ExtDict, AbstractUser],
        song: Union[ExtDict, Song],
        client: Client,
    ) -> Level:
        if isinstance(creator, ExtDict):
            creator = AbstractUser(**creator, client=client)

        if isinstance(song, ExtDict):
            if any(key.isdigit() for key in song.keys()):
                song = Song.from_data(song, client=client)
            else:
                song = Song(**song, client=client)

        string = data.get(Index.LEVEL_PASS)

        if string is None:
            copyable, password = False, None
        else:
            try:
                # decode password
                password = Coder.decode(type="levelpass", string=string)
            except Exception:
                # failed to get password
                copyable, password = False, None
            else:
                copyable = True

                if not password:
                    password = None

                else:
                    # password is in format 1XXXXXX
                    password = password[1:]

                    password = int(password) if password.isdigit() else None

        desc = Coder.do_base64(
            data.get(Index.LEVEL_DESCRIPTION, ""), encode=False, errors="replace"
        )

        level_data = data.get(Index.LEVEL_DATA, "")
        try:
            level_data = Coder.unzip(level_data)
        except Exception:  # conversion failed
            pass

        diff = data.getcast(Index.LEVEL_DIFFICULTY, 0, int)
        demon_diff = data.getcast(Index.LEVEL_DEMON_DIFFICULTY, 0, int)
        is_demon = bool(data.getcast(Index.LEVEL_IS_DEMON, 0, int))
        is_auto = bool(data.getcast(Index.LEVEL_IS_AUTO, 0, int))
        difficulty = Converter.convert_level_difficulty(
            diff=diff, demon_diff=demon_diff, is_demon=is_demon, is_auto=is_auto
        )

        return cls(
            id=data.getcast(Index.LEVEL_ID, 0, int),
            name=data.get(Index.LEVEL_NAME, "unknown"),
            description=desc,
            version=data.getcast(Index.LEVEL_VERSION, 0, int),
            creator=creator,
            song=song,
            data=level_data,
            password=password,
            copyable=copyable,
            is_demon=is_demon,
            is_auto=is_auto,
            low_detail_mode=bool(data.get(Index.LEVEL_HAS_LDM)),
            difficulty=difficulty,
            stars=data.getcast(Index.LEVEL_STARS, 0, int),
            coins=data.getcast(Index.LEVEL_COIN_COUNT, 0, int),
            verified_coins=bool(data.getcast(Index.LEVEL_COIN_VERIFIED, 0, int)),
            is_epic=bool(data.getcast(Index.LEVEL_IS_EPIC, 0, int)),
            original=data.getcast(Index.LEVEL_ORIGINAL, 0, int),
            downloads=data.getcast(Index.LEVEL_DOWNLOADS, 0, int),
            rating=data.getcast(Index.LEVEL_LIKES, 0, int),
            score=data.getcast(Index.LEVEL_FEATURED_SCORE, 0, int),
            uploaded_timestamp=data.get(Index.LEVEL_UPLOADED_TIMESTAMP, "unknown"),
            last_updated_timestamp=data.get(Index.LEVEL_LAST_UPDATED_TIMESTAMP, "unknown"),
            length=data.getcast(Index.LEVEL_LENGTH, 0, int),
            game_version=data.getcast(Index.LEVEL_GAME_VERSION, 0, int),
            stars_requested=data.getcast(Index.LEVEL_REQUESTED_STARS, 0, int),
            object_count=data.getcast(Index.LEVEL_OBJECT_COUNT, 0, int),
            type=data.getcast(Index.LEVEL_TIMELY_TYPE, 0, int),
            time_n=data.getcast(Index.LEVEL_TIMELY_INDEX, -1, int),
            cooldown=data.getcast(Index.LEVEL_TIMELY_COOLDOWN, -1, int),
            client=client,
        )

    @property
    def name(self) -> str:
        """:class:`str`: The name of the level."""
        return self.options.get("name", "Unnamed")

    @property
    def description(self) -> str:
        """:class:`str`: Description of the level."""
        return self.options.get("description", "")

    @property
    def version(self) -> int:
        """:class:`int`: Version of the level."""
        return self.options.get("version", 0)

    @property
    def downloads(self) -> int:
        """:class:`int`: Amount of the level's downloads."""
        return self.options.get("downloads", 0)

    @property
    def rating(self) -> int:
        """:class:`int`: Amount of the level's likes or dislikes."""
        return self.options.get("rating", 0)

    @property
    def score(self) -> int:
        """:class:`int`: Level's featured score."""
        return self.options.get("score", 0)

    @property
    def creator(self) -> AbstractUser:
        """:class:`.AbstractUser`: Creator of the level."""
        return self.options.get("creator", AbstractUser(client=self.options.get("client")))

    @property
    def song(self) -> Song:
        """:class:`.Song`: Song used in the level."""
        return self.options.get("song", Song(client=self.options.get("client")))

    @property
    def difficulty(self) -> Union[DemonDifficulty, LevelDifficulty]:
        """Union[:class:`.LevelDifficulty`, :class:`.DemonDifficulty`]: Difficulty of the level."""
        difficulty = self.options.get("difficulty", -1)

        if self.is_demon():
            return DemonDifficulty.from_value(difficulty)

        else:
            return LevelDifficulty.from_value(difficulty)

    @property
    def password(self) -> Optional[int]:
        """Optional[:class:`int`]: The password to copy the level.
        See :meth:`.Level.is_copyable`.
        """
        return self.options.get("password")

    def is_copyable(self) -> bool:
        """:class:`bool`: Indicates whether a level is copyable."""
        return bool(self.options.get("copyable"))

    @property
    def stars(self) -> int:
        """:class:`int`: Amount of stars the level has."""
        return self.options.get("stars", 0)

    @property
    def coins(self) -> int:
        """:class:`int`: Amount of coins in the level."""
        return self.options.get("coins", 0)

    @property
    def original_id(self) -> int:
        """:class:`int`: ID of the original level. (``0`` if is not a copy)"""
        return self.options.get("original", 0)

    @property
    def uploaded_timestamp(self) -> str:
        """:class:`str`: A human-readable string representing how much time ago level was uploaded."""
        return self.options.get("uploaded_timestamp", "unknown")

    @property
    def last_updated_timestamp(self) -> str:
        """:class:`str`: A human-readable string showing how much time ago the last update was."""
        return self.options.get("last_updated_timestamp", "unknown")

    @property
    def length(self) -> LevelLength:
        """:class:`.LevelLength`: A type that represents length of the level."""
        return LevelLength.from_value(self.options.get("length", -1))

    @property
    def game_version(self) -> int:
        """:class:`int`: A version of the game required to play the level."""
        return self.options.get("game_version", 0)

    @property
    def requested_stars(self) -> int:
        """:class:`int`: Amount of stars creator of the level has requested."""
        return self.options.get("stars_requested", 0)

    @property
    def objects(self) -> int:
        """:class:`int`: Amount of objects the level has in data."""
        return len(object_split(self.data))

    @property
    def object_count(self) -> int:
        """:class:`int`: Amount of objects the level according to the servers."""
        return self.options.get("object_count", 0)

    @property
    def type(self) -> TimelyType:
        """:class:`.TimelyType`: A type that shows whether a level is Daily/Weekly."""
        return TimelyType.from_value(self.options.get("type", 0))

    @property
    def timely_index(self) -> int:
        """:class:`int`: A number that represents current index of the timely.
        Increments on new dailies/weeklies. If not timely, equals ``-1``.
        """
        return self.options.get("time_n", -1)

    @property
    def cooldown(self) -> int:
        """:class:`int`: Represents a cooldown until next timely. If not timely, equals ``-1``."""
        return self.options.get("cooldown", -1)

    @property
    def data(self) -> Union[bytes, str]:
        """Union[:class:`str`, :class:`bytes`]: Level data, represented as a stream."""
        return self.options.get("data", "")

    @data.setter
    def data(self, value: Union[bytes, str]) -> None:
        """Set ``self.data`` to ``value``."""
        self.options.update(data=value)

    def is_timely(self, daily_or_weekly: Optional[str] = None) -> bool:
        """:class:`bool`: Indicates whether a level is timely/daily/weekly.
        For instance, let's suppose a *level* is daily. Then, the behavior of this method is:
        ``level.is_timely() -> True`` and ``level.is_timely('daily') -> True`` but
        ``level.is_timely('weekly') -> False``."""
        if self.type is None:  # pragma: no cover
            return False

        if daily_or_weekly is None:
            return self.type.value > 0

        assert daily_or_weekly in ("daily", "weekly")

        return self.type.name.lower() == daily_or_weekly

    def is_rated(self) -> bool:
        """:class:`bool`: Indicates if a level is rated (has stars)."""
        return self.stars > 0

    def is_featured(self) -> bool:
        """:class:`bool`: Indicates whether a level is featured."""
        return self.score > 0  # not sure if this is the right way though

    def is_epic(self) -> bool:
        """:class:`bool`: Indicates whether a level is epic."""
        return bool(self.options.get("is_epic"))

    def is_demon(self) -> bool:
        """:class:`bool`: Indicates whether a level is demon."""
        return bool(self.options.get("is_demon"))

    def is_auto(self) -> bool:
        """:class:`bool`: Indicates whether a level is auto."""
        return bool(self.options.get("is_auto"))

    def is_original(self) -> bool:
        """:class:`bool`: Indicates whether a level is original."""
        return not self.original_id

    def has_coins_verified(self) -> bool:
        """:class:`bool`: Indicates whether level's coins are verified."""
        return bool(self.options.get("verified_coins"))

    def download(self) -> Union[bytes, str]:
        """Union[:class:`str`, :class:`bytes`]: Returns level data, represented as string."""
        return self.data

    def has_ldm(self) -> bool:
        return bool(self.options.get("low_detail_mode"))

    def open_editor(self) -> Editor:
        return Editor.launch(self, "data")

    async def report(self) -> None:
        """|coro|

        Reports a level.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to report a level.
        """
        await self.client.report_level(self)

    async def upload(self, **kwargs) -> None:
        r"""|coro|

        Upload ``self``.

        Parameters
        ----------
        \*\*kwargs
            Arguments that :meth:`.Client.upload_level` accepts.
            Defaults are properties of the level.
        """
        track, song_id = (self.song.id, 0)

        if self.song.is_custom():
            track, song_id = song_id, track

        client = kwargs.pop("from_client", self.client)

        if client is None:  # pragma: no cover
            raise MissingAccess(
                message=(
                    "Could not find the client to upload level from. "
                    'Either attach a client to this level or provide "from_client" parameter.'
                )
            )

        password = kwargs.pop("password", self.password)

        args = dict(
            name=self.name,
            id=self.id,
            version=self.version,
            length=abs(self.length.value),
            track=track,
            song_id=song_id,
            two_player=False,
            is_auto=self.is_auto(),
            original=self.original_id,
            objects=self.objects,
            coins=self.coins,
            star_amount=self.stars,
            unlist=False,
            ldm=False,
            password=password,
            copyable=self.is_copyable(),
            description=self.description,
            data=self.data,
        )

        args.update(kwargs)

        uploaded = await client.upload_level(**args)

        self.options = uploaded.options

    async def delete(self) -> None:
        """|coro|

        Deletes a level.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to delete a level.
        """
        await self.client.delete_level(self)

    async def update_description(self, content: Optional[str] = None) -> None:
        """|coro|

        Updates level description.

        Parameters
        ----------
        content: :class:`str`
            Content of the new description. If ``None`` or omitted, nothing is run.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to update level's description.
        """
        if content is None:
            return

        await self.client.update_level_description(self, content)

    async def rate(self, stars: int = 1) -> None:
        """|coro|

        Sends level rating.

        Parameters
        ----------
        stars: :class:`int`
            Amount of stars to rate with.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to rate a level.
        """
        await self.client.rate_level(self, stars)

    async def rate_demon(
        self, demon_difficulty: Union[int, str, DemonDifficulty] = 1, as_mod: bool = False
    ) -> None:
        """|coro|

        Sends level demon rating.

        Parameters
        ----------
        demon_difficulty: Union[:class:`int`, :class:`str`, :class:`.DemonDifficulty`]
            Demon difficulty to rate a level with.

        as_mod: :class:`bool`
            Whether to send a demon rating as moderator.

        Raises
        ------
        :exc:`.MissingAccess`
            If attempted to rate a level as moderator without required permissions.
        """

        await self.client.rate_demon(self, demon_difficulty=demon_difficulty, as_mod=as_mod)

    async def send(self, stars: int = 1, featured: bool = True) -> None:
        """|coro|

        Sends a level to Geometry Dash Developer and Administrator, *RobTop*.

        Parameters
        ----------
        stars: :class:`int`
            Amount of stars to send with.

        featured: :class:`bool`
            Whether to send to feature, or to simply rate.

        Raises
        ------
        :exc:`.MissingAccess`
            Missing required moderator permissions.
        """
        await self.client.send_level(self, stars=stars, featured=featured)

    async def is_alive(self) -> bool:
        """|coro|

        Checks if a level is still on Geometry Dash servers.

        Returns
        -------
        :class:`bool`
            ``True`` if a level is still *alive*, and ``False`` otherwise.
            Also ``False`` if a client is not attached to the level.s
        """
        try:
            await self.client.search_levels_on_page(query=str(self.id))

        except MissingAccess:
            return False

        return True

    async def refresh(self) -> Optional[Level]:
        """|coro|

        Refreshes a level. Returns ``None`` on fail.

        .. note::

            This function actually refreshes a level and its stats.
            No need to do funky stuff with its return.

        Returns
        -------
        :class:`.Level`
            A newly fetched version. ``None`` if failed to fetch.
        """
        try:
            if self.is_timely():
                async_func = getattr(self.client, "get_" + self.type.name.lower())
                new_ver = await async_func()

                if new_ver.id != self.id:
                    log.warning(
                        f"There is a new {self.type.desc} Level: {new_ver!r}. Updating to it..."
                    )

            else:
                new_ver = await self.client.get_level(self.id)

        except MissingAccess:
            return log.warning("Failed to refresh level: %r. Most likely it was deleted.", self)

        self.options = new_ver.options

        return self

    async def comment(self, content: str, percentage: int = 0) -> Optional[Comment]:
        """|coro|

        Posts a comment on a level.

        Parameters
        ----------
        content: :class:`str`
            Body of the comment to post.

        percentage: :class:`int`
            Percentage to display. Default is ``0``.

            .. note::

                gd.py developers are not responsible for effects that changing this may cause.
                Set this parameter higher than 0 on your own risk.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to post a level comment.

        Returns
        -------
        Optional[:class:`.Comment`]
            Sent comment.
        """
        return await self.client.comment_level(self, content, percentage)

    async def like(self) -> None:
        """|coro|

        Likes a level.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to like a level.
        """
        await self.client.like(self)

    async def dislike(self) -> None:
        """|coro|

        Dislikes a level.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to dislike a level.
        """
        await self.client.dislike(self)

    async def get_leaderboard(
        self, strategy: Union[int, str, LevelLeaderboardStrategy] = 0
    ) -> List[LevelRecord]:
        """|coro|

        Retrieves the leaderboard of a level.

        Parameters
        ----------
        strategy: Union[:class:`int`, :class:`str`, :class:`.LevelLeaderboardStrategy`]
            A strategy to apply. This is converted to :class:`.LevelLeaderboardStrategy`
            using :func:`.utils.value_to_enum`.

        Returns
        -------
        List[:class:`.LevelRecord`]
            A list of user-like objects.
        """
        return await self.client.get_level_leaderboard(self, strategy=strategy)

    async def get_comments(
        self,
        strategy: Union[int, str, CommentStrategy] = 0,
        amount: int = 20,
        exclude: Tuple[Type[BaseException]] = DEFAULT_EXCLUDE,
    ) -> List[Comment]:
        """|coro|

        Retrieves level comments.

        Parameters
        ----------
        strategy: Union[:class:`int`, :class:`str`, :class:`.CommentStrategy`]
            A strategy to apply when searching. This is converted to :class:`.CommentStrategy`
            using :func:`.utils.value_to_enum`.

        amount: :class:`int`
            Amount of comments to retrieve. Default is ``20``.
            For ``amount < 0``, ``2 ** 31`` is added, allowing to fetch
            a theoretical limit of comments.

        exclude: Sequence[Type[:exc:`BaseException`]]
            Exceptions to ignore. By default includes only :exc:`.NothingFound`.

        Returns
        -------
        List[:class:`.Comment`]
            List of comments retrieved.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to fetch comments.

        :exc:`.NothingFound`
            No comments were found.

        :exc:`.FailedConversion`
            Raised if ``strategy`` can not be converted to :class:`.CommentStrategy`.
        """
        return await self.client.get_level_comments(
            self, strategy=strategy, amount=amount, exclude=exclude
        )
