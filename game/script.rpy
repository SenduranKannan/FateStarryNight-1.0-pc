# The script of the game goes in this file.
init:

    image gframefar:
        "gframe.png"
        zoom .5

    python:

        import math

        class Shaker(object):

            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }

            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                #
                self.start = [ self.anchors.get(i, i) for i in start ]  # central position
                self.dist = dist    # maximum distance, in pixels, from the starting point
                self.child = child

            def __call__(self, t, sizes):
                # Float to integer... turns floating point numbers to
                # integers.
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x

                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

                xpos = xpos - xanchor
                ypos = ypos - yanchor

                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

                return (int(nx), int(ny), 0, 0)

        def _Shake(start, time, child=None, dist=100.0, **properties):

            move = Shaker(start, child, dist=dist)

            return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

        Shake = renpy.curry(_Shake)
    #

    transform my_shake:
        linear 0.1 xoffset -2 yoffset 2
        linear 0.1 xoffset 3 yoffset -3
        linear 0.1 xoffset 2 yoffset -2
        linear 0.1 xoffset -3 yoffset 3
        linear 0.1 xoffset 0 yoffset 0
        repeat

#


# Declare characters used by this game. The color argument colorizes the
# name of the character.

define sinny = Character("Sinmara")
define sinn = Character("Beauty In Red")
define aratron = Character("Aratron")
define ara = Character("Handsome Gent")
define npc = Character("???")
define alert = Character("Mysterious Voice")
define gframe = Character("G-Frame")
image bg slums = "images/bg_slums.png"
image splash = "images/splash.png"
image m_menu = "gui/main_menu.png"
define flash = Fade(0.5, 1.0, 0.5, color="#FFFFFF")
define fadehold = Fade(0.5, 1.0, 0.5)
define wipeleftfast = CropMove(0.25, "wipeleft")
define sshake = Shake((0, 0, 0, 0), 1.0, dist=15)
define eyeopen = ImageDissolve("fx/eyeopen.png", 1.5, 100)
define eyeclose = ImageDissolve("fx/eyeopen.png", 1.5, 100, reverse=True)


# The game starts here.

label splashscreen:
    scene black
    with Pause(1)

    show splash with dissolve
    with Pause(2)
    scene black with dissolve
    with Pause(2)
    show m_menu with dissolve

    return

