import zipfile
import os
import shutil
import configparser
from tkinter import filedialog, Tk

configFileName = 'zipperConfig.ini'  # Use a consistent config file name

def writeConfig(sourceDirectory, outputDirectory, configFile=configFileName):
    config = configparser.ConfigParser()
    config['Paths'] = {
        'SourceDirectory': sourceDirectory,
        'OutputDirectory': outputDirectory
    }
    with open(configFile, 'w') as configfile:
        config.write(configfile)

def readConfig(configFile=configFileName):
    config = configparser.ConfigParser()
    if not os.path.exists(configFile):
        return None, None  # Return None if the config file does not exist
    config.read(configFile)
    try:
        sourceDirectory = config.get('Paths', 'SourceDirectory')
        outputDirectory = config.get('Paths', 'OutputDirectory')
        return sourceDirectory, outputDirectory
    except configparser.NoSectionError:
        return None, None  # Return None if the required section/keys are missing

def selectDirectory(promptMessage):
    # Create a new instance of the Tkinter window inside the function
    window = Tk()
    window.withdraw()  # Make the window invisible
    filePath = filedialog.askdirectory(title=promptMessage)
    window.destroy()  # Destroy the window after use
    return filePath

def zipper(zipFileName='directory_backup.zip'):
    sourceDirectoryPath, outputFilePath = readConfig()

    # If the config file doesn't exist or the paths are not set, ask the user to select them
    if not sourceDirectoryPath or not outputFilePath:
        sourceDirectoryPath = selectDirectory("Select the source directory to zip")
        outputFilePath = selectDirectory("Select the output directory for the zipped file")
        writeConfig(sourceDirectoryPath, outputFilePath)

    # Create a zip file of the source directory
    with zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(sourceDirectoryPath):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(sourceDirectoryPath, '..')))

    # Check if the output directory exists before moving the zip file
    if not os.path.exists(outputFilePath):
        print(f"The specified output directory {outputFilePath} does not exist.")
        outputFilePath = selectDirectory("Select the output directory for the zipped file")
        writeConfig(sourceDirectoryPath, outputFilePath)

    # Move the zip file to the specified output directory
    shutil.move(zipFileName, os.path.join(outputFilePath, zipFileName))

def main():
    # Ensure the current working directory is the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    zipper()

if __name__ == '__main__': #Call main(), it calling zipper() on the way
    main()