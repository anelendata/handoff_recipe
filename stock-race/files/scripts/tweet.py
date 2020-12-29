import json
import logging
import os
import sys
import time

import requests
from requests_oauthlib import OAuth1

import tweepy


logger = logging.getLogger(__name__)


class VideoTweet(object):
    """
    Modified from https://github.com/twitterdev/large-video-upload-python
    """
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, media_type):
        '''
        Defines video tweet properties
        '''
        self.media_types = [
            "tweet_gif",
            "video/mp4",
            "image/jpeg",
            "image/gif"
        ]
        if media_type not in self.media_types:
            raise Exception(
                f"{media_type} is not a supported format {self.media_types}")

        self.media_category = None
        if media_type == "tweet_gif":
            self.media_category = "tweet_gif"
        elif media_type == "video/mp4":
            self.media_category = "tweet_video"

        self.media_type = media_type
        self.MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
        self.POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

        self.media_id = None
        self.processing_info = None
        self.oauth = OAuth1(consumer_key,
                            client_secret=consumer_secret,
                            resource_owner_key=access_token,
                            resource_owner_secret=access_token_secret)

    def _check_status(self):
        '''
        Checks video processing status
        '''
        if self.processing_info is None:
            return

        state = self.processing_info['state']

        logger.info('Media processing status is %s ' % state)

        if state == u'succeeded':
            return

        if state == u'failed':
            raise Exception(self.processing_info)

        check_after_secs = self.processing_info['check_after_secs']

        logger.info('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = requests.get(url=self.MEDIA_ENDPOINT_URL,
                           params=request_params, auth=self.oauth)

        self.processing_info = req.json().get('processing_info', None)
        self._check_status()


    def _upload_init(self):
        '''
        Initializes Upload
        '''
        request_data = {
            'command': 'INIT',
            'media_type': self.media_type,
            'total_bytes': self.total_bytes,
            'media_category': self.media_category
        }

        req = requests.post(url=self.MEDIA_ENDPOINT_URL,
                            data=request_data, auth=self.oauth)
        media_id = req.json()['media_id']

        self.media_id = media_id


    def _upload_append(self):
        '''
        Uploads media in chunks and appends to chunks uploaded
        '''
        segment_id = 0
        bytes_sent = 0
        file = open(self.video_filename, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4*1024*1024)

            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media':chunk
            }

            req = requests.post(url=self.MEDIA_ENDPOINT_URL,
                                data=request_data, files=files, auth=self.oauth)

            if req.status_code < 200 or req.status_code > 299:
                raise Exception(req.text)

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            logger.info(f'{bytes_sent} of {self.total_bytes} bytes uploaded')

        logger.info('Upload chunks complete.')


    def _upload_finalize(self):
        '''
        Finalizes uploads and starts video processing
        '''
        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = requests.post(url=self.MEDIA_ENDPOINT_URL,
                            data=request_data, auth=self.oauth)

        self.processing_info = req.json().get('processing_info', None)
        self._check_status()


    def upload(self, file_name):
        self.video_filename = file_name
        self.total_bytes = os.path.getsize(self.video_filename)
        self._upload_init()
        self._upload_append()
        self._upload_finalize()
        media_id = self.media_id
        self.media_id = None
        self.total_bytes = None
        self.video_filename = None
        return media_id


    def tweet(self, message, media_id=None):
        '''
        Publishes Tweet with attached video
        '''
        request_data = {
            'status': message,
            'media_ids': [media_id]
        }

        req = requests.post(url=self.POST_TWEET_URL,
                            data=request_data, auth=self.oauth)
        logger.info(req.json())


    def update_with_tweepy(config):
        """
        This does not work with a large animated GIF (> 5MB)
        """
        twitter_auth_keys = {
            "consumer_key"        : config["api_key"],
            "consumer_secret"     : config["api_secret"],
            "access_token"        : config["access_token"],
            "access_token_secret" : config["access_secret"]
        }

        auth = tweepy.OAuthHandler(
                twitter_auth_keys['consumer_key'],
                twitter_auth_keys['consumer_secret']
                )
        auth.set_access_token(
                twitter_auth_keys['access_token'],
                twitter_auth_keys['access_token_secret']
                )
        api = tweepy.API(auth)

        response = api.media_upload(config["media_file"])
        media_id = response.media_id
        status = api.update_status(status=config["message"], media_ids=[media_id])
        logger.info(status)


if __name__ == '__main__':
    with open("files/twitter_config.json", "r") as f:
        config = json.load(f)

    videoTweet = VideoTweet(
        consumer_key=config["api_key"],
        consumer_secret=config["api_secret"],
        access_token=config["access_token"],
        access_token_secret=config["access_secret"],
        media_type="tweet_gif")

    media_id = videoTweet.upload(config["media_file"])
    videoTweet.tweet(config["message"], media_id)
