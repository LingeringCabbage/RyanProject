#!/usr/bin/env python
import time
from typing import Tuple

from samplebase import SampleBase
from PIL import Image
from rgbmatrix import graphics
from market_data import MarketData

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.tickers = ["NSANY", "NVDA", "SPY", "VOO", "IVZ", "QQQ", "META", "AAPL", "GOOG", "AMZN", "MSFT", "RYAN", "WMT", "KO", "GLD", "SLV", "DJI"]
        # self.parser.add_argument("-i", "--image", help="The image to display", default="./amzn.ppm")

    def draw_ticker_and_price(self, double_buffer, pos, font, info: Tuple[str, str, str]) -> int:
        ticker, price, change = info

        # Red text and down triangle for negative change, green text and up triangle for positive change
        triangle = "▼" if change[0] == "-" else "▲"
        color = graphics.Color(255, 0, 0) if change[0] == "-" else graphics.Color(0, 255, 0)

        # Graphics on top row
        ticker_len = graphics.DrawText(double_buffer, font, pos, 14, graphics.Color(255, 255, 255), ticker)

        # Graphics on bottom row
        price_len = graphics.DrawText(double_buffer, font, pos, 30, color, price)
        triangle_pos = pos + price_len + 5
        triangle_len = graphics.DrawText(double_buffer, font, triangle_pos, 30, color, triangle)

        change_pos = triangle_pos + triangle_len + 5
        change_len = graphics.DrawText(double_buffer, font, change_pos, 30, color, change)

        end_pos = change_pos + change_len
        return end_pos - pos    # Return the length of the entire drawing




    def run(self):
        md = MarketData()
        thread = md.load_tickers_background(self.tickers)
        thread.join()   # Wait for the thread to finish loading the data
        print(md.tickers_data)


        # self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        images = [Image.open(f"./images/{ticker.lower()}.ppm").convert('RGB') for ticker in self.tickers]
        # For graceful updating, we need a buffer that we load third_text into from the md tickers_data
        texts = md.tickers_data.copy()  # Initialize texts to the current market data. texts will be updated every minute.

        double_buffer = self.matrix.CreateFrameCanvas()

        # Text configuration
        font = graphics.Font()
        font.LoadFont("../../../fonts/8x13.bdf")
        textColor = graphics.Color(255, 255, 0)


        # Set up buffer
        idx = 0
        first_image = images[idx]
        second_image = images[(idx + 1) % len(images)]
        third_image = images[(idx + 2) % len(images)]
        first_text = texts[idx]
        second_text = texts[(idx + 1) % len(texts)]
        third_text = texts[(idx + 2) % len(texts)]


        # Refresh timer
        last_refresh_time = time.time()
        # Track last update time
        last_update_time = time.time()
        # Let's scroll!
        xpos = 0
        while True:
            current_time = time.time()

            if current_time - last_refresh_time >= 0.016:  # 60 seconds = 1 minute
                double_buffer.Clear()

                # TODO: Turn this into a for loop
                first_image_pos = xpos
                double_buffer.SetImage(first_image, first_image_pos)

                first_text_pos = first_image_pos + first_image.width + 5
                # first_text_len = graphics.DrawText(double_buffer, font, first_text_pos, 20, textColor, first_text)
                first_text_len = self.draw_ticker_and_price(double_buffer, first_text_pos, font, first_text)

                second_image_pos = first_text_pos + first_text_len + 20
                double_buffer.SetImage(second_image, second_image_pos)

                second_text_pos = second_image_pos + second_image.width + 5
                # second_text_len = graphics.DrawText(double_buffer, font, second_text_pos, 20, textColor, second_text)
                second_text_len = self.draw_ticker_and_price(double_buffer, second_text_pos, font, second_text)

                third_image_pos = second_text_pos + second_text_len + 20
                double_buffer.SetImage(third_image, third_image_pos)

                third_text_pos = third_image_pos + third_image.width + 5
                third_text_len = self.draw_ticker_and_price(double_buffer, third_text_pos, font, third_text)


                double_buffer = self.matrix.SwapOnVSync(double_buffer)

                if (second_image_pos == 0):
                    # Shift to the next image and text
                    idx = (idx + 1) % len(images)
                    first_image = images[idx]
                    second_image = images[(idx + 1) % len(images)]
                    third_image = images[(idx + 2) % len(images)]
                    first_text = texts[idx]
                    second_text = texts[(idx + 1) % len(texts)]
                    third_text = texts[(idx + 2) % len(texts)]

                    # Update the next immediate offscreen text to the corresponding ticker data
                    texts[(idx + 2) % len(texts)] = md.tickers_data[(idx + 2) % len(texts)]

                    xpos = 0
                xpos -= 1
                last_refresh_time = current_time
            
            if current_time - last_update_time >= 20:  # 60 seconds = 1 minute
                md.load_tickers_background(self.tickers)
                # print("Refreshed data")
                # print(md.tickers_data)
                last_update_time = current_time
                # Note: The new data will be available in md.tickers_data after a few seconds
            else:
                time.sleep(0.008)

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
