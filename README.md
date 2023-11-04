## Apache Benchmark

There is a Python script [abToCSV.py](abToCSV.py) which can be used to parse *ab*'s output to a CSV file.
The script can be used with a pipe from *ab* to read the data and convert it to CSV when *ab* finishes.

Example:
```bash
ab -n 50000 -c 200 http://127.0.0.1:8090/static-20k.html | python abToCSV.py --stdin --out out.csv -a
```
