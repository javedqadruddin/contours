from contours.parsers import parser
from contours.lib.parsing import poly_to_mask


def preprocess(file_pair):
    parsed_img, parsed_target = parser.parse(file_pair)
    width, height = parsed_img.shape
    return parsed_img, poly_to_mask(parsed_target, width, height)


def main():
    preprocess(test_file_pair)

if __name__ == "__main__":
    main()
