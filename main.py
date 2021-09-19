# Тестовое задание в WG Academy
# (с) Nikita Kulikov
import random
import sys
from os import path
import pygame
import constants
from Square import Square


# вычисление координат для отрисовки типа фишек которые должны находится в вертикальном ряду
def set_target_rows_coordinates(list_of_locked, list_of_types):
    locked_x = set()
    free_x = [int(constants.SIZE_OF_PIN / 2 + i * constants.SIZE_OF_PIN) for i in range(constants.NUMBER_OF_PINS)]
    win_condition_dict = dict()
    for locked_coordinates in list_of_locked:
        locked_x.add(locked_coordinates[0])
    for x in locked_x:
        free_x.remove(x)
    for _type in list_of_types:
        tmp = random.choice(free_x)
        win_condition_dict[_type] = [tmp, int(constants.SIZE_OF_PIN / 2)]
        free_x.remove(tmp)

    return win_condition_dict


# вычисление координат для фишек
def set_squares_coordinate_list(coordinates, color):
    number_of_squares = len(coordinates)
    list_of_squares = []
    for i in range(number_of_squares):
        list_of_squares.append(Square(coordinates[i][0], coordinates[i][1], color))
    return list_of_squares


# вычисление координат ЗАЛОЧЕНЫХ полей
def set_locked_squares_coordinates(locked_coordinates):
    _locked_squares = []
    for i in range(constants.LOCKED):
        _locked_squares.append(Square(locked_coordinates[i][0], locked_coordinates[i][1], 'lock'))
    return _locked_squares


# удаление с экрана всех фишек для их "перерисовки"
def kill_squares(lists_of_squares):
    for list_of_squares in lists_of_squares:
        for square in list_of_squares:
            square.kill()


# инициализация поля - составление списка всех координат которые существуют в приделах поля
def game_field_init():
    _all_coordinates = []
    for i in range(1, constants.NUMBER_OF_PINS+1):
        for j in range(constants.NUMBER_OF_PINS):
            _all_coordinates.append([int(constants.SIZE_OF_PIN / 2 + (j * constants.SIZE_OF_PIN)), int(constants.SIZE_OF_PIN / 2 + (i * constants.SIZE_OF_PIN))])
    return _all_coordinates


# процесс ЗАНЯТИЯ клетки фишкой
def taking_cell(field):
    poped = random.choice(field)
    field.remove(poped)
    return poped


# проверка не сгенерировались ли клетки в ряд
def is_not_row(list_of_locked):
    x_list = [cell[0] for cell in list_of_locked]
    if len(x_list) != constants.LOCKED:
        return True
    else:
        for i in range(constants.LOCKED):
            if x_list.count(x_list[i]) == 5:
                return False
            else:
                continue
    return True


# генерируем залоченые клетки
def locked_coordinates_init(field):
    # для выполнения вин кондишн нужно чтобы локнутые клетки не занимали определенное количество вертикальных рядов
    blocked_lines = constants.NUMBER_OF_PINS - constants.TYPES
    # список координат залоченых клеток
    list_of_locked = []
    # список возможных иксов
    valid_x = []
    # список возможных игриков
    valid_y = []
    # выборка линий в которых будут стоять залоченные клетки
    while len(valid_x) != blocked_lines:
        x = random.randint(0, constants.NUMBER_OF_PINS - 1)
        if not valid_x.count(x) and not valid_x.count(x+1) and not valid_x.count(x-1):
            valid_x.append(x)
        else:
            continue
    for i in range(0, constants.NUMBER_OF_PINS):
        valid_y.append(i)
    while len(list_of_locked) != constants.LOCKED:
        future_coordinate = [((random.choice(valid_x) + 1)*constants.SIZE_OF_PIN) - constants.SIZE_OF_PIN/2, ((random.choice(valid_y) + 1)*constants.SIZE_OF_PIN) - constants.SIZE_OF_PIN/2]
        if future_coordinate in field:
            list_of_locked.append(future_coordinate)
            if not is_not_row(list_of_locked):
                list_of_locked.pop()
                list_of_locked.pop()
            field.remove(future_coordinate)
        else:
            continue

    return list_of_locked


# инициализация координат групп фишек
def pawns_init(field):
    list_of_pins = []
    for i in range(constants.NUMBER_OF_PINS):
        list_of_pins.append(taking_cell(field))
    return list_of_pins


