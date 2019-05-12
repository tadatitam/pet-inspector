import os                           # for file operations
from subprocess import call         # for calling shell code
import re                           # for splitting self.os
import sys                          # for exit
import json                         # for reading configuration files

class VM(object):
    """
    Currently, we only consider Linux-based VMs.
    """
    def __init__(self, exp, os, config, browsers, pets, repeats, exp_config, server_config, memory=2048, diskspace=12000, gui="false"):
        self.vagrant_file = "Vagrantfile"
        self.create_file(self.vagrant_file)
        self.provision_file = "provision.sh"
        self.create_file(self.provision_file)
        self.execute_file = "execute.sh"
        self.create_file(self.execute_file)
        self.exp = exp
        self.os = os
        self.config = config
        self.browsers = browsers
        self.pets = pets
        self.repeats = repeats
        self.exp_config = exp_config
        self.server_config = server_config 
        self.memory = memory
        self.diskspace = diskspace
        self.gui = gui
        self.generate_vagrant()
        self.generate_provision()
        self.configure_execute()
        self.generate_execute()
    
    def generate_vagrant(self):
        fo = open(self.vagrant_file, "a")
        fo.write("Vagrant.configure(2) do |config|\n")
        fo.write("  config.vm.box = \"%s\"\n" % self.os)
        fo.write("  config.vm.provider \"virtualbox\" do |vb|\n")
        fo.write("    vb.gui = %s\n" % self.gui)
        fo.write("    vb.memory = \"%s\"\n" % self.memory)
#         fo.write("    vb.customize [\"modifyhd\", \"disk id\", \"--resize\", \"%s\"\n" % self.diskspace)
        fo.write("  end\n")
        fo.write("  config.ssh.forward_agent = true\n")
        fo.write("  config.ssh.forward_x11 = true\n")
        fo.write("  config.vm.provision :shell, path: \"%s\"\n" % self.provision_file)
        fo.write("end\n")
        fo.close()
    
    def generate_provision(self):
        fo = open(self.provision_file, "a")
        fo.write("#!/bin/bash\n")
        fo.write("apt-get update\n")
        fo.write("apt-get install -y xvfb python-pip python-dev\n")
        fo.write("apt-get install -y iceweasel\n")      # for debian jessie
        fo.write("pip install selenium==3.12.0\n")
        fo.write("pip install tbselenium xvfbwrapper\n")
        # moving appropriate firefox_profile.py file to selenium so that addons work
        fo.write("sudo cp /vagrant/collection/start_visit/addons/firefox_profile.py /usr/local/lib/python2.7/dist-packages/selenium/webdriver/firefox/\n")
        fo.close()
    
    def configure_execute_langver(self, lang, fo, d):
        # update locale
        if(lang=="de"):
            char = "de_DE.UTF-8"
        elif(lang=="fr"):
            char = "fr_FR.UTF-8"
        elif(lang=="ru"):
            char = "ru_RU.UTF-8"
        elif(lang=="ar"):
            char = "ar_SA.UTF-8"
        elif(lang=="ja"):
            char = "ja_JP.UTF-8"
        elif(lang=="ta"):
            char = "ta_IN.UTF-8"
        elif(lang=="vi"):
            char = "vi_VN.UTF-8"
        elif(lang=="en"):
            lang = "en-US"
            char = "en_EN.UTF-8"
        else:
            raw_input("Unsupported language")
            sys.exit(0)
        fo.write("sudo locale-gen "+char+"\n")
        fo.write("export LANG="+char+"\n")
        
        if("torver" in d):
            torver = d["torver"]
        else:
            torver = "8.0.2"
        if("bravever" in d):
            bravever = d["bravever"]
        else:
            #bravever = "latest"
            bravever = "0.19.134"
        if("firefoxver" in d):
            firefoxver = d["firefoxver"]
        else:
            firefoxver = "56.0"
        if("chromever" in d):
            chromever = d["chromever"]
        else:
            #chromever = "latest"
            chromever = "63.0.3239.108"

        # TODO: later include version info during the download stage        
        # for installing Firefox:
        fo.write("\necho \"Installing Firefox\"\n")
        fo.write("sudo apt-get purge firefox -y\n")
        fo.write("sudo rm -rf /opt/firefox\n")
        fo.write("wget -O firefox.tar.bz2 https://ftp.mozilla.org/pub/firefox/releases/"+firefoxver+"/linux-x86_64/"+lang+"/firefox-"+firefoxver+".tar.bz2\n")
        fo.write("tar -xjf firefox.tar.bz2\n")
        fo.write("sudo mv firefox /opt/\n")
        fo.write("sudo mv /usr/bin/firefox /usr/bin/firefox_old\n")
        fo.write("sudo ln -s /opt/firefox/firefox /usr/bin/firefox\n")
        fo.write("sudo rm -f firefox.tar.bz2\n")
        
       # for installing Tor:
        fo.write("\necho \"Extracting Tor\"\n")
        fo.write("wget -O tor.tar.xz https://www.torproject.org/dist/torbrowser/"+torver+"/tor-browser-linux64-"+torver+"_"+lang+".tar.xz\n")
        fo.write("tar -xvJf tor.tar.xz\n")
        fo.write("sudo rm -f tor.tar.xz\n")
        fo.write("\nexport TBB_PATH=$(pwd)/tor-browser_" + lang + "/\n")
        
       # for configuring correct geckodriver for Tor
        fo.write("sudo cp /vagrant/start_visit/drivers/tor/geckodriver_linux /usr/local/bin/geckodriver\n")

        # for installing Chrome:
        fo.write("\necho \"Installing Chrome\"\n")
        fo.write("sudo apt-get install -y libxss1 libappindicator1 libindicator7\n")
        if chromever == "latest":
            fo.write("wget -O google.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb\n")
        else:
            fo.write("wget -O google.deb https://www.slimjet.com/chrome/download-chrome.php?file=lnx%2Fchrome64_" + chromever + ".deb\n")
        fo.write("sudo dpkg -i google.deb\n")
        fo.write("sudo apt-get -f install -y\n")
        fo.write("sudo rm -f google.deb\n")

        
        # for installing Brave:
        fo.write("\necho \"Installing Brave\"\n")
        if bravever == "latest":    
            fo.write("wget -O brave.deb https://laptop-updates.brave.com/latest/dev/ubuntu64\n")
        else:
            #fo.write("wget -O brave.deb %s\n" % bravever)
            fo.write("wget -O brave.deb https://github.com/brave/browser-laptop/releases/download/v" + bravever + "dev/brave_" + bravever + "_amd64.deb\n")
        if("ubuntu" in self.os):
            fo.write("sudo dpkg -i brave.deb\n")
        elif("debian" in self.os):
            fo.write("sudo apt-get install -y gdebi\n")
            fo.write("sudo gdebi brave.deb\n")
        fo.write("sudo apt-get -f install -y\n")
        fo.write("sudo rm -f brave.deb\n")

    def configure_execute(self):
        fo = open(self.execute_file, "a")
        fo.write("#!/bin/bash\n")
        if(self.config != "None"):
            parent_path = os.path.dirname(os.path.abspath(__file__))
            config_file = "configs/"+self.config+".config.json"
            with open(os.path.join(parent_path, config_file)) as json_data:
                d = json.load(json_data)
                if("fonts" in d):
                    fo.write("\nmkdir ~/.fonts\n")
                    for font in d["fonts"]:
                        fo.write("sudo cp /vagrant/client/vm/configs/fonts/%s.ttf ~/.fonts/\n" % font)
                if("timezone" in d):
                    tz = d["timezone"]
                    fo.write("sudo timedatectl set-timezone %s\n" % tz)
                if("language" in d):
                    lang = d["language"]
                    self.configure_execute_langver(lang, fo, d)
        fo.close()
    
    def generate_execute(self):
        fo = open(self.execute_file, "a")
        fo.write("cd /vagrant/start_visit\n")
        fo.write("export PATH=$PATH:/vagrant/start_visit/drivers\n")
        fo.write("sudo cp /vagrant/start_visit/addons/firefox_profile.py /usr/local/lib/python2.7/dist-packages/selenium/webdriver/firefox/\n")
        
