# Bennett LMS Downloader

Script to download and save a well sorted local copy of all the files put on our Learning Managment System at Bennett University.

### Instructions to use

1. From the [releases section](https://github.com/anshuman73/bennett-lms-downloader/releases), download the appropriate zip folder according to your OS.
2. In your terminal run `pip install -r requirements.txt`
3. Extract the files and simply run the executable ```bennett-lms-downloader```.
4. It will ask you for your username and password to login into your LMS account to be able to access your courses and user specific data.
5. Once the credentials are approved, it will automatically create a folder named ```Bennett LMS Data``` and subsequently download and sort all your course data.
6. Everytime you want to update your local copy of the data, simply run the program again, it will automatically figure out which file already exists in your system, and download the new files. *Additionally, it will re-download any file that may have been edited or corrupted the last time the program was run to ensure integrity of data.*
7. **Please leave all the folders in the same location, else, the program will re-download them everytime your want to update your local copy of the files.**
