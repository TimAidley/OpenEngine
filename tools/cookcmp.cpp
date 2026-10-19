// Scratch: encode each input's base level through the engine's own BC7 cook path
// (CompressTextureCookLevel at the full quality, banding and endpoint repair included),
// decode it back with the engine's decoder, and write the decoded RGBA8 as PNG.
// Usage: cookcmp <out-dir> <image>...
#include "Assets/TextureCook.h"

#include <chrono>
#include <cstdio>
#include <filesystem>
#include <string>
#include <vector>

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include <stb_image.h>
#include <stb_image_write.h>

using namespace GameEngine;

int main(int argc, char** argv)
{
    if (argc < 3)
        return 2;
    const std::filesystem::path outDir = argv[1];
    std::filesystem::create_directories(outDir);
    for (int i = 2; i < argc; ++i)
    {
        int w = 0, h = 0, n = 0;
        uint8_t* pixels = stbi_load(argv[i], &w, &h, &n, 4);
        if (!pixels)
            continue;
        TextureCookMipLevel level;
        level.Width = static_cast<uint32>(w);
        level.Height = static_cast<uint32>(h);
        level.Bytes.assign(pixels, pixels + static_cast<size_t>(w) * h * 4);
        stbi_image_free(pixels);

        std::vector<uint8> payload;
        std::string error;
        const auto t0 = std::chrono::steady_clock::now();
        const bool ok = CompressTextureCookLevel(level, false, TextureCookOutput::BC7, 0, payload, error, {},
                                                 TextureCookEncodeQuality::Full, nullptr);
        const double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        std::vector<uint8> decoded;
        if (!ok || !DecodeBlockPayloadRGBA8(TextureFormat::BC7, level.Width, level.Height, payload.data(),
                                            payload.size(), decoded))
        {
            std::fprintf(stderr, "%s: %s\n", argv[i], error.c_str());
            continue;
        }
        const std::string stem = std::filesystem::path(argv[i]).stem().string();
        stbi_write_png((outDir / (stem + ".png")).string().c_str(), w, h, 4, decoded.data(), w * 4);
        std::printf("%s,%d,%d,%.1f\n", stem.c_str(), w, h, ms);
    }
}
