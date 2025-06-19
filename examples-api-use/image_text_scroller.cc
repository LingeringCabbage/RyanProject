#include "led-matrix.h"
#include "graphics.h"
#include <iostream>
#include <unistd.h>
#include <string>

using namespace rgb_matrix;

class ImageAndTextScroller {
public:
    ImageAndTextScroller(RGBMatrix *matrix, int spacing)
        : matrix_(matrix), spacing_(spacing) {
        canvas_ = matrix->CreateFrameCanvas();
    }

    bool LoadPPM(const char *filename) {
        std::cout << "Displaying PPM image: " << filename << std::endl;
        
        FILE *f = fopen(filename, "rb");
        if (!f) {
            std::cerr << "Error: Could not open " << filename << std::endl;
            return false;
        }
        fclose(f);

        usleep(2000000);  // Simulating image display for 2 seconds
        return true;
    }

    void ScrollText(const std::string &text, const Color &color) {
        Font font;
        if (!font.LoadFont("fonts/7x13.bdf")) {
            std::cerr << "Failed to load font" << std::endl;
            return;
        }

        int x_pos = matrix_->width();  // Start text off-screen
        while (x_pos + text.length() * 7 > 0) {
            canvas_->Clear();
            
            // Draw text
            DrawText(canvas_, font, x_pos, 10, color, nullptr, text.c_str(), 0);

            canvas_ = matrix_->SwapOnVSync(canvas_);
            usleep(50000);
            --x_pos;
        }
    }

    void Run(const char *image_file, const std::string &text, const Color &color) {
        if (LoadPPM(image_file)) {
            usleep(spacing_ * 100000);  // Adjust spacing delay
            ScrollText(text, color);
        }
    }

private:
    RGBMatrix *matrix_;
    FrameCanvas *canvas_;
    int spacing_;
};

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <image.ppm> <text> <spacing>" << std::endl;
        return 1;
    }

    const char *image_file = argv[1];
    std::string text = argv[2];
    int spacing = std::stoi(argv[3]);

    // Matrix options
    RGBMatrix::Options options;
    options.rows = 32;
    options.cols = 64;
    options.chain_length = 1;
    options.hardware_mapping = "regular";  // Modify if using different hardware

    // Runtime options (Fix for the error)
    rgb_matrix::RuntimeOptions runtime_options;
    
    // Corrected call with two arguments
    RGBMatrix *matrix = RGBMatrix::CreateFromOptions(options, runtime_options);
    if (!matrix) {
        std::cerr << "Matrix initialization failed" << std::endl;
        return 1;
    }

    ImageAndTextScroller scroller(matrix, spacing);
    scroller.Run(image_file, text, Color(255, 0, 0));

    delete matrix;
    return 0;
}