# проверка не победил ли игрок
def win_condition(greens, reds, blues, targets):
    is_winning = False
    greens_X = set()
    reds_X = set()
    blues_X = set()
    for i in range(constants.NUMBER_OF_PINS):
        greens_X.add(greens[i][0])
        reds_X.add(reds[i][0])
        blues_X.add(blues[i][0])
    if len(greens_X) == 1 and len(reds_X) == 1 and len(blues_X) == 1 and blues_X.pop() == targets["blue"][0] and \
            reds_X.pop() == targets["red"][0] and greens_X.pop() == targets["brown"][0]:
        is_winning = True
    return is_winning


# отрисовка текста
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(constants.FONT_NAME, size)
    text_surface = font.render(text, True, constants.COLOR.WHITE.value)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# отрисовка окна конца игры
def draw_game_over_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "CONGRATULATIONS!", int(constants.SIZE_OF_PIN / 2), int(constants.FIELD_WIDTH / 2), 0)
    draw_text(screen, "You win!", int(constants.SIZE_OF_PIN / 2), int(constants.FIELD_WIDTH / 2), int(constants.SIZE_OF_PIN / 2))
    draw_text(screen, "Press \"ESC\" key to go to main menu.", int(abs(constants.SIZE_OF_PIN / 2)) - int(constants.SIZE_OF_PIN / 4), int(constants.FIELD_WIDTH / 2), int(constants.SIZE_OF_PIN * 3))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(constants.FPS)
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
            if _event.type == pygame.KEYDOWN:
                if _event.key == pygame.K_ESCAPE:
                    waiting = False
    draw_start_window()


# отрисовка окна легенды игры, т.е. подсказки как выглядят те или иные клетки или фишки
def draw_legend_window():
    screen.blit(background, background_rect)
    draw_text(screen, "LEGEND", int(constants.SIZE_OF_PIN / 2), int(constants.FIELD_WIDTH / 2), 0)
    locked = pygame.transform.scale(constants.LOCKED_PIN_IMG, (constants.SIZE_OF_PIN-5, constants.SIZE_OF_PIN-5))
    free = pygame.transform.scale(constants.FREE_PIN_IMG, (constants.SIZE_OF_PIN-5, constants.SIZE_OF_PIN-5))
    blue = pygame.transform.scale(constants.BLUE_PLAYER_IMG, (constants.SIZE_OF_PIN-5, constants.SIZE_OF_PIN-5))
    red = pygame.transform.scale(constants.RED_PLAYER_IMG, (constants.SIZE_OF_PIN-5, constants.SIZE_OF_PIN-5))
    brown = pygame.transform.scale(constants.BROWN_PLAYER_IMG, (constants.SIZE_OF_PIN-5, constants.SIZE_OF_PIN-5))
    locked.set_colorkey(constants.COLOR.WHITE.value)
    free.set_colorkey(constants.COLOR.WHITE.value)
    blue.set_colorkey(constants.COLOR.WHITE.value)
    red.set_colorkey(constants.COLOR.WHITE.value)
    brown.set_colorkey(constants.COLOR.WHITE.value)
    screen.blit(locked, (0, int(constants.SIZE_OF_PIN / 2)))
    draw_text(screen, " - Locked cell", int(constants.SIZE_OF_PIN / 2), constants.SIZE_OF_PIN * 3, constants.SIZE_OF_PIN / 2)
    screen.blit(free, (0, int(constants.SIZE_OF_PIN / 2)*3))
    draw_text(screen, "-  Free cell", int(constants.SIZE_OF_PIN / 2), constants.SIZE_OF_PIN * 3, int(constants.SIZE_OF_PIN / 2)*3)
    screen.blit(blue, (0, int(constants.SIZE_OF_PIN / 2)*5))
    screen.blit(red, (50, int(constants.SIZE_OF_PIN / 2)*5))
    screen.blit(brown, (100, int(constants.SIZE_OF_PIN / 2)*5))
    draw_text(screen, "- pawns", int(constants.SIZE_OF_PIN / 2), constants.SIZE_OF_PIN * 4, int(constants.SIZE_OF_PIN / 2)*5)
    draw_text(screen, "Enter - Choose or unchoose pawn", int(constants.SIZE_OF_PIN / 2) - int(constants.SIZE_OF_PIN / 4), constants.SIZE_OF_PIN * 2, int(constants.SIZE_OF_PIN / 4)*16)
    draw_text(screen, "Press SPACE to go to main menu", int(constants.SIZE_OF_PIN / 2) - int(constants.SIZE_OF_PIN / 4), constants.SIZE_OF_PIN * 2, int(constants.SIZE_OF_PIN / 4) * 18)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(constants.FPS)
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
            if _event.type == pygame.KEYUP and _event.key == pygame.K_SPACE:
                waiting = False
    draw_start_window()


