#!/usr/bin/env python3

# Created by: Haokai Li
# Created on: Oct 2021
# This Program is about pybadge

import ugame
import stage
import time
import random
import supervisor

import constants


def splash_scene():
    # This function is the main splash scene

    coin_sound = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    # add background
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # size
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y
    )

    # used this program to split the image into tile :
    # https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # put background in game
    # set the frame rate
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers
    game.layers = [background]
    # render the background
    game.render_block()

    # loop
    while True:
        # wait for 1 second
        time.sleep(1.0)
        menu_scene()


def menu_scene():
    # This function is the main menu scene

    # add background
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")

    # add text
    text = []
    text1 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text1.move(30, 10)
    text1.text("MT FINAL Game")
    text.append(text1)

    text2 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    # size
    background = stage.Grid(
        image_bank_background, constants.SCREEN_X, constants.SCREEN_Y
    )

    # put background in game
    # set the frame rate
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers
    game.layers = text + [background]
    # render the background
    game.render_block()

    # loop
    while True:
        # get input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_START != 0:
            game_scene()

        # redraw Sprites
        game.tick()  # wait


def game_scene():
    # This function is the main game scene

    def show_fire():
        # This function show the fires
        for fire_number in range(len(fires)):
            if fires[fire_number].x < 0:
                fire_times = random.randint(0, 3)
                if fire_times == 0:
                    fires[fire_number].move(
                        constants.ROAD_FIRST_X,
                        constants.OFF_TOP_SCREEN,
                    )
                    break
                elif fire_times == 1:
                    fires[fire_number].move(
                        constants.ROAD_SECOND_X,
                        constants.OFF_TOP_SCREEN,
                    )
                    break
                elif fire_times == 2:
                    fires[fire_number].move(
                        constants.ROAD_THIRD_X,
                        constants.OFF_TOP_SCREEN,
                    )
                    break
                elif fire_times == 3:
                    fires[fire_number].move(
                        constants.ROAD_FOURTH_X,
                        constants.OFF_TOP_SCREEN,
                    )
                    break

    # score
    score = 0

    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(1, 1)
    score_text.text("Score: {0}".format(score))

    # game life
    game_life = constants.GAME_LIFE

    game_life_text = stage.Text(width=29, height=14)
    game_life_text.clear()
    game_life_text.cursor(0, 0)
    game_life_text.move(1, 10)
    game_life_text.text("Life: {0}".format(game_life))

    game_over_text = stage.Text(width=29, height=14)

    # add background
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprite = stage.Bank.from_bmp16("space_aliens.bmp")

    # button state
    a_button = constants.button_state["button_up"]
    left_button = constants.button_state["button_up"]
    right_button = constants.button_state["button_up"]

    # ship move number
    ship_address = 1

    # get sound ready
    boom_sound = open("boom.wav", "rb")
    crash_sound = open("crash.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # size
    background = stage.Grid(
        image_bank_background, constants.SCREEN_X, constants.SCREEN_Y
    )
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # sprite frame
    ship = stage.Sprite(image_bank_sprite, 4, constants.ROAD_SECOND_X, 100)

    # create list of fires for when we shoot
    fires = []
    for fire_number in range(constants.TOTAL_NUMBER_OF_FIRES):
        a_single_fire = stage.Sprite(
            image_bank_background, 6, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        fires.append(a_single_fire)
    # show two fires
    show_fire()
    show_fire()

    # put background in game
    # set the frame rate
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers
    game.layers = (
        [game_over_text]
        + [score_text]
        + [game_life_text]
        + [ship]
        + fires
        + [background]
    )
    # render the background
    game.render_block()

    # loop
    while True:
        # get input
        keys = ugame.buttons.get_pressed()

        # A button to forward
        if keys & ugame.K_O != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_still_pressed"]
                ship.move(ship.x, ship.y - 40)
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]

        if keys & ugame.K_X != 0:
            pass

        # check score
        if keys & ugame.K_START != 0:
            if game_life < 1:
                game_over_scene(score)

        # restart
        if keys & ugame.K_SELECT != 0:
            supervisor.reload()

        # left and right
        if keys & ugame.K_RIGHT != 0:
            if right_button == constants.button_state["button_up"]:
                if ship_address == 3:
                    ship_address = 0
                    right_button = constants.button_state["button_still_pressed"]
                else:
                    ship_address = ship_address + 1
                    right_button = constants.button_state["button_still_pressed"]
        else:
            if right_button == constants.button_state["button_still_pressed"]:
                right_button = constants.button_state["button_up"]

        if keys & ugame.K_LEFT != 0:
            if left_button == constants.button_state["button_up"]:
                if ship_address == 0:
                    ship_address = 3
                    left_button = constants.button_state["button_still_pressed"]
                else:
                    ship_address = ship_address - 1
                    left_button = constants.button_state["button_still_pressed"]
        else:
            if left_button == constants.button_state["button_still_pressed"]:
                left_button = constants.button_state["button_up"]

        if keys & ugame.K_UP != 0:
            pass
        if keys & ugame.K_DOWN != 0:
            pass

        # update game logic
        # forwoard
        if a_button == constants.button_state["button_released"]:
            ship.move(ship.x, ship.y + 40)

        # ship move
        if ship_address == 0:
            ship.move(constants.ROAD_FIRST_X, ship.y)
        elif ship_address == 1:
            ship.move(constants.ROAD_SECOND_X, ship.y)
        elif ship_address == 2:
            ship.move(constants.ROAD_THIRD_X, ship.y)
        elif ship_address == 3:
            ship.move(constants.ROAD_FOURTH_X, ship.y)

        # move fires
        for fire_number in range(len(fires)):
            if fires[fire_number].x > 0:
                fires[fire_number].move(
                    fires[fire_number].x,
                    fires[fire_number].y + constants.FIRE_SPEED,
                )
                if fires[fire_number].y > constants.SCREEN_Y:
                    fires[fire_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )
                    show_fire()
                    show_fire()
                    score += 1
                    score_text.clear()
                    score_text.cursor(0, 0)
                    score_text.move(1, 1)
                    score_text.text("Score: {0}".format(score))

        # fires collide ship
        for fire_number in range(len(fires)):
            if fires[fire_number].x > 0:
                if stage.collide(
                    fires[fire_number].x + 1,
                    fires[fire_number].y + 5,
                    fires[fire_number].x + 15,
                    fires[fire_number].y + 15,
                    ship.x,
                    ship.y,
                    ship.x + 15,
                    ship.y + 15,
                ):
                    # fire hit ship
                    fires[fire_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )
                    show_fire()
                    show_fire()
                    sound.stop()
                    sound.play(crash_sound)
                    game_life = game_life - 1
                    game_life_text.clear()
                    game_life_text.cursor(0, 0)
                    game_life_text.move(1, 10)
                    game_life_text.text("life: {0}".format(game_life))
                    if game_life < 1:
                        for fire_number in range(len(fires)):
                            if fires[fire_number].x > 0:
                                fires[fire_number].move(
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                                )
                        ship.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        sound.stop()
                        sound.play(boom_sound)
                        score_text.clear()
                        game_life_text.clear()
                        game_over_text.clear()
                        game_over_text.cursor(0, 0)
                        game_over_text.move(1, 1)
                        game_over_text.text("PRESS START")

        # redraw Sprite
        game.render_sprites([ship] + fires)
        game.tick()  # wait


def game_over_scene(final_score):
    # This function is the main game over scene

    # turn off sound from last scene
    sound = ugame.audio
    sound.stop()

    # add background
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # size
    background = stage.Grid(
        image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # add text
    text = []
    text1 = stage.Text(
        width=29, height=12, font=None, palette=constants.BLUE_PALETTE, buffer=None
    )
    text1.move(22, 20)
    text1.text("Final Score: {:0>2d}".format(final_score))
    text.append(text1)

    text2 = stage.Text(
        width=29, height=12, font=None, palette=constants.BLUE_PALETTE, buffer=None
    )
    text2.move(43, 60)
    text2.text("GAME OVER")
    text.append(text2)

    text3 = stage.Text(
        width=29, height=12, font=None, palette=constants.BLUE_PALETTE, buffer=None
    )
    text3.move(32, 110)
    text3.text("PRESS SELECT")
    text.append(text3)

    # put background in game
    # set the frame rate
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers
    game.layers = text + [background]
    # render the background
    game.render_block()

    # loop
    while True:
        # get input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_SELECT != 0:
            supervisor.reload()

        # redraw Sprites
        game.tick()  # wait


if __name__ == "__main__":
    splash_scene()
