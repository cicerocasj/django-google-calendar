# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  
  config.vm.provision "shell", path: "provisioning/main.sh"
  config.vm.synced_folder ".", "/home/vagrant/django-google-calendar", create: true
end
