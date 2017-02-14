#!/usr/bin/python3
# GoogleMapDownloader.py 
# Created by Adrien de Jauréguiberry
#
# A script which when given a longitude, latitude, length
# returns a high resolution google map

from urllib import request
from PIL import Image
import os
import math

class GoogleMapDownloader:
    """
        A class which generates high resolution google maps images given
        a gmap API key and position parameters
    """

    def __init__(self, API_key, lat, lng, lgth, img_size=1000):
        """
            GoogleMapDownloader Constructor
            Args:
                API_key: The GoogleMap API key to load images
                lat:    The latitude of the location required
                lng:    The longitude of the location required
                lgth:   Length of the map in m. The map will be a square.
                        warning: too big length will result in distorded map.
                img_size: The resolution of image as img_size X img_size
                        default to 1000
        """
        k = 104857.6
        self._img_size = img_size
        self._lat = lat
        self._lng = lng
        self._zoom = math.ceil(math.log2(k*img_size/lgth))
        temp_size = int((2**self._zoom)*lgth/k)
        self._nb_tiles = math.ceil(temp_size/500)
        self._tile_size = math.floor(temp_size/self._nb_tiles)
        self._API_key = API_key

        #print("Map will have a length of: " + str(int(k*temp_size/(2**self._zoom))) + " m")
        #print("Map will have a size   of: " + str(temp_size) + " p")

    def generateImage(self):
        """
            Generates an image by stitching a number of google map tiles together.
            
            Returns:
                A high-resolution Goole Map image.
        """

        tile_width = self._nb_tiles
        tile_height = self._nb_tiles

        lat_step = 0.95*self._tile_size/(2**self._zoom)
        lon_step = 1.405*self._tile_size/(2**self._zoom)

        border = 20        

        # Determine the size of the image
        width, height = self._tile_size * tile_width, self._tile_size * tile_height

        #Create a new image of the size require
        map_img = Image.new('RGB', (width,height))


        nb_tiles_max = tile_width*tile_height
        counter = 1
        for x in range(0, tile_width):
            for y in range(0, tile_height) :

                la = self._lat - y*lat_step + lat_step*(tile_height-1)/2
                lo = self._lng + x*lon_step - lon_step*(tile_width-1)/2

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

    latitude  = 47.547465
    longitude = -2.057472

    map_size  = 2000
    img_size  = 4000

    gmd = GoogleMapDownloader(gmap_key, latitude, longitude, map_size, img_size)

    #print("The tile coorindates are {}".format(gmd.getXY()))

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