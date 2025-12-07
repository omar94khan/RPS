import pandas as pd
from copy import deepcopy
from datetime import date
import math
import json

def RPS(
        FinanceAmount: float,
        ProfitRate: float,
        TenorMonths : int,
        PayDay : int,
        DisbursementDate : str,
        FirstEMIDate : str,
        repaymentMethod : str,
        TakafulFactor : float,
        EMI : float,
        GracePeriodDate : str = None,
        GracePeriodProfitRate : float = None
        ):
    
    DisbursementYear = int(DisbursementDate[0:4])
    DisbursementMonth = int(DisbursementDate[4:6])
    DisbursementDay = int(DisbursementDate[6:8])
    
    FirstEMIYear = int(FirstEMIDate[0:4])
    FirstEMIMonth = int(FirstEMIDate[4:6])

    if repaymentMethod != "Bullet":
        if PayDay > 28:
            raise ValueError("PayDay cannot be greater than 28.")

    if repaymentMethod == "Normal":
        rps = {
            'SNo' : [],
            'Date' : [],
            'Days' : [],
            'EMI' : [],
            'ProfitAmount' : [],
            'TakafulAmount' : [],
            'PrincipalAmount' : [],
            'OutstandingPrincipal' : []
           }


        for i in range(0,TenorMonths+1):
            rps['SNo'].append(i)
            
            if i == 0:
                rps['Date'].append(date(DisbursementYear, DisbursementMonth, DisbursementDay))
                rps['Days'].append(0)
                rps['EMI'].append(0)
                rps['ProfitAmount'].append(0)
                rps['TakafulAmount'].append(0)
                rps['PrincipalAmount'].append(0)
                rps['OutstandingPrincipal'].append(FinanceAmount)
            else:
                year = FirstEMIYear + ((FirstEMIMonth + (i-2))//12)
                month = ((FirstEMIMonth + (i-2)) % 12) + 1
                day = PayDay
                rps['Date'].append(date(year, month, day))  
                rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)
                rps['EMI'].append(EMI)
                rps['ProfitAmount'].append(rps['OutstandingPrincipal'][-1] * ProfitRate / 360 * rps['Days'][-1])
                # rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor * rps['Days'][-1] / 30)
                rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor)
                rps['PrincipalAmount'].append(max(rps['EMI'][-1] - rps['ProfitAmount'][-1] - rps['TakafulAmount'][-1],0))
                rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1] - rps['PrincipalAmount'][-1])


    elif repaymentMethod == "Bullet":
        rps = {
            'SNo' : [],
            'Date' : [],
            'Days' : [],
            'EMI' : [],
            'ProfitAmount' : [],
            'TakafulAmount' : [],
            'PrincipalAmount' : [],
            'OutstandingPrincipal' : []
           }


        if TenorMonths != 1:
            raise ValueError("Bullet payment can only work when TenorMonths = 1.")

        for i in range(0,TenorMonths+1):
            rps['SNo'].append(i)
            
            if i == 0:
                rps['Date'].append(date(DisbursementYear, DisbursementMonth, DisbursementDay))
                rps['Days'].append(0)
                rps['EMI'].append(0)
                rps['ProfitAmount'].append(0)
                rps['TakafulAmount'].append(0)
                rps['PrincipalAmount'].append(0)
                rps['OutstandingPrincipal'].append(FinanceAmount)
            else:
                year = FirstEMIYear + ((FirstEMIMonth + (i-2))//12)
                month = ((FirstEMIMonth + (i-2)) % 12) + 1
                day = PayDay
                rps['Date'].append(date(year, month, day))  
                rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)
                rps['EMI'].append(EMI)
                rps['ProfitAmount'].append(rps['OutstandingPrincipal'][-1] * ProfitRate / 360 * rps['Days'][-1])
                rps['TakafulAmount'].append(0)
                rps['PrincipalAmount'].append(max(rps['EMI'][-1] - rps['ProfitAmount'][-1] - rps['TakafulAmount'][-1],0))
                rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1] - rps['PrincipalAmount'][-1])


    elif repaymentMethod == "Grace":
                rps = {
                    'SNo' : [],
                    'Date' : [],
                    'Days' : [],
                    'EMI' : [],
                    "GracePeriodProfitRecovery" : [],
                    "GracePeriodTakafulRecovery" : [],
                    'ProfitAmount' : [],
                    'TakafulAmount' : [],
                    'PrincipalAmount' : [],
                    'OutstandingPrincipal' : []
                }

                if GracePeriodDate == DisbursementDate:
                    raise ValueError("Grace period cannot end on the same date as the loan disbursement. Please adjust GracePeriodDate value.")
                
                
                GracePeriodYear = int(GracePeriodDate[0:4])
                GracePeriodMonth = int(GracePeriodDate[4:6])
                GracePeriodDay = int(GracePeriodDate[6:8])


                # Creating the first row to show the disbursement of the loan

                rps['SNo'].append(0)
                rps['Date'].append(date(DisbursementYear, DisbursementMonth, DisbursementDay))
                rps['Days'].append(0)
                rps['EMI'].append(0)
                rps['ProfitAmount'].append(0)
                rps['TakafulAmount'].append(0)
                rps['GracePeriodTakafulRecovery'].append(0)
                rps['GracePeriodProfitRecovery'].append(0)
                rps['PrincipalAmount'].append(0)
                rps['OutstandingPrincipal'].append(FinanceAmount)


                # Creating the second row to show the end of grace period

                rps['SNo'].append(1)
                rps['Date'].append(date(GracePeriodYear, GracePeriodMonth, GracePeriodDay))  
                rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)
                rps['EMI'].append(0)
                rps['ProfitAmount'].append(0)
                rps['TakafulAmount'].append(0)
                rps['GracePeriodTakafulRecovery'].append(0)
                rps['GracePeriodProfitRecovery'].append(0)
                rps['PrincipalAmount'].append(0)
                rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1])



                # Calculating Grace Period Takaful and Profit
                
                if GracePeriodProfitRate is None:
                    print("GracePeriodProfitRate not found, setting to ProfitRate")
                    GracePeriodProfitRate = ProfitRate
                else:
                    print("GracePeriodProfitRate found: ", GracePeriodProfitRate)
    
                    

                nGraceMonths = ((GracePeriodYear - DisbursementYear) * 12) + GracePeriodMonth - DisbursementMonth
                GracePeriodTakaful = rps['OutstandingPrincipal'][-1] * TakafulFactor * nGraceMonths
                GracePeriodProfit = rps['OutstandingPrincipal'][-1] * GracePeriodProfitRate / 360 * rps['Days'][-1]

                SNo = 2
                year = FirstEMIYear
                month = FirstEMIMonth
                day = PayDay

                for i in range(SNo, TenorMonths+2 - nGraceMonths):
                    rps['SNo'].append(i)
                    rps['Date'].append(date(year, month, day))
                    rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)

                    rps['EMI'].append(EMI)
                    EMI_Remaining = EMI
                    
                    rps['ProfitAmount'].append(rps['OutstandingPrincipal'][-1] * ProfitRate / 360 * rps['Days'][-1])
                    EMI_Remaining = EMI_Remaining - rps['ProfitAmount'][-1]
                    
                    rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor)
                    EMI_Remaining = EMI_Remaining - rps['TakafulAmount'][-1]

                    rps['GracePeriodProfitRecovery'].append(max(min(EMI_Remaining, GracePeriodProfit),0))
                    GracePeriodProfit -= rps['GracePeriodProfitRecovery'][-1]
                    EMI_Remaining = EMI_Remaining - rps['GracePeriodProfitRecovery'][-1]
                    
                    rps['GracePeriodTakafulRecovery'].append(max(min(EMI_Remaining, GracePeriodTakaful),0))
                    GracePeriodTakaful -= rps['GracePeriodTakafulRecovery'][-1]
                    EMI_Remaining = EMI_Remaining - rps['GracePeriodTakafulRecovery'][-1]

                    rps['PrincipalAmount'].append(max(EMI_Remaining,0))
                    rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1] - rps['PrincipalAmount'][-1])


                    SNo += 1
                    year = FirstEMIYear + ((FirstEMIMonth + (i-2))//12)
                    month = ((FirstEMIMonth + (i-2)) % 12) + 1



                # while True:
                #     rps_copy = deepcopy(rps)
                #     for i in range(0,distributionMonths):
                #         year = FirstEMIYear + ((FirstEMIMonth + (i-1))//12)
                #         month = ((FirstEMIMonth + (i-1)) % 12) + 1
                #         day = PayDay
                #         rps_copy['Date'].append(date(year, month, day))  
                #         rps_copy['Days'].append((rps_copy['Date'][-1] - rps_copy['Date'][-2]).days)
                #         rps_copy['ProfitAmount'].append(rps_copy['OutstandingPrincipal'][-1] * ProfitRate / 360 * rps_copy['Days'][-1])
                #         # rps_copy['TakafulAmount'].append(rps_copy['OutstandingPrincipal'][-1] * TakafulFactor * rps_copy['Days'][-1] / 30)
                #         rps_copy['TakafulAmount'].append(rps_copy['OutstandingPrincipal'][-1] * TakafulFactor)
                #         rps_copy['GracePeriodTakafulRecovery'].append(GracePeriodTakaful / distributionMonths)
                #         rps_copy['GracePeriodProfitRecovery'].append(GracePeriodProfit / distributionMonths)
                #         rps_copy['EMI'].append(EMI)
                #         rps_copy['PrincipalAmount'].append(rps_copy['EMI'][-1] - rps_copy['ProfitAmount'][-1] - rps_copy['TakafulAmount'][-1] - rps_copy['GracePeriodTakafulRecovery'][-1] - rps_copy['GracePeriodProfitRecovery'][-1])
                #         rps_copy['OutstandingPrincipal'].append(rps_copy['OutstandingPrincipal'][-1] - rps_copy['PrincipalAmount'][-1])
                
                #     if sum(1 for i in rps_copy['PrincipalAmount'] if i < 0)== 0:
                #         break
                #     else:
                #         distributionMonths += 1

                # for i in range(0,TenorMonths-nGraceMonths):
                #     rps['SNo'].append(2+i)   
                #     if i in range (0, distributionMonths):
                #         year = FirstEMIYear + ((FirstEMIMonth + (i-1))//12)
                #         month = ((FirstEMIMonth + (i-1)) % 12) + 1
                #         day = PayDay
                #         rps['Date'].append(date(year, month, day))  
                #         rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)
                #         rps['ProfitAmount'].append(rps['OutstandingPrincipal'][-1] * ProfitRate / 360 * rps['Days'][-1])
                #         # rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor * rps['Days'][-1] / 30)
                #         rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor)
                #         rps['GracePeriodTakafulRecovery'].append(GracePeriodTakaful / distributionMonths)
                #         rps['GracePeriodProfitRecovery'].append(GracePeriodProfit / distributionMonths)
                #         rps['EMI'].append(EMI)
                #         rps['PrincipalAmount'].append(max(0,rps['EMI'][-1] - rps['ProfitAmount'][-1] - rps['TakafulAmount'][-1] - rps['GracePeriodTakafulRecovery'][-1] - rps['GracePeriodProfitRecovery'][-1]))
                #         rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1] - rps['PrincipalAmount'][-1])
                        
                #     else:
                #         year = FirstEMIYear + ((FirstEMIMonth + (i-1))//12)
                #         month = ((FirstEMIMonth + (i-1)) % 12) + 1
                #         day = PayDay
                #         rps['Date'].append(date(year, month, day))  
                #         rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)
                #         rps['EMI'].append(EMI)
                #         rps['ProfitAmount'].append(rps['OutstandingPrincipal'][-1] * ProfitRate / 360 * rps['Days'][-1])
                #         # rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor * rps['Days'][-1] / 30)
                #         rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor)
                #         rps['GracePeriodTakafulRecovery'].append(0)
                #         rps['GracePeriodProfitRecovery'].append(0)
                #         rps['PrincipalAmount'].append(max(0,rps['EMI'][-1] - rps['ProfitAmount'][-1] - rps['TakafulAmount'][-1] - rps['GracePeriodTakafulRecovery'][-1] - rps['GracePeriodProfitRecovery'][-1]))
                #         rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1] - rps['PrincipalAmount'][-1])

    elif repaymentMethod == "PrincipalGrace":
        rps = {
            'SNo' : [],
            'Date' : [],
            'Days' : [],
            'EMI' : [],
            # "GracePeriodProfitRecovery" : [],
            # "GracePeriodTakafulRecovery" : [],
            'ProfitAmount' : [],
            'TakafulAmount' : [],
            'PrincipalAmount' : [],
            'OutstandingPrincipal' : []
           }

        if GracePeriodDate == DisbursementDate:
            raise ValueError("Grace period cannot end on the same date as the loan disbursement. Please adjust GracePeriodDate value.")
        
        if GracePeriodProfitRate is None:
            print("GracePeriodProfitRate not found, setting to ProfitRate")
            GracePeriodProfitRate = ProfitRate
        else:
            print("GracePeriodProfitRate found: ", GracePeriodProfitRate)
    
        # Creating the first row to show the disbursement of the loan

        rps['SNo'].append(0)
        rps['Date'].append(date(DisbursementYear, DisbursementMonth, DisbursementDay))
        rps['Days'].append(0)
        rps['EMI'].append(0)
        rps['ProfitAmount'].append(0)
        rps['TakafulAmount'].append(0)
        # rps['GracePeriodTakafulRecovery'].append(0)
        # rps['GracePeriodProfitRecovery'].append(0)
        rps['PrincipalAmount'].append(0)
        rps['OutstandingPrincipal'].append(FinanceAmount)


        # Displaying the Profit Due during the Grace Period

        SNo = 1

        CurrentMonth = DisbursementMonth
        CurrentYear = DisbursementYear

        if date(CurrentYear, CurrentMonth, PayDay) <= date(DisbursementYear, DisbursementMonth, DisbursementDay):    
            # Incrementing CurrentDate by 1 month
            if CurrentMonth == 12:
                CurrentMonth = 1
                CurrentYear += 1
            else:
                CurrentMonth += 1
            
        CurrentDate = date(CurrentYear, CurrentMonth, PayDay)
        
        GracePeriodYear = int(GracePeriodDate[0:4])
        GracePeriodMonth = int(GracePeriodDate[4:6])
        GracePeriodDay = int(GracePeriodDate[6:8])
        GraceEndDate = date(GracePeriodYear, GracePeriodMonth, GracePeriodDay)
    
        while CurrentDate <= GraceEndDate:
            rps['SNo'].append(SNo)
            rps['Date'].append(CurrentDate)
            rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)
            rps['ProfitAmount'].append(round(rps['OutstandingPrincipal'][-1] * GracePeriodProfitRate / 360 * rps['Days'][-1],3))
            rps['TakafulAmount'].append(round(rps['OutstandingPrincipal'][-1] * TakafulFactor,3))
            # rps['GracePeriodProfitRecovery'].append(0)
            # rps['GracePeriodTakafulRecovery'].append(0)
            rps['EMI'].append(rps['ProfitAmount'][-1] + rps['TakafulAmount'][-1])
            rps['PrincipalAmount'].append(0)
            rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1])

            SNo += 1

            # Incrementing CurrentDate by 1 month
            if CurrentMonth == 12:
                CurrentMonth = 1
                CurrentYear += 1
            else:
                CurrentMonth += 1
            CurrentDate = date(CurrentYear, CurrentMonth, PayDay)


        for i in range(SNo, TenorMonths+1):
            rps['SNo'].append(i)
            rps['Date'].append(CurrentDate)
            rps['Days'].append((rps['Date'][-1] - rps['Date'][-2]).days)

            rps['EMI'].append(EMI)
            EMI_Remaining = EMI
            
            rps['ProfitAmount'].append(rps['OutstandingPrincipal'][-1] * ProfitRate / 360 * rps['Days'][-1])
            EMI_Remaining = EMI_Remaining - rps['ProfitAmount'][-1]
            
            rps['TakafulAmount'].append(rps['OutstandingPrincipal'][-1] * TakafulFactor)
            EMI_Remaining = EMI_Remaining - rps['TakafulAmount'][-1]
            
            # rps['GracePeriodProfitRecovery'].append(0)
            # rps['GracePeriodTakafulRecovery'].append(0)
            

            rps['PrincipalAmount'].append(max(EMI_Remaining,0))
            rps['OutstandingPrincipal'].append(rps['OutstandingPrincipal'][-1] - rps['PrincipalAmount'][-1])


            SNo += 1
            # Incrementing CurrentDate by 1 month
            if CurrentMonth == 12:
                CurrentMonth = 1
                CurrentYear += 1
            else:
                CurrentMonth += 1
            CurrentDate = date(CurrentYear, CurrentMonth, PayDay)


    else:
        raise AttributeError("Please input the correct repaymentMethod. (Normal / Bullet / Grace / PrincipalGrace)")
    df = pd.DataFrame(rps)

    return df

