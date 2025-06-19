import time
import sys
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def display_image(image_path):
    options=RGBMatrixOptions()
    options.rows=32
    options.cols=64
    options.chain_length=2
    options.parallel=1
    options.hardware_mapping='adafruit-hat'
    
    matrix=RGBMatrix(options=options)
    
    try:
        image= Image.open(image_path)
        
        image=image.resize((128,32), Image.Resampling.LANCZOS)
        
        if image.mode != 'RGB':
            image=image.convert('RGB')
            
            matrix.SetImage(image)
            
            print("Press Ctrl-C to Stop.")
            
            while True:
                time.sleep(100)
                
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python display_image.py <path_to_image>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    display_image(image_path)
        