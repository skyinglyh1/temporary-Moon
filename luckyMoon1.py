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

TOTAL_ONG_FOR_ADMIN = "G1"
LUCKY_TOTAL_SUPPLY_KEY = "G2"
LUCKY_TO_ONG_RATE_KEY = "G3"
PROFIT_PER_LUCKY_KEY = "G4"
ROUND_PREFIX = "G5"
CURRET_ROUND_NUM_KEY = "G6"
REFERRAL_BONUS_PERCENTAGE_KEY = "G8"

ROUND_STATUS_KEY = "R1"
ROUND_END_BET_TIME_KEY = "R2"
ROUND_EXPLODE_NUM_HASH_KEY = "R3"
ROUND_EXPLODE_NUM_KEY = "R4"
ROUND_PLAYER_BET_BALANCE_KEY = "R5"
ROUND_PLAYER_ADDRESS_LIST_KEY = "R6"

# PLAYER_REFERRAL_KEY + referral -> toBeReferred
PLAYER_REFERRAL_KEY = "P1"
LUCKY_BALANCE_KEY = "P2"
PROFIT_PER_LUCKY_FROM_KEY = "P3"
DIVIDEND_BALANCE_KEY = "P4"
ONG_BALANCE_KEY = "P5"

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
    if operation == "setReferralBonusPercentage":
        if len(args) != 1:
            return False
        referralBonus = args[0]
        return setReferralBonusPercentage(referralBonus)
    if operation == "addReferral":
        if len(args) != 2:
            return False
        toBeReferred = args[0]
        referral = args[1]
        return addReferral(toBeReferred, referral)
    if operation == "addMultiReferral":
        if len(args) != 1:
            return False
        toBeReferredReferralList = args[0]
        return addMultiReferral(toBeReferredReferralList)
    if operation == "addDividendToLuckyHolders":
        if len(args) != 1:
            return False
        ongAmount = args[0]
        return addDividendToLuckyHolders(ongAmount)
    if operation == "startNewRound":
        if len(args) != 2:
            return False
        explodePoint = args[0]
        salt = args[1]
        return startNewRound(explodePoint, salt)
    if operation == "endCurrentRound":
        if len(args) != 3:
            return False
        explodePoint = args[0]
        salt = args[1]
        effectiveEscapeAcctPointList = args[2]
        return endCurrentRound(explodePoint, salt, effectiveEscapeAcctPointList)
    if operation == "endCurrentRoundWithCost":
        if len(args) != 2:
            return False
        explodePoint = args[0]
        effectiveEscapeAcctPointList = args[1]
        return endCurrentRoundWithCost(explodePoint, effectiveEscapeAcctPointList)
    if operation == "adminInvest":
        if len(args) != 1:
            return False
        ongAmount = args[0]
        return adminInvest(ongAmount)
    if operation == "adminWithdraw":
        if len(args) != 2:
            return False
        toAcct = args[0]
        ongAmount = args[1]
        return adminWithdraw(toAcct, ongAmount)
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
    if operation == "withdraw":
        if len(args) != 1:
            return False
        account = args[0]
        return withdraw(account)
    ######################## for Player to invoke End ###############
    ####################### Global Info Start #####################
    if operation == "getTotalOngForAdmin":
        return getTotalOngForAdmin()
    if operation == "getLuckySupply":
        return getLuckySupply()
    if operation == "getLuckyToOngRate":
        return getLuckyToOngRate()
    if operation == "getReferralBonusPercentage":
        return getReferralBonusPercentage()
    if operation == "getCurrentRound":
        return getCurrentRound()
    if operation == "getExplodePoint":
        return getExplodePoint()
    if operation == "getReferral":
        if len(args) != 1:
            return False
        toBeReferred = args[0]
        return getReferral(toBeReferred)
    ####################### Global Info End #####################
    ####################### Round Info Start #####################
    if operation == "getRoundBetStatus":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getRoundBetStatus(roundNumber)
    if operation == "getRoundStatus":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getRoundStatus(roundNumber)
    if operation == "getRoundBetsEndTime":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getRoundBetsEndTime(roundNumber)

    if operation == "getRoundExplodePointHash":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getRoundExplodePointHash(roundNumber)
    if operation == "getRoundExplodePoint":
        if len(args) != 1:
            return False
        roundNumber = args[0]
        return getRoundExplodePoint(roundNumber)
    # if operation == "getRoundPlayersList":
    #     if len(args) != 1:
    #         return False
    #     roundNumber = args[0]
    #     return getRoundPlayersList(roundNumber)
    if operation == "verifyRoundExplodePointIsRandom":
        if len(args) != 2:
            return False
        roundNumber = args[0]
        salt = args[1]
        return verifyRoundExplodePointIsRandom(roundNumber, salt)
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
        if len(args) != 2:
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
        setLuckyToOngRate(1, 2)
        setReferralBonusPercentage(20)
        Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, 0), ROUND_STATUS_KEY), STATUS_OFF)
    return True

