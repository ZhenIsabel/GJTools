import time

import cv2
import role_move
import find_box
# time.sleep(3)
# role_action.reset_visual_field()

def show_imag(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_match_image(match_res,template,image):
    min_val, max_val, min_loc, max_loc = cv2.dminMaxLoc(match_res)
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = (top_left[0]+w, top_left[1]+h)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)
    show_imag('temp', image)


def move_test():
    begin_find_loc_2 = [-980, -530]
    begin_find_loc_1 = [-825, -525]
    find_area_2 = [55, 30]
    begin_find_direct_1 = 0.6
    find_area_1 = [55, 47]
    begin_find_direct_2 = -0.5
    role_move.move_to(begin_find_loc_1, None, 1, 5)
    role_move.turn_to(begin_find_direct_1)
    role_move.move_map(find_area_1[0],
                                find_area_1[1], find_box.find_box_under_footer,
                                begin_find_loc_1
                                )

