import main

def test1():
    print "test1() running.."
    params = {'Country': 2, 'State': 552, 'City': 9676, 'period': 'Haftalik'}
    main.getPrayerTimes(params)

def test2():
    print "test2() running.."
    params = {'Country': 15, 'State': 14073, 'period': 'Haftalik'}
    main.getPrayerTimes(params)

def test3():
    print "test3() running.."
    params = {'Country': 2, 'State': 552, 'City': 9676, 'period': 'Aylik'}
    main.getPrayerTimes(params)

def runTest(x):
    if x == 1:
        test1()
    elif x == 2:
        test2()
    elif x == 3:
        test3()
    else:
        print "Default testcase(test1) called"
        test1()


if __name__ == '__main__':
    runTest(int(raw_input('Select Testcase: ')))
    #test1()
    #test2()
    #test3()