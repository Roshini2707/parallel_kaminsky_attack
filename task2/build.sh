# any build steps,
# such as pip install, go build, etc
# should be run here to generate the pada executable
# do not run the executable here
TOOL="pada"
SCRIPT="pada.py"
INSTALL_DIR="$HOME/.local/bin"

# Install essential libraries
pip install pyinstaller scapy dnspython

# Notify user about the compilation process
echo "Beginning the compilation of $TOOL from $SCRIPT"

# Remove any previous build files or artifacts
rm -rf dist build "$TOOL.spec"

# Make the Python script executable
chmod +x "$SCRIPT"

# Use PyInstaller to package the script as a single executable
pyinstaller --onefile "$SCRIPT"

# Grant the necessary raw network access capabilities to the generated file
sudo setcap cap_net_raw+ep ./dist/pada

# Move the compiled tool to the current directory
mv "dist/$TOOL" .

# Create the installation directory if it does not already exist
mkdir -p "$INSTALL_DIR"

# Copy the executable to the installation directory
cp "$TOOL" "$INSTALL_DIR/"

# Set the same network access capabilities on the installed tool
sudo setcap cap_net_raw+ep "$INSTALL_DIR/$TOOL"

# Ensure the executable has the correct permissions
chmod +x "$INSTALL_DIR/$TOOL" "$TOOL"

if [[ ":$PATH:" != ":$INSTALL_DIR:" ]]; then
    echo "There was an issue running the tool."
    echo "Please add this line to your shell configuration file:"
    echo "export PATH=\"$INSTALL_DIR:\$PATH\""
else
    echo "$TOOL is successfully installed and ready to use!"
fi

