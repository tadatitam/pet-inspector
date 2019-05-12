import time                                 # for sleeping for a given duration
import sys                                  # some prints, exit
import os, platform                         # for running  os, platform specific function calls
import json                                 # for reading configuration files
from selenium import webdriver              # for running the driver on websites
from selenium.webdriver.common.keys import Keys     # for pressing enter on Chrome and Tor

from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def press_enter(t):
    time.sleep(t)
    try:
        self.driver.switch_to.alert.send_keys(Keys.ENTER)
    except:
        pass

def get_display_parameters(config):
    config_file = "../client/vm/configs/"+config+".config.json"
    with open(config_file) as json_data:
        d = json.load(json_data)
        if("displaywidth" in d):
            width = d["displaywidth"]
        if("displayheight" in d):
            height = d["displayheight"]
        if("displaydepth" in d):
            depth = d["displaydepth"]
        return width, height, depth

class PetConfig:
    def __init__(self):
        self.petfco={"ghf": "ghostery_f",
                "apf": "adblock_plus_f",
                "fb": "fp_block",
                "uof": "ublock_origin_f",
                "df": "disconnect_f",
                "pbf": "privacy_badger_f",
                "cfbf": "canvas_fingerprint_blocker_f",
                "cb": "canvasblocker",
                "sf": "stop_fingerprinting",
                "ss": "shape_shifter",
                "cdf": "canvas_defender_f",
                "to": "totalspoof",
                "bl": "blender",
                "nee": "no_enumerable_extensions",
                "bi": "blend_in",
                "ns": "no_script",
                "ss": "scriptsafe_f"}

        self.petcco={"ghc": "ghostery_c",
                "apc": "adblock_plus_c",
                "uoc": "ublock_origin_c",
                "cfb": "canvas_fingerprint_block",
                "cdc": "canvas_defender_c",
                "sc": "scriptsafe",
                "rg": "rubber_glove",
                "gl": "glove",
                "rua": "random_user_agent",
                "pe": "privacy_extension",
                "hmf": "hide_my_footprint",
                "dc": "disconnect_c",
                "pbc": "privacy_badger_c",
                "tr": "trace"}

        self.petf = {"None":"", "ghostery_f": "ghostery-7.3.3.7.xpi", 
                "ghostery_f": "ghostery-7.3.3.7.xpi",
                "adblock_plus_f": "adblock_plus-3.0.2.xpi",
                "fp_block": "fp_block-1.0.1.xpi",
                "ublock_origin_f": "ublock_origin-1.14.14.xpi",
                "disconnect_f": "disconnect-5.18.21.xpi",
                "privacy_badger_f": "privacy_badger-2017.11.20.xpi",
                "canvas_fingerprint_blocker_f": "canvas_blocker_no_fingerprint-0.1.1-an+fx.xpi",
                "canvasblocker": "canvasblocker-0.4.0.2.xpi",
                "stop_fingerprinting": "stop_fingerprinting-0.1.0.xpi",
                "shape_shifter": "shape_shifter-0.0.2.xpi",
                "canvas_defender_f": "canvas_defender-1.1.0.xpi",
                "totalspoof": "totalspoof-1.20.xpi",
                "blender": "blender-0.1.7.xpi",
                "no_enumerable_extensions": "no_enumerable_extensions-0.0.1.xpi",
                "blend_in": "blend_in-61.0t52-an+fx.xpi",
                "no_script": "noscript-5.1.8.3.xpi",
                "scriptsafe_f": "scriptsafe-1.0.9.8.xpi",
                "fprandom": "fprandom/firefox",
                "tracking_protection":"", "cookie_blocking":""}

        self.petc = {"None":"", "do_not_track":"", 
                "ghostery_c": "ghostery-7.3.3.7.crx",
                "adblock_plus_c": "adblock_plus-1.13.4.crx",
                "ublock_origin_c": "ublock_origin-1.14.8.crx",
                "canvas_fingerprint_block": "canvas_fingerprint_block-1.5.crx",
                "canvas_defender_c": "canvas_defender-1.1.0.crx",
                "scriptsafe": "scriptsafe-1.0.9.1.crx",
                "rubber_glove": "rubber_glove-14.7.8.0.crx",
                "glove": "glove-0.1.1.crx",
                "random_user_agent": "Random-User-Agent_v2.2.5.crx",
                "privacy_extension": "privacy_extension-1.1.crx",
                "hide_my_footprint": "hide_my_footprint-1.3.2.crx",
                "disconnect_c": "disconnect-5.18.23.crx",
                "privacy_badger_c": "privacy_badger-2017.11.20.crx",
                "trace": "trace-1.0.2.crx"}

        self.pet = {"firefox":self.petf,"chrome":self.petc}
        self.petco = {"firefox":self.petfco,"chrome":self.petcco}

        self.driver_path = {"linux" : {"firefox": "drivers/geckodriver_linux", "chrome": "drivers/chromedriver_linux"},
                            "windows" : {"firefox": "drivers\\geckodriver.exe", "chrome": "drivers\\chromedriver.exe"},
                            "darwin" : {"firefox": "drivers/geckodriver_macos", "chrome": "drivers/chromedriver_macos"} }

        self.petpf = {"tracking_protection": ["privacy.trackingprotection.enabled",True],
                    "cookie_blocking":  ["network.cookie.cookieBehavior", 2]} 
        self.petpc = {"do_not_track" : ["prefs", {"enable_do_not_track": True}]}

        self.petp = {"firefox":self.petpf,"chrome":self.petpc}    

        self.addons_path = {"firefox" : os.path.join("addons","firefox"),
                            "chrome" : os.path.join("addons","chrome") }

        # TODO: update the path variables and other related values based on your own machine configuration
        self.browser_path = {"linux" : {"firefox": { "native": "/home/milan/MYPET/SOFT/firefox/firefox", 
                                                     "vm": "/usr/bin/firefox",
                                                   },
                                        "chrome": { "native": "/usr/bin/google-chrome",
                                                    "vm": "/usr/bin/google-chrome"
                                                  }
                                        },
                            "windows" : {"firefox": { "native": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                                                      "vm": ""
                                                    }, 
                                        "chrome": { "native": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                                                    "vm": ""
                                                  }
                                        },
                            "darwin" : {"firefox": { "native":"/Applications/Firefox.app/Contents/MacOS/firefox",
                                                     "vm": ""
                                                   },
                                        "chrome": { "native": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                                                    "vm": ""
                                                  }
                            }}                            

        self.unsupported = [("windows","firefox","fprandom"), ("windows", "chrome", "fprandom"), ("darwin", "chrome", "fprandom"), ("darwin", "firefox", "fprandom")]

        self.tor_native_path = {"darwin": "/Applications/TorBrowser.app/Contents/MacOS/firefox",
                             "linux": "/home/milan/MYPET/SOFT/TOR/tor-browser_en-US",
                             "windows": "C:\\Users\\Milan\\MYPET\\Tor Browser"
                        } 

        self.brave_path = {"native": { "windows": "",
                                "darwin": "/Applications/Brave.app/Contents/MacOS/Brave",
                                "linux": ""
                                },
                          "vm": { "linux": "/usr/bin/brave",
                                     "darwin": "",
                                     "windows": ""
                                   }
                        }



    def getPetBrowserDriverPath(self,my_pet,my_browser,env_type):
        plt= platform.system().lower()

        # Exit if (plt, my_pet, my_browser) is not supported 
        for (o,b,p) in self.unsupported:
            if (plt == o and my_pet == p and my_browser == b):
                print "Platform:" + plt + " Browser:" + my_browser + " Pet:" + my_pet + " not supported"
                sys.exit(0)

        # Exit if platform is not supported
        if plt not in self.browser_path.keys():
            print "Platform: " + plt + " not supported"
            sys.exit(0)

        # Exit if browser is not supported under the given platform 
        if my_browser not in self.browser_path[plt].keys():
            print "Browser: " + my_browser + "not supported"
            sys.exit(0)

        cwd = os.path.dirname(os.path.abspath(__file__))
        special_pets = ["tor", "brave"]
        
        if my_pet not in special_pets:
            # Retrieve the correct path for the browser executable
            bPath = self.browser_path[plt][my_browser][env_type]
            if bPath != "": bPath = os.path.join(cwd,bPath) 

            # Retrieve the correct path for the driver
            dPath = self.driver_path[plt][my_browser]
            if dPath != "": dPath = os.path.join(cwd, dPath) 
            
            if my_pet in self.petco[my_browser].keys(): my_pet = self.petco[my_browser][my_pet] 
            if my_pet not in self.pet[my_browser].keys():
                print "PET: " + my_pet+ " not supported in" + my_browser
                sys.exit(0)
            aPath = self.pet[my_browser][my_pet]
            if aPath != "":  aPath = os.path.join(cwd, self.addons_path[my_browser], aPath)

            pref = self.petp[my_browser][my_pet] if my_pet in self.petp[my_browser].keys() else None
            # TODO: linux firefox fprandom
