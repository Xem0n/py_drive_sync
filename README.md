## how to run  
0. optonally create a virtual environment  
```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

1. install dependencies  
```bash
pip install -r requirements.txt
```

2. ensure there's credentials.json in the project root directory.  
   If you don't have it, follow these steps to create it:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Drive API for your project
   - Create credentials for a desktop application and download the `credentials.json` file
   - Place the `credentials.json` file in the root directory of this project

   (or something like that, idk)

3. run the application  
```bash
python main.py local_file drive_file_id
```

## how to build  
1. install cx freeze  
```bash
pip install cx_freeze
```

2. run the build script from the project root directory  
```bash
python setup.py build
```