label start:

    show m_menu:
        ease 1 zoom 1.5
    scene black with fade
    with Pause(2)
    stop music fadeout 1.0
    $ renpy.movie_cutscene("initialize.webm")
    with Pause(3)

    scene bg_streets with flash
    play music "audio/Dark Clouds To Clear.mp3" volume 0.5

    menu:
        "Huh? What is this place?":
            jump choice1

        "...Am I dreaming again?":
            jump choice1

    # These display lines of dialogue.

    label choice1:
        $ menu_flag = True
        play sound "audio/robot.mp3" volume 0.5
        with Pause(2)

    menu:
        "...What was that?":
            jump choice2

    label choice2:
        $ menu_flag = True
        play sound "audio/robot.mp3" volume 0.5
        with Pause(2)
        play sound "audio/robot.mp3" volume 0.25
        with Pause(2)
        play sound "audio/robot.mp3" volume 0.1
        with Pause(2)

    menu:
        "...The sound disappeared.":
            with Pause(1)
            jump choice3


    label choice3:
        $ menu_flag = True

    menu:
        "Should I follow it?":
            jump choice4a

        "Best to avoid that.":
            jump choice4b

    label choice4a:
        $ menu_flag = True
        "Maybe it's still nearby."
        jump choice5

    label choice4b:
        $ menu_flag = True
        "That sounded dangerous. Better to go the other way."
        jump choice5

    label choice5:
        play sound "audio/footsteps.mp3"
        scene bg_streets2 with fadehold
        with Pause(2)
        "I walk, and walk, and walk.{w=0.5} But no matter what I do,
        I never seem to be able to escape this concrete prison."
        "It's bright, starry buildings for miles. By the time I realize this, I am panting and thirsty."
        "I can only say one thing."
    menu:
        "This place is {b}HUGE!{/b}":
            jump choice6

    label choice6:
        show bg_streets2:
            ease 1 yalign 0.0
        with Pause(3)
        show bg_streets2:
            ease 1 xalign 0.0
        with Pause(2)
    menu:
        "The lights are on, but there's no one inside?":
            show bg_streets2:
                ease 1 truecenter
            jump choice7

    label choice7:
        "I feel worried all of a sudden. This city looks homely. Lively. Yet
        I can't see anyone around the streets."
        "All I can hear are weird, mechanical noises."
        window hide
        play sound "audio/robot.mp3" volume 0.5
        with Pause(2)
        window show
        "Again, that weird noise. I don't know where it's coming from, but
        it's definitely getting closer."
        "Maybe I should move."
        play music "audio/siren.mp3" volume 0.5 fadeout 1
        window hide
        with Pause(2)

    menu:
        "Huh?":
            jump choice8

    label choice8:
        window show
        alert "Attention, visitors. The Virtual Holy Grail War will commence in T-minus 30 seconds."
        alert "You have 72 hours to locate the Holy Grail and destroy it. Failure to do so will result in
        {b}immediate{/b} termination."
        alert "Whether you fight, or kill, to accomplish your objective, it is none of our concern."
        alert "Those who do not fight will not survive."
        alert "Ending transmission."
        window hide
        with Pause(2)

    menu:
        "Did they just say...":
            jump choice9

    label choice9:
    menu:
        "{b}A Holy Grail War?{/b}":
            jump choice10

    label choice10:
        play sound "audio/robot.mp3" volume 0.5
        with Pause(1)
        "I hear mechanical steps behind me.{w=1} I shudder as I take a deep breath and turn around."
        play sound "audio/robot.mp3" volume 0.75
        window hide
        with Pause(1)
        show gframe with dissolve
        play sound "audio/robot.mp3"
        with Pause(1)

    menu:
        "What the...":
            jump choice11

    label choice11:
        play sound "audio/robot.mp3" volume 0.5
        window show
        gframe "{cps=20}Participate...Participate in the Grail War.{/cps}"
        gframe "{cps=20}Kill as many as you want.{w=1} Burn the city to ashes.{w=1}{/cps}"
        gframe "{cps=20}If you do not...{/cps}"
        with Pause(1)
        window hide
        hide gframe with dissolve
        play sound "audio/robot.mp3"
        show gframe2 with dissolve
        play music "audio/Enemy.mp3" volume 0.5 fadein 1
        gframe "{b}EXTERMINATE!{/b}"
        window hide

    menu:
        "?!?!?":
            play sound "audio/punch.mp3" volume 0.5
            show gframe2 with sshake
            with Pause(0.3)
            play sound "audio/punch.mp3" volume 0.5
            show gframe2 with sshake
            with Pause(0.3)
            play sound "audio/punch.mp3" volume 0.5
            hide gframe2 with sshake and dissolve
            with Pause(0.3)
            jump choice12

    label choice12:

    menu:
        "Ow!":
            jump choice13

        "These robots mean business!":
            jump choice13

    label choice13:
        play sound "audio/running.mp3"
        scene bg_streets with fadehold
        window show
        "I run. I run as fast as I can. Not only did these robots almost give me
        a heart attack, but they slapped me around like a ragdoll."
        "Of course, that's why I couldn't avoid them. If I can't even fight back, what hopes do I have of running away?"
        window hide
        with Pause(1)
        play sound "audio/robot.mp3"
        show gframe at right with dissolve
        with Pause(1)
        play sound "audio/robot.mp3"
        show gframe as grunt1 at left with dissolve
        with Pause(2)
        play sound "audio/robot.mp3"
        show gframe as grunt2 at center with dissolve

    menu:
        "Crap! I'm surrounded!":
            play sound "audio/robot.mp3"
            window show
            gframe "{b}OBLITERATE! OBLITERATE!{/b}"
            with Pause(0.2)
            "It seems hopeless to even run. They block my path like stone walls.
            All I see around me are just robots."
            window hide
            with Pause(1)
            hide gframe as grunt1
            hide gframe as grunt2
            hide gframe
            with dissolve
            with Pause(0.5)
            show gframe2 with dissolve
            window show
            gframe "{b}EXTERMINATE!{/b}"
            jump choice14

    label choice14:
        play sound "audio/uzi.mp3"
        show bg_streets with sshake
        play sound "audio/blood.mp3"
        with Pause(0.3)
        show blood with dissolve and sshake
        hide blood with dissolve
        "What...?" with fadehold
        with Pause(0.3)
        "They even have guns inside them...It hurts."
        with Pause(0.3)
        "I can see my blood pooling down on the floor." with fade
        "Great, now I'm even blacking out..."
        with Pause(0.3)
        window hide
        play sound "audio/robot.mp3"
        scene black with fadehold
        with Pause(1)
        stop music fadeout 2.0
        with Pause(1)

    menu:
        "Guess I'm screwed.":
            npc "Hey, you."
            npc "What are you moping around for?"
            npc "At least blow up a few of these suckers before you die."
            "Cocky, boisterious words fill my ears as I hear someone approach this disastrous scene."
            "They sound spiteful, maybe even angry. Were they really expecting me to take on so many bots at once?!"
            "I hear them sigh, as if their patience has run dry."
            with Pause(1)
            npc "Ugh, whatever.{w=1} Just piss off unless you want to get burned too, small fry."
            with Pause(1)
            "Before I can even react, I hear something sizzle..."
            $ renpy.movie_cutscene("sinny_blast.webm")
            play music "audio/Sinmara.ogg" volume 0.5 fadeout 1 loop
            window hide
            show bg_streetsfire with flash
            with Pause(2)
            jump choice15

    label choice15:

    menu:
        "....What the hell happened here?!":
            play sound "audio/robot.mp3"
            show gframe with dissolve
            with Pause(0.3)
            play sound "audio/explosion.mp3"
            show explosion with dissolve and sshake
            hide gframe with dissolve
            hide explosion with dissolve
            with Pause(0.5)
            "The robots that stood in front of me start falling down like molasses. Giant, flaming meteors crash down on their bodies."
            "I can see their corpses in a crater, melting away like ice cream."
            with Pause(1)
            npc "Wow, that's all it took? You heaps of scrap are nothing but junk.{w=1} Back in my day, trees burned {b}better{/b} than you!"
            window hide
            hide gframe with dissolve
            play sound "audio/footsteps.mp3"
            show sinnyblack with dissolve
            "The fierce woman reveals herself to me, but I can barely see her through the smoke and ashes. She looks thin. Petite, even. But if that is the case,"
            "...why does she feel taller than me?"
            with Pause(1)
            npc "Are ya done ogling yet?{w=1} I can see you, ya know..."
            "Her words alone convey her killing intent perfectly. I gulp and step away, worried that she might kill me for funsies."
            hide sinnyblack with dissolve
            show sinny with dissolve
            with Pause(2)
            sinn "Not dead yet? I'm surprised. Nothing worth destroying though, unfortunately."
            "Destroying?{w=0.5} Me?"
            "The chills that run down my spine simply get colder."
            window hide
            play sound "audio/robot.mp3"
            hide sinny with dissolve
            show bg_streetsfire:
                ease 1 xalign 0.75 yalign 0.5
            with Pause(1)
            play sound "audio/robot.mp3"
            show gframe:
                xalign 0.75
                yalign 0.5
                zoom 0.3

            show gframe as thug1:
                xalign 0.25
                yalign 0.5
                zoom 0.3

            show gframe as thug2:
                xalign 0.5
                yalign 0.5
                zoom 0.3
            with dissolve
            with Pause(1)

    menu:
        "There's more of them!":
            show bg_streetsfire
            show sinny with dissolve
            sinn "Yeah, yeah, yeah!{w=0.2} That's what I'm talking about! Come add fuel to the fire, you oversized toasters!"
            "She doesn't seem to be worried about it at all..."
            window hide
            hide gframe
            hide thug1
            hide thug2
            hide sinny
            with dissolve
            show bg_streetsfire:
                ease 1 xalign 0.75 yalign 0.5
            play sound "audio/robot.mp3"
            show gframe2 with dissolve
            with Pause(1)
            play sound "audio/explosion.mp3"
            show explosion with dissolve and sshake
            hide explosion with dissolve
            with Pause(0.3)
            play sound "audio/crash.wav"
            hide gframe2 with moveoutbottom
            with Pause(0.5)

    menu:
        "'Holy SHIT!'":
            jump choice16
        "'You're packing heat!'":
            jump choice16

    label choice16:
        show sinny with dissolve
        sinn "Oh. Good to know you aren't mute, twerp. Did you have stage fright before or something?"
        window hide
        play sound "audio/robot.mp3"
        show gframe2 behind sinny with dissolve
        with Pause(0.5)
        hide sinny with dissolve
        play sound "audio/slash.mp3"
        show slash with dissolve
        hide slash with dissolve
        with Pause(0.3)
        play sound "audio/crash.wav"
        hide gframe2 with moveoutbottom
        with Pause(0.5)
        show sinny with dissolve
        sinn "{cps=20}AhahaHAHAHAHAHAHAH!{/cps}"
        sinn "Keep 'em coming! I'll grind you all to bits! Holy Grail War? More like a slaughterhouse just for me!"
        "{b}'Wait, you know about the Holy Grail War?'{/b}"
        sinn "Uh, duh? Everybody does. Didn't you hear the announcement? Now shut up."
        window hide
        hide sinny with dissolve
        play sound "audio/robot.mp3"
        show gframe
        show gframe as thug1 at left
        show gframe as thug2 at right
        with dissolve
        play sound "audio/slash.mp3"
        show slash with dissolve
        hide slash with dissolve
        with Pause(0.1)
        play sound "audio/explosion.mp3"
        show explosion with dissolve and sshake
        hide explosion with dissolve
        with Pause(0.1)
        play sound "audio/crash.wav"
        hide gframe
        hide thug1
        hide thug2
        with moveoutbottom
        with Pause(0.5)

    menu:
        "She's chewing through them like tissue paper...":
            show sinny with dissolve
            sinn "Is that all you've got?!{w=0.5} The modern age really is soft, huh?"
            "She casts me a glance while saying that."
            window hide
            hide sinny with dissolve
            show bg_streetsfire
            play sound "audio/explosion.mp3"
            with Pause(1)
            play sound "audio/crash.wav"
            "She keeps mowing down hordes of robots with slashes alone. Her sword melts her opponents with the greatest of ease. I'm witnessing a one-sided slaughter."
            scene bg_sword1 with fade
            "Her weapon is that clunky looking sword. Despite how rough and heavy it looks, she easily spins it around like a piece of string."
            "Anytime she slashes, chunks of fire and magma are spit out. Those bots stand no chance."
            scene bg_sword2 with fade
            "And let's not forget about the blade itself. She just cleaved four robots in half with one slash. Then she proceeded to stab them like a shish kebab."
            "But there's something else about it. That sword feels{w=0.3}...familiar, somehow. Have I met this woman before?"
            "Fact stands that I have a good idea on what she is."
            window hide
            scene bg_streetsfire with fade
            show sinny with dissolve
    menu:
        "'You're a Servant, aren't you?'":
            "She glances at me with a bored look."
            sinn "What about it? Does being a Servant prevent me from being so {b}kickass?{/b}"
            sinn "The hell are you supposed to be anyway?"
            "As she asks me that, I glance down to my body and take a good look."
            "My bullet wounds have healed. I barely even feel the pain anymore."
            "Wait,{w=0.2} am I-"
            jump stopmusic

    label stopmusic:
         stop music fadeout 2.0
         hide sinny with dissolve
         window hide
         play sound "audio/crash.wav"
         with Pause(1)
         play sound "audio/explosion.mp3"
         show sinny with dissolve
         sinn "Awww, c'mon now! This is getting boring. Are you just going to keep sending the same crappy golems at-"
         window hide
         play sound "audio/heavypunch.mp3"
         hide sinny with moveoutleft
         sinn "OWWWWWWWWWW!"
         with Pause(0.3)
         window hide

    menu:
        "What the-?!":
            jump choice17

        "'Are you alright?'":
            jump choice17

    label choice17:
        play sound "audio/robofeet.mp3"
        show bg_streetsfire with sshake
        with Pause(2.3)
        show bg_streetsfire with sshake
        with Pause(2)
        show bg_streetsfire with sshake
        with Pause(2)
        show ggolem with dissolve and sshake
        with Pause(1)
        play music "audio/Battle.mp3" volume 0.5 fadeout 1 loop
        play sound "audio/robot.mp3"
        gframe "{b}EXTERMINATE.{/b}"
        window hide

    menu:
        "This looks bad!":
            play sound "audio/heavypunch.mp3"
            show bg_streetsfire:
                ease 1 yalign 0.5
            with sshake
            "Before I can escape from the robot's clutches, it grabs me with its gigantic hands and raises me up."
            "This thing is so tall that I can't even see the top of its head!"
            "Its cold, rusty hands tighten around me. I can feel my spine crying out in pain."
            "{b}'Aaaaargh!'{/b}" with sshake
            "I scream out of desperation."
            window hide
            play sound "audio/explosion.mp3"
            show explosion with dissolve and sshake
            hide explosion with dissolve
            with Pause(0.1)
            "That must have woken her up."
            sinn "{b}HEY DICKHEAD!{w=0.1} WHO DO YOU THINK YOU ARE?!{/b}"
            window hide
            hide ggolem with dissolve
            show sinny with dissolve
            sinn "You think you're {i}soooooo{/i} cool by punching me through a dozen buildings, don't you?"
            sinn "That didn't even hurt!"
            "She says with a trail of blood right behind her..."
            hide sinny with dissolve
            show ggolem with dissolve
            gframe "{b}EXTERMINATE.{/b}"
            play sound "audio/robot.mp3"
            with Pause(0.5)
            window hide
            hide ggolem with moveoutleft
            show sinny with dissolve
            play sound "audio/heavypunch.mp3"
            show sinny with sshake
            with Pause(0.5)
            play sound "audio/splat.mp3"
            show blood with dissolve
            hide blood with dissolve
            with Pause(0.5)
    menu:
        "'...That doesn't sound good.'":
            sinn "Just a flesh wound!"
            play sound "audio/footsteps.mp3"
            hide sinny with moveoutright
            show ggolem with dissolve
            play sound "audio/slash.mp3"
            show slash with dissolve
            hide slash with dissolve
            play sound "audio/explosion.mp3"
            show explosion with dissolve and sshake
            hide explosion with dissolve
            with Pause(0.5)
            gframe "...."
            sinn "Ugh!{w=0.2} At least burn properly, you garbage truck!" with sshake
            play sound "audio/robot.mp3"
            hide ggolem with moveouttop
            with Pause(0.5)
            show sinny with dissolve
            play sound "audio/heavypunch.mp3"
            show sinny with sshake
            hide sinny with moveoutbottom
            with Pause(0.5)

    menu:
        "It jumped and crashed on top of her?!":
            sinn "{cps=10}Bleh...{/cps}"
            "It sounds like she's out cold..."
            "This is bad!{w=0.3} Terrible even!"
            "I couldn't even handle the small ones, let alone this giant robot!"
            "{cps=20}All I can do is struggle in vain...{/cps}"
            play sound "audio/robot.mp3"
            show ggolem with dissolve
            with Pause(1)
            "It stares me down with it single eye.{w=0.3} Its red gaze pierces my very soul."
            "I tremble and start begging for my life."
            "{b}'Please,{w=0.2} don't!{w=0.2} I don't even know why I'm here!'{/b}"
            gframe "..."
            play sound "audio/robot.mp3"
            gframe "{b}EXTERMINATE.{/b}"
            "How foolish to think that I could reason with a machine..."
            play sound "audio/splat.mp3"
            show blood with dissolve and sshake
            hide blood with dissolve
            "It starts gripping me tightly.{w=0.3} My body can't hold on as I start puking out blood.{w=0.3} I feel like a grape being squeezed."
            "{b}'AAAAAAAAAAGGGGGH!'{/b}" with sshake
            "I scream pathetically out of pain and misery. The giant doesn't respond. It just squeezes me even harder."
            "{cps=20}I'm beginning to lose consciousness...{/cps}" with fade
            "My vision grows dim as my skin turns pale. At this point, I wonder how much of my body is still intact."
            "The lady in red is still underneath me. The giant's foot is crushing her like a piston."
            "I can see blood under his foot.{w=0.3} She probably won't make it."
            "Just like me."
            with Pause(0.5)
            play sound "audio/splat.mp3"
            show blood with dissolve and sshake
            hide blood with dissolve
            stop music fadeout 5.0
            "I'm too mangled to even scream. I just pray for this to end."
            "Funny,{w=0.2} I never even figured out why I found myself here."
            "Guess it doesn't matter now."
            "I close my eyes,{w=0.2} and hope that my next cough is my last."
            with Pause(0.5)
            gframe "...."
            play sound "audio/flame.mp3"
            gframe "...?"
            with Pause(0.5)
            "Just when I think it's over, I hear an odd noise from the giant.{w=0.5} To be specific,{w=0.2} the area under him."
            "It's followed by a warm light,{w=0.2} one brighter than the numerous lamposts and buildings that surround me."
            "Even the giant's eye pales in comparison."
            play sound "audio/robot.mp3"
            gframe "...?!"
            with Pause(0.5)
            "The giant seems confused, stepping around as he raises his foot to check underneath."
            "The woman is {b}no longer there.{/b}"
            "Instead,{w=0.2} the giant's leg now has burns on it."
            "I'm starting to slowly piece things together."
            play music "audio/1coma.mp3" volume 0.5 fadein 5.0
            npc "Finally catching on, motherfucker?"
            npc "{b}GOOD!{/b}" with sshake
            with Pause(0.5)
            "I hear gloating from afar. The voice is familiar."
            "It's definitely her.{w=0.2} Even the giant knows that."
            "It turns around to face her."
            "But things{cps=3}...{/cps}are different now."
            "Even someone as clueless as me can see that."
            play sound "audio/robot.mp3"
            gframe "...?!!?!?!??!?!?!?"
            "It's tilted.{w=0.5} It knows that what it's witnessing is incredible."
            "If I didn't know any better,{w=0.2} I'd think the machine is getting {i}worried.{/i}"
            play sound "audio/firecrackle.mp3" loop
            show cg_sinny1 with fade
            "I can feel the heat from here."
            "It scorches. It burns. It's warm enough to make my blood {i}evaporate.{/i}"
            "Even the ground around me is starting to melt."
            show cg_sinny2 with fade
            "Yet she holds on to that sword regardless. You could say she's the master of that overwhelming heat."
            "I can see her determination through her grip alone.{w=0.2} Though, considering her demeanour, I guess I could be confusing that for rage..."
            gframe "{b}ALERT.{w=0.3} ALERT.{w=0.3} NOBLE PHANTOM USAGE = IMMINENT.{/b}"
            sinn "I see..."
            show cg_sinny3 with fade
            with Pause(0.5)
            sinn "{b}So even a machine like you can feel fear?{/b}"
            sinn "Great! I'm {i}soooooo{/i} gonna enjoy this,{w=0.3} {b}you piece of shit.{/b}"
            "Her smile is brimming with malice. At this point, I'm not even worried about her anymore."
            "{i}I'm worried about myself.{/i}"
            "{b}'Hey. HEY! I'm still here, you know?'{/b} I scream, but I feel like she's ignoring me." with sshake
            sinn "So what?{w=0.2} I never said that I would save you, twerp. After all..."
            play music "<from 173>audio/1coma.mp3" volume 0.75 fadein 1
            show cg_sinny4 with dissolve
            with Pause(0.5)
            "{b}I'm born to destroy!{/b}"
            "Oh no. No no no no no no no."
            "This is going where I think it's going."
            play sound "audio/robot.mp3"
            gframe "{b}PREPARING DEFENSIVE MANEUVERS.{w=0.3} RELEASING UNNEEDED BAGGAGE.{w=0.3}{/b}"
            "Whether out of pity or out of necessity, the giant suddenly releases its grip. I slide out of his hand, mangled and bleeding, but quickly start running away."
            "I have a good feeling of what's about to come next."
            sinn "For creation to begin,{w=0.3} the old must be destroyed..."
            sinn "It must be burnt away,{w=0.3} to make room for the new..."
            sinn "This is the scream of a rebel soul, burning bright! Oh, sword of dawn, that which will allow for a new beginning..."
            sinn "{b}BURN IT ALL DOWN!{/b}" with sshake
            sinn "{b}Noble Phantasm,{w=0.5} LÆVATEINN, SWORD OF THE SEVEN SEALS!{/b}"
            play sound "audio/explosion.mp3"
            hide cg_sinny4
            hide cg_sinny3
            hide cg_sinny2
            hide cg_sinny1
            with flash
            scene bg_streetsfire with flash
            play sound "audio/heavypunch.mp3"
            show ggolem with moveintop
            with Pause(0.5)

    menu:
        "She just sliced it in half!":
            hide ggolem with dissolve
            show sinny with dissolve
            sinn "Well,{w=0.3} look at you!"
            sinn "Not so high and mighty now, are we?"
            with Pause(0.5)
            hide sinny with dissolve
            play sound "audio/robot.mp3"
            show ggolem with dissolve
            gframe "{b}...ERROR.{w=0.3} ERROR.{w=0.3} UNABLE TO PERFORM NORMAL FUNCTIONS.{/b}"
            window hide
            play sound "audio/explosion.mp3"
            show explosion with dissolve and sshake
            hide explosion with dissolve
            with Pause(0.1)
            play sound "audio/crash.wav"
            hide ggolem with moveoutbottom
            sinn "Sheesh,{w=0.3} just shut up and stay down, will you?"
            sinn "This is why the modern age sucks!"
            with Pause(0.5)
            "I don't even know what happened.{w=0.3} One second I saw a sword,{w=0.2} the next I saw it bisect the giant mech in half."
            "Its lower body is lying around just a few feet away from its torso."
            "All this,{w=0.2} done by a single Servant..."
            show sinny with dissolve
            "Could this be...{w=0.3}Fate/Grand Order: Cosmos of the Lostbelt™?"
            sinn "What you staring at?"
            "{b}'Nothing!'{/b}" with sshake
            sinn "Hmph."
            play sound "audio/robot.mp3"
            "Aw shit.{w=0.5} I knew it wouldn't be {i}that{/i} easy..."
            hide sinny with dissolve
            scene cg_ggolem with fade
            play sound "audio/robot.mp3"
            show cg_ggolem:
                ease 1 yalign 0.0
            gframe "{b}COMMANDS OVERWRITTEN.{w=0.3}{/b}"
            gframe "{b}ERGO ={w=0.3} I DO NOT GIVE A FUCK.{/b}"
            gframe "{b}OPERATION:{w=0.3} KILL DA HOE! INITIATED.{/b}"
            sinn "Hell yeah!{w=0.3} That's more like it!{w=0.3} Looks like I finally knocked some sense into you!"

    menu:
        "'It's fighting even without its legs?!'":
         sinn "Well duh!{w=0.3} Gotta introduce a bit of chaos in the system, don't you think?"
         sinn "He gets 11 out of 10 from me for effort alone!"
         play sound "audio/robot.mp3"
         gframe "{b}DIE!{w=0.3} DIE!{w=0.3} {cps=60}DIEDIEDIEDIEDIEDIEDIEDIEDIEDIEDIEDIEDIE
         DIEDIEDIEDIEDIE.{/cps}{/b}"
         sinn "So cute!{w=0.3} It's like a baby Jotunn!" with sshake
    menu:
        "'That thing is literally trying to {b}kill us!{/b}'":
         sinn "Ugh,{w=0.3} stop whining, loser!{w=0.3} Just let me handle it!"
         show bg_streetsfire
         show sinny
         with dissolve
         play sound "audio/heavypunch.mp3"
         show sinny with sshake
         sinn "See?{w=0.3} Easy as pie!"
         "She blocked it..."
         "...{b}with just one hand!{/b}"
         hide sinny with dissolve
         with Pause(0.5)
         show ggolem with dissolve
         gframe "{b}IMPOSSIBLE...{w=0.3}DOES NOT COMPUTE...{/b}"
         sinn "Great, now you're back to being a lameass.{w=0.2} Oh well."
         sinn "{b}I was going to destroy you one way or another.{/b}"
         sinn "{b}LÆVATEINN,{w=0.5} SWORD OF THE SEVEN SEALS!{/b}"
         play music "<from 217 to 333>audio/1coma.mp3" volume 0.75 fadein 1
         play sound "audio/explosion.mp3"
         show cg_firepillar with flash
         with Pause(1)
         hide cg_firepillar with fade
         show bg_streetsfire
         play sound "audio/crash.wav"
         hide ggolem with moveoutbottom
         show bg_streetsfire with sshake

    menu:
        "'Incredible...'":
            sinn "Flattery will get you nowhere, twerp."
            sinn "But good to know that you aren't a buzzkill!"
            show sinny with dissolve
            "She steps forward and looks at the robot's corpse. It's burnt to ashes. I can't even recognize it anymore."
            sinn "Hah! I found his head!"
            "She proceeds to play with it like a soccer ball before kicking it to outer space."
            "I wonder if anyone will ever find it."
            sinn "Sheesh, that was fun!"
            sinn "If only {i}he{/i} were around to see this too..."
            "...He?"
            "I'd love to pry, but considering how volatile this woman seems, I'll hold it until later."
            sinn "Well,{w=0.3} since that's done."
            "She looks over to me as she slicks robot oil out of her sword."
            stop music fadeout 5.0
            sinn "I wonder how well you would burn.{w=0.5} It's been a while since I've torched flesh."

    menu:
        "'Wait, what?'":
            jump choice18

        "'I've done nothing to you!'":
            jump choice18

    label choice18:
        play music "audio/Confrontation.mp3" volume 0.5 loop
        sinn "So what? I never said I'd protect you."
        sinn "Especialy since you aren't a {b}Master.{/b}"
        "That word echoes in my head.{w=0.5} Master?{w=0.5} Master?{w=0.5} Why does it sound so familiar?"
        sinn "You were practically dying just a few moments ago, but look at you now."
        "I stare back at my body."
        "My guts are back in place. My wounds are stiched. I'm no longer drooling blood."
        "Yeah, I'm definitely not human."
        sinn "Are you a Servant? Like, the weak kind?"

    menu:
        "'I don't know...'":
            sinn "You don't? Ugh. How boring."
            sinn "Out of kindness, I'll be quick."
            "I wince,{w=0.2} seeing a blade head straight for my face.{w=0.2} I'm too paralyzed from fear to move."
            with Pause(0.5)
            play audio "audio/slash.mp3"
            show slash with dissolve
            hide slash with dissolve
            with Pause(0.5)
            play sound "audio/swordclash.mp3"
            with Pause(0.7)
            show bg_streetsfire with sshake
            with Pause(0.5)
            "...But before it can reach its target, something else prods out of the shadows and intercepts the blow. The two weapons clash with no clear victor."
            play sound "audio/footsteps.mp3"
            hide sinny with dissolve
            show aratron_stand with dissolve
            ara "Interesting to see you here, Saber."
            sinn "Huh?!?"
            hide aratron_stand with dissolve
            show sinny:
                xalign 2.0
                yalign 1.0
            show aratron_stand:
                xalign -1.0
                yalign 1.0
            with dissolve
            sinn "What are {b}YOU{/b} doing here, you stuck up bastard?" with sshake
            ara "Same reason as you, I assume. I was summoned for this {b}Holy Grail War.{/b}"
            sinn "...You can't be serious.{w=0.2} That's too huge of a coincidence to be true!"
            sinn "Plus, someone who is all talk and no bite like you wouldn't last a day in here!"
            ara "Believe me, I am not pleased that you are here as well."
            ara "If possible,{w=0.5} I would rather see you disappear at once."
            sinn "{cps=50}Oh you wanna fucking go?!{/cps}" with sshake
            with Pause(0.3)

    menu:
        "'Uh, hello? I'm still here!'":
            hide aratron_stand
            hide sinny
            with dissolve
            show aratron_stand with dissolve
            ara "Ah yes, please forgive that insignificant spat.{w=0.2} There is no point in listening to a rabid beast like Saber, after all."
            sinn "{cps=50}I can hear you, bitch!{/cps}"
            ara "I'll keep it brief just to preserve our sanity."
            ara "You are both Servants,{w=0.2} correct?"

    menu:
        "'Um, maybe...'":
            "The mysterious man raises an eyebrow at my reply."
            "Come to think of it, where did they even come from? Did the blasts from that woman's sword give away our location?"
            "He seems to know her, though. He called her by her Class container after all."
            "Saber...{w=0.3}The strongest Class."
            "No wonder she destroyed that robot with ease."
            ara "Well, that's rather odd. For a Servant to be unable to remember their True Name."
            ara "But I shall ignore that for now."
            ara "Saber, did you perhaps hear an announcement about a Holy Grail War?"
            hide aratron_stand with dissolve
            show sinny with dissolve
            sinn "Well, duh!{w=0.3} You just told me you were here for a Grail War!"
            ara "I see..."
            hide sinny with dissolve
            show sinny:
                xalign 2.0
                yalign 1.0
            show aratron_stand:
                xalign -1.0
                yalign 1.0
            with dissolve
            ara "{i}Then things are more suspicious than I thought.{/i}"
            sinn "What? Why are you talking in circles?!"
            ara "Have you encountered any other Servants besides this man?"
            sinn "Nope.{w=0.2} I just woke up an hour ago."
            ara "I too, woke up just an hour ago."
            sinn "...What you getting at? Trying to make us bed buddies or something?"
            sinn "For the last time, I'm {b}MARRIED{/b}, you mouthbreathing bottom fe-" with sshake
            ara "I was fighting {b}Lancer{/b} and {b}Archer{/b} just a few minutes ago."
            sinn "...What?"
            ara "The same Lancer and Archer from the last Holy Grail War. You know the ones."
            sinn "You're shitting me!" with sshake
            ara "A good reaction. This further proves my theory."
            ara "As Servants, we should not remember memories of our past fights in Holy Grail Wars. Yet not only do we all remember our memories of Persepolis..."
            ara "But the same Servants from Persepolis have been summoned here."
            sinn "Did the winner wish for something dumb or some other shit?"
            ara "No. This feels bigger than that. I was trying to ask Lancer and Archer about it, but they saw me as a threat before I could even speak."
            sinn "Can't blame them."
            ara "..."
            "Persepolis? Holy Grail War? Lancer and Archer?"
            "It's too much for me to grasp. Just what are these two talking about?"
            ara "Ahem.{w=0.5} Anyway."
            ara "Since I sense something suspicious at foot, I will relent from participating in this Grail War."
            ara "Instead, I wish to study it. Understand why we were all brought here."
            ara "I ask for your cooperation in that regard, Saber."
            sinn "Heh..."
            sinn "{cps=50}HAHAHAHAHAH!{/cps}" with sshake
            sinn "Not a chance."
            sinn "I bet you're making this shit up because you lost against Lancer and Archer."
            sinn "So you just want me to cover your ass!"
            ara "I expected nothing less from you."
            ara "However, what if I told you..."
            ara "That I found {i}him?{/i}"
            sinn "?!?" with sshake
            ara "Help me and I shall bring you to him."
            sinn "...."
            "Him again. Was that the guy Saber was talking about just a few minutes ago?"
            "I wonder who they are..."
            sinn "...Ugh, fine."
            sinn "I don't have a Master anyway, so I might as well use you as a meatshield while I'm at it."
            ara "A fine proposition."
            sinn "Don't act smug with me, bitch."
            hide sinny
            hide aratron_stand
            with dissolve
            show aratron_stand with dissolve
            ara "Our negotations are done. You can rest easy now, Servant."
            "This is embarrassing.{w=0.5} Being addressed like a child by fellow Servants makes my blood boil."
            "It's best to avoid trouble, but I decide to assert myself. Don't want to be a doormat after all."
            "{b}'Can I at least get a rundown on what's going on?'{/b}"
            ara "Certainly. Follow me, and I shall brief you on what happened to Saber and I."
            ara "There is a safehouse just a mile away. We would be best to move quickly."
            ara "I assume that I wasn't the only one to notice Saber's outburst."
            sinn "Shut the hell up!" with sshake
            ara "Case in point."
            hide aratron_stand with dissolve
            show sinny with dissolve
            sinn "Fine, I'll go to your stupid base or whatever."
            sinn "But you better bring me to {i}him{/i}, you got me?!"
            sinn "Or I swear..."
            sinn "{b}I'll burn this entire place to the ground.{/b}"
            "I shiver at that thought..."
            hide sinny with dissolve
            show aratron_stand with dissolve
            ara "You have my word."
            ara "Now, let us leave."
            ara "We have much to discuss..."
            stop music fadeout 5.0
            hide aratron_stand with fadehold
            scene black with fade
            "What will happen to Saber, Caster and this mysterious Holy Grail War?"
            "What will happen to you, Servant X, a mythical Servant that doesn't know of their True Name?"
            "What will happen to Nat, who will probably have died from cringe by the time she gets to this page?"
            "Who knows..."
            "What we do know, however..."
            "Is that Chapter Two NEVER EVER!"
            ":rofl: :rofl: :rofl: :rofl: :rofl:"







































    # This ends the game.

    return
