# Captures for Game-Crafters-Guild/OpenEngine#30

Particles fogging themselves after the fog passes. Each scene was rendered by the Player built from
`main` at 89224a2 and from `fix/particle-fog`, on Linux (Fedora 44, GCC 16, Debug,
`linux-x64-local`), windowed at 1280x720 with `--screenshot` after 400 warm-up frames
(`GE_SCREENSHOT_WARMUP_FRAMES=400`). The particles are simulated in real time, so their exact
positions differ a little between runs.

`captures/<scene>-main-vs-head.png` stacks `main` (top) over the branch (bottom).

## Pose (every capture)

- Camera position (0, 110, -6), rotation quaternion (x, y, z, w) = (0.122, 0, 0, 0.9925): about 14
  degrees below the horizon, looking along +Z.
- Vertical field of view 60 degrees, near 0.1, far 3000; manual exposure, EV100 15.4.

## Emitters (every scene)

Pairs of smoke emitters (`project/Assets/Particles/Puff.particlestack`): the left of each pair
additive (`Materials/Additive.material`: SrcAlpha, One), the right premultiplied
(`Materials/Premultiplied.material`: One, OneMinusSrcAlpha, with a premultiplied texture).

- Near: (-3 / 3, 108.5, 14), about 20 m from the camera.
- Hill: (-45 / 45, 72, 170), in front of the terrain.
- Sky: (-45 / 45, 150, 200), against the sky (Clouds: (-90 / 90, 300, 900), above the cloud floor).

## Scenes

- HeightFog: distance-only height fog, min distance 20, smooth length 100, max distance 500,
  density 1, max opacity 0.95, sky fog off.
- VolumetricFog: global volumetric fog, max distance 300, density 0.015, base height 90, falloff
  120, no noise; a warm point light by the near pair and a blue one by the hill pair.
- Clouds: atmospheric cloud layer, floor 250, depth 300, sky fill 1, physical sky.
- FogGlow: the height fog with fog glow at intensity 8, radius 8; both emitters of each pair
  additive with emission 30.

`project/make_scenes.py <dir>` writes the scenes; `project/<scene>.config` opens each one:

```
Player --config <scene>.config --asset-root project/Assets --screenshot out.png
```
