#!/bin/bash
# Author: ELNAMAKI
# Initial requirements for running the tools developed in this class for code visualization and analysis.

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_file="installation_log.txt"

# Define the list of packages and their dependencies
packages=("pydot" "ast" "termcolor" "prettytable" "matplotlib")
dependencies=("graphviz" "python-ast" "python-termcolor" "python-prettytable" "python-matplotlib")

# Function to check if a package is installed
check_package() {
    if ! python -c "import $1" &> /dev/null; then
        return 1
    fi
    return 0
}

# Function to check if a dependency is installed
check_dependency() {
    if ! dpkg -l | grep -q "^ii\s*$1\s"; then
        return 1
    fi
    return 0
}

# Function to install a package
install_package() {
    echo -e "${YELLOW}Installing $1...${NC}"
    pip install $1 > /dev/null 2>&1
}

# Function to display a progress bar
progress_bar() {
    local duration=$1
    local steps=$2
    local step_duration=$((duration / steps))
    local progress_char="▉"
    local empty_char="▁"
    local progress=""
    for ((i = 0; i <= steps; i++)); do
        progress+="▉"
        echo -ne "${GREEN}[${progress}${empty_char:$i}]${NC} Installing... ($((i * 100 / steps))%)\r"
        sleep $step_duration
    done
    echo -e "${GREEN}[${progress}]${NC} Installation complete!            "
}

# Main installation loop
for package in "${packages[@]}"; do
    if ! check_package $package; then
        # Check for dependencies before installing
        package_index=$((${!packages[@]}))
        dependency=${dependencies[$package_index]}
        if ! check_dependency $dependency; then
            echo -e "${RED}Error: $dependency is not installed. Please install it first.${NC}"
            echo "$(date +'%Y-%m-%d %H:%M:%S') - Error: $dependency is not installed." >> $log_file
        else
            read -p "Package '$package' is not installed. Do you want to install it? (y/n): " choice
            if [ "$choice" == "y" ]; then
                install_package $package
                progress_bar 5 20 # Simulated progress bar for demonstration
                echo "$(date +'%Y-%m-%d %H:%M:%S') - Installed $package." >> $log_file
            else
                echo -e "${RED}Skipping installation of $package.${NC}"
                echo "$(date +'%Y-%m-%d %H:%M:%S') - Skipped installation of $package." >> $log_file
            fi
        fi
    else
        echo -e "${GREEN}$package is already installed.${NC}"
    fi
done

# Print colorful message
echo -e "${BLUE}Now you can use${NC}"
echo -e "${RED}  _____   _____ _____ "
echo -e " |  __ \\ / ____|_   _|"
echo -e " | |  | | |      | |  "
echo -e " | |  | | |      | |  "
echo -e " | |__| | |____ _| |_ "
echo -e " |_____/ \\_____|_____|"
echo -e "                      "
echo -e "      tools ${NC}"
