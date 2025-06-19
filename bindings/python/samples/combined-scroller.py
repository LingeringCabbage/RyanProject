#!/usr/bin/env python
# Combined image and text scroller with alternating display

from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import time
import os
import shutil

options= RGBMatrixOptions()
options.cols=128
options.hardware_mapping='adafruit-hat'
options.drop_privileges = False
matrix= RGBMatrix(options=options)

class CombinedScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(CombinedScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Your Text Here!")
        self.parser.add_argument("-i", "--image", help="The image to display", default="../../../examples-api-use/runtext.ppm")
        self.parser.add_argument("-d", "--duration", help="Duration for each mode in seconds", default=10, type=int)
        
    def run(self):
        # Create canvas for double buffering
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        # Load font for text
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        text_color = graphics.Color(255, 255, 0)  # Yellow
        
        # Handle image with permission fix
        image_path = self.args.image
        temp_image_path = "/tmp/led_matrix_image.ppm"
        
        # Copy the image to a temp location with accessible permissions
        try:
            shutil.copy2(image_path, temp_image_path)
            os.chmod(temp_image_path, 0o666)  # Make readable by all
            image = Image.open(temp_image_path).convert('RGB')
        except Exception as e:
            print(f"Error handling image: {e}")
            print("Falling back to default text-only mode")
            image = None
        
        # Get image dimensions if we have an image
        if image:
            image = image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
            img_width, img_height = image.size
        
        # Get text from arguments
        my_text = self.args.text
        
        # Duration for each mode
        mode_duration = self.args.duration
        
        while True:
            # Image scrolling mode (only if we have a valid image)
            if image:
                mode_start_time = time.time()
                img_pos = 0
                
                while time.time() - mode_start_time < mode_duration:
                    img_pos += 1
                    if (img_pos > img_width):
                        img_pos = 0
                        
                    offscreen_canvas.Clear()
                    offscreen_canvas.SetImage(image, -img_pos)
                    offscreen_canvas.SetImage(image, -img_pos + img_width)
                    offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                    time.sleep(0.01)
            
            # Text scrolling mode
            mode_start_time = time.time()
            text_pos = offscreen_canvas.width
            
            while time.time() - mode_start_time < mode_duration:
                offscreen_canvas.Clear()
                text_length = graphics.DrawText(offscreen_canvas, font, text_pos, 10, text_color, my_text)
                text_pos -= 1
                
                if (text_pos + text_length < 0):
                    text_pos = offscreen_canvas.width
                    
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(0.05)

# Main function
if __name__ == "__main__":
    combined_scroller = CombinedScroller()
    if (not combined_scroller.process()):
        combined_scroller.print_help()
