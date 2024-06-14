import pytest
import time
import subprocess
import threading


def test_the_package_imports():
    """
    The module loads, and looks like what we expect.
    """
    from pspy import pspy as pspy_module
    
    assert pspy_module is not None
    P = pspy_module.PSpy()
    assert P is not None
    assert P.pids is not None     

def test_i_see_my_pids_i_create():    
    from pspy import pspy as pspy_module
    P = pspy_module.PSpy()
    SLEEP_TIME = 10
    print(f"Sleeping {SLEEP_TIME}s, to see if I can catch new processes.")    
    subprocess.Popen(["for i in {1..10}; do ping 8.8.8.8 -c 1; sleep 1; done"],shell=True)    
    new_pids = P.Spin(10)
    #if we have none.. I dunno what wacky environ we are in..
    assert len(new_pids) > 0
    found_ping = False
    found_bash = False
    for pid in new_pids:
        (p,u,c) = pid
        if c.strip() == "ping 8.8.8.8 -c 1":
            found_ping = "found_ping"
        if c.strip() == "/bin/sh -c for i in {1..10}; do ping 8.8.8.8 -c 1; sleep 1; done":
            found_bash = "found_bash"

    #kinda silly, but helps output on pytest -v
    assert found_ping == "found_ping"
    assert found_bash == "found_bash"    
    assert P is not None    


def test_stuff():
    assert True == True