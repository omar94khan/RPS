The purpose of this project was to initially solve a problem that the bank had with regards to quickly generating repayment schedules for loans that they were disbursing.

There are four different repayment schedule types that get generated. 

1) Normal
   This Repayment schedule is your run-of-the-mill RPS, which calculates the profit accrued between each installment, the takaful/insurance owed by the client with each installment, and the portion of the principal that is being repaid by the client with each installment, while keeping the client's monthly installments consistent.
2) Grace
   This Repayment Schedule allows for the user to define a period in between the disbursement of the loan, and the first installment that is paid by the client, as the Grace Period tenor. The profit and insurance that is accrued during the Grace Period will be paid back by the client after their first installment begins.
3) Bullet
   This Repayment Schedule allows the client to fully pay off their loan in one installment, which covers the entire principal, as well as the profit that has been accrued.
4) PrincipalGrace
   Unlike the normal Grace repayment method, this Repayment Schedule does show that the client will need to service their profit and insurance accrued during the Grace Period, but they will be exempt from paying part of their principal during this time.

There are two main function within this application that can be used.
1) /api/cob-obb-rps-service/rpsgeneratewithEMI

This API is used to generate the RPS where we give the system the EMI we need to use, and in the response we see how much the client's reducing rate comes out to.

   Sample Payload:
 ```
{
    "FinanceAmount": 2400,                            // This is the amount of the loan disbursed
    "EMI": 300,                                       // This is the targetted installment that the client is willing to pay per month
    "TenorMonths": 12,                                // This is the total number of months for the loan (including the grace period)
    "PayDay": 28,                                     // This is the date at which the client's installment will become due on each month (cannot be greater than 28)
    "DisbursementDate": "20251202",                   // This specifies the date of the disbursement of the loan. Format = YYYYMMDD
    "GracePeriodDate": "20260302",                    // This specifies the end of the Grace Period for the loan. Format = YYYYMMDD. Only needed if the repaymentMethod is either Grace or PrincipalGrace
    "FirstEMIDate": "20260328",                       // This specifies the date at which the client will be paying their first full installment. Format = YYYYMMDD
    "TakafulFactor": 0.01229,                         // This is the monthly rate at which the client owes their monthly insurance. This is charged at the end of the month on the basis of the principal outstanding. Formatted as a percentage. In the example it is 0.01229% insurance charge per month.
    "GracePeriodProfitRate" : 0.065,                  // This is the profit rate the client is to be charged with during their Grace Period. Formatted as a decimal. In the example the Grace Period Profit Rate is 6.5% annual. Only needed when the repaymentMethod is PrincipalGrace.
    "repaymentMethod": "PrincipalGrace"               // This defines the type of Repayment Schedule that is meant to be generated.
}
```

Sample Response:
```
{
    "ProfitRate": 28.36,
    "RPS": [
        {
            "Date": "2025-12-02",
            "Days": 0,
            "EMI": 0.0,
            "OutstandingPrincipal": 2400.0,
            "PrincipalAmount": 0.0,
            "ProfitAmount": 0.0,
            "SNo": 0,
            "TakafulAmount": 0.0
        },
        {
            "Date": "2026-01-02",
            "Days": 31,
            "EMI": 58.9,
            "OutstandingPrincipal": 2400.0,
            "PrincipalAmount": 0.0,
            "ProfitAmount": 58.605,
            "SNo": 1,
            "TakafulAmount": 0.295
        },
        {
            "Date": "2026-02-02",
            "Days": 31,
            "EMI": 58.9,
            "OutstandingPrincipal": 2400.0,
            "PrincipalAmount": 0.0,
            "ProfitAmount": 58.605,
            "SNo": 2,
            "TakafulAmount": 0.295
        },
        {
            "Date": "2026-03-02",
            "Days": 28,
            "EMI": 53.228,
            "OutstandingPrincipal": 2400.0,
            "PrincipalAmount": 0.0,
            "ProfitAmount": 52.933,
            "SNo": 3,
            "TakafulAmount": 0.295
        },
        {
            "Date": "2026-04-02",
            "Days": 31,
            "EMI": 300.0,
            "OutstandingPrincipal": 2158.9,
            "PrincipalAmount": 241.1,
            "ProfitAmount": 58.605,
            "SNo": 4,
            "TakafulAmount": 0.295
        },
        {
            "Date": "2026-05-02",
            "Days": 30,
            "EMI": 300.0,
            "OutstandingPrincipal": 1910.182,
            "PrincipalAmount": 248.718,
            "ProfitAmount": 51.017,
            "SNo": 5,
            "TakafulAmount": 0.265
        },
        {
            "Date": "2026-06-02",
            "Days": 31,
            "EMI": 300.0,
            "OutstandingPrincipal": 1657.061,
            "PrincipalAmount": 253.121,
            "ProfitAmount": 46.644,
            "SNo": 6,
            "TakafulAmount": 0.235
        },
        {
            "Date": "2026-07-02",
            "Days": 30,
            "EMI": 300.0,
            "OutstandingPrincipal": 1396.423,
            "PrincipalAmount": 260.638,
            "ProfitAmount": 39.158,
            "SNo": 7,
            "TakafulAmount": 0.204
        },
        {
            "Date": "2026-08-02",
            "Days": 31,
            "EMI": 300.0,
            "OutstandingPrincipal": 1130.693,
            "PrincipalAmount": 265.73,
            "ProfitAmount": 34.099,
            "SNo": 8,
            "TakafulAmount": 0.171
        },
        {
            "Date": "2026-09-02",
            "Days": 31,
            "EMI": 300.0,
            "OutstandingPrincipal": 858.442,
            "PrincipalAmount": 272.251,
            "ProfitAmount": 27.61,
            "SNo": 9,
            "TakafulAmount": 0.139
        },
        {
            "Date": "2026-10-02",
            "Days": 30,
            "EMI": 300.0,
            "OutstandingPrincipal": 578.834,
            "PrincipalAmount": 279.609,
            "ProfitAmount": 20.286,
            "SNo": 10,
            "TakafulAmount": 0.105
        },
        {
            "Date": "2026-11-02",
            "Days": 31,
            "EMI": 300.0,
            "OutstandingPrincipal": 293.039,
            "PrincipalAmount": 285.794,
            "ProfitAmount": 14.134,
            "SNo": 11,
            "TakafulAmount": 0.072
        },
        {
            "Date": "2026-12-02",
            "Days": 30,
            "EMI": 300.0,
            "OutstandingPrincipal": 0.0,
            "PrincipalAmount": 293.039,
            "ProfitAmount": 6.925,
            "SNo": 12,
            "TakafulAmount": 0.036
        }
    ]
}
```


