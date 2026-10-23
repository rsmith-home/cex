import requests
from time import sleep

wishlist_box_ids = [
    "083717110217C",    # NES Castlevania 3, Unboxed
    "074299009266C",    # NES Donkey Kong, Unboxed
    "50109950398505C",  # NES Donkey Kong 3, Unboxed
    "974299009273C",    # NES Donkey Kong Jr, Unboxed
    "0214811060295C",   # NES Double Dragon 3, Unboxed
    "013388110360C",    # NES Duck Tales 2, Unboxed
    "013388110070c",    # NES Mega Man, Unboxed
    "0133881100705C",   # NES Metal Gear, Unboxed
    "045496630348C",    # NES Metroid, Unboxed
    "0454966303625C",   # NES Rainbow Islands, Unboxed
    "083717110026C",    # NES Rush 'N Attack, Unboxed
    "045496630539c",    # NES Tetris Unboxed
    "045496630737C",    # NES Tetris 2 Unboxed
    "040458011081AB",   # NES Adventures of Lolo 2, w/ Manual, Boxed
    "020763110099AB",   # NES Batman: The Video Game, w/ Manual, Boxed
    "013388110087AB",   # NES Bionic Commando, w/ Manual, Boxed
    "020763110068AB",   # NES Blaster Master, w/ Manual, Boxed
    "045496430399AB",   # NES Boulder Dash, w/ Manual, Boxed
    "045496430108AB",   # NES Boy and His Blob, w/ Manual, Boxed
    "020588010062AB",   # NES Bubble Bobble, w/ Manual, Boxed
    "083717110040AB",   # NES Castlevania, w/ Manual, Boxed
    "083717110149AB",   # NES Castlevania 2 Simon's Quest, w/ Manual, Boxed
    "083717110217AB",   # NES Castlevania 3, w/ Manual, Boxed
    "013388110209AB",   # NES Chip 'N Dale Rescue Rangers, w/ Manual, Boxed
    "045496630478AB",   # NES Cobra Triangle, w/ Manual, Boxed
    "074299009266AB",   # NES Donkey Kong, w/ Manual, Boxed
    "045496630423AB",   # NES Donkey Kong Classics, w/ Manual, Boxed
    "974299009273AB",   # NES Donkey Kong Jr, w/ Manual, Boxed
    "50109950398505AB", # NES Donkey Kong 3, w/ Manual, Boxed
    "045496430085AB",   # NES Double Dragon, w/ Manual, Boxed
    "021481106029AB",   # NES Double Dragon II, w/ Manual, Boxed
    "0214811060295AB",  # NES Double Dragon III, w/ Manual, Boxed
    "013388110162AB",   # NES Duck Tales, w/ Manual, Boxed
    "013388110360AB",   # NES Duck Tales 2, w/ Manual, Boxed
    "0478757000629AB",  # NES Gradius, w/ Manual, Boxed
    "045496430023AB",   # NES Super Off Road, w/ Manual, Boxed
    "045496430382AB",   # NES Kabuki Quantum Fighter, w/ Manual, Boxed
    "045496630720AB",   # NES Kirby's Adventure, w/ Manual, Boxed
    "045496630324AB",   # NES Legend Of Zelda, The, w/ Manual, Boxed
    "032264900123AB",   # NES Maniac Mansion, w/ Manual, Boxed
    "013388110070AB",   # NES Mega Man, w/ Manual, Boxed
    "045496430405AB",   # NES Mega Man 3, w/ Manual, Boxed
    "045496430450AB",   # NES Mega Man 4, w/ Manual, Boxed
    "045496630348AB",   # NES Metroid, w/ Manual, Boxed
    "5024866130010AB",  # NES Micro Machines, w/ Manual, Boxed
    "0454964304985AB",  # NES Paperboy, w/ Manual, Boxed
    "5013156610240AB",  # NES Parasol Stars, w/ Manual, Boxed
    "083717110187AB",   # NES Probotector II, w/ Manual, Boxed
    "045496630614AB",   # NES Punch-Out, w/ Manual, Boxed
    "0454966303625AB",  # NES Rainbow Islands, w/ Manual, Boxed
    "045496630393AB",   # NES R.C Pro AM, w/ Manual, Boxed
    "0837171100265AB",  # NES Rygar, w/ Manual, Boxed
    "018946110073AB",   # NES Shadow Warriors Ninja Gaiden, w/ Manual, Boxed
    "045496630591AB",   # NES Snake Rattle 'N Roll, w/ Manual, Boxed
    "045496630140AB",   # NES Super Mario Bros., w/ Manual, Boxed
    "045496630386AB",   # NES Super Mario Bros. 2, w/ Manual, Boxed
    "045496630584AB",   # NES Super Mario Bros. 3, w/ Manual, Boxed
    "013388110261AB",   # NES Talespin, w/ Manual, Boxed
    "083717120032AB",   # NES Teenage Mutant Hero Turtles, w/ Manual, Boxed
    "0837171200325AB",  # NES Teenage Mutant Hero Turtles II, w/ Manual, Boxed
    "045496630539AB",   # NES Tetris, w/ Manual, Boxed
    "045496630737AB",   # NES Tetris 2, w/ Manual, Boxed
    "021481102038AB",   # NES Tiger Heli, w/ Manual, Boxed
    "04549673013055AB", # NES Wrath of the Black Manta, w/ Manual, Boxed
    "045496630331AB",   # NES Zelda II: The Adventures of Link, w/ Manual, Boxed
    "3362932401209c",   # SNES Actraiser 2, Unboxed
    "020763115018C",    # SNES Aero The Acrobat 2, Unboxed
    "083717150053c",    # SNES Axelay, Unboxed
    "5026102018069c",   # SNES Claymates, Unboxed
    "039854000423C",    # SNES Hagane, The Final Conflict, Unboxed
    "045496830113C",    # SNES Kirby's Dream Course, Unboxed
    "045496330569c",    # SNES Lufia, Unboxed
    "5018247559415c",   # SNES Metal Marines, Unboxed
    "083717150008c",    # SNES Parodius, Unboxed
    "045496330088c",    # SNES Plok, Unboxed
    "715664393077c",    # SNES R-Type III, Unboxed
    "045496330170c",    # SNES Secret Of Mana, Unboxed
    "9315973020001c",   # SNES Shadowrun
    "3362932401483c",   # SNES Soul Blazer, Unboxed
    "045496830380c",    # SNES Super Punch Out, Unboxed
    "045496330484c",    # SNES Terranigma, Unboxed
    "045496830533c",    # SNES Tetris Attack, Unboxed
    "5013658050322C",   # SNES Top Gear 3000, Unboxed
    "083717150046c",    # SNES Turtles in Time
    "719631000036AB",   # SNES Actraiser, w/ Manual, Boxed
    "3362932401209AB",  # SNES Actraiser 2, w/ Manual, Boxed
    "020763110310AB",   # SNES Aero The Acrobat, w/ Manual, Boxed
    "020763115018AB",   # SNES Aero The Acrobat 2, w/ Manual, Boxed
    "083717150053AB",   # SNES Axelay, w/ Manual, Boxed
    "5026102018069AB",  # SNES Claymates, w/ Manual, Boxed
    "045496830489AB",   # SNES Donkey Kong Country 2, w/ Manual, Boxed
    "045496830557AB",   # SNES Donkey Kong Country 3, w/ Manual, Boxed
    "045496830021AB",   # SNES F Zero, w/ Manual, Boxed
    "013388130108AB",   # SNES Goof Troop, w/ Manual, Boxed
    "045496830540AB",   # SNES Kirby's Fun Pack, w/ Manual, Boxed
    "045496830410AB",   # SNES Kirby's Ghost Trap, w/ Manual, Boxed
    "045496830113AB",   # SNES Kirby's Dream Course, w/ Manual, Boxed
    "083717150022AB",   # SNES Legend of the Mystical Ninja, w/ Manual, Boxed
    "045496830076AB",   # SNES Legend of Zelda, The: A Link to the Past, w/ Manual, Boxed
    "045496330033AB",   # SNES Lost Vikings, w/ Manual, Boxed
    "083717145073AB",   # SNES Pop 'N TwinBee, w/ Manual, Boxed
    "083717110071AB",   # SNES Pop 'N TwinBee Rainbow Bell Adventures, w/ Manual, Boxed
    "5026102020062AB",  # SNES Rock N Roll Racing, w/ Manual, Boxed
    "9315973020001AB",  # SNES Shadowrun, w/ Manual, Boxed
    "045496330347AB",   # SNES Super Mario All Stars, w/ Manual, Boxed
    "045496980337AB",   # SNES Super Mario All Stars & Super Mario World, w/ Manual, Boxed
    "045496830144AB",   # SNES Super Mario Kart, w/ Manual, Boxed
    "32965808306021AB", # SNES Super Mario World (Yellow Box), w/ Manual, Boxed
    "3296580830602AB",  # SNES Super Mario World (Red Box), w/ Manual, Boxed
    "045496830298AB",   # SNES Super Metroid, w/ Manual, Boxed
    "045496830BBEB",    # SNES Super Metroid, Big Box Ltd Ed., w/ Manual, Boxed
    "013388130085AB",   # SNES Super Pang, w/ Manual, Boxed
    "083717150039AB",   # SNES Super Probotector, w/ Manual, Boxed
    "045496330019AB",   # SNES Super R-Type, w/ Manual, Boxed
    "715664393077AB",   # SNES R-Type III, w/ Manual, Boxed
    "021481601029AB",   # SNES Super Smash TV, w/ Manual, Boxed
    "045496830403AB",   # SNES Tetris & Dr Mario, w/ Manual, Boxed
    "045496830533AB",   # SNES Tetris Attack, w/ Manual, Boxed
    "741648001010AB",   # SNES Top Gear, w/ Manual, Boxed
    "74168001089AB",    # SNES Top Gear 2, w/ Manual, Boxed
    "5013658050322AB",  # SNES Top Gear 3000, w/ Manual, Boxed
    "045496830366AB",   # SNES Wario's Woods, w/ Manual, Boxed
    "045496870072AB",   # N64 Goldeneye, w/ Manual, Boxed
    "045496870461AB",   # N64 Super Smash Bros, w/ Manual, Boxed
    "045496870201AB",   # N64 Banjo Kazooie, w/ Manual, Boxed
    "3455196414624AB",  # N64 Extreme G, w/ Manual, Boxed
    "045496870782AB",   # N64 Paper Mario, w/ Manual, Boxed
    "045496870249AB",   # N64 1080 Snowboarding, w/ Manual, Boxed
    "4988602687965AB",  # N64 Castlevania Legacy of Darkness, w/ Manual, Boxed
    "045496870720AB",   # N64 Banjo Tooie, w/ Manual, Boxed
    "5030945020691AB",  # N64 Beetle Adventure Racing, w/ Manual, Boxed
    "045496870393AB",   # N64 Mario Party, w/ Manual, Boxed
    "045496870690AB",   # N64 Mario Party 2, w/ Manual, Boxed
    "045496870898AB",   # N64 Mario Party 3, w/ Manual, Boxed
    "045496870362AB",   # N64 Mario Golf, w/ Manual, Boxed
    "4988602602487AB",  # N64 Mystical Ninja 2, w/ Manual, Boxed
    "5030917030772",    # GameCube Call of Duty 2 Big Red One
    "SLEGGCS053B",      # GameCube Chibi Robo, + Manual, Boxed
    "5060004761869",    # GameCube Billy Hatcher and the Giant Egg
    "SLEGGCS179B",      # GameCube Legend of Zelda: Four Swords Adventures (Game Only), + Manual, Boxed
    "SLEGGCS180B",      # GameCube Legend of Zelda: Four Swords+Official Link Cable/OuterBox/Manual, Boxed
    "SLEGGCS174B",      # GameCube Kirby Air Ride, + Manual, Boxed
    "045496961305",     # GameCube Mario Party 5
    "SLEGGCS209B",      # GameCube Mario Party 7 (With Mic/Outer-Box), + Manual, Boxed
    "SLEGGCS268B",      # GameCube Odama (with Microphone), + Manual, Boxed
    "5055277007851",    # Wii Conduit 2
    "3499550267808",    # Wii Dokapon Kingdom
    "045496900021",     # Wii Excite Truck
    "5030917090790",    # Wii Goldeneye 007 + Gold Controller
    "5060102952442",    # Wii Ivy the Kiwi
    "3296580807000",    # Wii Klonoa - Door to Phantomile
    "045496368579",     # Wii Monster Hunter Tri + Classic Controller Pro
    "5055277008629",    # Wii Sonic Colours
    "8717418227739",    # Wii Spectrobes: Origins
    "4012927092569",    # Wii Tornado Outbreak
    "045496401450",     # Wii Mario Party 9
    "800265939837",     # Wii U Shmup Collection
    "045496479091",     # Switch Bayonetta Origins
    "810023030720",     # Switch YS VIII
    "045496429942",     # Switch Fire Emblem Warriors Three Hopes
    "045496425746",     # Switch Tokyo Mirage
    "5056280435914",    # Switch Danganronpa Decadence
    "045496424671",     # Switch Astral Chain
    "0045496429874",    # Switch Live A Live
    "045496425821",     # Switch Xenoblade Chronicles: Definitive Edition
    "045496420956",     # Switch Xenoblade Chronicles 2
    "045496422813",     # Switch Xenoblade Chronicles 2: Torna - The Golden Country
    "0045496429805",    # Switch Xenoblade Chronicles 3
    "045496426095",     # Switch Bravely Default II
    "045496428464",     # Switch Metroid Dread
    "0811949033499",    # Switch Ori: The Collection
    "5902385110006",    # Switch Dying Light Platinum Edition
    "5902367642051",    # Switch Witcher 3: Wild Hunt Complete Edition
    "5056280414568",    # Switch Deadly Premonition: Origins
    "045496423575",     # Switch Deadly Premonition 2: A Blessing in Disguise
    "810023030874",     # Switch Labyrinth of Refrain: Coven of Dusk
    "3391892004328",    # Switch Ni No Kuni: Wrath of the White Witch
    "0810023031581",    # Switch Disgaea 1 Complete
    "5060112431838",    # Switch Disgaea 5 Complete
    "0810023036654",    # Switch Disgaea 6: Defiance of Destiny
    "045496479701",     # Switch Pikmin 1+2
    "810023037491",     # Switch Silver Case 2425, The
    "045496423391",     # Switch Marvel Ultimate Alliance 3: The Black Order
    "045496511432",     # Switch Another Code: Recollection
    "5060264375783",    # Switch Morbid: The Seven Acolytes
    "884095213671",     # Switch Fitness Boxing: Fist of the North Star
    "5021290098077",    # Switch Dragon Quest Monsters: The Dark Prince
    "810100860899",     # Switch Monster Menu: The Scavenger's Cookbook: Deluxe Edition
    "810023032342",     # Switch Caligula Effect, The: Overdose
    "810023037422",     # Switch Caligula Effect 2, The
    "5060327535062",    # Switch Nelke & the Legendary Alchemists: Ateliers of the New World
    "810023031925",     # Switch Yomawari: The Long Night Collection
    "5055277042302",    # Switch Shin Megami Tensei III Nocturne HD Remaster
    "0810023033929",    # Switch Alliance Alive HD
    "8424365722674",    # Switch Mail Mole
    "0810023034261",    # Switch Disaster Report 4: Summer Memories
    "0810100860493",    # Switch void* tRrLM2(); //Void Terrarium 2
    "0810100861452",    # Switch Rhapsody: Marl Kingdom Chronicles
    "0810100862664",    # Switch Crymachina
    "810100861698",     # Switch GrimGrimoire OnceMore - Deluxe Edition
    "810023039723",     # Switch Labyrinth of Galleria: The Moon Society
    "0810023038856",    # Switch Yurukill: The Calumniation Games
    "0810100861131",    # Switch Raiden III x MIKADO MANIAX - Deluxe Edition
    "810100863388",     # Switch Legend of Legacy, The - HD Remastered
    "7350002931752",    # Switch Redemption Reapers
    "045496424312",     # Switch Fire Emblem: Three Houses Limited Ed. w/Artbook, USB, Badges & Steelbook
    "SGBOS236AB",       # GB Metroid II: Return of Samus, w/ Manual, Boxed
    "SGBCG165AB",       # GBC Harvest Moon, w/ Manual, Boxed
    "045496733131C",    # GBA Donkey Kong Country, Unboxed
    "4012927080498AB",  # GBA Breath Of Fire 2, w/ Manual, Boxed
    "3307210114303AB",  # GBA Boktai - The Sun is in Your Hand, w/ Manual, Boxed
    "4012927081112AB",  # GBA Boktai 2: Solar Boy Django, w/ Manual, Boxed
    "4988602081565AB",  # GBA Castlevania, w/ Manual, Boxed
    "045496734855AB",   # GBA Castlevania - NES Classics, w/ Manual, Boxed
    "4012927081440AB",  # GBA Castlevania Aria & Harmony, w/ Manual, Boxed
    "045496461478AB",   # GBA Donkey Kong: King of Swing, w/ Manual, Boxed
    "045496733971AB",   # GBA Donkey Kong Country 2, w/ Manual, Boxed
    "045496735852AB",   # GBA Donkey Kong Country 3, w/ Manual, Boxed
    "045496731403AB",   # GBA F-Zero Maximum Velocity, w/ Manual, Boxed
    "045496733988AB",   # GBA F-Zero GP Legend, w/ Manual, Boxed
    "045496734923AB",   # GBA Final Fantasy I & II (1&2), w/ Manual, Boxed
    "045496736873AB",   # GBA Final Fantasy IV (4) Advance, w/ Manual, Boxed
    "SGBAFINE001AB",    # GBA Final Fantasy V (5) Advance, w/ Manual, Boxed
    "045496738433AB",   # GBA Final Fantasy VI (6) Advance, w/ Manual, Boxed
    "5026555040938AB",  # GBA Grand Theft Auto, w/ Manual, Boxed
    "3307210154811AB",  # GBA Harvest Moon - Friends of Mineral Town, w/ Manual, Boxed
    "045496731830AB",   # GBA Kirby Nightmare in Dream Land, w/ Manual, Boxed
    "SNINGBAG003AB",    # GBA Klonoa, w/ Manual, Boxed
    "045496734374AB",   # GBA Mario Party Advance, w/ Manual, Boxed
    "5055060940099AB",  # GBA Megaman And Bass, w/ Manual, Boxed
    "5055060940266AB",  # GBA Megaman, Battle Chip Challenge, w/ Manual, Boxed
    "3307210118677AB",  # GBA Megaman Battle Network 2, w/ Manual, Boxed
    "5055060940136AB",  # GBA Megaman Battle Network 3 White, w/ Manual, Boxed
    "5055060940112AB",  # GBA Megaman Battle Network 3 Blue, w/ Manual, Boxed
    "5055060940303AB",  # GBA Megaman Battle Network 4 - Red Sun, w/ Manual, Boxed
    "5055060940334AB",  # GBA Megaman Battle Network 4 Blue Moon, w/ Manual, Boxed
    "5055060940488AB",  # GBA Megaman Battle Network 6: Cybeast Gregar, w/ Manual, Boxed
    "SNINGBAG004AB",    # GBA Megaman: Battle Network 6 - Cybeast Falzar, w/ Manual, Boxed
    "5055060940228AB",  # GBA Megaman Zero 2, w/ Manual, Boxed
    "5055060940365AB",  # GBA Megaman Zero 3, w/ Manual, Boxed
    "5055060940471AB",  # GBA Megaman Zero 4, w/ Manual, Boxed
    "045496733254AB",   # GBA Mario Golf Advance Tour, w/ Manual, Boxed
    "045496731465AB",   # GBA Mario Kart Super Circuit, w/ Manual, Boxed
    "045496734398AB",   # GBA Mario Power Tennis, w/ Manual, Boxed
    "045496733995AB",   # GBA Mario vs Donkey Kong, w/ Manual, Boxed
    "5060050940126AB",  # GBA Metal Slug Advance, w/ Manual, Boxed
    "045496734862AB",   # GBA Metroid (NES Classics), w/ Manual, Boxed
    "4012927080443AB",  # GBA Ninja Cop, w/ Manual, Boxed
    "785138320366AB",   # GBA Pokemon Emerald, w/ Manual, Boxed
    "045496732530AB",   # GBA Pokemon Ruby, w/ Manual, Boxed
    "0454967341141AB",  # GBA Pokemon Fire Red + Wireless Adaptor, w/ Manual, Boxed
    "045496732547AB",   # GBA Pokemon Sapphire, w/ Manual, Boxed
    "045496731397AB",   # GBA Super Mario Advance, w/ Manual, Boxed
    "045496731540AB",   # GBA Super Mario World: Super Mario Advance 2, w/ Manual, Boxed
    "045496731861AB",   # GBA Yoshi's Island: Super Mario Advance 3, w/ Manual, Boxed
    "045496733384AB",   # GBA Super Mario Advance 4: Super Mario Bros 3, w/ Manual, Boxed
    "045496734381AB",   # GBA Super Mario Ball, w/ Manual, Boxed
    "045496732370AB",   # GBA Wario Ware Inc., w/ Manual, Boxed
    "045496735579AB",   # GBA Yoshi's Universal Gravitation, w/ Manual, Boxed
    "045496734893AB",   # GBA Zelda II: The Adventure of Link, w/ Manual, Boxed
    "5060102951919",    # DS Avalon Code, w/Manual
    "5055277001385",    # DS Bleach: The 3rd Phantom
    "3700577000034",    # DS Blue Dragon: Awakened Shadow w/Manual
    "5060050946111",    # DS Boing! Docomodake
    "4012927081303",    # DS Castlevania: Dawn of Sorrow
    "5060102950226",    # DS Contact
    "5060177950046",    # DS Dementium (15), w/Manual
    "3700577000393",    # DS Dragon Ball: Origins 2, w/Manual
    "3296580810246",    # DS Dragon Ball Z: Attack Of The Saiyans
    "5060121821248",    # DS Dragon Quest V: The Hand of the Heavenly Bride
    "045496471415",     # DS Dragon Quest Monsters: Joker 2
    "4012927083055",    # DS Eledees: The Adventures of Kai and Zero
    "5060201651482",    # DS Emily The Strange: Strangerous
    "4012927083093",    # DS Enchanted Folk and the School of Wizardry w/Manual
    "5060121822979",    # DS Final Fantasy Tactics A2
    "5060102951223",    # DS Flower, Sun and Rain
    "045496470814",     # DS Ghost Trick: Phantom Detective
    "5055277005413",    # DS Infinite Space
    "8023171012483",    # DS Izuna: The Legend of the Ninja
    "045496471484",     # DS Kirby Mass Attack
    "045496739843",     # DS Kirby Super Star Ultra w/Manual
    "5060102952015",    # DS Luminous Arc 2
    "013388320110",     # DS Mega Man ZX Advent
    "5055060942093",    # DS Megaman Starforce Dragon, w/Manual
    "5055060942055",    # DS Megaman Starforce Pegasus
    "5055060942147",    # DS Megaman Starforce 2: Zerker X Ninja, w/Manual
    "5055060942123",    # DS Megaman Starforce 2: Zerker X Saurian
    "5060050946333",    # DS Metal Slug 7, w/Manual
    "5060112742149",    # DS Mushroom Men: Rise Of The Fungi
    "5055060942277",    # DS Okamiden
    "3700577003066",    # DS One Piece: Gigant Battle
    "045496740467",     # DS Pokemon Mystery Dungeon: Explorers of Sky
    "5060102952602",    # DS Pucca Power Up
    "5060121824157",    # DS Rhapsody: A Musical Adventure, w/Manual
    "5060102950417",    # DS Rune Factory, A Fantasy Harvest Moon
    "5060102951964",    # DS Rune Factory 2, w/Manual
    "730865400447",     # DS Shin Megami Tensei: Devil Survivor 2
    "5060004765928",    # DS Sonic Rush
    "4012927082928",    # DS Time Hollow, w/Manual
    "5060121824799",    # DS Valkyrie Profile - Covenant of the Plume
    "5060121822665",    # DS World Ends With You, The
    "045496523138",     # 3DS Castlevania - Mirror of Fate
    "4020628778569",    # 3DS Radiant Historia Perfect Chronology, w/Manual
    "5013715020244ab",  # Megadrive The Lost Vikings
    "5012967992293ab",  # Megadrive Shinobi 3
    "4974365610791ab",  # Megadrive Sonic 3
    "4974365615635ab",  # Megadrive Sonic & Knuckles
    "4974365615390AB",  # Megadrive Streets Of Rage 3, w/ Manual, Boxed
    "4974365610265ab",  # Megadrive Wonderboy in Monster World
    "ssegsatg048ab",    # Saturn Dark Saviour
    "SSEGSATG062AB",    # Saturn Dragon Force, w/ Manual, Boxed
    "SSEGSATG083AB",    # Saturn Guardian Heroes, w/ Manual, Boxed
    "SSEGSATG141AB",    # Saturn NiGHTS Into Dreams..., w/ Manual, Boxed
    "SSEGSATG147AB",    # Saturn Panzer Dragoon, w/ Manual, Boxed
    "SSEGSATG145AB",    # Saturn Panzer Dragoon II: Zwei, w/ Manual, Boxed
    "SSEGSATG146AB",    # Saturn Panzer Dragoon Saga (4 Disc), w/ Manual, Boxed (w/ Cardboard Sleeve)
    "ssegsatg191ab",    # Saturn Story of Thor 2
    "sps1g1015ab",      # PS1 Ape Escape
    "sps1g1204ab",      # PS1 Crash Team Racing
    "sps1g1213ab",      # PS1 Croc: Legend of the Gobbos
    "sps1g1377ab",      # PS1 Final Fantasy IX
    "sps1g1577ab",      # PS1 Legacy of Kain: Soul Reaver
    "sps1g1609ab",      # PS1 The Lost Vikings 2
    "SPS1G214AB",       # PS1 PaRappa the Rapper: The Hip Hop Hero, w/ Manual, Boxed
    "sps1g216ab",       # PS1 Parasite Eve II
    "sps1g331ab",       # PS1 RC de Go
    "sps1g470ab",       # PS1 Spider-Man
    "sps1g481ab",       # PS1 Spyro The Dragon
    "sps1g479ab",       # PS1 Spyro 2
    "SPS1G517AB",       # PS1 Strider 2 (Incl. Strider 1), w/ Manual, Boxed
    "sps1g526ab",       # PS1 Suikoden, w/ Manual, Boxed
    "SPS1G683AB",       # PS1 Um Jammer Lammy, w/ Manual, Boxed
    "sps1g697ab",       # PS1 Vandal Hearts II, w/ Manual, Boxed
    "slegps2s084b",     # PS2 Ar Tonelico 2: Melody Of The Metafalica, + Manual, Boxed
    "slegps2s186b",     # PS2 Blood Will Tell, + Manual, Boxed
    "4012927023228",    # PS2 Contra - Shattered Soldier
    "4012927026977",    # PS2 Crime Life - Gang Wars
    "4012927024249",    # PS2 CY Girls
    "SLEGPS2S455B",     # PS2 Demon Chaos, + Manual, Boxed
    "slegps2s529b",     # PS2 Drakengard 2, + Manual, Boxed
    "4012927020920",    # PS2 Ephemeral Fantasia
    "5055060920343",    # PS2 Everblue
    "5055060920701",    # PS2 Everblue 2
    "4005209068512",    # PS2 Evil Dead: Regeneration
    "5060121820357",    # PS2 Final Fantasy VII (7): Dirge Of Cerberus
    "5060121820487",    # PS2 Final Fantasy XII (12)
    "711719164210",     # PS2 Genji: Dawn of the Samurai
    "SLEGPS2S768B",     # PS2 Getaway Limited Edition (Ltd to 1000 copies), Mint
    "SLEGPS2S768A",     # PS2 Getaway Limited Edition (Ltd to 1000 copies), + Manual, Boxed
    "SLEGPS2S771B",     # PS2 Ghost In The Shell - Stand Alone Complex, + Manual, Boxed
    "SLEGPS2S795B",     # PS2 God Hand, + Manual, Boxed
    "711719607397",     # PS2 God of War 2 Special Edition
    "4012927020432",    # PS2 Gradius III and IV
    "012927025314",     # PS2 Gradius V
    "SLEGPS2S831B",     # PS2 Grim Grimoire, + Manual, Boxed
    "SLEGPS2S833B",     # PS2 Growlanser: Heritage Of War, + Manual
    "5060057022320",    # PS2 Gungrave Overdose
    "5021290026568",    # PS2 Hitman - Blood Money Special Edition
    "slegps2s1007b",    # PS2 Kaido Racer, + Manual, Boxed
    "slegps2s1006b",    # PS2 Kaido Racer 2, + Manual, Boxed
    "711719622055",     # PS2 Killzone: Collector's Edition Steelbook (2 Disc)
    "3307210208583",    # PS2 King Kong, Limited Collectors Edition
    "5060073300921",    # PS2 La Pucelle Tactics
    "036675002303",     # PS2 Maken Shao - Demon Sword
    "slegps2s1136b",    # PS2 Mana Khemia: Alchemists Of Al-Revis-w/Outer Box/OST/Poster,+Manual,Boxed
    "4012927025918",    # PS2 Nanobreaker
    "slegps2s1322b",    # PS2 Neo Contra, + Manual, Boxed
    "5060121822610",    # PS2 Odin Sphere
    "5060004766789",    # PS2 Outrun 2006
    "slegps2s1407b",    # PS2 Persona 3, + Manual, Boxed
    "SLEGPS2S1410B",    # PS2 Persona 4 (With CD), + Manual, Boxed
    "slegps2s1650b",    # PS2 Samurai Western (European Packaging), + Manual, Boxed
    "SLEGPS2S1658B",    # PS2 Scarface: Collectors Edition, + Manual, Boxed
    "5036675005359",    # PS2 Shin Megami Tensei: Lucifers Call
    "slegps2s1705b",    # PS2 Shin Megami Tensei: Devil Summoner, + Manual, Boxed
    "5036675008602",    # PS2 Shin Megami Tensei: Digital Devil Saga 2
    "5036675007742",    # PS2 Shin Megami Tensei - Digital Devil Saga
    "5036675008695",    # PS2 Shin Megami Tensei: Digital Devil Saga 2 Collector's Edition w/OST
    "711719652779",     # PS2 Shinobido: Way Of The Ninja
    "slegps2s1820b",    # PS2 Sol Divide, + Manual, Boxed
    "slegps2s1833b",    # PS2 Soul Nomad and the World Eaters, + Manual, Boxed
    "307210171146",     # PS2 Star Ocean - Till The End Of Time (2 Disc)
    "023171009162",     # PS2 Steambot Chronicles
    "012927027134",     # PS2 Steel Lancer Arena International
    "slegps2s1970b",    # PS2 Sword Of Etheria, + Manual, Boxed
    "711719281924",     # PS2 Twisted Metal Black
    "SLEGPS2S2121B",    # PS2 Ultimate Spider-Man Limited Edition w/Comic, + Manual, Boxed
    "5032921017367",    # PS2 Way of the Samurai
    "5030930048440",    # PS2 We Love Katamari
    "SLEGPS2S2187B",    # PS2 Wild Arms 5, + Manual, Boxed
    "3307210123305",    # PS2 Wizardry - Tales Of The Forsaken Land
    "8023171006192",    # PS2 Yakuza Fury
    "slegps2s2278b",    # PS2 Yakuza 2 (18), + Manual, Boxed
    "813633015910",     # PS3 Disgaea Triple Play Collection
    "5055060929704",    # PS3 Ducktales Remastered
    "711719110071",     # PS3 God of War Trilogy (18)
    "813633015026",     # PS3 Hyperdimension Neptunia Hypercollection
    "3296580810161",    # PS3 Katamari Forever
    "711719227359",     # PS3 Killzone Trilogy (18)
    "9006113003267",    # PS3 Syberia: Complete Collection
    "0711719161196",    # PS3 Twisted Metal 2012 (18)
    "4020628758820",    # PS4 428: Shibuya Scramble
    "5056280424703",    # PS4 Bladed Fury
    "5060264373529",    # PS4 Children of Morta
    "8436016712101",    # PS4 Creature in the Well
    "4020628633998",    # PS4 DARQ
    "5060264374007",    # PS4 Dead Cells
    "8718591188954",    # PS4 Desolatium
    "9006113008897",    # PS4 Elex
    "5016488140928",    # PS4 Eternights
    "711719363705",     # PS4 Ghost of Tsushima
    "711719274971",     # PS4 Killzone: Shadow Fall
    "9120080075970",    # PS4 Kingdoms of Amalur: Re-Reckoning
    "5016488139687",    # PS4 Kukoos
    "5907813598777",    # PS4 Lords Of The Fallen
    "3760156488035",    # PS4 Marsupilami
    "5055957702793",    # PS4 Mortal Shell
    "5026555423045",    # PS4 Red Dead Redemption 2
    "3760328371165",    # PS4 Relayer
    "9120080075505",    # PS4 Remnant: From The Ashes
    "3512899117204",    # PS4 Surge, The
    "5906961190918",    # PS4 Tails Of Iron
    "636676491646",     # PS4 Thomas Was Alone
    "813633014616",     # PS4 Tokyo Twilight Ghost Hunters
    "813633017990",     # PS4 Tokyo Twilight Ghost Hunters: Daybreak Special Gigs
    "3512899118690",    # PS4 Vampyr
    "5055957703127",    # PS4 Ved
    "8718591183423",    # PS4 World to the West
    "5055277033041",    # PS4 Yakuza Kiwami 2
    "5055277036561",    # PS4 Yakuza Remastered Collection
    "5060327534096",    # PS4 Nights of Azure 2
    "5060690790112",    # PS4 Root Letter: Last Answer
    "5055377600341",    # PSP Adventures To Go
    "5060102953340",    # PSP Blazing Souls Accelate
    "3307212818452",    # PSP Brothers in Arms: D-Day/Rainbow Six:Vegas
    "879278110007",     # PSP Dead Head Fred
    "083717260226",     # PSP Death Jr. II: Root of Evil
    "5060073304271",    # PSP Disgaea - Afternoon Of Darkness
    "8023171011400",    # PSP Exit 2
    "711719102861",     # PSP Fat Princess: Fistful of Cake
    "5060121823174",    # PSP Final Fantasy VII (7): Crisis Core CE +Book
    "5021290047693",    # PSP Final Fantasy IV / Final Fantasy IV: After Years
    "3700577000454",    # PSP Fullmetal Alchemist: Brotherhood
    "3700577002090",    # PSP Gods Eater: Burst
    "5060102952497",    # PSP Harvest Moon - Leaf Valley
    "5060050947255",    # PSP King Of Fighters Collection - Orochi Saga
    "5021290043138",    # PSP Kingdom Hearts - Birth By Sleep SE
    "5036675013859",    # PSP Legend Of Heroes: Trails In The Sky w/ Manual
    "5055060910146",    # PSP Megaman Maverick Hunter X
    "5055060910283",    # PSP Megaman: Powered Up, w/Manual
    "4012927060766",    # PSP Metal Gear Acid 2
    "4012927063576",    # PSP Metal Gear Solid Portable Ops/Coded Arms
    "4012927063491",    # PSP Metal Gear Solid Portable ops/Silent Hill
    "3760165160236",    # PSP Metal Slug XX, w/Manual
    "5055277007271",    # PSP Phantasy Star Portable 2
    "3307211659308",    # PSP Rainbow 6 Vegas/Driver 76/Prince of Persia
    "083717260042",     # PSP Rengoku
    "5060050947477",    # PSP Samurai Shodown - Anthology
    "5036675013910",    # PSP Shin Megami Tensei: Persona 2 w/ Manual
    "50366750139LE",    # PSP Shin Megami Tensei: Persona 2 Col. Ed. Slip Box,Soundtrack,6 Cards&Poster
    "5036675013668",    # PSP Shin Megami Tensei: Persona 3
    "5036675013613",    # PSP Shin Megami Tensei: Persona 3 Col. Ed. Artbook/6 Cards/Poster/Slip Box
    "5021290046504",    # PSP Tactics Ogre
    "3307210209658",    # PSP Tales of Eternia
    "5060073306862",    # PSP Undead Knights
    "813633010403",     # PSP What Did I Do To Deserve This, My Lord? 2
    "711719109297",     # PSP White Knight Chronicles - Origins
    "3391891961516",    # PS Vita Touch My Katamari
    "813633017846",     # PS Vita Legend of Heroes, The: Trails of Cold Steel II
    "882224017725",     # Xbox Jade Empire 2 Disc Limited Edition
    "5026555240918",    # Xbox Red Dead Revolver
    "4988607740016",    # Xbox Bloody Roar Extreme
    "3296580804207",    # Xbox 360 Ace Combat 6
    "88537014awnd",     # Xbox 360 Alan Wake Limited Ed
    "3546430140444",    # Xbox 360 Alone in the Dark - Tin Edition
    "SLEGX360S041B",    # Xbox 360 Arcana Heart 3 Limited Ed + Manual
    "3307215624470",    # Xbox 360 Assassin's Creed Double Pack
    "3307215760390",    # Xbox 360 Assassin's Creed Heritage Collection
    "3307215589281",    # Xbox 360 Assassin's Creed: Revelations Collector's Ed. w/Artbook, DVD & OST(No DLC)
    "4005209096096",    # Xbox 360 Avatar: Legend Of Aang, Burning Earth
    "SLEGX360S148B",    # Xbox 360 Blades of Time + Manual
    "4510772105330",    # Xbox 360 BlazBlue: Calamity Trigger Limited Ed
    "4510772105545",    # Xbox 360 Blazblue: Continuum Shift Limited Ed
    "4510772106306",    # Xbox 360 BlazBlue: Continuum shift Extend Limited Ed
    "5024866345247",    # Xbox 360 Bodycount
    "5030917051227",    # Xbox 360 Call Of Duty 4 - Collectors Ed. (15)
    "5050013373016",    # Xbox 360 Call of Duty: Black Ops (18) Hardened Ed. w/Medal (No DLC)
    "5030917199271",    # Xbox 360 Call Of Duty: Modern Warfare Trilogy (18) 3 Disc
    "3307219930911",    # Xbox 360 Child Of Eden
    "5060004766512",    # Xbox 360 Condemned
    "882224260633",     # Xbox 360 Crackdown
    "5030930087791",    # Xbox 360 Dante's Inferno Death Edition (No DLC)
    "882224373029",     # Xbox 360 Dead or Alive Xtreme 2
    "3307210341655",    # Xbox 360 Elder Scrolls IV: Oblivion - Shivering Isles Expansion (15)
    "SLEGX360S490B",    # Xbox 360 Fatal Inertia + Manual
    "SLEGX360S516B",    # Xbox 360 Fist Of The North Star: Kens Rage 2 + Manual
    "882224918381",     # Xbox 360 Forza 3 Limited Ed
    "0885370861594",    # Xbox 360 Forza Horizon 2
    "5060138436312",    # Xbox 360 Golden Axe: Beast Rider (18)
    "5030917032943",    # Xbox 360 Gun
    "88537016xndc",     # Xbox 360 Halo Reach Limited Ed
    "885370405538",     # Xbox 360 Halo Reach/Halo Anniversary Double Pack
    "SLEGX360S662B",    # Xbox 360 Infernal: Hell's Vengeance + Manual
    "5060138438934",    # Xbox 360 Iron Man - Tin Edition
    "5024866335033",    # Xbox 360 Jericho - Tin Edition
    "4020628513412",    # Xbox 360 Killer Is Dead Fan Ed. w/Artbook & OST (No DLC)
    "SLEGX360S723B",    # Xbox 360 Knights Contract (15) + Manual
    "5030930063115",    # Xbox 360 Left 4 Dead
    "5030930077822",    # Xbox 360 Left 4 Dead GOTY
    "5030930081294",    # Xbox 360 Left 4 Dead 2
    "5051892122306",    # Xbox 360 Midway Arcade Origins
    "3307211609273",    # Xbox 360 Naruto - The Broken Bond
    "4005209076999",    # Xbox 360 Outfit, The
    "3307210226075",    # Xbox 360 Over G Fighters
    "5026555245456",    # Xbox 360 Prey
    "882224053440",     # Xbox 360 Project Gotham Racing 3
    "s360proe002",      # Xbox 360 Project Gotham Racing 3/Live Arcade Pack
    "882224523547",     # Xbox 360 Project Gotham Racing 4
    "5030917033377",    # Xbox 360 Quake 4
    "3307210505613",    # Xbox 360 Rainbow Six Vegas 2 - Tin Edition
    "5030930049607",    # Xbox 360 Ridge Racer 6
    "5055277010141",    # Xbox 360 Rise Of Nightmares (18) (Kinect)
    "5026555246217",    # Xbox 360 Spec Ops: The Line (18)
    "5030917087431",    # Xbox 360 Spiderman Shattered Dimensions
    "SLEGX360S1203B",   # Xbox 360 Splatterhouse + Manual
    "3307210254122",    # Xbox 360 Splinter Cell Conviction
    "5055060963494",    # Xbox 360 Steel Battalion Heavy Armor (Kinect)
    "3391891955256",    # Xbox 360 Stoked Big Air Edition
    "5030917192937",    # Xbox 360 Teenage Mutant Ninja Turtles: Mutants in Manhattan (12)
    "5021290054264",    # Xbox 360 Tomb Raider 2013 Survival Ed. w/Artbook (No DLC)
    "8717418156268",    # Xbox 360 Turok - Tin Edition
    "5060112740787",    # Xbox 360 Two Worlds
    "5060112740916",    # Xbox 360 Two Worlds Collectors Ed
    "5060138438941",    # Xbox 360 Viking - Battle For Asgard - Tin Edition
    "5060146461559",    # Xbox 360 Walking Dead, The - Telltale Season 2
    "SLEGX360S1395B",   # Xbox 360 Wartech + Manual
    "5030917069468",    # Xbox 360 Wolfenstein 2009
    "5050740025950",    # Xbox 360 Worms: The Revolution Collection
    "882224260770",     # Xbox 360 XBLA Compilation: GWRE, Bejeweled 2, etc
    "s360arce001",      # Xbox 360 Xbox Arcade
    "s360arce002",      # Xbox 360 Xbox Arcade
    "s360arce003",      # Xbox 360 Xbox Arcade
    "0811949035554",    # Xbox One Cuphead
    "5060188671831",    # Xbox One Grip Combat Racing
]