def setLuckyToOngRate(ong, lucky):
    RequireWitness(Admin)
    Put(GetContext(), LUCKY_TO_ONG_RATE_KEY, Div(Mul(Mul(lucky, LuckyMagnitude), Magnitude), Mul(ong, ONGMagnitude)))
    Notify(["setRate", ong, lucky])
    return True

def setReferralBonusPercentage(referralBonus):
    RequireWitness(Admin)
    Require(referralBonus >= 0)
    Require(referralBonus <= 100)
    Put(GetContext(), REFERRAL_BONUS_PERCENTAGE_KEY, referralBonus)
    Notify(["setReferralBonus", referralBonus])
    return True

def addReferral(toBeReferred, referral):
    RequireWitness(Admin)
    RequireScriptHash(toBeReferred)
    RequireScriptHash(referral)
    Require(not getReferral(toBeReferred))
    Require(toBeReferred != referral)
    Put(GetContext(), concatKey(PLAYER_REFERRAL_KEY, toBeReferred), referral)
    Notify(["addReferral", toBeReferred, referral])
    return True

def addMultiReferral(toBeReferredReferralList):
    RequireWitness(Admin)
    for toBeReferredReferral in toBeReferredReferralList:
        toBeReferred = toBeReferredReferral[0]
        referral = toBeReferredReferral[1]
        RequireScriptHash(toBeReferred)
        RequireScriptHash(referral)
        Require(not getReferral(toBeReferred))
        Require(toBeReferred != referral)
        Put(GetContext(), concatKey(PLAYER_REFERRAL_KEY, toBeReferred), referral)
    Notify(["addMultiReferral", toBeReferredReferralList])
    return True

def addDividendToLuckyHolders(ongAmount):
    RequireWitness(Admin)
    luckySupply = getLuckySupply()
    if luckySupply == 0:
        # Lucky supply is Zero, there is no Lucky.
        Notify(["noLucky"])
        return False
    profitPerLuckyToBeAdd = Div(Mul(ongAmount, Magnitude), getLuckySupply())
    oldProfitPerLucky = Get(GetContext(), PROFIT_PER_LUCKY_KEY)
    Put(GetContext(), PROFIT_PER_LUCKY_KEY, Add(profitPerLuckyToBeAdd, oldProfitPerLucky))
    Notify(["addDividendToLuckyHolders", ongAmount])
    return True

def startNewRound(explodePoint, salt):
    RequireWitness(Admin)
    currentRound = getCurrentRound()
    Require(getRoundStatus(currentRound) == STATUS_OFF)

    # start new round
    nextRound = Add(currentRound, 1)
    Put(GetContext(), CURRET_ROUND_NUM_KEY, nextRound)
    explodePointHash = sha256(explodePoint)^sha256(salt)
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, nextRound), ROUND_EXPLODE_NUM_HASH_KEY), explodePointHash)
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, nextRound), ROUND_STATUS_KEY), STATUS_ON)
    now = GetTime()
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, nextRound), ROUND_END_BET_TIME_KEY), Add(now, BettingDuration))
    Notify(["startNewRound", nextRound, now, explodePointHash])
    return True

def endCurrentRound(explodePoint, salt, effectiveEscapeAcctPointList):
    RequireWitness(Admin)
    currentRound = getCurrentRound()
    hash = sha256(explodePoint)^sha256(salt)
    Require(hash == getRoundExplodePointHash(currentRound))
    # if hash != getRoundExplodePointHash(currentRound):
    #     # the explodePoint and salt are wrong
    #     Notify(["Error", 101])
    #     return False
    Require(getRoundBetStatus(currentRound) == False)
    # if getRoundBetStatus(currentRound):
    #     # please wait for the bets end
    #     Notify(["Error", 102])
    #     return False
    Require(getRoundStatus(currentRound) == STATUS_ON)
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_EXPLODE_NUM_KEY), explodePoint)
    effectiveEscapeAcctPointOddsProfitList = _settleAccounts(currentRound, explodePoint, effectiveEscapeAcctPointList)
    Require(_closeRound(currentRound))
    Notify(["endCurrentRound", currentRound, explodePoint, salt, effectiveEscapeAcctPointOddsProfitList])
    return True