# отрисовка главного меню
def draw_start_window():
    screen.blit(background, background_rect)
    draw_text(screen, "Welcome to ", int(constants.SIZE_OF_PIN / 2), int(constants.FIELD_WIDTH / 2), 0)
    draw_text(screen, "Test game.", int(constants.SIZE_OF_PIN / 2), int(constants.FIELD_WIDTH / 2), int(constants.SIZE_OF_PIN / 2))
    draw_text(screen, 'Press Enter to start or \"L\" for legend', int(abs(constants.SIZE_OF_PIN / 2)) - int(constants.SIZE_OF_PIN / 4), int(constants.FIELD_WIDTH / 2), int(constants.SIZE_OF_PIN * 3))
    draw_text(screen, 'Press \"Q\" to EXIT', int(abs(constants.SIZE_OF_PIN / 2)) - int(constants.SIZE_OF_PIN / 4), int(constants.FIELD_WIDTH / 2), int(constants.SIZE_OF_PIN * 4))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(constants.FPS)
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                sys.exit()
            if _event.type == pygame.KEYUP:
                if _event.key == pygame.K_l:
                    draw_legend_window()
                    waiting = False
                if _event.key == pygame.K_RETURN:
                    waiting = False
                if _event.key == pygame.K_q:
                    sys.exit()


# инициализация pygame и pygame.mixer
def start_init():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(path.join(constants.SOUND_DIR, "background_music.mp3"))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)
    pygame.display.set_caption("WG Academy test")


# вычисление координат для выбора клетки
def new_coordinates(event_key, cell):
    _moving = 'selected'
    if event_key == pygame.K_LEFT and cell[0] - constants.SIZE_OF_PIN > 0:
        cell[0] -= constants.SIZE_OF_PIN
    if event_key == pygame.K_RIGHT and cell[0] + constants.SIZE_OF_PIN < constants.WINDOW_WIDTH:
        cell[0] += constants.SIZE_OF_PIN
    if event_key == pygame.K_UP and cell[1] - constants.SIZE_OF_PIN > 25:
        cell[1] -= constants.SIZE_OF_PIN
    if event_key == pygame.K_DOWN and cell[1] + constants.SIZE_OF_PIN < constants.WINDOW_HEIGHT:
        selected[1] += constants.SIZE_OF_PIN
    if event.key == pygame.K_RETURN:
        if selected not in locked_coordinate and selected not in all_coordinates:
            select_sound.play().set_volume(0.1)
            _moving = 'pawn'
        else:
            shovel_sound.play().set_volume(0.1)
    return cell, _moving


# вычисление новых координат для фишек
def set_new_selected_coordinates(list_of_pawns, event_key):
    indexOfMoving = list_of_pawns.index(selected)
    _moving = 'pawn'
    if event_key == pygame.K_LEFT:
        future_cordinates = [list_of_pawns[indexOfMoving][0] - constants.SIZE_OF_PIN,
                             list_of_pawns[indexOfMoving][1]]
        if future_cordinates in all_coordinates:
            all_coordinates.remove(future_cordinates)
            all_coordinates.append(coordinates_of_moving)
            list_of_pawns[indexOfMoving][0] -= constants.SIZE_OF_PIN
            selected[0] -= constants.SIZE_OF_PIN
    if event_key == pygame.K_RIGHT:
        future_cordinates = [list_of_pawns[indexOfMoving][0] + constants.SIZE_OF_PIN,
                             list_of_pawns[indexOfMoving][1]]
        if future_cordinates in all_coordinates:
            all_coordinates.remove(future_cordinates)
            all_coordinates.append(coordinates_of_moving)
            list_of_pawns[indexOfMoving][0] += constants.SIZE_OF_PIN
            selected[0] += constants.SIZE_OF_PIN
    if event_key == pygame.K_UP:
        future_cordinates = [list_of_pawns[indexOfMoving][0],
                             list_of_pawns[indexOfMoving][1] - constants.SIZE_OF_PIN]
        if future_cordinates in all_coordinates:
            all_coordinates.remove(future_cordinates)
            all_coordinates.append(coordinates_of_moving)
            list_of_pawns[indexOfMoving][1] -= constants.SIZE_OF_PIN
            selected[1] -= constants.SIZE_OF_PIN
    if event_key == pygame.K_DOWN:
        future_cordinates = [list_of_pawns[indexOfMoving][0],
                             list_of_pawns[indexOfMoving][1] + constants.SIZE_OF_PIN]
        if future_cordinates in all_coordinates:
            all_coordinates.remove(future_cordinates)
            all_coordinates.append(coordinates_of_moving)
            list_of_pawns[indexOfMoving][1] += constants.SIZE_OF_PIN
            selected[1] += constants.SIZE_OF_PIN
    if event.key == pygame.K_RETURN:
        move_sound.play().set_volume(0.1)
        _moving = 'selected'
    return _moving


