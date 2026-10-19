# Captures for Game-Crafters-Guild/OpenEngine#35

BC7 from the texture cook, `main` (DirectXTex's full search) against the branch (bc7e's `slow` preset). Each texture's base level was encoded by the engine's own `CompressTextureCookLevel` at `TextureCookEncodeQuality::Full` (banding and `RepairBC7TransparentEndpoints` included, no worker pool, so one thread), then decoded by the engine's `DecodeBlockPayloadRGBA8`. One scratch program, built against each arm's `Engine` with the flags of `EngineTextureTests`.

- `main`: 89224a2. Branch: a23a228 (the encode is unchanged at the later fold commits).
- Linux (Fedora 44, GCC 16, DebugFast, `linux-x64-local`). DirectXTex and basisu are vcpkg Release builds in both arms.
- The sources are textures that ship in this repository (paths below), so the captures carry no third-party game content.

## Images

- `captures/<texture>-main-vs-head.png`: source, `main`, branch, then each arm's RGB error against the source multiplied by 8. Colour tiles are composited over 50% grey for display; the error tiles compare raw RGB, so texels with alpha 0 (whose RGB the encoders may change freely) show at leaf edges.
- `captures/<texture>-crop.png`: the centre 128 x 128 texels of source, `main` and branch at 3x, nearest-neighbour.

## Results

PSNR against the source; alpha only for textures that carry alpha.

| Texture (source path) | Size | main ms | branch ms | main RGB dB | branch RGB dB | main alpha dB | branch alpha dB |
|---|---|---|---|---|---|---|---|
| oak_color (`Packages/eztree/Assets/Textures/EZTree/leaves/oak_color.png`) | 512x512 | 14943 | 119 | 36.14 | 37.95 | 34.77 | 38.46 |
| aspen_color (`Packages/eztree/Assets/Textures/EZTree/leaves/aspen_color.png`) | 512x512 | 12306 | 69 | 36.17 | 37.79 | 34.69 | 38.99 |
| pine_color (`Packages/eztree/Assets/Textures/EZTree/leaves/pine_color.png`) | 512x512 | 16229 | 106 | 36.34 | 38.05 | 33.79 | 38.12 |
| oak_color_1k (`Packages/eztree/Assets/Textures/EZTree/bark/oak_color_1k.jpg`) | 512x512 | 30448 | 314 | 45.81 | 46.45 | - | - |
| moon_full (`Engine/Assets/Textures/Sky/MoonPhases/moon_full.png`) | 1024x1024 | 78917 | 777 | 49.43 | 50.81 | 49.02 | 48.53 |
| crest_foam (`Apps/Editor/Assets/Examples/Materials/Ocean/crest_foam.png`) | 450x450 | 20057 | 238 | 51.66 | 53.46 | - | - |
| lensDirt1 (`Engine/Assets/Textures/Bloom/lensDirt1.png`) | 1920x1080 | 278937 | 2707 | 47.03 | 47.47 | - | - |

The branch is ahead on RGB PSNR for every texture (+0.44 to +1.81 dB) and on alpha for the three leaf textures (+3.7 to +4.3 dB); on `moon_full` its alpha is 0.49 dB behind.
