#!/bin/bash
# Install and configure wxstation
# Created by Steven Fairchild on 20210407
if [[ "$(whoami)" != "root" ]]; then
    clear
    printf "Must run as root user or with sudo.\nExiting!\n"
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
wxstation_password='P@ssw0rd'
database_name='weather'
user='wxstation'

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
        echo "Successfully install python packages"
    else
        echo "$error_msg"
    fi
}
# Create and setup mariadb
setup_db() {
    printf "Configuring weather database\nSetting root password\n"
    mysql -e "UPDATE mysql.user SET Password = PASSWORD('$root_password') WHERE User = 'root'"
    echo "Creating $database_name database"
    mysql -e "CREATE DATABASE IF NOT EXISTS $database_name;"
    echo "Creating user $user@localhost"
    mysql -e "CREATE USER IF NOT EXISTS '$user'@localhost IDENTIFIED BY '$wxstation_password';"
    echo "Granting $user privileges to $database_name"
    mysql -e "GRANT ALL PRIVILEGES ON \`$database_name\`.* TO '$user'@localhost;"
    echo "Reloading grant tables"
    mysql -e "FLUSH PRIVILEGES;"
    echo "Creating sensors table"
    mysql -e "USE weather; \
            CREATE TABLE IF NOT EXISTS sensors ( \
            ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT, \
            stationid VARCHAR(10), \
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
            ambient_temperature DECIMAL(6,3) NOT NULL, \
            wind_direction DECIMAL(6,3), \
            wind_speed DECIMAL(6,3), \
            wind_gust_speed DECIMAL(6,3), \
            humidity DECIMAL(6,3) NOT NULL, \
            rainfall DECIMAL(6,3), \
            air_pressure DECIMAL(6,3) NOT NULL, \
            PM25 DECIMAL(6,3), \
            PM10 DECIMAL(6,3) \
            );"
    echo "Creating packets table"
    mysql -e "USE weather; \
            CREATE TABLE IF NOT EXISTS packets( \
            ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT, \
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  \
            packet VARCHAR(100) NOT NULL, \
            transmitted BOOL NOT NULL \
            );"
    echo "Mariadb has been setup!"
}
if [[ "$1" == "--database-only" ]]; then
    echo "Setting up database only!"
    setup_db
    echo "Done setting up database!"
    exit 0
fi
create_user
install_pkgs
setup_db
echo "All done!"
exit 0