##### The project was made in python version 3.8.5

# How to use:

## Clone the project:

```shell
git clone https://github.com/MatteusSouza/fortnite-power-ranking.git

```

## instal requirement:

```shell
pip3 install -r requirements.txt

```

## Import into your project and get the data.

```python
from fortnite_pr import PowerRanking
pr = PowerRanking()
top5 = pr.get_power_ranking(quantity=5)
print(top5)

```

You can pass 3 parameter: platform and region as a string and quantity as an int.

Platforms values: pc, console, mobile, global || global is default

Regions: NAE, NAW, EU, OCE, BR, ASIA, ME, global || global is default

Quantity: How much as you need. || 5 is default.
<br><br>


### With no parameter:
```python
pr.get_power_ranking()
```

You will receive with default settings

`platform='global'`, `region='global'`, `quantity=5`
<br><br>

### With parameter:
```python
pr.get_power_ranking('PC', 'BR', 250)
```

## How to create a json file:

The method `create_json_file()` have the parameters: `dataframe`, `filename`, `orient`.

By default, the parameters are: `filename='power_ranking.json'` and `orient='records'`.

To create a json file, first you will need the dataframe, after call the function `create_json_file()` and pass the dataframe.

```python
pr = PowerRanking()
top200 = pr.get_power_ranking(quantity=200) #This will return a dataframe.
pr.create_json_file(top5)

```

### With parameters
```python
pr.create_json_file(top200, 'top200.json', orient='index')

```

If you prefer, you can use original function `to_json()` directly from pandas.

```python
pr.to_json('filename.json', orient='index', indent=2, force_ascii=False)
```
[Read how to use the pandas to_json () function.](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html)
