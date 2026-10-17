# Writes the fog capture scenes: one camera pose, the same three pairs of smoke emitters (additive on
# the left, premultiplied on the right): near the camera, in front of the hill and against the sky.
import sys
out = sys.argv[1]

BASE = """[scene name="{name}" version=1]

[entity id="sun"]
Light.type = 0
Light.color = (1, 0.96, 0.9)
Light.intensity = 100000
Light.intensityUnit = Lux
Light.castsShadows = true
Light.castsLight = true
Light.cascadeCount = 4
Name.value = "Sun"
Transform.position = (0, 10, 0)
Transform.rotation = (0.35, 0.27, -0.1, 0.89)
Transform.scale = (1, 1, 1)

[entity id="ambient"]
Light.type = 3
Light.color = (0.6, 0.65, 0.75)
Light.intensity = 14000
Light.intensityUnit = Lux
Name.value = "Ambient"
Transform.position = (0, 0, 0)
Transform.rotation = (0, 0, 0, 1)
Transform.scale = (1, 1, 1)

[entity id="sky"]
Name.value = "Sky Environment"
SkyEnvironment.Enabled = true
SkyEnvironment.Mode = 1
SkyEnvironment.GradientSkyTopColor = (0.2, 0.42, 0.78)
SkyEnvironment.GradientSkyHorizonColor = (0.6, 0.72, 0.86)
SkyEnvironment.GradientSkyBottomColor = (0.32, 0.3, 0.28)
SkyEnvironment.GradientSkyIntensity = 18000
SkyEnvironment.AutoSunMoon = false
SkyEnvironment.TimeOfDayDrivesSunLight = false
SkyEnvironment.SunLight = "sun"
Transform.position = (0, 0, 0)
Transform.rotation = (0, 0, 0, 1)
Transform.scale = (1, 1, 1)

[entity id="camera"]
Camera.enabled = true
Camera.fovY = 60
Camera.nearZ = 0.1
Camera.farZ = 3000
Camera.exposureControl = 1
Camera.manualExposureEV = 15.4
Name.value = "Main Camera"
Transform.position = (0, 110, -6)
Transform.rotation = (0.122, 0, 0, 0.9925)
Transform.scale = (1, 1, 1)

[entity id="terrain"]
Name.value = "Terrain"
Terrain.enabled = true
Terrain.sizeX = 512
Terrain.sizeZ = 512
Terrain.heightScale = 100
Terrain.patchGridSize = 128
Terrain.samplesPerMeter = 1
Terrain.lodRangeScale = 1
Terrain.renderLayerMask = 1
Terrain.castShadows = true
Terrain.receiveShadows = true
Transform.position = (0, 0, 0)
Transform.rotation = (0, 0, 0, 1)
Transform.scale = (1, 1, 1)

[entity id="post_fx"]
Name.value = "Post FX"
PostProcessVolume.enabled = true
PostProcessVolume.isGlobal = true
PostProcessVolume.weight = 1
PostProcessVolume.priority = 0
{effects}
Transform.position = (0, 0, 0)
Transform.rotation = (0, 0, 0, 1)
Transform.scale = (1, 1, 1)
{extra}"""

def emitter(id, name, material, pos, scale, emission=0.0):
    lines = [f'[entity id="{id}"]', f'Name.value = "{name}"',
             'ParticleEmitter3D.enabled = true',
             'ParticleEmitter3D.Stack = [path="Particles/Puff.particlestack"]',
             'ParticleEmitter3D.Amount = 500', 'ParticleEmitter3D.TicksPerSecond = 60',
             'ParticleEmitter3D.Seed = 1337',
             f'ParticleRenderer.Material = [path="Materials/{material}.material"]',
             f'ParticleRenderer.Texture = [path="Textures/{"PuffPremultiplied" if material == "Premultiplied" else "PuffStraight"}.png"]',
             'ParticleRenderer.InheritScale = true']
    if emission:
        lines += ['ParticleRenderer.EmissionColor = (1, 0.55, 0.2, 1)', f'ParticleRenderer.EmissionIntensity = {emission}']
    lines += [f'Transform.position = ({pos[0]}, {pos[1]}, {pos[2]})', 'Transform.rotation = (0, 0, 0, 1)',
              f'Transform.scale = ({scale}, {scale}, {scale})', '']
    return '\n'.join(lines)

