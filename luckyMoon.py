"""
LuckyMoon Game
"""
from boa.interop.Ontology.Contract import Migrate
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash, GetCallingScriptHash, GetEntryScriptHash, GetScriptContainer
from boa.interop.Ontology.Native import Invoke
from boa.interop.Ontology.Runtime import GetCurrentBlockHash
from boa.builtins import ToScriptHash, concat, state, sha256
from boa.interop.System.Transaction import GetTransactionHash
"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/Utils.py
"""
def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)


"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/SafeCheck.py
"""
def Require(condition):
    """
	If condition is not satisfied, return false
	:param condition: required condition
	:return: True or false
	"""
    if not condition:
        Revert()
    return True

def RequireScriptHash(key):
    """
    Checks the bytearray parameter is script hash or not. Script Hash
    length should be equal to 20.
    :param key: bytearray parameter to check script hash format.
    :return: True if script hash or revert the transaction.
    """
    Require(len(key) == 20)
    return True

def RequireWitness(witness):
    """
	Checks the transaction sender is equal to the witness. If not
	satisfying, revert the transaction.
	:param witness: required transaction sender
	:return: True if transaction sender or revert the transaction.
	"""
    Require(CheckWitness(witness))
    return True
"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/SafeMath.py
"""

def Add(a, b):
    """
    Adds two numbers, throws on overflow.
    """
    c = a + b
    Require(c >= a)
    return c

def Sub(a, b):
    """
    Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    Require(a>=b)
    return a-b

def ASub(a, b):
    if a > b:
        return a - b
    if a < b:
        return b - a
    else:
        return 0

