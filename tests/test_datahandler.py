from contours.handlers import datahandler

def test_get_img_filename():
    icontour_file = 'IM-0001-0059-icontour-manual.txt'
    ocontour_file = 'IM-0001-0059-ocontour-manual.txt'
    corr_image = '59.dcm'
    assert (datahandler._get_img_filename(icontour_file),
            datahandler._get_img_filename(ocontour_file)) == (corr_image, corr_image)
