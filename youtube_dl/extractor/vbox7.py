# encoding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import urlencode_postdata


class Vbox7IE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?vbox7\.com/play:(?P<id>[^/]+)'
    _TESTS = [{
        'url': 'http://vbox7.com/play:0946fff23c',
        'md5': 'a60f9ab3a3a2f013ef9a967d5f7be5bf',
        'info_dict': {
            'id': '0946fff23c',
            'ext': 'mp4',
            'title': 'Борисов: Притеснен съм за бъдещето на България',
        },
    }, {
        'url': 'http://vbox7.com/play:249bb972c2',
        'md5': '99f65c0c9ef9b682b97313e052734c3f',
        'info_dict': {
            'id': '249bb972c2',
            'ext': 'mp4',
            'title': 'Смях! Чудо - чист за секунди - Скрита камера',
        },
        'skip': 'georestricted',
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(
            r'<title>(.*)</title>', webpage, 'title').split('/')[0].strip()

        video_url = self._search_regex(
            r'src\s*:\s*(["\'])(?P<url>.+?.mp4.*?)\1',
            webpage, 'video url', default=None, group='url')

        thumbnail_url = self._og_search_thumbnail(webpage)

        if not video_url:
            info_response = self._download_webpage(
                'http://vbox7.com/play/magare.do', video_id,
                'Downloading info webpage',
                data=urlencode_postdata({'as3': '1', 'vid': video_id}),
                headers={'Content-Type': 'application/x-www-form-urlencoded'})
            final_url, thumbnail_url = map(
                lambda x: x.split('=')[1], info_response.split('&'))

        if '/na.mp4' in video_url:
            self.raise_geo_restricted()

        return {
            'id': video_id,
            'url': self._proto_relative_url(video_url, 'http:'),
            'title': title,
            'thumbnail': thumbnail_url,
        }
