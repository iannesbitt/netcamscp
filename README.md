# NetCamSCP
Local network webcam image retriever and uploader intended to work with EC2 PEM keys. This script is intended to be run from cron, launchd, or a similar Windows scheduler.

## Setup

#### Installation on Unix/Linux
Unzip this package to a directory you have read, write, and execute access to, like your home directory `~/`. Ensure the shebang (the directory string at the beginning of the python executable, starting with `#!`) points to the directory specified by the `which python` command in your terminal. By default, it is set to `#!/usr/local/bin/python`, which is a pretty standard directory for a Unix python version installed with Homebrew, but yours may be different. Linux users: you may have success using `#!/usr/bin/env python`. Proceed to the **Settings** section.

#### Installation on Windows
Unzip this package to a directory you have read, write, and execute access to, like your home directory. Proceed to the **Settings** section.

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
  - **"verbose"** - `true` or `false` depending on whether or not you would like more print output.

#### Scheduling
If you intend to use this script in a repetitive manner as is intended, you will want to schedule it to run every x minutes or hours. On Unix/Linux, this means using `launchd` or `crontab`. On Windows, this means using Windows Scheduler. Windows Scheduler is a fairly straightforward GUI tool and thus I won't cover it here. Basically, you point it at the location of the `netcamscp.py` file and set a time interval. I have set up this script with Windows Scheduler and achieved good results.

On Mac, Linux, or other *nix, scheduling is usually run through `crontab`. Sadly, as of 2016, Apple seems to be quietly phasing out `crontab` support at some point in the near future. Nevertheless at El Capitan 10.11.5 they still include access to `crontab` features and I plan on using it until they forcibly wrest it from my hands. Side rant to no one: Why get rid of something so simple that works so well? Admittedly, it's not hard to convert cron jobs to launchd jobs, but Apple has opted for XML formatting in `launchd` which turns simple one-liner cron jobs into like, sixty lines of XML ugliness. I don't get it. Anyway, here's what you need to make `crontab` jobs.

##### `crontab` setup
  - Run crontab -e as yourself (not root) which will open your cron scheduler in the vim editor (unless, like me, you've changed your default editor to nano)
  - Add the following line, replacing x with an integer >= 1 (your script will run every x minutes): `*/x * * * * ~/netcamscp/netcamscp.py 2>&1` (the `2>&1` bit tells the cron emailer not to email you the logs, which is nice considering it runs every x minutes.)
    - Obviously, if you don't unzip pywx to your home folder (`~/`), you'll need to replace the path with the location of the root pywx folder.
    - If you'd like a log to be kept, you can modify the cron job to append the print output of the program to a file like the following: `*/x * * * * ~/netcamscp/netcamscp.py cap.Actions.all >> ~/pywx/pywx.log 2>&1`
  - Save the crontab file and quit the editor.
