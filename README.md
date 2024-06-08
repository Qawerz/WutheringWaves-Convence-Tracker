# WutheringWaves Convence Tracker
A simple python script that shows the number of pulls you've made in the termial

![preview](https://raw.githubusercontent.com/Qawerz/WutheringWaves_pulls_tracker/main/preview.png)

## How to get a link?
1. Log in to the game.
2. Go to Menu
3. Select Convene
4. Click on a story
5. Minimize the game and go to the path where the game is installed + `\Client\Saved\Logs\`, for example: `O:\Epic Games\Wuthering Waves\Wuthering Waves Game\Client\Saved\Logs`
6. Open file called `Client.log` and look for the link that starts with `https://aki-gm-resources-oversea.aki-game.net/aki/gacha/index.html#/record` there

## Console Arguments
- `--no_skip_three_star=1` - Show all pulls you've made, including a three-star weapon. 
- `--auto_link=1` - automatically find the link from `Client.log` file. For working need to change config var in code before using.
