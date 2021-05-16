# Instruction
## Setup environment
```bash
conda env create -f environment.yml
conda activate mathi
``` 
## Download DVF data
```bash
python ./crawl_data.py
```
## data cleaning and augmentation
```bash
python format_data.py
```
## launch website
```bash 
python app.py
```