#            if my_pet == "fprandom":
#                bPath = aPath
#                dPath = os.path.join(cwd, "drivers/geckodriver")
#                aPath = None

            return aPath, bPath, dPath, pref 
        else:
            if my_pet == "brave":
                dPath = os.path.join(cwd, self.driver_path[plt]["chrome"])
                bPath = self.brave_path[env_type][plt]
                return bPath, dPath

            elif my_pet == "tor":
                if plt == "darwin":
                    gecko = "drivers/tor/geckodriver_macos"
                elif plt == "linux":
                    gecko = "drivers/tor/geckodriver_linux"
                # TODO: if windows, add another case and download the correct geckodriver under drivers/tor from https://github.com/mozilla/geckodriver/releases/tag/v0.17.0
                dPath = os.path.join(cwd, gecko)
                bPath = self.tor_native_path[plt]
                return bPath, dPath

    
class Browser:
    
    def __init__(self, config, browser, pet, env_type, proxy_setting):

        """
        If given valid proxy settings, this function will configure socks5 proxy properly on chrome (brave) and firefox.
        """
        def setup_socks5_proxy(browser, profile, proxy_setting):
            if proxy_setting is not None:
                address = proxy_setting["address"]
                port = proxy_setting["port"]
                bypass_list = proxy_setting["bypass-list"]

                if browser == "chrome":
                    # https://sordidfellow.wordpress.com/2015/05/21/ssh-tunnel-for-chrome/
                    profile.add_argument("--proxy-server=socks5://%s:%s" % (address, port))
                    profile.add_argument("--proxy-bypass-list=%s" % bypass_list)
                    print("socks5 proxy configured on chrome")

                elif browser == "firefox":
                    # https://developer.mozilla.org/en-US/docs/Mozilla/Preferences/Mozilla_networking_preferences
                    profile.set_preference("network.proxy.type", 1)
                    profile.set_preference("network.proxy.socks", address)
                    profile.set_preference("network.proxy.socks_port", port)
                    profile.set_preference("network.proxy.socks_version", 5)
                    profile.set_preference("network.proxy.socks_remote_dns", "true")
                    profile.set_preference("network.proxy.no_proxies_on", bypass_list)
                    print("socks5 proxy configured on firefox")

        """
            If the program is run in a virtual machine, xvfbwrapper has to get installed first.        
        """
        self.env_type = env_type
        if (env_type == "vm"):
            print("xvfb")
            from xvfbwrapper import Xvfb
            width, height, depth = get_display_parameters(config)
            self.vdisplay = Xvfb(width=width, height=height, colordepth=depth)
            self.vdisplay.start()

        print("Browser:", browser, "PET:", pet)
        pet_config = PetConfig()

        if pet == "brave":
            print("brave")
            chrome_options = ChromeOptions()
            bPath, dPath = pet_config.getPetBrowserDriverPath(pet,browser,env_type)
            print(bPath, dPath)
            chromedriver = dPath
            chrome_options.binary_location = bPath
            setup_socks5_proxy("chrome", chrome_options, proxy_setting)
            os.environ["webdriver.chrome.driver"] = chromedriver
            if env_type == "vm":
                chrome_options.add_argument("--no-sandbox")
            self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
            press_enter(1)
            return

        elif pet == "tor":
            plt= platform.system().lower()
            if plt == "darwin" or plt == "windows": # https://stackoverflow.com/questions/15316304/open-tor-browser-with-selenium
                print("native tor")
                bPath, dPath = pet_config.getPetBrowserDriverPath(pet,browser,env_type)
                print(bPath, dPath)
                profile = FirefoxProfile()
                profile.set_preference("network.proxy.type", 0)
                binary = FirefoxBinary(bPath)
                self.driver = webdriver.Firefox(firefox_profile = profile, firefox_binary= binary, executable_path = dPath)
            elif plt == "linux": # https://medium.com/@manivannan_data/selenium-with-tor-browser-using-python-7b3606b8c55c
                print("vm tor")
                from tbselenium.tbdriver import TorBrowserDriver
                pref_dict = {"network.proxy.no_proxies_on": "http://10.0.2.2/, http://192.168.4.204/"}
                self.driver = TorBrowserDriver(os.environ['TBB_PATH'], pref_dict = pref_dict)
            return


        aPath, bPath, dPath, pref = pet_config.getPetBrowserDriverPath(pet,browser,env_type)
        if (browser == "firefox"):
            fp = FirefoxProfile()
            setup_socks5_proxy("firefox", fp, proxy_setting)
            binary = FirefoxBinary(bPath)
            if pref != None:
                fp.set_preference(pref[0],pref[1])
            self.driver = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary, executable_path=dPath)

            if (aPath):
                self.driver.install_addon(aPath)            

        elif (browser == "chrome"):
            chrome_options = ChromeOptions()
            chrome_options = webdriver.ChromeOptions() #https://github.com/SeleniumHQ/selenium/issues/5966
            setup_socks5_proxy("chrome", chrome_options, proxy_setting)

            if aPath:
                chrome_options.add_extension(aPath)
            if pref != None:
                chrome_options.add_experimental_option(pref[0],pref[1])
	        chrome_options.binary_location = bPath
            os.environ["webdriver.chrome.driver"] = dPath
	    
            time.sleep(1)
            self.driver = webdriver.Chrome(executable_path=dPath, chrome_options=chrome_options)
            # to escape the alert chrome display on first visit
            time.sleep(1)
            press_enter(1)
        elif(browser == "safari"):
            self.driver = webdriver.Safari()
        else:
            print("Unsupported Browser")
            sys.exit(0)

    def quit(self):
        try:
            self.driver.quit()
        except:
            self.driver.close()     # for Tor
        if (self.env_type == "vm"):
            self.vdisplay.stop()


    def visit_sites(self, site_list, delay=5): 
        """Visits all pages in site_list with delay"""
        for site in site_list:
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                self.driver.get(site)
                time.sleep(delay)
            except:
                print("Unexpected error:", sys.exc_info()[0])
