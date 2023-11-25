```
usage: ab to CSV [-h] (--inp INP | --stdin) --out OUT [-a] [--extra_data EXTRA_DATA]

options:
  -h, --help            show this help message and exit
  --inp INP             Input file
  --stdin               Input from stdin
  --out OUT             Output file
  -a                    Append to input file
  --extra_data EXTRA_DATA
                        Add extra data. Format is the same as in Ansible for --extra-vars: "k1=v1 k2=v2"
```

## Apache Benchmark

There is a Python script [abToCSV.py](abToCSV.py) which can be used to parse *ab*'s output to a CSV file.
The script can be used with a pipe from *ab* to read the data and convert it to CSV when *ab* finishes.

#### Example
```bash
ab -n 10000 -c 150 http://127.0.0.1:8090/static-20k.html | python abToCSV.py --stdin --out out.csv -a
```
###### CSV file example

|server|host|port|path|doc_len|conc|time|r_comp|r_fail|rps|tpr|tpr_all|50|66|75|80|90|95|98|99|100|
|------|----|----|----|-------|----|----|------|------|---|---|-------|--|--|--|--|--|--|--|--|---|
|Apache/2.4.57|127.0.0.1|8090|/static-20k.html|20480|150|14.709|10000|0|679.84|220.639|1.471|207|234|253|270|325|371|417|460|649|
|nginx/1.25.2|127.0.0.1|8091|/static-20k.html|20480|150|11.468|10000|0|871.97|172.025|1.147|155|183|206|221|273|319|399|446|682|
|lighttpd/1.4.72|127.0.0.1|8092|/static-20k.html|20480|150|7.035|10000|0|1421.42|105.528|0.704|96|114|127|136|166|194|232|265|394|


### Add extra data
In case you need to add extra data such as the machine's specs, you can  use the option 
`--extra_data` which follow the same format `"k1=v1 k2=v2"` as [Ansible's](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#key-value-format) `--extra-vars`

#### Example
```bash
ab -n 10000 -c 150 http://127.0.0.1:8090/static-20k.html | python abToCSV.py --stdin --out out.csv -a --extra_data "ram=2048 vcpu=2"
```
###### CSV file example

|server|host|port|path|doc_len|conc|time|r_comp|r_fail|rps|tpr|tpr_all|50|66|75|80|90|95|98|99|100|ram|vcpu|
|------|----|----|----|-------|----|----|------|------|---|---|-------|--|--|--|--|--|--|--|--|---|---|----|
|Apache/2.4.57|127.0.0.1|8090|/static-20k.html|20480|150|14.709|10000|0|679.84|220.639|1.471|207|234|253|270|325|371|417|460|649|2048|2|

This works also when using `-a`. If a csv header was previously defined, it will place the value in the correct column.


