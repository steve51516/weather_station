#!/bin/bash
# Install and configure wxstation
# Created by Steven Fairchild on 20210407

# Print usage message
usage() {
    printf "Script usage\n\t--database-only - Setup database only\n\t--pkgs-only - Install debian and python packages only\n\t --help - Print this message\n"
}

if [[ "$(whoami)" != "root" ]]; then
    echo -e "\n\033[0;31mThis script must be ran as root!"
    echo -e "EXITING! RUN AS ROOT!\n\033[0m"
    usage
    exit 0
else
    clear
fi

# Set environment variables
error_msg="Errors occured. Please review"
debian_pkgs="mariadb-server libmariadb3 libmariadb-dev"
py_pkgs="mariadb bme280pi gpiozero pyserial aprslib"
user="wxstation"
# database setup variables
root_password='password'
db_userpass='P@ssw0rd'
db_name='weather'

# Create user service account and service
create_user() {
    grep wxstation /etc/passwd &> /dev/null
    if [[ "$?" != "0" ]]; then
        useradd -m -d /opt/wxstation -c "wxstation service account" -r wxstation
        usermod -aG tty wxstation
    fi
    cp wxstation.service /etc/systemd/system/
    systemctl --enable wxstation.service
    echo "Installed wxstation.service"
}

install_pkgs() {
    echo "Installing required database packages and connector"
    apt install $debian_pkgs -y
    if [[ "$?" -eq "0" ]]; then
        echo "Successfully installed $debian_pkgs"
    else
        echo "$error_msg"
    fi
    echo "Installing python packages..."
    pip3 install $py_pkgs #--user $user
    if [[ "$?" -eq "0" ]]; then
        echo "Successfully installed python packages"
    else
        echo "$error_msg"
    fi
}

# Create and setup mariadb
setup_db() {
    local sqlscript="$(pwd)/tables.sql"
    printf "Creating $db_name database\n"
    mysql -e "CREATE DATABASE IF NOT EXISTS $db_name;"
    echo "creating $user in mariadb"
    mysql -e "CREATE USER IF NOT EXISTS '$user'@localhost IDENTIFIED BY '$db_userpass';"
    echo "Securing mariadb root account"
    mysql -e "UPDATE mysql.user SET Password = PASSWORD('$root_password') WHERE User = 'root'"
    mysql -e "GRANT ALL PRIVILEGES ON \`$db_name\`.* TO '$user'@localhost;"
    mysql -e "FLUSH PRIVILEGES;"
    mysql < $sqlscript $db_name
}

if [[ ! -z $1 ]]; then
    if [[ "$1" == "--database-only" ]]; then
        echo "Setting up database only!"
        setup_db
        echo "Done setting up database!"
        exit 0
    elif [[ "$1" == "--pkgs-only" ]]; then
        install_pkgs
        echo "Done installing packages!"
        echo "Exiting!"
        exit 0
    elif [[ "$1" == "--help" ]]; then
        usage
    fi
else
    create_user
    install_pkgs
    setup_db
    echo "All done!"
fi
exit 0