#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "lottie_engine.h"

namespace py = pybind11;

PYBIND11_MODULE(_pylottie, m) {
    py::class_<LottieEngine>(m, "LottieEngine")
        .def(py::init<>())
        .def("load_from_file", &LottieEngine::load_from_file)
        .def("load_from_data", &LottieEngine::load_from_data)
        .def("total_frames", &LottieEngine::total_frames)
        .def("duration", &LottieEngine::duration)
        .def("frame_rate", &LottieEngine::frame_rate)
        .def("width", &LottieEngine::width)
        .def("height", &LottieEngine::height)
        .def("render_rgba", [](LottieEngine& eng, int frame, int w, int h) {
            py::array_t<uint8_t> out({ h, w, 4 });
            auto buf = out.mutable_unchecked<3>();

            std::vector<uint32_t> tmp(w * h);
            eng.render(frame, tmp.data(), w, h);

            for (int y = 0; y < h; y++) {
                for (int x = 0; x < w; x++) {
                    uint32_t p = tmp[y * w + x];
                    buf(y,x,0) = (p >> 16) & 0xFF;
                    buf(y,x,1) = (p >> 8) & 0xFF;
                    buf(y,x,2) = p & 0xFF;
                    buf(y,x,3) = (p >> 24) & 0xFF;
                }
            }
            return out;
        });
}