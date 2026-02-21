#pragma once

#include <string>
#include <memory>
#include <vector>
#include <rlottie.h>

class LottieEngine {
public:
    bool load_from_file(const std::string& path);
    bool load_from_data(const std::string& json);

    int total_frames() const;
    double duration() const;
    double frame_rate() const;

    int width() const;
    int height() const;

    void render(int frame, uint32_t* buffer, int w, int h);

private:
    std::shared_ptr<rlottie::Animation> animation_;
};