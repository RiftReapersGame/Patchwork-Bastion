import sys;sys.path.insert(0,'/home/claude/snd')
from lib import *
C='/home/claude/dl/CC0-Public-Domain-Sounds/'
K=C+'kenney_'
P={
 'lance':C+'Micro Pack - Organic Wooshes/Swish 3.wav','lance2':C+'Micro Pack - Organic Wooshes/Swish 5.wav',
 'thunk':C+'Micro Pack - Organic Wooshes/Thunk 1.wav','twirl':C+'Micro Pack - Organic Wooshes/Twirl Smol 2.wav',
 'puff':C+'100-cc0-sfx-2/sfx100v2_air_01.ogg','gust':C+'100-cc0-sfx-2/sfx100v2_air_02.ogg','gust3':C+'100-cc0-sfx-2/sfx100v2_air_03.ogg',
 'cannon1':C+'25-CC0-bang-sfx/cannon_01.ogg','cannon2':C+'25-CC0-bang-sfx/cannon_02.ogg','cannon3':C+'25-CC0-bang-sfx/cannon_03.ogg','cannon4':C+'25-CC0-bang-sfx/cannon_04.ogg','cannon5':C+'25-CC0-bang-sfx/cannon_05.ogg',
 'bang1':C+'25-CC0-bang-sfx/bang_01.ogg','bang2':C+'25-CC0-bang-sfx/bang_02.ogg','bang3':C+'25-CC0-bang-sfx/bang_03.ogg','bang4':C+'25-CC0-bang-sfx/bang_04.ogg','bang5':C+'25-CC0-bang-sfx/bang_05.ogg',
 'expl':C+'100-CC0-SFX/explosion.ogg',
 'splash1':C+'40-cc0-water-splash-slime-sfx/slime_03.ogg','splash2':C+'40-cc0-water-splash-slime-sfx/splash_02.ogg',
 'blade1':C+'80-CC0-RPG-SFX/blade_01.ogg','blade2':C+'80-CC0-RPG-SFX/blade_02.ogg','blade3':C+'80-CC0-RPG-SFX/blade_03.ogg',
 'chop':K+'rpgaudio/Audio/chop.ogg','creak':K+'rpgaudio/Audio/creak1.ogg','plank':K+'impactsounds/Audio/impactPlank_medium_000.ogg',
 'bell':K+'impactsounds/Audio/impactBell_heavy_000.ogg','bell2':K+'impactsounds/Audio/impactBell_heavy_002.ogg',
 'fire1':C+'80-CC0-RPG-SFX/spell_fire_01.ogg','fire2':C+'80-CC0-RPG-SFX/spell_fire_02.ogg','fire3':C+'80-CC0-RPG-SFX/spell_fire_03.ogg','fire4':C+'80-CC0-RPG-SFX/spell_fire_04.ogg','fire5':C+'80-CC0-RPG-SFX/spell_fire_05.ogg','fire6':C+'80-CC0-RPG-SFX/spell_fire_06.ogg','fire7':C+'80-CC0-RPG-SFX/spell_fire_07.ogg',
 'spell1':C+'80-CC0-RPG-SFX/spell_01.ogg','spell2':C+'80-CC0-RPG-SFX/spell_02.ogg',
 'ice1':K+'impactsounds/Audio/impactGlass_light_000.ogg','ice2':K+'impactsounds/Audio/impactGlass_light_002.ogg','ice3':K+'interfacesounds/Audio/glass_002.ogg',
 'gem':C+'80-CC0-RPG-SFX/item_gem_01.ogg','gem2':C+'80-CC0-RPG-SFX/item_gem_03.ogg',
 'rock1':C+'75-cc0-breaking-falling-hit-sfx/bfh1_rock_breaking_01.ogg','rock2':C+'75-cc0-breaking-falling-hit-sfx/bfh1_rock_breaking_02.ogg','mining':K+'impactsounds/Audio/impactMining_000.ogg',
 'rockfall1':C+'75-cc0-breaking-falling-hit-sfx/bfh1_rock_falling_01.ogg','rockfall2':C+'75-cc0-breaking-falling-hit-sfx/bfh1_rock_falling_03.ogg','rockfall3':C+'75-cc0-breaking-falling-hit-sfx/bfh1_rock_falling_05.ogg',
 'woodbreak':C+'75-cc0-breaking-falling-hit-sfx/bfh1_wood_breaking_01.ogg','woodbreak2':C+'100-CC0-wood-metal-SFX/wood_breaking_01.ogg',
 'stomp':C+'80-CC0-creature-sfx-2/stomp_01.ogg','punch':K+'impactsounds/Audio/impactPunch_heavy_000.ogg',
 'roar1':C+'80-CC0-RPG-SFX/creature_roar_01.ogg','roar2':C+'80-CC0-RPG-SFX/creature_roar_02.ogg','roar3':C+'80-CC0-RPG-SFX/creature_roar_03.ogg','roar4':C+'80-CC0-creature-sfx-2/roar_04.ogg','roar5':C+'80-CC0-creature-SFX/roar_01.ogg',
 'grunt1':C+'80-CC0-creature-SFX/grunt_01.ogg','grunt2':C+'80-CC0-creature-SFX/grunt_02.ogg','grunt3':C+'80-CC0-creature-SFX/grunt_03.ogg','grunt4':C+'80-CC0-creature-SFX/grunt_04.ogg','grunt5':C+'80-CC0-creature-SFX/grunt_05.ogg',
 'hurt1':C+'80-CC0-creature-SFX/hurt_01.ogg','hurt2':C+'80-CC0-creature-SFX/hurt_02.ogg','hurt3':C+'80-CC0-creature-SFX/hurt_03.ogg','hurt4':C+'80-CC0-creature-SFX/hurt_04.ogg','hurt5':C+'80-CC0-creature-SFX/hurt_05.ogg',
 'cdie1':C+'80-CC0-creature-sfx-2/die_01.ogg','cdie2':C+'80-CC0-creature-sfx-2/die_02.ogg','cdie3':C+'80-CC0-creature-sfx-2/die_03.ogg','cdie4':C+'80-CC0-creature-sfx-2/die_04.ogg','cdie5':C+'80-CC0-RPG-SFX/creature_die_01.ogg',
 'troll1':C+'80-CC0-creature-SFX/troll_01.ogg','troll2':C+'80-CC0-creature-SFX/troll_02.ogg','troll3':C+'80-CC0-creature-SFX/troll_03.ogg',
 'cute3':C+'80-CC0-creature-SFX/cute_03.ogg','bug2':C+'80-CC0-creature-SFX/bug_02.ogg','bug5':C+'80-CC0-creature-sfx-2/bug_05.ogg','cmisc2':C+'80-CC0-RPG-SFX/creature_misc_02.ogg','att1':C+'80-CC0-creature-sfx-2/attack_01.ogg','att2':C+'80-CC0-creature-sfx-2/attack_02.ogg',
 'wing':C+'Micro Pack - Organic Wooshes/Gentle Swish.wav',
 'dshuf':K+'casinoaudio/Audio/dieShuffle1.ogg','dshuf2':K+'casinoaudio/Audio/dieShuffle2.ogg','dthrow':K+'casinoaudio/Audio/dieThrow1.ogg','dthrow2':K+'casinoaudio/Audio/dieThrow2.ogg',
 'cfan':K+'casinoaudio/Audio/cardFan1.ogg','cslide':K+'casinoaudio/Audio/cardSlide1.ogg','cslide2':K+'casinoaudio/Audio/cardSlide3.ogg','cplace':K+'casinoaudio/Audio/cardPlace1.ogg','cplace2':K+'casinoaudio/Audio/cardPlace3.ogg','cshove':K+'casinoaudio/Audio/cardShove2.ogg','cshuffle':K+'casinoaudio/Audio/cardShuffle.ogg',
 'latch':K+'rpgaudio/Audio/metalLatch.ogg','coins':K+'rpgaudio/Audio/handleCoins.ogg','coins2':K+'rpgaudio/Audio/handleCoins2.ogg',
 'coin1':C+'80-CC0-RPG-SFX/item_coins_01.ogg','coin2':C+'80-CC0-RPG-SFX/item_coins_02.ogg','coin3':C+'80-CC0-RPG-SFX/item_coins_03.ogg','coin4':C+'80-CC0-RPG-SFX/item_coins_04.ogg',
 'chip1':K+'casinoaudio/Audio/chipLay1.ogg','chip2':K+'casinoaudio/Audio/chipsCollide1.ogg',
 'click':K+'interfacesounds/Audio/click_002.ogg','select':K+'interfacesounds/Audio/select_002.ogg','confirm':K+'interfacesounds/Audio/confirmation_002.ogg','back':K+'interfacesounds/Audio/back_002.ogg','err':K+'interfacesounds/Audio/error_004.ogg',
 'book':K+'rpgaudio/Audio/bookFlip2.ogg','gong':C+'100-CC0-SFX/gong_01.ogg','gong2':C+'100-CC0-SFX/gong_02.ogg','bellA':C+'100-CC0-SFX/bell_01.ogg','bellB':C+'100-CC0-SFX/bell_02.ogg',
 'chime':K+'interfacesounds/Audio/glass_005.ogg','hammer':C+'100-CC0-wood-metal-SFX/hammer_01.ogg','hammer2':C+'100-CC0-wood-metal-SFX/wood_hammer_01.ogg',
 'thunder':C+'100-cc0-sfx-2/sfx100v2_thunder_01.ogg','glitch':K+'interfacesounds/Audio/glitch_002.ogg',
 'metalfall':C+'75-cc0-breaking-falling-hit-sfx/bfh1_metal_falling_01.ogg','hit7':C+'75-cc0-breaking-falling-hit-sfx/bfh1_hit_07.ogg',
}
import json
for k,v in P.items():
    try:
        a=load(v);d,pk,r=stats(a);print(f'{k:10s} {d:6.2f}s pk{pk:6.1f} rms{r:6.1f}')
    except Exception as e:print(k,'ERR',e)
json.dump(P,open('/home/claude/snd/P.json','w'))
