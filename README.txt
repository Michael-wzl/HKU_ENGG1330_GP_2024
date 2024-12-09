This is the group project for the HKU course ENGG1330

#Game Title: DepressionLand

#Project Overview:
This is a 2D maze game that metaphorically represents the journey of curing depression. The player will navigate through a moving maze with limited vision in limited time, putting items in certain places. For detailed description of how to play the game, please refer to the Game Manual section.

#Preparations and Running the game:
Before running the game, please make sure that all the packages are installed. In most cases they will already be included in the standard Python library. The dependencies are listed in the <requirements.txt> file. 
Then, you can navigate to the directory containing the main.py file in the terminal and run the main.py file with the following command:
```
python3 main.py
```
***(Note: the game is not supported on Windows! Linux, Ubuntu and MacOS are recommended.)***

#Game Manual:
##rules:
- The player needs to find and place the targets(Those special symbols in the map, like !, $, % etc. ) in the maze within the time limit.
- The player can collect or place the beacons as they want, given that they have enough beacon in the backpack. 
- Any modification to the source code, the user data or the log file can lead to undefined behaviors and breakdown of the game, so plz do not do so. 

##game walkthrough:
1. Login
You will first be asked to type in your UserName.
If we find that you are a new player, you will be asked to set up an account. 
If we find that you already have an account, you will be asked to type in your password correctly within 3 attempts, after which you will be asked to quit the game. 
If you login successfully, you will be logged out and be asked to enlarge the terminal if your size of the terminal is too small to display the contents. 
If you login successfully, you will be logged out if you have reached the max level, which is currently 3. 
If you login successfully, you can choose whether to read the background story. 
2. Gaming
(1) User Interface Introduction
On the top of the screen is the title in red. 
The next line informs you of the available beacon in your backpack and the targets to reach. 
The line below the information line is the timer. 
The line below the timer is the message display window, in which messages such as the metaphoric meaning for the target you just reached will be displayed. 
The view in the frame is the player view, which is limited and can be blocked by the wall.
If you are viewing the global map, you can see the map of the whole maze and the position of all the targets. However, you cannot see yourself and the beacon you placed. 
(2) User Control Introduction
See the <controls> section. 
(3) Walkthrough
If you reach all the targets within the time limit, you will either be sent to the next level, or you will be displayed the success end scene and get logged out. 
If you fail to reach all the targets within the time limit, you will be displayed the fail end scene and get logged out. 

##explanation of the symbols in the game:
1. '@' is the player
2. '#' is the wall
3. 'B' is the beacon
4. ['!','$','%','&','*','?','+','=','>','<'] are the targets

##controls:
- **direction keys**:direction keys are used to move the player around the maze.
- **B**:the player can place or collect beacons by pressing the key 'B'. 
If you step on a space and press 'B', you can place a beacon if you still have one in your backpack. 
If you step on a 'B' and then press 'B', you can collect the beacon. 
If you step on a target and press 'B', a message will be posted on the screen telling you not to do so. 
- **T**:the player can reach a target by steping on the target and pressing the key 'T'.
- **M**:the player can view or hide the whole map by pressing the key 'M'.
If you are viewing the player view, after pressing 'M' the map of the whole maze will be displayed. 
If you are viewing the map of the whole maze, after pressing 'M' the player view will be displayed. 
- **X**:the player can log out by pressing the key 'X'.
Note that if you log out halfway in the game, the targets you have already reached will not be saved. Only the level will be saved. 
- **R**:the player can restart the game by pressing the key 'R'
Note that if you restart halfway in the game, the targets you have already reached will not be saved. Only the level will be saved. 

The following contents are for those who want to have a better understanding of the game. 
#Features:
- **good stories and moral**:the game tries to display the depression in work and life of contemporary working women.
- **randomized maze**:the maze is randomly generated and has a solution.
- **moving maze**:the maze will be dynamically changed according to the player's progress.
- **visibility limit**:the sight range of the player is limited.
- **infinite level system**:different levels of difficulty are set and there is no end to the game.
- **mission system**:players need to find and place specific targets in the maze.
- **beacon system**:players can place or collect beacons according to their needs.
- **time limit**:players need to complete the tasks within the time limit, otherwise they will fail the game.
- **login system**:players can log in with their own accounts and encrypted passwords and save their progress.
- **ASCII art**:the game contains several ASCII arts and animations.

