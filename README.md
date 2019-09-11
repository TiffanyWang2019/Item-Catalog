# Item Catalog
This project to build a website with Flask, third party OAuths and API endpoints.

## How to run:
1. Download the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
2. Ensure python3, [Vagrant](https://www.vagrantup.com/), and [VirtualBox](https://www.virtualbox.org/) are installed. (I used this [vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile).)
3. Copy my project in the vagrant directory.
4. Open the terminal and navigate to the vagrant folder, and then enter `vagrant up` to bring the server online and `vagrant ssh` to log in.
5. Enter `cd /vagrant/catalog` to navigate to my project folder, and then enter `pip3 install -r requirements.txt`.
6. Run `python3 app.py`.
7. Visit `http://localhost:8000` to access the website

#Output:
The application has following features:
1. Register new users
2. Login and logout
3. Login in with Google Accounts
4. Show categories and items
5. Add categories and items
6. Edit and delete items
7. API Endpoints

You can view the screenshots in output_screenshots folder.
