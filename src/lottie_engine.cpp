#include "lottie_engine.h"
#include <fstream>
#include <sstream>

static std::string read_file(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    if (!f) return {};
    std::ostringstream ss;
    ss << f.rdbuf();
    return ss.str();
}

bool LottieEngine::load_from_file(const std::string& path) {
    std::string json = read_file(path);
    if (json.empty()) return false;

    animation_ = rlottie::Animation::loadFromData(json, "", "");
    return animation_ != nullptr;
}

bool LottieEngine::load_from_data(const std::string& json) {
    if (json.empty()) return false;

    animation_ = rlottie::Animation::loadFromData(json, "", "");
    return animation_ != nullptr;
}

int LottieEngine::total_frames() const {
    return animation_ ? animation_->totalFrame() : 0;
}

double LottieEngine::duration() const {
    return animation_ ? animation_->duration() : 0.0;
}

double LottieEngine::frame_rate() const {
    return animation_ ? animation_->frameRate() : 0.0;
}

int LottieEngine::width() const {
    if (!animation_) return 0;
    size_t w, h;
    animation_->size(w, h);
    return (int)w;
}

int LottieEngine::height() const {
    if (!animation_) return 0;
    size_t w, h;
    animation_->size(w, h);
    return (int)h;
}

void LottieEngine::render(int frame, uint32_t* buffer, int w, int h) {
    if (!animation_ || !buffer) return;

    rlottie::Surface surface(buffer, w, h, w * 4);
    animation_->renderSync(frame, surface);
}