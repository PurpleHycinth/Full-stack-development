import pygame
import sqlite3
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Game")

# Database
db = sqlite3.connect('database.db')
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS data(name TEXT, highscore REAL)")
db.commit()

def welcome(name, highscore):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Hello {name}!", True, BLACK)
    text2 = font.render("Welcome to Math Game", True, BLACK)
    text3 = font.render(f"Your high score: {highscore}", True, BLACK)
    text4 = font.render("Press Enter to start", True, BLACK)

    screen.fill(WHITE)
    screen.blit(text, (150, 150))
    screen.blit(text2, (150, 200))
    screen.blit(text3, (150, 250))
    screen.blit(text4, (150, 300))
    pygame.display.flip()

def main():
    name = ""
    highscore = 0
    ask = True

    # Check the number of rows in the table
    data = c.execute("SELECT * FROM data")
    if not data.fetchall():
        while ask:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name == "":
                            print("Please enter a valid name!")
                        else:
                            ask = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            welcome(name, "0")

        c.execute("INSERT INTO data VALUES(?, ?)", (name, "0"))
        db.commit()
        welcome(name, "0")
        highscore = 0
    else:
        data = c.execute("SELECT * FROM data")
        for row in data:
            name = row[0]
            highscore = row[1]
        welcome(name, highscore)

    score = 0
    lose = False

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not lose:
            calc = random.randint(0, 1)

            if calc == 0:
                fnum = random.randint(2, 50)
                snum = random.randint(2, 50)
                result = fnum + snum
                inp = f"[+] {fnum} + {snum} = "

            else:
                fnum = random.randint(1, 10)
                snum = random.randint(1, 10)
                result = fnum * snum
                inp = f"[+] {fnum} * {snum} = "

            def ask_user():
                userInput = input(inp)
                try:
                    userInput = int(userInput)
                    return userInput
                except ValueError:
                    print("Enter a valid value")
                    return ask_user()

            userInput = ask_user()

            if userInput == result:
                score += 1
                if score > highscore:
                    c.execute("UPDATE data SET highscore = ? WHERE name = ?", (score, name))
                    db.commit()
                    print(f"Correct! High score! Your score: {score}")
                else:
                    print(f"Correct! Your score: {score}")
            else:
                score = 0
                print("Oops! Wrong Answer!")
                user_again = input("[+] Play again? (y,n) : ").lower()
                if user_again == "n":
                    print("Goodbye!")
                    db.close()
                    lose = True

if __name__ == "__main__":
    main()