if __name__ == "__main__":
    # инициализация игры и окна игры
    start_init()
    # определяем "поверхность" экрана
    screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    # фон
    background_img = pygame.image.load(path.join(constants.IMG_DIR, 'background.png')).convert()
    background = pygame.transform.scale(background_img, (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    background_rect = background.get_rect()
    clock = pygame.time.Clock()
    # инициализируем звук
    move_sound = pygame.mixer.Sound(path.join(constants.SOUND_DIR, "splash2.wav"))
    select_sound = pygame.mixer.Sound(path.join(constants.SOUND_DIR, "splash1.wav"))
    shovel_sound = pygame.mixer.Sound(path.join(constants.SOUND_DIR, "shovel.ogg"))
    all_sprites = pygame.sprite.Group()
    # список всех координат, а так же после инициализации список свободных клеток
    all_coordinates = game_field_init()
    # список координат ЗАБЛОЧЕНЫХ клеток
    locked_coordinate = locked_coordinates_init(all_coordinates)
    # список координат каждой фишки зеленого игрока
    green_coordinates = pawns_init(all_coordinates)
    # список координат каждой фишки КРАСНОГО цвета
    red_coordinates = pawns_init(all_coordinates)
    # список координат каждой фишки СИНЕГО цвета
    blue_coordinates = pawns_init(all_coordinates)
    # выбранная фишка или координаты "индикатора выбора"
    selected = [constants.FIELD_WIDTH / 2, constants.FIELD_HEIGHT / 2]
    # целевые столбцы
    target = set_target_rows_coordinates(locked_coordinate, ["blue", 'red', 'brown'])
    # какой объект двигается
    moving = 'selected'

    draw_start_window()

    # игровой цикл
    is_running = True
    while is_running:
        clock.tick(constants.FPS)
        # обработка событий
        # проверка не выиграл ли игрок
        if win_condition(green_coordinates, red_coordinates, blue_coordinates, target):
            draw_game_over_screen()
            is_running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if moving == 'selected':
                if event.type == pygame.KEYDOWN:
                    selected, moving = new_coordinates(event.key, selected)
            elif moving == 'pawn':
                coordinates_of_moving = [selected[0], selected[1]]
                if coordinates_of_moving in green_coordinates:
                    if event.type == pygame.KEYDOWN:
                        moving = set_new_selected_coordinates(green_coordinates, event.key)
                if coordinates_of_moving in red_coordinates:
                    if event.type == pygame.KEYDOWN:
                        moving = set_new_selected_coordinates(red_coordinates, event.key)
                if coordinates_of_moving in blue_coordinates:
                    if event.type == pygame.KEYDOWN:
                        moving = set_new_selected_coordinates(blue_coordinates, event.key)

        # Рендеринг
        screen.blit(background, background_rect)
        # расстановка фишек по полю
        selected_square = [Square(selected[0], selected[1], "select", size=constants.SIZE_OF_PIN + 5)]
        green_squares = set_squares_coordinate_list(green_coordinates, "brown")
        red_squares = set_squares_coordinate_list(red_coordinates, "red")
        blue_squares = set_squares_coordinate_list(blue_coordinates, "blue")
        locked_squares = set_locked_squares_coordinates(locked_coordinate)
        free_squares = set_squares_coordinate_list(all_coordinates, "free")
        target_squares = []
        for key in target.keys():
            target_squares.append(set_squares_coordinate_list([target[key]], key))
        all_sprites.add(selected_square, red_squares, blue_squares, green_squares, locked_squares, free_squares, target_squares)
        # отрисовываем фишки на поле
        all_sprites.draw(screen)
        pygame.draw.line(screen, (50, 33, 37), (0, 50), (constants.WINDOW_WIDTH, 50), 5)
        # "переворачиваем" экран чтобы обновление картинки было без "пролагов"
        pygame.display.flip()
        kill_squares([green_squares, red_squares, blue_squares, selected_square, free_squares])

    pygame.quit()
