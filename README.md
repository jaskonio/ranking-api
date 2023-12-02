# ranking-api

## Prepare virual environment in Linux

```cmd
python3 -m  venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Prepare virual environment in Windows

```cmd
python3 -m  venv env
.\env\Scripts\Activate.ps1
pip3 install -r requirements.txt
```

## Development

```cmd
 uvicorn main:app --reload
```

## Docker

### Build

```cmd
    docker build -t ranking-api .
```

### Run

```cmd
    docker run -d --rm --name ranking-api -p 9000:8080 ranking-api
```

### Stop

```cmd
    docker stop ranking-api
```

## Testing

Execute unittest:

```cmd
    python -m unittest discover -s tests/ -p 'test*.py' -v --locals
```


```cmd
    pytest .\tests\ --html=reports\execution\report_execution_test.html
```

## Coverage Code

First, run the coverage module to generate the coverage data:

```cmd
    coverage run -m unittest
```

Second, turn the coverage data into a report:

```cmd
    coverage report --include app\*
```

To generate the coverage report in HTML format, you change the option of the coverage module to HTML like this:

```cmd
    coverage html --include app\*
```

```cmd
    coverage run -m unittest && coverage report && coverage report
```

## Style

Check pylint

```cmd
pylint ./app/
```
