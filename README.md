# GoogleMapDownloader

Created by Adrien de Jauréguiberry

A script that builds a high resolution satellite image by downloading tiles from Google Map. It is designed to work with the free version of the API like this:

Give a gps position (lat,long), a map length, an image size and a key.
The script will compute the adapted zoom and the tile size, and download all the tiles with a little more pixels to crop the Google logo. Then it assembles the tiles in one image.

The map will be a square whose center is (lat,long) with an edge of map length (in m) and image size (in pixels).


          map length (m)
        image size (pixels)
<_______________________________>
_________________________________
|                               |
|                               |
|                               |
|          (lat,long)           |
|              X                |
|                               |
|                               |
|                               |
|_______________________________|


The key parameter is not necessary but it might allow you to download much more if you request one on GMap site.

You can run the given example in a python 3 console like this:
```
import GoogleMapDownloader as gmd
gmd.run_example()
```
