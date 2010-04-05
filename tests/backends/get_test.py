import unittest

from mopidy.backends.dummy import DummyBackend, DummyCurrentPlaylistController
from mopidy.mixers.dummy import DummyMixer
from mopidy.models import Playlist, Track

class CurrentPlaylistGetTest(unittest.TestCase):
    def setUp(self):
        self.b = DummyBackend(mixer=DummyMixer())
        self.c = self.b.current_playlist

    def test_get_by_id_returns_unique_match(self):
        track = Track(id=1)
        self.c.playlist = Playlist(tracks=[Track(id=13), track, Track(id=17)])
        self.assertEqual(track, self.c.get(id=1))

    def test_get_by_id_raises_error_if_multiple_matches(self):
        track = Track(id=1)
        self.c.playlist = Playlist(tracks=[Track(id=13), track, track])
        try:
            self.c.get(id=1)
            self.fail(u'Should raise LookupError if multiple matches')
        except LookupError as e:
            self.assertEqual(u'"id=1" match multiple tracks', e[0])

    def test_get_by_id_raises_error_if_no_match(self):
        self.c.playlist = Playlist(tracks=[Track(id=13), Track(id=17)])
        try:
            self.c.get(id=1)
            self.fail(u'Should raise LookupError if no match')
        except LookupError as e:
            self.assertEqual(u'"id=1" match no tracks', e[0])

    def test_get_by_uri_returns_unique_match(self):
        track = Track(uri='a')
        self.c.playlist = Playlist(
            tracks=[Track(uri='z'), track, Track(uri='y')])
        self.assertEqual(track, self.c.get(uri='a'))

    def test_get_by_uri_raises_error_if_multiple_matches(self):
        track = Track(uri='a')
        self.c.playlist = Playlist(tracks=[Track(uri='z'), track, track])
        try:
            self.c.get(uri='a')
            self.fail(u'Should raise LookupError if multiple matches')
        except LookupError as e:
            self.assertEqual(u'"uri=a" match multiple tracks', e[0])

    def test_get_by_uri_raises_error_if_no_match(self):
        self.c.playlist = Playlist(tracks=[Track(uri='z'), Track(uri='y')])
        try:
            self.c.get(uri='a')
            self.fail(u'Should raise LookupError if no match')
        except LookupError as e:
            self.assertEqual(u'"uri=a" match no tracks', e[0])

    def test_get_by_multiple_criteria_returns_elements_matching_all(self):
        track1 = Track(id=1, uri='a')
        track2 = Track(id=1, uri='b')
        track3 = Track(id=2, uri='b')
        self.c.playlist = Playlist(tracks=[track1, track2, track3])
        self.assertEqual(track1, self.c.get(id=1, uri='a'))
        self.assertEqual(track2, self.c.get(id=1, uri='b'))
        self.assertEqual(track3, self.c.get(id=2, uri='b'))

    def test_get_by_criteria_that_is_not_present_in_all_elements(self):
        track1 = Track(id=1)
        track2 = Track(uri='b')
        track3 = Track(id=2)
        self.c.playlist = Playlist(tracks=[track1, track2, track3])
        self.assertEqual(track1, self.c.get(id=1))


class StoredPlaylistsGetTest(unittest.TestCase):
    def setUp(self):
        self.b = DummyBackend(mixer=DummyMixer())
        self.s = self.b.stored_playlists

    def test_get_by_name_returns_unique_match(self):
        playlist = Playlist(name='b')
        self.s.playlists = [Playlist(name='a'), playlist]
        self.assertEqual(playlist, self.s.get(name='b'))

    def test_get_by_name_returns_first_of_multiple_matches(self):
        playlist = Playlist(name='b')
        self.s.playlists = [playlist, Playlist(name='a'), Playlist(name='b')]
        try:
            self.s.get(name='b')
            self.fail(u'Should raise LookupError if multiple matches')
        except LookupError as e:
            self.assertEqual(u'"name=b" match multiple playlists', e[0])

    def test_get_by_id_raises_keyerror_if_no_match(self):
        self.s.playlists = [Playlist(name='a'), Playlist(name='b')]
        try:
            self.s.get(name='c')
            self.fail(u'Should raise LookupError if no match')
        except LookupError as e:
            self.assertEqual(u'"name=c" match no playlists', e[0])