def endCurrentRoundWithCost(explodePoint, effectiveEscapeAcctPointList):
    RequireWitness(Admin)
    currentRound = getCurrentRound()
    Require(GetTime() >= Add(3600, getRoundBetsEndTime(currentRound)))
    # if GetTime() < Add(3600, getRoundBetsEndTime(currentRound)):
    #     # Still in the punishment time, please wait for the punish to be ended.
    #     Notify(["Error", 103])
    #     return False
    Require(getRoundStatus(currentRound) == STATUS_ON)
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), ROUND_EXPLODE_NUM_KEY), explodePoint)
    effectiveEscapeAcctPointOddsProfitList = _settleAccounts(currentRound, explodePoint, effectiveEscapeAcctPointList)
    Require( _closeRound(currentRound))
    Notify(["endCurrentRoundWithCost", currentRound, explodePoint, effectiveEscapeAcctPointOddsProfitList])
    return True


def adminInvest(ongAmount):
    RequireWitness(Admin)
    Require(_transferONG(Admin, ContractAddress, ongAmount))
    Put(GetContext(), TOTAL_ONG_FOR_ADMIN, Add(getTotalOngForAdmin(), ongAmount))
    Notify(["adminInvest", ongAmount])
    return True

def adminWithdraw(toAcct, ongAmount):
    RequireWitness(Admin)
    currendRound = getCurrentRound()
    Require(getRoundStatus(currendRound) == STATUS_OFF)

    totalOngForAdmin = getTotalOngForAdmin()
    Require(ongAmount <= totalOngForAdmin)
    Put(GetContext(), TOTAL_ONG_FOR_ADMIN, Sub(getTotalOngForAdmin(), ongAmount))

    Require(_transferONGFromContact(toAcct, ongAmount))
    Notify(["adminWithdraw", toAcct, ongAmount])
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
    Require(getRoundBetStatus(currentRound))
    playerRoundBalance = getPlayerBetBalance(currentRound, account)
    Require(not playerRoundBalance)
    Require(_transferONG(account, ContractAddress, ongAmount))
    Put(GetContext(), TOTAL_ONG_FOR_ADMIN, Add(getTotalOngForAdmin(), ongAmount))

    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, currentRound), concatKey(ROUND_PLAYER_BET_BALANCE_KEY, account)), ongAmount)

    updateDividend(account)

    _referralLuckyBalanceToBeAdd = 0
    acctLuckyBalanceToBeAdd = Div(Mul(ongAmount, getLuckyToOngRate()), Magnitude)
    Put(GetContext(), concatKey(LUCKY_BALANCE_KEY, account), Add(getLuckyBalanceOf(account), acctLuckyBalanceToBeAdd))

    if len(getReferral(account)) == 20:
        _referralLuckyBalanceToBeAdd = Div(Mul(acctLuckyBalanceToBeAdd, getReferralBonusPercentage()), 100)
        _referral = getReferral(account)
        Put(GetContext(), concatKey(LUCKY_BALANCE_KEY, _referral), Add(getLuckyBalanceOf(_referral), _referralLuckyBalanceToBeAdd))

    Put(GetContext(), LUCKY_TOTAL_SUPPLY_KEY, Add(getLuckySupply(), Add(acctLuckyBalanceToBeAdd, _referralLuckyBalanceToBeAdd)))
    Notify(["bet", currentRound, account, ongAmount])
    return True

def withdraw(account):
    RequireWitness(account)
    ongBalance = getOngBalanceOf(account)
    updateDividend(account)
    dividendBalance = getDividendBalanceOf(account)
    ongAmountToBeWithdraw = Add(ongBalance, dividendBalance)
    Require(ongAmountToBeWithdraw > 0)
    Require(_transferONGFromContact(account, ongAmountToBeWithdraw))
    Delete(GetContext(), concatKey(ONG_BALANCE_KEY, account))
    Delete(GetContext(), concatKey(DIVIDEND_BALANCE_KEY, account))
    Notify(["withdraw", account, ongAmountToBeWithdraw])
    return True
######################## Methods for Players End ######################################
################## Global Info Start #######################

def getTotalOngForAdmin():
    return Get(GetContext(), TOTAL_ONG_FOR_ADMIN)

# def getEarningForAdmin():
#     Require(getRoundStatus(getCurrentRound()) == STATUS_OFF)
#     return Get(GetContext(), TOTAL_ONG_FOR_ADMIN)

def getLuckySupply():
    return Get(GetContext(), LUCKY_TOTAL_SUPPLY_KEY)

def getLuckyToOngRate():
    """
    Div(Mul(Mul(lucky, LuckyMagnitude), Magnitude), Mul(ong, ONGMagnitude))
     lucky * 10^8
    ------------- * Magnitude
     ong * 10^9
    :return:
    """
    return Get(GetContext(), LUCKY_TO_ONG_RATE_KEY)

