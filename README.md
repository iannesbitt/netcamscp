# NetCamSCP
Local network webcam image retriever and uploader intended to work with EC2 PEM keys. This script is intended to be run from cron, launchd, or a similar Windows scheduler.
## Setup
#### Installation
Unzip this package to a directory you have read, write, and execute access to. Ensure the hashbang (the directory string at the beginning of the python executable, starting with `#!`) points to the directory specified by the `which python` command in your terminal. Currently, it is set to `#!/usr/local/bin/python`, which is a pretty standard directory for a Unix python version installed with Homebrew.
#### Settings
You must have a `settings.json` file at the root of this project, and each field must be filled out with correct settings in order for this script to operate properly. The settings file is populated with seven string fields and one boolean.
##### Strings
  - **"image_loc"** - The full URL (with prefix) of the image you would like to fetch. Can be self-referential (http://127.0.0.1/image.jpg for example, but code needs to be altered slightly to allow for a local OS path).
  - **"temp_loc"** - The local path where the image will be written. Be careful as this script will overwrite an image of the same name.
  - **"server_hostname"** - The hostname of the remote server to which the image will be copied. This is simply an SSH hostname, no paths. (dev.example.com or 192.168.1.100)
  - **"server_img_loc"** - The server path to copy to once SSH has connected. 
  - **"user"** - The username for the remote server.
  - **"pkey"** - The local path to the .PEM authentication key file, if applicable.
  - **"pswd"** - The password, if applicable.
##### Booleans
  - **"using_pkey"** - Should be set to `true` if using a .PEM hash string file for authentication (necessary for SSH/SCP access to many EC2 instances). `false` if using standard password string.