2) /api/cob-obb-rps-service/rpsgenerate

This API is used to generate the RPS where we give the system the profit rate we need to use, and in the response we see how much the client's EMI comes out to.

   Sample Payload:
 ```
{
    "FinanceAmount": 2400,                        // Same as above
    "ProfitRate": 0.05,                           // This signifies the rate at which the client will be charged a profit each month. Format = annualized profit rate as a decimal.
    "TenorMonths": 12,                            // Same as above
    "PayDay": 28,                                 // Same as above
    "DisbursementDate": "20251202",               // Same as above
    "GracePeriodDate": "20260202",                // Same as above
    "FirstEMIDate": "20260328",                   // Same as above
    "TakafulFactor": 0.01229,                     // Same as above
    "repaymentMethod": "Grace"                    // Same as above
}
```

Sample Response:
```
[
    {
        "Date": "2025-12-02",
        "Days": 0,
        "EMI": 0.0,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 2400.0,
        "PrincipalAmount": 0.0,
        "ProfitAmount": 0.0,
        "SNo": 0,
        "TakafulAmount": 0.0
    },
    {
        "Date": "2026-02-02",
        "Days": 62,
        "EMI": 0.0,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 2400.0,
        "PrincipalAmount": 0.0,
        "ProfitAmount": 0.0,
        "SNo": 1,
        "TakafulAmount": 0.0
    },
    {
        "Date": "2026-04-28",
        "Days": 85,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 20.667,
        "GracePeriodTakafulRecovery": 0.59,
        "OutstandingPrincipal": 2201.486,
        "PrincipalAmount": 198.514,
        "ProfitAmount": 0.283,
        "SNo": 2,
        "TakafulAmount": 0.295
    },
    {
        "Date": "2026-05-28",
        "Days": 30,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 1981.5,
        "PrincipalAmount": 219.987,
        "ProfitAmount": 0.092,
        "SNo": 3,
        "TakafulAmount": 0.27
    },
    {
        "Date": "2026-06-28",
        "Days": 31,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 1761.48,
        "PrincipalAmount": 220.02,
        "ProfitAmount": 0.085,
        "SNo": 4,
        "TakafulAmount": 0.244
    },
    {
        "Date": "2026-07-28",
        "Days": 30,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 1541.421,
        "PrincipalAmount": 220.059,
        "ProfitAmount": 0.073,
        "SNo": 5,
        "TakafulAmount": 0.217
    },
    {
        "Date": "2026-08-28",
        "Days": 31,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 1321.328,
        "PrincipalAmount": 220.093,
        "ProfitAmount": 0.066,
        "SNo": 6,
        "TakafulAmount": 0.19
    },
    {
        "Date": "2026-09-28",
        "Days": 31,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 1101.198,
        "PrincipalAmount": 220.13,
        "ProfitAmount": 0.057,
        "SNo": 7,
        "TakafulAmount": 0.162
    },
    {
        "Date": "2026-10-28",
        "Days": 30,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 881.031,
        "PrincipalAmount": 220.168,
        "ProfitAmount": 0.046,
        "SNo": 8,
        "TakafulAmount": 0.135
    },
    {
        "Date": "2026-11-28",
        "Days": 31,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 660.828,
        "PrincipalAmount": 220.203,
        "ProfitAmount": 0.038,
        "SNo": 9,
        "TakafulAmount": 0.108
    },
    {
        "Date": "2026-12-28",
        "Days": 30,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 440.588,
        "PrincipalAmount": 220.24,
        "ProfitAmount": 0.028,
        "SNo": 10,
        "TakafulAmount": 0.081
    },
    {
        "Date": "2027-01-28",
        "Days": 31,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 220.312,
        "PrincipalAmount": 220.276,
        "ProfitAmount": 0.019,
        "SNo": 11,
        "TakafulAmount": 0.054
    },
    {
        "Date": "2027-02-28",
        "Days": 31,
        "EMI": 220.349,
        "GracePeriodProfitRecovery": 0.0,
        "GracePeriodTakafulRecovery": 0.0,
        "OutstandingPrincipal": 0.0,
        "PrincipalAmount": 220.31,
        "ProfitAmount": 0.009,
        "SNo": 12,
        "TakafulAmount": 0.03
    }
]
```

