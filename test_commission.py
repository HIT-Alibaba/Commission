from datetime import date
from Commission.utils import date_from_string, get_commission
from Commission.utils import get_total_sales_before_commission as get_total


def test_date_from_string():
    d = date_from_string("2015-1-2")
    assert d == date(2015, 1, 2)

    
def test_get_commission_with_not_qualified_sales():
    r1 = get_commission(0, 10, 10)
    r2 = get_commission(10, 0, 10)
    r3 = get_commission(10, 10, 0)
    assert r1 == 0 
    assert r2 == 0
    assert r3 == 0
   
    
def test_get_commission_with_qualified_sales_less_than_1000():
    r1 = get_commission(5, 5, 1)
    t1 = get_total(5, 5, 1) 
    assert r1 == t1 * 0.1
    
    
def test_get_commission_with_qualified_sales_equals_1000():
    r2 = get_commission(10, 10, 10)
    t2 = get_total(10, 10, 10) 
    assert r2 == 1000 * 0.1
   
    
def test_get_commission_with_qualified_sales_more_than_1000_less_than_1800():
    r3 = get_commission(10, 10, 11)
    t3 = get_total(10, 10, 11) 
    assert r3 == (1000 * 0.1 + (t3 - 1000) * 0.15)
    
    
def test_get_commission_with_qualified_sales_equals_1800():
    r4 = get_commission(20, 20, 12)
    t4 = get_total(20, 20, 12)
    assert r4 == 1000 * 0.1 + 800 * 0.15
    
    
def test_get_commission_with_qualified_sales_more_than_1800():
    r5 = get_commission(20, 20, 20)
    t5 = get_total(20, 20, 20)
    assert r5 == (1000 * 0.1 + 800 * 0.15 + (t5 - 1800) * 0.2)