def Mul(a, b):
    """
    Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    if a == 0:
        return 0
    c = a * b
    Require(c / a == b)
    return c

def Div(a, b):
    """
    Integer division of two numbers, truncating the quotient.
    """
    Require(b > 0)
    c = a / b
    return c

def Pwr(a, b):
    """
    a to the power of b
    :param a the base
    :param b the power value
    :return a^b
    """
    c = 0
    if a == 0:
        c = 0
    elif b == 0:
        c = 1
    else:
        i = 0
        c = 1
        while i < b:
            c = Mul(c, a)
            i = i + 1
    return c

def Sqrt(a):
    """
    Return sqrt of a
    :param a:
    :return: sqrt(a)
    """
    c = Div(Add(a, 1), 2)
    b = a
    while(c < b):
        b = c
        c = Div(Add(Div(a, c), c), 2)
    return c


ONGAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
Admin = ToScriptHash('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p')
INIIT_KEY = "Init"
LUCKY_TOTAL_SUPPLY_KEY = "LuckySupply"
LUCKY_BALANCE_KEY = "LuckyBalance"

LUCKY_TO_ONG_RATE_KEY = "LuckyToOng"

PROFIT_PER_LUCKY_KEY = "ProfitPerLucky"
PROFIT_PER_LUCKY_FROM_KEY = "ProfitPerLuckyFrom"
DIVIDEND_BALANCE_KEY = "DividendBalance"
ONG_BALANCE_KEY = "OngBalance"

ROUND_PREFIX = "G01"
CURRET_ROUND_NUM_KEY = "G02"
TABLE_KEY = "G03"

ROUND_STATUS_KEY = "R1"
ROUND_END_BET_TIME_KEY = "R2"
ROUND_EXPLODE_NUM_HASH_KEY = "R3"
ROUND_EXPLODE_NUM_KEY = "R4"
ROUND_PLAYER_BET_BALANCE_KEY = "R5"


STATUS_ON = "RUNNING"
STATUS_OFF = "END"
BettingDuration = 20
ONGMagnitude = 1000000000
LuckyDecimals = 8
LuckyMagnitude = 100000000
Magnitude = 1000000000000000000000000000000
OddsMagnitude = 100

ContractAddress = GetExecutingScriptHash()
def Main(operation, args):
    ######################## for Admin to invoke Begin ###############
    if operation == "init":
        return init()
    if operation == "setLuckyToOngRate":
        if len(args) != 2:
            return False
        ong = args[0]
        lucky = args[1]
        return setLuckyToOngRate(ong, lucky)
    if operation == "setOddsTable":
        if len(args) != 1:
            return False
        keyValueList = args[0]
        return setOddsTable(keyValueList)
    if operation == "storeExplodeNumberHash":
        if len(args) != 1:
            return False
        explodeNumber = args[0]
        return storeExplodeNumberHash(explodeNumber)
    if operation == "addDividendToLuckyHolders":
        if len(args) != 1:
            return False
        ongAmount = args[0]
        return addDividendToLuckyHolders(ongAmount)
    if operation == "startNewRound":
        return startNewRound()
    if operation == "endBet":
        return endBet()
    if operation == "endCurrentRound":
        if len(args) != 2:
            return False
        explodeNumber = args[0]
        effectiveEscapeAcctPointList = args[1]
        return endCurrentRound(explodeNumber, effectiveEscapeAcctPointList)
    if operation == "migrateContract":
        if len(args) != 8:
            return False
        code = args[0]
        needStorage = args[1]
        name = args[2]
        version = args[3]
        author = args[4]
        email = args[5]
        description = args[6]
        newContractHash = args[7]
        return migrateContract(code, needStorage, name, version, author, email, description, newContractHash)
    ######################## for Admin to invoke End ###############
    ######################## for Player to invoke Begin ###############
    if operation == "bet":
        if len(args) != 2:
            return False
        account = args[0]
        ongAmount = args[1]
        return bet(account, ongAmount)
    ######################## for Player to invoke End ###############
    ####################### Global Info Start #####################
    if operation == "getOdds":
        if len(args) != 1:
            return False
        escapePoint = args[1]
        return getOdds(escapePoint)
    if operation == "getLuckySupply":
        return getLuckySupply()
    if operation == "getLuckyToOngRate":
        return getLuckyToOngRate()
    if operation == "getCurrentRound":
        return getCurrentRound()
    if operation == "getExplodePoint":
        return getExplodePoint()
    ####################### Global Info End #####################
    ####################### Round Info Start #####################
    if operation == "getRoundStatus":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getRoundStatus(roundNumber)
    if operation == "getRoundEndTime":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getRoundEndTime(roundNumber)
    if operation == "getExplodeNumberHash":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getExplodeNumberHash(roundNumber)
    ####################### Round Info End #####################
    ######################### For testing purpose Begin ##############
    if operation == "getOngBalanceOf":
        if len(args) != 1:
            return False
        account = args[0]
        return getOngBalanceOf(account)
    if operation == "getLuckyBalanceOf":
        if len(args) != 1:
            return False
        account = args[0]
        return getLuckyBalanceOf(account)
    if operation == "getDividendBalanceOf":
        if len(args) != 1:
            return False
        account = args[0]
        return getDividendBalanceOf(account)
    if operation == "getPlayerBetBalance":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        account = args[1]
        return getPlayerBetBalance(roundNumber, account)
    ######################### For testing purpose End ##############
    return False
####################### Methods that only Admin can invoke Start #######################
def init():
    RequireWitness(Admin)
    inited = Get(GetContext(), INIIT_KEY)
    if inited:
        Notify(["idiot admin, you have initialized the contract"])
        return False
    else:
        Put(GetContext(), INIIT_KEY, 1)
        Notify(["Initialized contract successfully"])
        # startNewRound()
        setLuckyToOngRate(1, 2)
    return True

def setLuckyToOngRate(ong, lucky):
    RequireWitness(Admin)
    Put(GetContext(), LUCKY_TO_ONG_RATE_KEY, Div(Mul(Mul(lucky, LuckyMagnitude), Magnitude), Mul(ong, ONGMagnitude)))
    Notify(["setRate", ong, lucky])
    return True

def setOddsTable(keyValueList):
    RequireWitness(Admin)
    for keyValue in keyValueList:
        Put(GetContext(), concatKey(TABLE_KEY, keyValue[0]), keyValue[1])
    Notify(["setOddsTableSuccessful"])
    return True

def storeExplodeNumberHash(explodeNumber):
    RequireWitness(Admin)
    currentRound = getCurrentRound()
    explodeNumberHash = sha256(explodeNumber)
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_EXPLODE_NUM_HASH_KEY), explodeNumberHash)
    Notify(["explodeNumberHash", currentRound, explodeNumberHash])
    return True


def addDividendToLuckyHolders(ongAmount):
    RequireWitness(Admin)
    profitPerLuckyToBeAdd = Div(Mul(ongAmount, Magnitude), getLuckySupply())
    Put(GetContext(), PROFIT_PER_LUCKY_KEY, profitPerLuckyToBeAdd)
    Notify(["addOngToLuckyHolders", ongAmount])
    return True

def startNewRound():
    RequireWitness(Admin)
    currentRound = getCurrentRound()
    Require(getRoundStatus(currentRound) == STATUS_OFF)

    nextRound = Add(currentRound, 1)
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, nextRound), ROUND_STATUS_KEY), STATUS_ON)
    now = GetTime()
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, nextRound), ROUND_END_BET_TIME_KEY), Add(now, BettingDuration))
    Notify(["startNewRound", nextRound, now])
    return True

def endBet():
    RequireWitness(Admin)
    currentRound = getCurrentRound()
    Require(GetTime() > getRoundEndTime(currentRound))
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_STATUS_KEY), STATUS_OFF)
    Notify(["endBet", currentRound])
    return True

def endCurrentRound(explodeNumber, effectiveEscapeAcctPointList):
    RequireWitness(Admin)
    currentRound = getCurrentRound()
    Require(sha256(explodeNumber) == getExplodeNumberHash(currentRound))
    effectiveEscapeAcctList = []
    effectiveEscapePointList = []
    profitList = []
    for effectiveEscapeAcctPoint in effectiveEscapeAcctPointList:
        account = effectiveEscapeAcctPoint[0]
        escapePoint = effectiveEscapeAcctPoint[1]
        Require(escapePoint <= explodeNumber)
        effectiveEscapeAcctList.append(account)
        effectiveEscapePointList.append(escapePoint)
        odds = getOdds(escapePoint)
        betBalance = getPlayerBetBalance(currentRound, account)
        ongBalanceToBeAdd = Div(Mul(betBalance, odds), OddsMagnitude)
        Put(GetContext(), concatKey(ONG_BALANCE_KEY, account), Add(getOngBalanceOf(account), ongBalanceToBeAdd))
        profitList.append(Sub(ongBalanceToBeAdd, betBalance))
    Notify(["endCurrentRound", currentRound, effectiveEscapeAcctList, effectiveEscapeAcctPointList, profitList])
    startNewRound()
    return True


def migrateContract(code, needStorage, name, version, author, email, description, newContractHash):
    RequireWitness(Admin)
    param = state(ContractAddress)
    totalOngAmount = Invoke(0, ONGAddress, 'balanceOf', param)
    res = _transferONGFromContact(newContractHash, totalOngAmount)
    Require(res)
    if res == True:
        res = Migrate(code, needStorage, name, version, author, email, description)
        Require(res)
        Notify(["Migrate Contract successfully", Admin, GetTime()])
        return True
    else:
        Notify(["MigrateContractError", "transfer ONG to new contract error"])
        return False
####################### Methods that only Admin can invoke End #######################

######################## Methods for Players Start ######################################
def bet(account, ongAmount):
    RequireWitness(account)
    currentRound = getCurrentRound()
    Require(getRoundStatus(currentRound) == STATUS_ON)
    Require(_transferONG(account, ContractAddress, ongAmount))
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(ROUND_PLAYER_BET_BALANCE_KEY, account)), Add(getPlayerBetBalance(currentRound, account), ongAmount))

    updateDividend(account)
    luckyBalanceToBeAdd = Div(Mul(ongAmount, getLuckyToOngRate()), Magnitude)
    Put(GetContext(), concatKey(LUCKY_BALANCE_KEY, account), Add(getLuckyBalanceOf(account), luckyBalanceToBeAdd))
    Put(GetContext(), LUCKY_TOTAL_SUPPLY_KEY, Add(getLuckySupply(), luckyBalanceToBeAdd))
    Notify(["bet", currentRound, account, ongAmount])
    return True

######################## Methods for Players End ######################################
################## Global Info Start #######################
def getOdds(escapePoint):
    return Get(GetContext(), concatKey(TABLE_KEY, escapePoint))

def getLuckySupply():
    return Get(GetContext(), LUCKY_TOTAL_SUPPLY_KEY)

def getLuckyToOngRate():
    return Get(GetContext(), LUCKY_TO_ONG_RATE_KEY)

def getCurrentRound():
    return Get(GetContext(), CURRET_ROUND_NUM_KEY)

def getExplodePoint():
    blockHash = GetCurrentBlockHash()
    tx = GetScriptContainer()
    txhash = GetTransactionHash(tx)
    randomNumber = abs(blockHash ^ txhash) % 1000
    explodePoint = Add(abs(randomNumber), 1)
    return explodePoint
################## Global Info End #######################


####################### Round Info Start #####################
def getRoundStatus(roundNumber):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_STATUS_KEY))

def getRoundEndTime(roundNumber):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_END_BET_TIME_KEY))

def getExplodeNumberHash(roundNumber):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_EXPLODE_NUM_HASH_KEY))
####################### Round Info End #####################


####################### Player Info Start #####################
def getOngBalanceOf(account):
    return Get(GetContext(), concatKey(ONG_BALANCE_KEY, account))

def getLuckyBalanceOf(account):
    return Get(GetContext(), concatKey(LUCKY_BALANCE_KEY, account))

def getDividendBalanceOf(account):
    dividendInStorage = Get(GetContext(), concatKey(DIVIDEND_BALANCE_KEY, account))
    profitPerLucky = Get(GetContext(), PROFIT_PER_LUCKY_KEY)
    profitPerLuckyFrom = Get(GetContext(), concatKey(PROFIT_PER_LUCKY_FROM_KEY, account))
    unsharedProfitPerLucky = Sub(profitPerLucky, profitPerLuckyFrom)
    luckyBalance = getLuckyBalanceOf(account)
    if unsharedProfitPerLucky > 0 and luckyBalance > 0:
        unsharedProfit = Div(Mul(unsharedProfitPerLucky, luckyBalance), Magnitude)
        return Add(dividendInStorage, unsharedProfit)
    return dividendInStorage

def getPlayerBetBalance(roundNumber, account):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), concatKey(ROUND_PLAYER_BET_BALANCE_KEY, account)))
####################### Player Info End #####################


######################### Utility Methods Start #########################
def updateDividend(account):
    profitPerLucky = Get(GetContext(), PROFIT_PER_LUCKY_KEY)
    profitPerLuckyFrom = Get(GetContext(), concatKey(PROFIT_PER_LUCKY_FROM_KEY, account))
    unsharedProfitPerLucky = Sub(profitPerLucky, profitPerLuckyFrom)
    luckyBalance = getLuckyBalanceOf(account)
    if unsharedProfitPerLucky > 0 and luckyBalance > 0:
        Put(GetContext(), concatKey(DIVIDEND_BALANCE_KEY, account), getDividendBalanceOf(account))
        Put(GetContext(), concatKey(PROFIT_PER_LUCKY_FROM_KEY, account), profitPerLucky)
    return True

def _transferONG(fromAcct, toAcct, amount):
    """
    transfer ONG
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    RequireWitness(fromAcct)
    param = state(fromAcct, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False

def _transferONGFromContact(toAcct, amount):
    param = state(ContractAddress, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False

def concatKey(str1,str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)
######################### Utility Methods Start #########################