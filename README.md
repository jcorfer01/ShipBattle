# ShipBattle
This project is a two player game developed with Python using object-oriented programming.
<br><br>
The code has been developed in ‘Visual Studio Code’, with the
help of the documentation provided by the [‘PyGame’](https://www.pygame.org/news) and [‘StackOverflow’](https://stackoverflow.com) pages.
<br><br>
On the other hand, the images are not copyrighted because most of them were created with
[Bing's AI image generator](https://www.bing.com/images/create?toWww=1&redig=DDA9833D58D149B28398193306311B00 ) (‘Copilot | Designer’). The game background has been acquired through the free image bank [‘FreePik’](https://www.freepik.es/vector-gratis/fondo-galaxia-acuarela_21643353.htm#fromView=image_search_similar&page=1&position=17&uuid=94c97f65-08cb-42eb-b659-323a2e24d6d6). The images have
been edited with three browser tools: [‘Iloveimg’](https://www.iloveimg.com/es/redimensionar-imagen) (resize images), [‘Photopea’](https://www.photopea.com) (edit image layers), and ['Remove.bg'](https://www.remove.bg/es/upload) (remove background).
<br><br>
On the other hand, the music for the menus and during the gameplay has been taken from a
[‘Youtube’ video](https://www.youtube.com/watch?v=5bn3Jmvep1k), whose creator allows its use for any project for free. In addition, the sound effects have been created by recording sounds with a microphone and then editing them with [‘Mp3cut’](https://mp3cut.net/es/) in order to cut their duration to implement them in the
pygame.mixer.Sound(“route”) class.
## The stages of the application:
1. “Main” Menu
   1. “TAG Selection” Menu
      1. “Game” Screen
      2. “Pause” Screen
      3. “Game Over” Screen
   2. “Options” Menu
   3. “Match History” Menu
## Files structure:
During the development of the project, the different files that will be used within the project have been organized into folders in order to implement 
the use of relative paths when accessing these files so that the game can be installed anywhere by the user.
<br><br>
The first folders we find within the project correspond to an extension of 'Visual Studio Code' known as 'Python Environment Manager'. This extension allows working on a project without the need to download the necessary packages to the computer's 'Python,' but rather in its own "environment." The packages that need to be downloaded for the project are saved in the ".venv" folder, which can later be selected as the "Workspace Environment" to allow the developer to work on the project with the packages downloaded in that folder.
<br><br>
Next, we find the "files" folder, which contains two text files to store data. The file "Historial_Jugadores.txt" stores the results of won, lost, and tied games for each player in the format "TAG:NumGamesWon:NumGamesLost:NumGamesTied:" so that it can later be used by the "History" menu. The other file, "Historial_Partidas.txt," stores the history of all the games played along with their results, the date, and the time each game finishes, so the last 10 games can be displayed in the "History" menu.
<br><br>
The following folder is the "sources" folder, which contains everything necessary to apply the same type of font (American Captain) to all text created within the application, mainly through a custom method that returns a `pygame.font.Font("font.ttf", size)` to simplify the code.
<br><br>
Right below "sources", we have the "img" folder. Here are all the images used for the game interface, whether for backgrounds or sprite designs. The first image is used for the bullet sprites generated by the ships. The next four images correspond to the buttons in the "Options" menu to enable or disable the music and sound effects. The "Button.png" image is used as the background for the rest of the buttons in the menus. To display the controls for each player, an image ("Controls.png") has been created as a help guide, which appears when the help icon ("Help_Icon.png") is pressed. During the game, the number of lives each player has is displayed at the bottom of the screen along with the image "Heart.png." The background used for the "Main Menu" is the image "MainMenu_Background.png," and for the other backgrounds (for submenus and the game), "Space_Background.jpg" is used. Finally, there are the images used for the ship sprites, differentiating between the left and right ship images for each state of immunity (when immune to bullets and when not immune).
<br><br>
The last folder is "music," where all the sound effects ("Shot_Sound.mp3" for the sound of the bullets, and "Impact_Sound.mp3" for when there is any collision) and music played in the "Main Menu" and its submenus ("Menu_Music.mp3") are stored, as well as the music that plays during the "Game" state ("Fight_Music.mp3").
<br><br>
The rest of the files are ".py" files, which contain the classes and methods that use the files inside the folders to execute and ensure the proper functioning of the game. To start the game you just have to run the "main.py" file and have fun!
### NOTES:
- To be able to run the program, it is mandatory that you have [Visual Studio Code](https://code.visualstudio.com/) and the extension [Python Environment Manager](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager).
- Inside this repository, you will find the project report in Spanish with more details about the development and management of the application, as well as a brief example video.
- The ["stagesImages"](stagesImages) folder includes images with the different stages of the game to serve as a visual example of how the application works.
