#!/usr/bin/env python 
# coding: utf8 
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!

###################################
## PICASA PHOTO, ALBUM MANAGER MODULE
## from    : http://code.google.com/apis/picasaweb/docs/1.0/developers_guide_python.html
## to      : this
###################################    


###################################
## UTILITIES
###################################    
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)


###################################
## MODULE IMPORTS
###################################    

import gdata.photos.service
import gdata.media
import gdata.geo


###################################
## UTILITIES
###################################    


###################################
## CLASSES
###################################    
class Manage:
    SOURCE=None
    PICASA_USERNAME=None
    PICASA_USERPASSWORD=None

    client=None
    
    def __init__(self, app_config, gdata_user=None, session=None):
        """
            Calls set_gdata_client to ... set the (gdata) client attribute
        """
        self.set_gdata_client(app_config, gdata_user=gdata_user, session=session)

    def set_gdata_client(self, app_config, gdata_user=None, session=None):
        """
            Uses Gdata Client Programmatic Login
            
            Params:
                gdata_user  : first to be checked
                session     : second to checked for .gdata_user
        """
        # keys & scope
        self.SOURCE = '%s-%s' % (app_config.APP_DETAILS[0], 
                               '' if len(app_config.APP_DETAILS)<2 else app_config.APP_DETAILS[1])
        self.PICASA_USERNAME = app_config.PICASA_API[0]
        self.PICASA_USERPASSWORD = app_config.PICASA_API[1]
    
        self.client = gdata.photos.service.PhotosService()
        
        if gdata_user:
            self.client.email = gdata_user['email']
            self.client.password = gdata_user['password']
        elif session and session.gdata_user:
            self.client.email = session.gdata_user['email']
            self.client.password = session.gdata_user['password']
        else:
            self.client.email = '%s@gmail.com' % self.PICASA_USERNAME
            self.client.password = self.PICASA_USERPASSWORD
        
        self.client.source = self.SOURCE
        self.client.ProgrammaticLogin()

    
    def get_albums_feed(self, limit=100):
        feed = self.client.GetUserFeed(limit=limit)
        return feed.entry
    
    def get_album_by_id(self, album_id):
        feed = self.client.GetUserFeed()
        for entry in feed.entry:
            if entry.gphoto_id.text == album_id:
                return entry
    
    def get_album_photos(self, album_id, username=None, limit=100, raw_feed=False):
        if not username:
            username=self.PICASA_USERNAME
            
        album_id=album_id
        album_feed = self.client.GetFeed(
            '/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, album_id), limit=limit)
        if raw_feed:
            return album_feed.entry
        else:
            album=[]
            for photo in album_feed.entry:
                album.append(self.get_photo_details(photo))
            return album
    
    def get_album_photo_by_id(self, album_id, photo_id, username=None, raw_feed=False):
        if not username:
            username=self.PICASA_USERNAME
        
        photos=self.get_album_photos(album_id, username=username, limit=100, raw_feed=raw_feed)
        if raw_feed:
            return filter(lambda x: x.gphoto_id.text==photo_id, photos)[0]
        else:    
            return filter(lambda x: x.id==photo_id, photos)[0]
    
    def initialize_photo_metadata(self, photo):
        if not photo.media:
            photo.media = gdata.media.Group()
        if not photo.media.keywords:
            photo.media.keywords = gdata.media.Keywords()
        
        if not photo.geo:
            photo.geo = gdata.geo.Where()
        if not photo.geo.Point:
            photo.geo.Point = gdata.geo.Point()
        photo.geo.Point.pos = gdata.geo.Pos(text='%s %s' % ('45', '-45'))
    
    def get_photo_details(self, photo):
        album_id=photo.albumid.text
        _id=photo.gphoto_id.text
        _title=photo.title.text
        camera = 'unknown'
        if photo.exif.make and photo.exif.model:
          camera = '%s %s' % (photo.exif.make.text, photo.exif.model.text)
        url=photo.content.src
        thumbnail_url=photo.media.thumbnail[0].url
        return Struct(**{'album_id':album_id, 'id':_id, 'title':_title, 
                'camera':camera, 'url': url, 'thumbnail_url':thumbnail_url})
        
    def get_album_thumbnail(self, album_id, username=None):
        if not username:
            username=self.PICASA_USERNAME
            
        return self.get_album_photos(album_id, username=username, limit=1)[0]
            
    def get_recent_photos(self, username=None):
        if not username:
            username=self.PICASA_USERNAME
            
        photos = self.client.GetUserFeed(kind='photo', limit='10')
        recent=[]
        for photo in photos.entry:
            recent.append(self.get_photo_details(photo))
        return recent
    
    def get_album_gallery(self, username=None, limit=100):
        if not username:
            username=self.PICASA_USERNAME
                
        albums_feed=self.get_albums_feed(limit=limit)
        gallery=[]
        for entry in albums_feed:
            gallery.append(self.get_album_thumbnail(entry.gphoto_id.text))
        return gallery
