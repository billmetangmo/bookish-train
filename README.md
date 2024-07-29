# Bookish-train

## Overview
This project includes 2 scripts for:  
- `extract-domains.sh` extracting and sanitizing domain names from URLs provided in a text file
- `script.py` connecting to given HTTP URLs provided as command line parameters, extracts all links from each URL, and outputs the results in different formats based on the `-o` option specified by the user

## Requirements
- Bash shell
- Grep, awk, sed (standard Unix/Linux utilities)
- python3
- kubectl and access to k8s cluster
- Write acess to github container registry `billmetangmo/bookish-train`
- [trivy](https://trivy.dev/)
- [skaffold](https://skaffold.dev/)


## Usage (script.py)

Firstly, install python packages
  ```bash
  pip install -r requirements.txt
  ```

  ```bash
  python3 script.py -u "https://news.ycombinator.com/" -o "stdout"
  ```

  ```bash
  python3 script.py -u "https://news.ycombinator.com/" -u "https://arstechnica.com/" -o 'json'
  ```

## Usage (extract-domains)

```bash
./extract-domains.sh input.txt output.txt 1
```
- Replace `input.txt` with your file containing URLs.
- Replace `output.txt` with your desired output file.
- Replace `1` with `1` or `2` to choose the extraction method.

## Deployment
```bash
skaffold run
```

