from contours.parsers import parser
from contours.lib.parsing import poly_to_mask

test_file_pair = ('/home/javed/Code/Exercise1/data/final_data/dicoms/SCD0000101/108.dcm', '/home/javed/Code/Exercise1/data/final_data/contourfiles/SC-HF-I-1/i-contours/IM-0001-0108-icontour-manual.txt')


def preprocess(file_pair):
    parsed_img, parsed_target = parser.parse(file_pair)
    width, height = parsed_img.shape
    #print(parsed_img, poly_to_mask(parsed_target, width, height))
    return parsed_img, poly_to_mask(parsed_target, width, height)


def main():
    preprocess(test_file_pair)

if __name__ == "__main__":
    main()