#Technical Aspects:
The project tries to implement the idea of Object-Oriented Programming. So we will introduce the project moduel by moduel. (The sequence of the introduction indicates the importance of the moduel)
## **main.py**
main.py is the main function of the game, which controls the flow of the game. 
## **gamemap_pkg**
This module is mainly responsible for: 
1. generating the maze randomly and ensuring that the maze has solutions; (implemented by <gen_algo_pkg>, which contains three different map generation algorithms)
2. sparsly distributing the missions in the maze; (implemented by <mission_distributor.py>)
3. controlling the visibility of the player; (implemented by <visible.py>)
4. partially modifying the maze; (implemented by the modify_maze function in <GameMap.py>)
5. managing the location of the items and missions in the maze. (implemented by <GameMap.py>)
## **player_pkg**
This is module is mainly responsible for:
1. managing the movement of the player and updating the player's location; (implemented by the move function in <Player.py>)
2. managing other behaviors of the player, like placing beacons and finishing missions; (implemented by set_beacon and set_mission functions in <Player.py>)
## **backpack_pkg**
This module is mainly responsible for:
1. managing the beacons and missions in the backpack; (implemented by Backpack.py)
## **login_pkg**
This module is mainly responsible for:
1. managing the login system of the game; (implemented by <login_manager.py>)
2. managing the user data; (implemented by <user_manager.py>)
## **animation_pkg**
This module is mainly responsible for:
1. managing the animations of the game; (implemented by <display_start_scene.py>, <display_start_scene_nofirst.py>, <display_end_scene_success.py>, <display_end_scene_fail.py>, <display_algo.py>)
## **other files and folders**
1. <depressionland.log>: recording the log of the game, which is mainly used for debugging, recording the game progress and facilitating tracebacks after hidden bugs;
2. <usr_data>: storing the user data.
3. <__pycache__>: storing the compiled python files, which are automatically generated by the python interpreter to improve the execution efficiency.
4. <__init__.py>: the initial file of the package, which is used to identify the package.

#File structure:
.
├── README.md
├── animation_pkg
│   ├── __init__.py
│   ├── __pycache__
│   │   └── ...
│   ├── art_data
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── ...
│   │   ├── end
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   └── ...
│   │   │   ├── end.py
│   │   │   ├── fail.py
│   │   │   └── success.py
│   │   └── start
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   └── ...
│   │       ├── notice.py
│   │       ├── scream.py
│   │       ├── walking.py
│   │       └── welcome.py
│   ├── Animation.py
│   ├── display_algo.py
│   ├── display_end_scene_fail.py
│   ├── display_end_scene_success.py
│   ├── display_start_scene.py
│   └── display_start_scene_nofirst.py
├── backpack_pkg
│   ├── Backpack.py
│   ├── __init__.py
│   └── __pycache__
│       └── ...
├── gamemap_pkg
│   ├── __init__.py
│   ├── __pycache__
│   │   └── ...
│   ├── map_gen_pkg
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── ...
│   │   ├── gen_algo_pkg
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   └── ...
│   │   │   ├── prim_map_gen_v2.py
│   │   │   ├── recursive_backtracker_map_gen_v2.py
│   │   │   └── recursive_division_map_gen_v2.py
│   │   ├── map_generator.py
│   │   └── mission_distributor.py
│   ├── GameMap.py
│   └── visible.py
├── login_pkg
│   ├── __init__.py
│   ├── __pycache__
│   │   └── ...
│   ├── login_manager.py
│   └── user_manager.py
├── player_pkg
│   ├── Player.py
│   ├── __init__.py
│   └── __pycache__
│       └── ...
├── usr_data
│   └── level.txt
├── depressionland.log
├── requirements.txt
└── main.py

22 directories, 90 files

#Prospects:
1. More items available and thus more fun
2. Higher efficiency of the programme (Like not using copy.deepcopy, and, had we been allowed to use numpy, use numpy for the maze generation part.)
3. The maze will become ugly after modification, so perhaps better algorithms for maze modification?
4. 3D would be awesome...
5. Fix the logging system...

#How to contribute to the project:
This project will be uploaded to the github repository after the grading is over. So you can fork the repository and make your own branch later on. After you have made your changes, you can create a pull request to the main branch.
Link to the repository: N/A (to be updated after the grading is over)

#Contributors: (No specific order)
- University Number: 3036290821 Name: Wang Ziling 
(Group leader and responsible for designing the structure of the project and implementing the map generation algorithms, map modification, mission distribution, the login system and debugging)
- University Number: 3036392710 Name: Tsoi Hiu Yin
(Responsible for the backpack system and designing the ASCII animations)
- University Number: 3036445440 Name: Li Chengzhang
(Responsible for the player package, the testing of the game, and the video cutting)
- University Number: 3036289169 Name: Wang Pengrun
(Responsible for the player package and designing the ASCII arts)
- University Number: 3036290742 Name: Zhao Wenqi
(Responsible for the visibility algorithm, the background story, the ASCII animations, and coordinating the meetings)

#References:
- The game inspired by The Maze Runner.
- The title inspired by Alice in Wonderland.
- The maze generation algorithms are adapted from the following link: 
https://blog.csdn.net/qq_41517936/article/details/107047349?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-107047349-blog-88285926.235%5Ev43%5Epc_blog_bottom_relevance_base7&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-107047349-blog-88285926.235%5Ev43%5Epc_blog_bottom_relevance_base7&utm_relevant_index=1
- The generative AI, Cursor, is used to help with the debugging. 
- Curses learnt from:
https://docs.python.org/zh-cn/3/howto/curses.html
- Logging system learnt from:
https://docs.python.org/zh-cn/3/library/logging.html

#Acknowledgement:
All of the team members have dedicatedly contributed to the project and helped each other during the development process. I, as the group leader, would like to express my sincere gratitude to them. 
I would also like to thank the authors of all the references for their great work and their kind open-sourcing.
My thanks also go to the course instructors and TAs for their guidance and help.