boxes = {}
stores = {}

def _calculate_weighting(box):
    if box['ecomQuantityOnHand'] == 0:
        return 0
    if box['ecomQuantityOnHand'] < 6:
        return 5
    elif box['ecomQuantityOnHand'] < 11:
        return 4
    elif box['ecomQuantityOnHand'] < 21:
        return 3
    elif box['ecomQuantityOnHand'] < 30:
        return 2
    else:
        return 1

headers = {"user-agent": "CeXiOS/7.2.15(0) /OS 26.3.1/iPhone 14/U-03CAAE84-5AF9-4A3A-9FCE-7E991DD23AF7"}

resp = requests.get("https://wss2.cex.uk.webuy.io/v3/stores", headers=headers)
resp.raise_for_status()
for store in resp.json()['response']['data']['stores']:
    store['wishlistBoxes'] = []
    store['totalWeighting'] = 0
    stores[store['storeId']] = store

for box_id in wishlist_box_ids:
    resp = requests.get("https://wss2.cex.uk.webuy.io/v3/boxes/{0}/detail".format(box_id), headers=headers)
    resp.raise_for_status()
    if resp.json()['response']['data'] is None:
        continue
    box = resp.json()['response']['data']['boxDetails'][0]
    box['weighting'] = _calculate_weighting(box)
    box['nearestStoreNames'] = []

    if box['collectionQuantity'] > 0:
        resp = requests.get("https://wss2.cex.uk.webuy.io/v3/boxes/{0}/neareststores"
                            # "?latitude=51.522556&longitude=0.592793".format(box_id), headers=headers)  # Brighton
                            "?latitude=54.664533&longitude=-1.632944".format(box_id), headers=headers)  # Home
        resp.raise_for_status()
        if resp.json()['response']['data']:
            for store in resp.json()['response']['data']['nearestStores']:
                store_id = int(store['storeId'])
                box['nearestStoreNames'].append(store['storeName'])
                stores[store_id]['wishlistBoxes'].append(box)
                stores[store_id]['totalWeighting'] += box['weighting']

    boxes[box_id] = box
    if (len(boxes) % 50) == 49:
        sleep(60.0)
    else:
        sleep(2.0)

for store in stores.items():
    store[1]['wishlistBoxes'] = {box['boxName']: box for box in
                                 sorted(store[1]['wishlistBoxes'], key=lambda x: x['collectionQuantity'])}

best_stores = sorted(stores.items(), key=lambda x: x[1]['totalWeighting'], reverse=True)
rarest_boxes = sorted(list(filter(lambda box: box[1]['collectionQuantity'] > 0, boxes.items())), key=lambda x: x[1]['collectionQuantity'])
out_of_stock_boxes = list(filter(lambda box: box[1]['collectionQuantity'] == 0, boxes.items()))
t=0
t=1