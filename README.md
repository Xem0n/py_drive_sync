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

2. run the application  
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
