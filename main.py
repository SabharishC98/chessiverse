import pygame, asyncio
import chess
import speech_recognition as sr

# Initialize Pygame
pygame.init()

# Set up the display with new dimensions (600x600)
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Voice Chess')

# Initialize the chess board
board = chess.Board()

# Function to draw the chessboard
def draw_board():
    square_size = 75  # Each square is 75x75 pixels
    for row in range(8):
        for col in range(8):
            color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 255, 0)
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Function to draw the chess pieces
def draw_pieces():
    piece_images = {
        'P': 'white-pawn.png', 'N': 'white-knight.png', 'B': 'white-bishop.png',
        'R': 'white-rook.png', 'Q': 'white-queen.png', 'K': 'white-king.png',
        'p': 'black-pawn.png', 'n': 'black-knight.png', 'b': 'black-bishop.png',
        'r': 'black-rook.png', 'q': 'black-queen.png', 'k': 'black-king.png'
    }
    
    square_size = 75  # Updated to match the board size
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = pygame.image.load(f'images/{piece_images[piece.symbol()]}')
            piece_image = pygame.transform.scale(piece_image, (square_size, square_size))  # Resize the image to fit
            x, y = chess.square_file(square) * square_size, (7 - chess.square_rank(square)) * square_size
            screen.blit(piece_image, (x, y))

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to capture and recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

# Function to parse voice commands into chess moves
def parse_command(command):
    parts = command.replace(" ","")
    if len(parts)==2:
        return f'{parts.lower()}'
    else:# e.g., "knight"
          # e.g., "f3"
        return f'{parts[0].upper()}{parts[1:len(parts)].lower()}'  # e.g., "Nf3"

# Function to make a move on the chessboard
def make_move(move):
    try:
        board.push_san(move)
        print('Move executed:', move)
    except ValueError:
        print('Invalid move')

# Function to process voice commands
def process_command(command):
    move = parse_command(command)
    make_move(move)

async def main():
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board()
        draw_pieces()
        pygame.display.flip()

        command = recognize_speech()
        if command:
            process_command(command)
        await asyncio.sleep(0)
asyncio.run(main())
pygame.quit()

