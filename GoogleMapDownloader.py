#!/usr/bin/python3
# GoogleMapDownloader.py 
# Created by Adrien de Jauréguiberry
#
# A script which when given a longitude, latitude, length
# returns a high resolution google map

from urllib import request
from PIL import Image
import os
from math import *

class GoogleMapDownloader:
    """
        A class which generates high resolution google maps images given
        a gmap API key and location parameters
    """

    def __init__(self, API_key, lat, lng, lgth, img_size=1000):
        """
            GoogleMapDownloader Constructor
            Args:
                API_key:  The GoogleMap API key to load images
                lat:      The latitude of the location required
                lng:      The longitude of the location required
                lgth:     Length of the map in m. The map will be a square.
                          warning: too big length will result in distorded map due to mercator projection.
                img_size: The resolution of the output image as img_size X img_size
                          default to 1000
        """
        lat_rad = (pi/180)*lat
        self._img_size = img_size
        self._lat = lat
        self._lng = lng
        self._zoom = floor(log2(156543.03 * img_size / lgth))
        self._resolution = 156543.03 / (2 ** self._zoom) #(m/px)
        self._nb_tiles = ceil(img_size/500)
        self._tile_lgth = lgth/self._nb_tiles
        self._tile_size = int(self._tile_lgth/self._resolution)
        self._API_key = API_key

    def getMercatorFromGPS(self,lng,lat):
    	x = 6371000 * lng
    	y = 6371000 * log(tan(pi/4 + lat/2))
    	return (x,y)

    def getGPSFromMercator(self,x,y):
    	lng = x/6371000
    	lat = 2*atan(exp(y/6371000)) - pi/2
    	return (lng,lat)

    def generateImage(self):
        """
            Generates an image by stitching a number of google map tiles together.
            
            Returns:
                A high-resolution Goole Map image.
        """

        lat_rad = (pi/180)*abs(self._lat)
        lng_rad = (pi/180)*abs(self._lng)
        xy_loc  = self.getMercatorFromGPS(lng_rad,lat_rad)

        xy_with_step  = [xy_loc[0]+self._tile_lgth , xy_loc[1]+self._tile_lgth]
        gps_with_step = self.getGPSFromMercator(xy_with_step[0], xy_with_step[1])

        lat_step = (180/pi)*(gps_with_step[1] - lat_rad)
        lon_step = (180/pi)*(gps_with_step[0] - lng_rad)

        border = 20        

        # Determine the size of the image
        width, height = self._tile_size * self._nb_tiles, self._tile_size * self._nb_tiles

        #Create a new image of the size require
        map_img = Image.new('RGB', (width,height))


        nb_tiles_max = self._nb_tiles**2
        counter = 1
        for x in range(0, self._nb_tiles):
            for y in range(0, self._nb_tiles) :

                la = self._lat - y*lat_step + lat_step*(self._nb_tiles-1)/2
                lo = self._lng + x*lon_step - lon_step*(self._nb_tiles-1)/2

                url = 'https://maps.googleapis.com/maps/api/staticmap?'
                url += 'center='+str(la)+','+str(lo)
                url += '&zoom='+str(self._zoom)
                url += '&size='+str(self._tile_size+2*border)+'x'+str(self._tile_size+2*border)
                url += '&maptype=satellite'
                if self._API_key:url += '&key='+self._API_key
                print('getting tile '+str(counter)+"/"+str(nb_tiles_max))
                counter+=1

                current_tile = str(x)+'-'+str(y)
                request.urlretrieve(url, current_tile)
            
                im = Image.open(current_tile)
                map_img.paste(im.crop((border,border,self._tile_size+border,self._tile_size+border)), (x*self._tile_size, y*self._tile_size))
              
                os.remove(current_tile)

        print("Resizing map")
        return map_img.resize((self._img_size,self._img_size))

def run_example():
    # Create a new instance of GoogleMap Downloader

    #GMap API is not free! Even if this script we adapted to use free acount settings
    #you might need a project key.
    #You can find one here: https://developers.google.com/maps/documentation/static-maps/intro
    gmap_key  = "" 

    latitude  = 73.295938
    longitude = -25.315502

    map_size  = 200000
    img_size  = 1320

    gmd = GoogleMapDownloader(gmap_key, latitude, longitude, map_size, img_size)


    try:
        # Get the high resolution image
        img = gmd.generateImage()
    except IOError:
        print("ERROR: Could not generate the image - use another key or change the location")
    else:
        #Save the image to disk
        img.save("high_resolution_map.jpg")
        print("The map has successfully been created")
        
#run_example()