import start_browser 
import sys                  # for command line arguments
import time                 # for sleeping for some duration
import json
import ast
import os as oslib
from time import localtime, strftime

def test_pet(exp, os, config, browser, pet, env_type, repeats, exp_config, server_config):

    try:
        def get_server_attributes(data):
            fp_sites = data["fp_sites"]
            use_socks5 = data["socks5_proxy"]
            proxy_setting = None
            if use_socks5:
                proxy_setting = data["proxy_setting"]

            return fp_sites, proxy_setting

        cwd = oslib.path.dirname(oslib.path.abspath(__file__))
        with open(oslib.path.join(cwd, "../", exp_config)) as f:
            data = json.load(f)
            test_behaviors = data["test_behaviors"]

        with open(oslib.path.join(cwd, "../", server_config)) as f:
            data = json.load(f)
            fp_sites, proxy_setting = get_server_attributes(data)

        repeats = int(repeats) if not isinstance(repeats, (int, long)) else repeats

        print("configure the browser")
        unit = sim_browser(config, browser, pet, env_type, proxy_setting)
        time.sleep(5)
        print("visit sites")
        if "cross_reload" in test_behaviors:
            cross_reload(unit, exp, os, config, browser, pet, repeats, fp_sites[0])
        if "cross_site" in test_behaviors:
            cross_site(unit, exp, os, config, browser, pet, fp_sites)
        if "cross_session" in test_behaviors:
            cross_session(unit, exp, os, config, browser, pet, fp_sites[0])

        print("exit")
        cleanup_browser(unit)
    except Exception as e:
        if pet == "tor":
            print("If native, first launch Tor application locally before running the script.\n This is to get SOCKS host running on port 9150.")
        print(e)

def sim_browser(config, browser, pet, env_type, proxy_setting):
    b = start_browser.Browser(config, browser, pet, env_type, proxy_setting)
    return b

def cross_session(unit, exp, os, config, browser, pet, fp_site):
    html_args = "?exp="+exp+"&os="+os+"&config="+config+"&browser="+browser+"&pet="+pet+"&type=session"
    fp_site += html_args
    unit.visit_sites([fp_site+"&sess=0"], delay=10)
    print("Sleeping since", time.strftime("%a, %d %b %Y %H:%M:%S +0000", localtime()))
    time.sleep(2700)        # for 2700 seconds == 45 minutes
    unit.visit_sites([fp_site+"&sess=1"],  delay=10)
    
def cross_site(unit, exp, os, config, browser, pet,  fp_sites):
    time.sleep(10)
    for fp_site in fp_sites:
        html_args = "?exp="+exp+"&os="+os+"&config="+config+"&browser="+browser+"&pet="+pet
        fp_site += html_args
        unit.visit_sites([fp_site], delay=10)

def cross_reload(unit, exp, os, config, browser, pet, repeats, fp_site):
    html_args = "?exp="+exp+"&os="+os+"&config="+config+"&browser="+browser+"&pet="+pet+"&type=reload"
    fp_site += html_args
    repeats = int(repeats)
    for _ in range(repeats):
        unit.visit_sites([fp_site], delay=10)
    sys.stdout.write("\n")
    sys.stdout.flush()

def check(unit, fp_list):
    unit.visit_sites(fp_list)

def cleanup_browser(unit):
    unit.quit()

if __name__ == '__main__':
    if(len(sys.argv) != 10):
        print("Call as follows: python start_pet.py <exp> <os> <config> <browser> <pet> <env_type> <repeats> <exp_config> <server_config>")
        sys.exit(0)

    EXP = sys.argv[1]
    OS = sys.argv[2] 
    CONFIG = sys.argv[3] # "None" if running natively
    BROWSER = sys.argv[4] # "firefox" or "chrome"
    PET = sys.argv[5]
    ENV_TYPE = sys.argv[6] # "native" or "vm"
    REPEATS = sys.argv[7]
    EXP_CONFIG = sys.argv[8] # "vm_all.json" etc.
    SERVER_CONFIG = sys.argv[9] # "vm_server.json" etc

    test_pet(EXP, OS, CONFIG, BROWSER, PET, ENV_TYPE, REPEATS, EXP_CONFIG, SERVER_CONFIG)
