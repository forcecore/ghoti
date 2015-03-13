# Which Format? #
OpenCV supports many _raster_ image formats such as JPG, BMP, GIF and PNG.
  * BMP usually have no compression that saved images take a lot of disk space.
  * GIF has compression and supports animation. However, this format discards color information by quantizing images into 256 colors.
  * JPG is capable of supporting full colors with compression. However, the compression is a lossy one: color information is slightly distorted (usually unperceivable to human eyes).
  * PNG supports compression and unlike JPG, no information is lost/modified during compression, making this format ideal for "chroma key" technique.
The extractor supports all of the formats mentioned above.

Currently, the extractor considers magenta (>=256, <=2, >=253) as background.
To use only exact (255,0,255) as background color, JPG format should not be used, as they distort the color information. PNG is recommended in this case.
To use other colors than magenta as background, ghoti.py should be modified.
See [Tuning](Tuning.md) page for details.

# Removing background #
Background removal would be easier if the image was photographed with magenta background. If that is not the case, background removal requires some effort, depending on the method.
  * GrabCut algorithm:
    * Introduction: http://research.microsoft.com/en-us/um/cambridge/projects/visionimagevideoediting/segmentation/grabcut.htm
    * J. Talbot's implementation of GrabCut algorithm : http://www.justintalbot.com/course-work/
      * http://www.morethantechnical.com/2009/12/14/extending-justin-talbots-grabcut-impl-w-code/
    * GrabCut is implemented in OpenCV 2.1 as well.
  * GIMP (an image editor) has Foreground Select tool, based on SIOX algorithm.
    * http://docs.gimp.org/en/gimp-tool-foreground-select.html