def getReferralBonusPercentage():
    return Get(GetContext(), REFERRAL_BONUS_PERCENTAGE_KEY)

def getCurrentRound():
    return Get(GetContext(), CURRET_ROUND_NUM_KEY)

def getExplodePoint():
    """
    :return: a random number in the range of 1 to 1 000 000
    """
    blockHash = GetCurrentBlockHash()
    tx = GetScriptContainer()
    txhash = GetTransactionHash(tx)
    randomNumber = abs(blockHash ^ txhash) % 1000000
    explodePoint = Add(abs(randomNumber), 1)
    return explodePoint

def getReferral(toBeReferred):
    return Get(GetContext(), concatKey(PLAYER_REFERRAL_KEY, toBeReferred))
################## Global Info End #######################


####################### Round Info Start #####################
def getRoundBetStatus(roundNumber):
    return GetTime() <= getRoundBetsEndTime(roundNumber)

def getRoundStatus(roundNumber):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_STATUS_KEY))

def getRoundBetsEndTime(roundNumber):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_END_BET_TIME_KEY))

def getRoundExplodePointHash(roundNumber):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_EXPLODE_NUM_HASH_KEY))

def getRoundExplodePoint(roundNumber):
    return Get(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_EXPLODE_NUM_KEY))

def verifyRoundExplodePointIsRandom(roundNumber, salt):
    Require(getRoundStatus(roundNumber) == STATUS_OFF)
    tryToVerifyHash = sha256(getRoundExplodePoint(roundNumber))^sha256(salt)
    return tryToVerifyHash == getRoundExplodePointHash(roundNumber)
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
def _settleAccounts(roundNumber, explodePoint, effectiveEscapeAcctPointList):
    effectiveEscapeAcctPointOddsProfitList = []
    totalOngForAdminToBeSub = 0
    for effectiveEscapeAcctPoint in effectiveEscapeAcctPointList:
        account = effectiveEscapeAcctPoint[0]
        escapePoint = effectiveEscapeAcctPoint[1]
        # Require(escapePoint < explodePoint)
        if escapePoint < explodePoint and escapePoint >= 100:
            odds = escapePoint
            betBalance = getPlayerBetBalance(roundNumber, account)
            ongBalanceForPlayerToBeAdd = Div(Mul(betBalance, odds), OddsMagnitude)
            totalOngForAdminToBeSub = Add(totalOngForAdminToBeSub, ongBalanceForPlayerToBeAdd)
            effectiveEscapeAcctPointOddsProfit = []
            effectiveEscapeAcctPointOddsProfit.append(account)
            effectiveEscapeAcctPointOddsProfit.append(escapePoint)
            effectiveEscapeAcctPointOddsProfit.append(Sub(ongBalanceForPlayerToBeAdd, betBalance))
            effectiveEscapeAcctPointOddsProfitList.append(effectiveEscapeAcctPointOddsProfit)
            Put(GetContext(), concatKey(ONG_BALANCE_KEY, account), Add(getOngBalanceOf(account), ongBalanceForPlayerToBeAdd))
    Put(GetContext(), TOTAL_ONG_FOR_ADMIN, Add(getTotalOngForAdmin(), totalOngForAdminToBeSub))
    return effectiveEscapeAcctPointOddsProfitList

def _closeRound(roundNumber):
    Put(GetContext(), concatKey(concatKey(ROUND_PREFIX, roundNumber), ROUND_STATUS_KEY), STATUS_OFF)
    return True

def updateDividend(account):
    profitPerLucky = Get(GetContext(), PROFIT_PER_LUCKY_KEY)
    profitPerLuckyFrom = Get(GetContext(), concatKey(PROFIT_PER_LUCKY_FROM_KEY, account))
    unsharedProfitPerLucky = Sub(profitPerLucky, profitPerLuckyFrom)
    luckyBalance = getLuckyBalanceOf(account)
    if unsharedProfitPerLucky > 0 and luckyBalance > 0:
        Put(GetContext(), concatKey(DIVIDEND_BALANCE_KEY, account), getDividendBalanceOf(account))
        Put(GetContext(), concatKey(PROFIT_PER_LUCKY_FROM_KEY, account), profitPerLucky)
    return True

def _checkIsInRoundPlayersList(account, playersList):
    for player in playersList:
        if account == player:
            return True
    return False


def _getRandomNumber(interval):
    blockHash = GetCurrentBlockHash()
    tx = GetScriptContainer()
    txhash = GetTransactionHash(tx)
    randomNumber = abs(blockHash ^ txhash) % Add(interval, 1)
    return randomNumber

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