from librespot.core import Session
from librespot.metadata import TrackId
from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality

SESSION: Session = Session.Builder().stored_file().create()

track_id = TrackId.from_uri("spotify:track:6NAmbftWAovcMCnJzDCFsU")

stream = SESSION.content_feeder().load(track_id, VorbisOnlyAudioQuality(AudioQuality.HIGH), False, None)