def pairs(sky=(150, 200, 45, 7), emission=0.0, right='Premultiplied'):
    out = ''
    sy, sz, sx, ss = sky
    for tag, y, z, x, s in [('near', 108.5, 14, 3, 0.8), ('hill', 72, 170, 45, 6), ('sky', sy, sz, sx, ss)]:
        out += emitter(f'{tag}_add', f'{tag} additive', 'Additive', (-x, y, z), s, emission)
        out += '\n' + emitter(f'{tag}_pre', f'{tag} {right.lower()}', right, (x, y, z), s, emission) + '\n'
    return out

HEIGHT_FOG = """HeightFogEffect.Enabled = true
HeightFogEffect.Intensity = 1
HeightFogEffect.Density = 1
HeightFogEffect.MaxOpacity = 0.95
HeightFogEffect.DistanceFogEnabled = true
HeightFogEffect.MinDistance = 20
HeightFogEffect.SmoothLength = 100
HeightFogEffect.MaxDistance = 500
HeightFogEffect.HeightFogEnabled = false
HeightFogEffect.SkyEnabled = false"""

VOLUMETRIC_FOG = """VolumetricFogEffect.Enabled = true
VolumetricFogEffect.MaxDistance = 300
VolumetricFogEffect.Density = 0.015
VolumetricFogEffect.BaseHeight = 90
VolumetricFogEffect.HeightFalloff = 120
VolumetricFogEffect.NoiseEnabled = false"""

LIGHTS = ''.join(f"""[entity id="{id}"]
Name.value = "{id}"
Light.type = 1
Light.color = {col}
Light.intensity = {lm}
Light.intensityUnit = Lumen
Light.Range = 150
Transform.position = {pos}
Transform.rotation = (0, 0, 0, 1)
Transform.scale = (1, 1, 1)

""" for id, col, pos, lm in [('lamp_near', '(1, 0.6, 0.3)', '(0, 106, 20)', 3000000), ('lamp_far', '(0.4, 0.7, 1)', '(0, 85, 165)', 30000000)])

CLOUDS = """AtmosphericCloudLayer.Enabled = true
AtmosphericCloudLayer.FloorHeight = 250
AtmosphericCloudLayer.LayerDepth = 300
AtmosphericCloudLayer.SkyFill = 1
AtmosphericCloudLayer.VaporMass = 1
AtmosphericCloudLayer.Opacity = 1"""

GLOW = HEIGHT_FOG + """
HeightFogEffect.FogGlowEnabled = true
HeightFogEffect.FogGlowIntensity = 8
HeightFogEffect.FogGlowRadius = 8"""

scenes = {
    'NoFog': ('', pairs()),
    'HeightFog': (HEIGHT_FOG, pairs()),
    'VolumetricFog': (VOLUMETRIC_FOG, pairs() + LIGHTS),
    # The far pair above the cloud floor and beyond it, seen up through the layer.
    'Clouds': (CLOUDS, pairs(sky=(300, 900, 90, 22))),
    # Emission draws whole quads under the premultiplied material, so both glow emitters are additive.
    'FogGlow': (GLOW, pairs(emission=30.0, right='Additive')),
}
for name, (effects, extra) in scenes.items():
    text = BASE.format(name=name, effects=effects, extra='\n' + extra)
    if name == 'Clouds':
        # The cloud layer is lit from the physical sky.
        text = text.replace('SkyEnvironment.Mode = 1', 'SkyEnvironment.Mode = 0')
    open(f'{out}/{name}.scene', 'w').write(text)
