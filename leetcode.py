def letterCombinations(digits: str):

    d2l_dict = {"2":"ABC", "3":"def", "4":"ghi", "5":"jkl", "6":"mno", "7":"pqrs" , "8":"tuv", "9":"wxyz"}
    for s in digits:
        d2l_dict[s]

print(letterCombinations("23"))