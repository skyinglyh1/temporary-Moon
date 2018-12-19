## About setOddsTable
1. If we pass List containing 1000 elements while each element contains key and value when invoking ```setOddsTable```,
    Plsease use ```luckyMoon.py``` contract.

2. If we pass List containing 1000 values when invoking ```setOddsTable```, the corresponding part in contract should be modified into the following.
```
def setOddsTable(valueList):
    RequireWitness(Admin)
    Put(GetContext(), TABLE_KEY, Serialize(valueList))
    Notify(["set OddsTable Successfully!"])
    return True
```
```
def getOdds(escapePoint):
    valueInfo = Get(GetContext(), TABLE_KEY)
    valueList = Deserialize(valueInfo)
    Require(escapePoint < len(valueList))
    Require(escapePoint > 0)
    return valueList[escapePoint]
```

## Notes
This two contracts are provided in order to select the most economical and rigorous way to store the key<->value table.
