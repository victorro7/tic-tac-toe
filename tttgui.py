import pygame
import sys
import time

import tictactoe as ttt
import easytictactoe as ettt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
pygame.display.set_caption('Tic Tac Toe"')
screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
mode = ettt
board = mode.initial_state()
ai_turn = False



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        easyButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        easy = mediumFont.render("Easy", True, black)
        easyRect = easy.get_rect()
        easyRect.center = easyButton.center
        pygame.draw.rect(screen, white, easyButton)
        screen.blit(easy, easyRect)

        impossibleButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        impossible = mediumFont.render("Impossible", True, black)
        impossibleRect = impossible.get_rect()
        impossibleRect.center = impossibleButton.center
        pygame.draw.rect(screen, white, impossibleButton)
        screen.blit(impossible, impossibleRect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if easyButton.collidepoint(mouse):
                time.sleep(0.2)
                mode = ettt
                user = mode.X
            elif impossibleButton.collidepoint(mouse):
                time.sleep(0.2)
                mode = ttt
                user = mode.X

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != mode.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = mode.terminal(board)
        player = mode.player(board)

        # Show title
        if game_over:
            winner = mode.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            elif winner is "X":
                title = "Congrats you won!!"
            elif winner is "O":
                title = "You lost :("
        elif user == player:
            title = "Your Turn"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)


        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = mode.minimax(board)
                board = mode.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == mode.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = mode.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = mode.initial_state()
                    ai_turn = False

    pygame.display.flip()
