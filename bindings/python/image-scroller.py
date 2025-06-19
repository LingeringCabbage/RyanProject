#!/home/thomasgreiner/rpi-rgb-led-matrix/bindings/python/venv/bin/python
import time
from typing import Tuple

from samplebase import SampleBase
from PIL import Image
from rgbmatrix import graphics
from market_data import MarketData

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="./amzn.ppm")

    def draw_ticker_and_price(self, double_buffer, pos, font, info: Tuple[str, str, str]) -> int:
        ticker, price, change = info
        color = graphics.Color(0, 255, 0)

        # Graphics on top row
        ticker_len = graphics.DrawText(double_buffer, font, pos, 16, color, ticker)

        # Graphics on bottom row
        price_len = graphics.DrawText(double_buffer, font, pos, 30, color, price)
        triangle_pos = pos + price_len + 5
        triangle_len = graphics.DrawText(double_buffer, font, triangle_pos, 30, color, "▲")
        # upside_down_triangle_len = graphics.DrawText(double_buffer, font, triangle_pos, 30, color, "▼")
        change_pos = triangle_pos + triangle_len + 5
        change_len = graphics.DrawText(double_buffer, font, change_pos, 30, color, change)

        end_pos = change_pos + change_len
        return end_pos - pos    # Return the length of the entire drawing




    def run(self):
        # md = MarketData()
        # md.load_tickers_background(["AAPL", "GOOG", "AMZN"])
        # time.sleep(7)
        # print(md.tickers_data)

        if not 'image' in self.__dict__:
            self.image = Image.open("./aapl.ppm").convert('RGB')
            self.image2 = Image.open("./goog.ppm").convert('RGB')
            self.image3 = Image.open(self.args.image).convert('RGB')
        # self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        # self.image2.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        # self.image3.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        images = [self.image, self.image2, self.image3]

        double_buffer = self.matrix.CreateFrameCanvas()

        # Text configuration
        font = graphics.Font()
        font.LoadFont("../../../fonts/8x13.bdf")
        textColor = graphics.Color(255, 255, 0)

        texts = [("AAPL", "100.00", "1.00"), ("GOOG", "200.00", "2.00"), ("AMZN", "300.00", "3.00")]


        # Set up buffer
        idx = 0
        first_image = images[idx]
        second_image = images[(idx + 1) % len(images)]
        third_image = images[(idx + 2) % len(images)]
        first_text = texts[idx]
        second_text = texts[(idx + 1) % len(texts)]
        third_text = texts[(idx + 2) % len(texts)]

        # Let's scroll!
        xpos = 0
        while True:
            double_buffer.Clear()

            # TODO: Turn this into a for loop
            first_image_pos = xpos
            double_buffer.SetImage(first_image, first_image_pos)

            first_text_pos = first_image_pos + first_image.width + 5
            # first_text_len = graphics.DrawText(double_buffer, font, first_text_pos, 20, textColor, first_text)
            first_text_len = self.draw_ticker_and_price(double_buffer, first_text_pos, font, first_text)

            second_image_pos = first_text_pos + first_text_len + 5
            double_buffer.SetImage(second_image, second_image_pos)

            second_text_pos = second_image_pos + second_image.width + 5
            # second_text_len = graphics.DrawText(double_buffer, font, second_text_pos, 20, textColor, second_text)
            second_text_len = self.draw_ticker_and_price(double_buffer, second_text_pos, font, second_text)

            third_image_pos = second_text_pos + second_text_len + 5
            double_buffer.SetImage(third_image, third_image_pos)

            third_text_pos = third_image_pos + third_image.width + 5
            third_text_len = self.draw_ticker_and_price(double_buffer, third_text_pos, font, third_text)


            double_buffer = self.matrix.SwapOnVSync(double_buffer)

            if (second_image_pos == 0):
                idx = (idx + 1) % len(images)
                first_image = images[idx]
                second_image = images[(idx + 1) % len(images)]
                third_image = images[(idx + 2) % len(images)]
                first_text = texts[idx]
                second_text = texts[(idx + 1) % len(texts)]
                third_text = texts[(idx + 2) % len(texts)]
                xpos = 0
            xpos -= 1
            time.sleep(0.02)

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()