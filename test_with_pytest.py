from season import *
from timeInterval import *
from year import *


def test_fractions():
    assert timeInterval(1.25) == (1,6)
    assert timeInterval(0, 7.5) == (0,7,540)
    assert timeInterval(1.1) == (1,2,432)
    assert timeInterval(0,0,1.5) == (0,0,1)
def test_nagative_input():
    assert timeInterval(2,-1) == (1,23)
    assert timeInterval(-1,-1,-1) == (-2,22,1079)
    assert timeInterval(0,-30) == (-2,18)

exampleMonth = timeInterval(1,17,107)
def test_ge():
    assert BHRD >= exampleMonth
    assert not (exampleMonth >= BHRD)
def test_adding_tuple():
    assert exampleMonth + (1,12) == (3,5,107)

# Try negitave time
def test_negetive_result():
    assert BHRD - (7,) == (-5, 5, 204)
    assert BHRD - (7, 5, 204) == (-5,)
    assert BHRD - (7, 6) == (-6, 23, 204)

# Test indexing
def test_index_retreval():
    assert BHRD[0] == 2
    assert BHRD[1] == 5
    assert BHRD[2] == 204
def test_index_setting():
    newExample = timeInterval()
    newExample[0] = 1
    newExample[1] = 2
    newExample[2] = 3
    assert newExample[0] == 1
    assert newExample[1] == 2
    assert newExample[2] == 3
def test_index_out_of_bounds():
    try: assert BHRD[3]
    except IndexError : pass

def test_non_tuple_comparison():
    try: assert BHRD == 2
    except TypeError as err: 
        assert err.args[0] == "Can only compare timeInterval or tuple"
    try: assert BHRD >= 2
    except TypeError as err: 
        assert err.args[0] == "Can only compare timeInterval or tuple"
def test_non_tuple_math():
    try: BHRD + 2
    except TypeError as err: 
        assert err.args[0] == "Can only add timeInterval or tuple"
    try: BHRD - 2
    except TypeError as err: 
        assert err.args[0] == "Can only subtract timeInterval or tuple"

def test_len_func():
    assert len(BHRD) == 3
    assert len(solarYear) == 2
    assert len(timeInterval(1)) == 1
    assert len(timeInterval()) == 0
def test_eq():
    assert BHRD == (2, 5, 204)
def test_gt():
    assert BHRD >= (1,2,3)