def goalSeek(
        FinanceAmount: float,
        ProfitRate: float,
        TenorMonths : int,
        PayDay : int,
        DisbursementDate : str,
        FirstEMIDate : str,
        TakafulFactor : float,
        repaymentMethod : str,
        GracePeriodDate : str = None,
        GracePeriodProfitRate : float = None
        ):
    
    ProfitRate /= 100
    TakafulFactor /= 100

    if ProfitRate != 0:
        EMI = FinanceAmount / ((1 - pow((1+(ProfitRate/12)),-TenorMonths))/(ProfitRate/12))
    else:
        EMI = FinanceAmount / TenorMonths


    df = RPS(FinanceAmount = FinanceAmount,
        ProfitRate = ProfitRate,
        TenorMonths = TenorMonths,
        PayDay = PayDay,
        DisbursementDate = DisbursementDate,
        GracePeriodDate = GracePeriodDate,
        FirstEMIDate = FirstEMIDate,
        TakafulFactor = TakafulFactor,
        EMI = EMI,
        repaymentMethod = repaymentMethod,
        GracePeriodProfitRate = GracePeriodProfitRate)

    delta_old = df.iloc[-1]['OutstandingPrincipal']
    change = 0.0001
    gradient = 1

    while delta_old >= 0.0005 or delta_old <= -0.0005:

        if delta_old >= 0.0005:
            EMI += change

            df = RPS(FinanceAmount = FinanceAmount,
                ProfitRate = ProfitRate,
                TenorMonths = TenorMonths,
                PayDay = PayDay,
                DisbursementDate = DisbursementDate,
                GracePeriodDate = GracePeriodDate,
                FirstEMIDate = FirstEMIDate,
                TakafulFactor = TakafulFactor,
                EMI = EMI,
                repaymentMethod = repaymentMethod,
                GracePeriodProfitRate = GracePeriodProfitRate)
            
            delta_new = df.iloc[-1]['OutstandingPrincipal']
            gradient = (delta_new - delta_old) / change

        if delta_old <= -0.0005:
            EMI -= change

            df = RPS(FinanceAmount = FinanceAmount,
                ProfitRate = ProfitRate,
                TenorMonths = TenorMonths,
                PayDay = PayDay,
                DisbursementDate = DisbursementDate,
                GracePeriodDate = GracePeriodDate,
                FirstEMIDate = FirstEMIDate,
                TakafulFactor = TakafulFactor,
                EMI = EMI,
                repaymentMethod = repaymentMethod,
                GracePeriodProfitRate = GracePeriodProfitRate)
            
            delta_new = df.iloc[-1]['OutstandingPrincipal']
            gradient = (delta_new - delta_old) / change

        delta_old = delta_new

        change = abs(delta_old / gradient)
        if change == math.inf or change == -math.inf:
            change = abs(delta_old / 2)

    df['EMI'] = round(df['EMI'] , 3)
    df['ProfitAmount'] = round(df['ProfitAmount'] , 3)
    df['TakafulAmount'] = round(df['TakafulAmount'] , 3)
    df['PrincipalAmount'] = round(df['PrincipalAmount'] , 3)

    df['OutstandingPrincipal'] = round(df['OutstandingPrincipal'] , 3)

    if repaymentMethod == "Grace":
        df['GracePeriodTakafulRecovery'] = round(df['GracePeriodTakafulRecovery'], 3)
        df['GracePeriodProfitRecovery'] = round(df['GracePeriodProfitRecovery'], 3)


    if df['PrincipalAmount'].sum() != FinanceAmount:
        df.loc[df.shape[0]-1,'PrincipalAmount'] = round(FinanceAmount - round(df.loc[0:df.shape[0]-2,'PrincipalAmount'].sum(),3),3)

    if TakafulFactor != 0:
        if repaymentMethod != "Grace":
            for i in range(0, df.shape[0]):
                df.loc[i, 'TakafulAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i][['ProfitAmount','PrincipalAmount']].sum().sum(),3),0)
        else:
            for i in range(0, df.shape[0]):
                df.loc[i, 'TakafulAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i][['ProfitAmount','PrincipalAmount','GracePeriodTakafulRecovery','GracePeriodProfitRecovery']].sum().sum(),3),0)
    else:
        if repaymentMethod != "Grace":
            for i in range(0, df.shape[0]):
                df.loc[i, 'ProfitAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i]['PrincipalAmount'].sum(),3),0)
        else:
            for i in range(0, df.shape[0]):
                df.loc[i, 'ProfitAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i][['PrincipalAmount','GracePeriodTakafulRecovery','GracePeriodProfitRecovery']].sum().sum(),3),0)
 
 
    # Rounding off the the final Outstanding Principal value to ensure it is non-negative
    df.loc[df.shape[0]-1, 'OutstandingPrincipal'] = abs(max(round(df.loc[df.shape[0]-1, 'OutstandingPrincipal'],0), 0))
    
    difference = df.loc[df.shape[0]-1, 'ProfitAmount'] + df.loc[df.shape[0]-1, 'TakafulAmount'] + df.loc[df.shape[0]-1, 'PrincipalAmount'] - df.loc[df.shape[0]-1, 'EMI']

    if difference != 0:
        df.loc[df.shape[0]-1, 'ProfitAmount'] = df.loc[df.shape[0]-1, 'ProfitAmount'] - difference

    for i in range(0,df.shape[0]):
        df.loc[i,'Date'] = str(df.loc[i,'Date'])

    return df.to_json(orient = 'records')



def goalSeekwithEMI(
        FinanceAmount: float,
        EMI: float,
        TenorMonths : int,
        PayDay : int,
        DisbursementDate : str,
        FirstEMIDate : str,
        TakafulFactor : float,
        repaymentMethod : str,
        GracePeriodDate : str = None,
        GracePeriodProfitRate : float = None
        ):
    
    # ProfitRate /= 100
    TakafulFactor /= 100

    if EMI == FinanceAmount / TenorMonths:
        ProfitRate = 0
    else:
        ProfitRate = (EMI * TenorMonths - FinanceAmount) / (FinanceAmount * TenorMonths)


    df = RPS(FinanceAmount = FinanceAmount,
        ProfitRate = ProfitRate,
        TenorMonths = TenorMonths,
        PayDay = PayDay,
        DisbursementDate = DisbursementDate,
        GracePeriodDate = GracePeriodDate,
        FirstEMIDate = FirstEMIDate,
        TakafulFactor = TakafulFactor,
        EMI = EMI,
        repaymentMethod = repaymentMethod,
        GracePeriodProfitRate = GracePeriodProfitRate)

    delta_old = df.iloc[-1]['OutstandingPrincipal']
    change = 0.00001
    gradient = 1
    loop_count = 0
    

    while delta_old >= 0.0005 or delta_old <= -0.0005:

        # print(loop_count)
        # loop_count += 1
        

        if delta_old >= 0.0005:
            ProfitRate -= change

            df = RPS(FinanceAmount = FinanceAmount,
                ProfitRate = ProfitRate,
                TenorMonths = TenorMonths,
                PayDay = PayDay,
                DisbursementDate = DisbursementDate,
                GracePeriodDate = GracePeriodDate,
                FirstEMIDate = FirstEMIDate,
                TakafulFactor = TakafulFactor,
                EMI = EMI,
                repaymentMethod = repaymentMethod,
                GracePeriodProfitRate = GracePeriodProfitRate)
            
            delta_new = df.iloc[-1]['OutstandingPrincipal']
            gradient = (delta_new - delta_old) / change

        if delta_old <= -0.0005:
            ProfitRate += change

            df = RPS(FinanceAmount = FinanceAmount,
                ProfitRate = ProfitRate,
                TenorMonths = TenorMonths,
                PayDay = PayDay,
                DisbursementDate = DisbursementDate,
                GracePeriodDate = GracePeriodDate,
                FirstEMIDate = FirstEMIDate,
                TakafulFactor = TakafulFactor,
                EMI = EMI,
                repaymentMethod = repaymentMethod,
                GracePeriodProfitRate = GracePeriodProfitRate)
            
            delta_new = df.iloc[-1]['OutstandingPrincipal']
            gradient = (delta_new - delta_old) / (change)

        delta_old = delta_new

        change = abs(delta_old / gradient)
        if change == math.inf or change == -math.inf:
            change = abs(delta_old / 2)

    df['EMI'] = round(df['EMI'] , 3)
    df['ProfitAmount'] = round(df['ProfitAmount'] , 3)
    df['TakafulAmount'] = round(df['TakafulAmount'] , 3)
    df['PrincipalAmount'] = round(df['PrincipalAmount'] , 3)

    df['OutstandingPrincipal'] = round(df['OutstandingPrincipal'] , 3)

    if repaymentMethod == "Grace":
        df['GracePeriodTakafulRecovery'] = round(df['GracePeriodTakafulRecovery'], 3)
        df['GracePeriodProfitRecovery'] = round(df['GracePeriodProfitRecovery'], 3)


    if df['PrincipalAmount'].sum() != FinanceAmount:
        df.loc[df.shape[0]-1,'PrincipalAmount'] = round(FinanceAmount - round(df.loc[0:df.shape[0]-2,'PrincipalAmount'].sum(),3),3)

    if TakafulFactor != 0:
        if repaymentMethod != "Grace":
            for i in range(0, df.shape[0]):
                df.loc[i, 'TakafulAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i][['ProfitAmount','PrincipalAmount']].sum().sum(),3),0)
        else:
            for i in range(0, df.shape[0]):
                df.loc[i, 'TakafulAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i][['ProfitAmount','PrincipalAmount','GracePeriodTakafulRecovery','GracePeriodProfitRecovery']].sum().sum(),3),0)
    else:
        if repaymentMethod != "Grace":
            for i in range(0, df.shape[0]):
                df.loc[i, 'ProfitAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i]['PrincipalAmount'].sum(),3),0)
        else:
            for i in range(0, df.shape[0]):
                df.loc[i, 'ProfitAmount'] = max(round(df.loc[i, 'EMI'] - df.iloc[i][['PrincipalAmount','GracePeriodTakafulRecovery','GracePeriodProfitRecovery']].sum().sum(),3),0)
 
 
    # Rounding off the the final Outstanding Principal value to ensure it is non-negative
    df.loc[df.shape[0]-1, 'OutstandingPrincipal'] = abs(max(round(df.loc[df.shape[0]-1, 'OutstandingPrincipal'],0), 0))
    
    difference = df.loc[df.shape[0]-1, 'ProfitAmount'] + df.loc[df.shape[0]-1, 'TakafulAmount'] + df.loc[df.shape[0]-1, 'PrincipalAmount'] - df.loc[df.shape[0]-1, 'EMI']

    if difference != 0:
        df.loc[df.shape[0]-1, 'ProfitAmount'] = df.loc[df.shape[0]-1, 'ProfitAmount'] - difference

    for i in range(0,df.shape[0]):
        df.loc[i,'Date'] = str(df.loc[i,'Date'])

    final_result = {"ProfitRate" : round(ProfitRate * 100, 2),
        "RPS" : json.loads(df.to_json(orient = 'records'))}

    final_result = json.dumps(final_result)

    return final_result