#         fo.write("export PATH=$PATH:drivers/chromedriver_macos\n")
#         fo.write("export PATH=$PATH:drivers/chromedriver_linux\n")
        for browser in self.browsers:
            for pet in self.pets[browser]:
                fo.write("python start_pet.py %s %s %s %s %s vm %s %s %s\n" % (self.exp, re.split("/", self.os)[-1], self.config, browser, pet, self.repeats, self.exp_config, self.server_config))
        fo.close()
    
    def create_file(self, file):
        PATH="./"+file
#        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
#            response = raw_input("This will overwrite file %s... Continue? (Y/n)" % file)
#            if response == 'n':
#                sys.exit(0)
        fo = open(file, "w")
        fo.write("# This is an auto-generated file. Do not edit. Your edits will be discarded upon next experiment run\n")
        fo.write("# In order to make changes reflect here, update the corresponding methods in vm/vm.py\n")
        fo.close()
    
    def provision(self):
        # run vagrant up
        call(["vagrant", "up", "--provision"])
        
    def launch(self):
        # run vagrant up
        call("vagrant ssh -c 'sh /vagrant/execute.sh'", shell=True)#; sh /vagrant/execute.sh'"])
        
    def package(self):
        name = self.exp+re.split("/", self.os)[-1]+self.config
        try:
            os.remove(name)
        except OSError:
            pass            
        call(["vagrant", "package", "--output", name])
        
    def quit(self):
        # remove vagrant and execute files
        call(["vagrant", "halt"])
        
    def destroy(self):
        # run vagrant destroy
        call(["vagrant", "destroy", "-f"])
        


if __name__ == '__main__':
    vm = VM()
    vm.create()
