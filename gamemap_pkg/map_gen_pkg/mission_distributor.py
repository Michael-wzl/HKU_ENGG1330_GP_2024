import random
import logging

logger = logging.getLogger(__name__)

def mission_distributor(level,width_int,height_int,roads_l2):
    missions_l2 = []
    mission_num = 7*level//2 #3 for level 1, 7 for level 2, 10 for level 3
    if mission_num > 10:
        mission_num = 10 #at most 10 missions
    mission_signs = ['!','$','%','&','*','?','+','=','>','<'] #the 10 signs reserved for missions

    if level <= 2:
        # the old algorithm: denser and easier
        lower_band_row = 0
        upper_band_row = width_int//mission_num-1
        delta_row = width_int//mission_num-1
        lower_band_col = 0
        upper_band_col = height_int//mission_num-1
        delta_col = height_int//mission_num-1
        for _ in range(mission_num):
            mission_appearance = random.choice(mission_signs)
            mission_signs.remove(mission_appearance)

            row = 0
            col = 0

            while roads_l2[row][col] == '#':
                row = random.randint(lower_band_row,upper_band_row)
                col = random.randint(lower_band_col,upper_band_col)
            missions_l2.append([mission_appearance,row,col])

            lower_band_row += delta_row
            upper_band_row += delta_row
            lower_band_col += delta_col
            upper_band_col += delta_col

        return missions_l2
    else:
        lower_band_row = 0
        upper_band_row = width_int//mission_num-1
        delta_row = height_int//mission_num-1
        lower_band_col = 0
        upper_band_col = width_int//mission_num-1
        delta_col = height_int//mission_num-1
        # the new algorithm: more sparse and harder
        num_areas = 5  # divide the map into 5x5 areas
        area_width = width_int // num_areas
        area_height = height_int // num_areas

        for _ in range(mission_num):
            mission_appearance = random.choice(mission_signs)
            mission_signs.remove(mission_appearance)

            # random select an area
            area_x = random.randint(0, num_areas - 1)
            area_y = random.randint(0, num_areas - 1)

            # random select a place in the selected area
            row = random.randint(area_x * area_width, (area_x + 1) * area_width - 1)
            col = random.randint(area_y * area_height, (area_y + 1) * area_height - 1)

            # make sure no collision with the wall
            attempts = 0
            max_attempts = 50  # max attempts
            while roads_l2[row][col] == '#' and attempts < max_attempts:
                row = random.randint(area_x * area_width, (area_x + 1) * area_width - 1)
                col = random.randint(area_y * area_height, (area_y + 1) * area_height - 1)
                attempts += 1

            if attempts < max_attempts:
                missions_l2.append([mission_appearance, row, col])
            else:
                logging.warning(f"No appropreiate place for mission in ({area_x}, {area_y}!")

        # If not enough mission, try in other regions
        while len(missions_l2) < mission_num and mission_signs:
            mission_appearance = random.choice(mission_signs)
            mission_signs.remove(mission_appearance)

            for area_x in range(num_areas):
                for area_y in range(num_areas):
                    if any(area_x * area_width <= m[1] < (area_x + 1) * area_width and 
                            area_y * area_height <= m[2] < (area_y + 1) * area_height for m in missions_l2):
                        continue  # already occupied

                    row = random.randint(area_x * area_width, (area_x + 1) * area_width - 1)
                    col = random.randint(area_y * area_height, (area_y + 1) * area_height - 1)

                    attempts = 0
                    while roads_l2[row][col] == '#' and attempts < max_attempts:
                        row = random.randint(area_x * area_width, (area_x + 1) * area_width - 1)
                        col = random.randint(area_y * area_height, (area_y + 1) * area_height - 1)
                        attempts += 1

                    if attempts < max_attempts:
                        missions_l2.append([mission_appearance, row, col])
                        break
                if len(missions_l2) == mission_num:
                    break
            if len(missions_l2) == mission_num:
                break
        lower_band_col += delta_col
        upper_band_col += delta_col

        return missions_l2

#wzl
