# Public Accountability Audits | Youtube Data Scraper


### ⚙️ Setup
To setup this program, download the json credentials file for the service account for your project. This can be done from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Once you have this file, rename it to `creds.json` and move it into the root of this repository.

Update the `channel_list.json` file with the list of handles from the YouTube channels you wish to pull the data from. You can omit the `@` (optional).

**Ensure you install the packages needed for this project:** 
```sh
python3 -m pip install -r requirements.txt
``` 
> 💡 Note: use `python` instead of `python3` if you're running this on Windows.

### Running

To run the program, you just need to run the `main.py` file in the root directory of this repository. Running this from the command line is preferred, as it will not close the command line when an error occurs.
```sh
python main.py
```