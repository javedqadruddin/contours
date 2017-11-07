from contours import generator

def test_normalize_file_lists():
    inner_generator = generator.TrainingDataGenerator(contour_option='both')
    list1 = [('a','1'),('b','1'),('c','1')]
    list2 = [('a','2'),('b','2'),('e','2'),('f','2')]
    assert [('a','1','2'),('b','1','2')] == inner_generator._normalize_file_lists(list1,list2)

def test_normalize_file_lists_subset():
    inner_generator = generator.TrainingDataGenerator(contour_option='both')
    list1 = [('a','1'),('b','1'),('c','1')]
    list2 = [('a','2'),('b','2')]
    assert [('a','1','2'),('b','1','2')] == inner_generator._normalize_file_lists(list1,list2)

def test_normalize_file_lists_superset():
    inner_generator = generator.TrainingDataGenerator(contour_option='both')
    list1 = [('a','1'),('b','1')]
    list2 = [('a','2'),('b','2'),('c','2')]
    assert [('a','1','2'),('b','1','2')] == inner_generator._normalize_file_lists(list1,list2)
