from contours.lib import parsing

def parse(file_pair):
    img_file, target_file = file_pair
    parsed_img = parsing.parse_dicom_file(img_file)
    parsed_target = parsing.parse_contour_file(target_file)
    return(parsed_img, parsed_target)
