from . import *
from singleton_decorator import singleton

import spotipy
import spotipy.util

"""""

Holds the spotify singleton. This class is used as the communicator with spotify.

"""""

log = setup_logger(__name__)


@singleton
@dataclass
class Spotify:
    sp: object = None

    def __post_init__(self):
        self.create_token()

    def create_token(self):
        token = None

        def token_helper():
            return spotipy.util.prompt_for_user_token(
                username=username,
                scope=scope,
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri
            )

        token = token_helper()
        if token:
            log.info(f"Spotify token successfully generated for user: {username}.")
        else:
            log.error(f"Failure during spotify token generation for user: {username}.")
