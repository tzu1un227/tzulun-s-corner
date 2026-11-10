def isValidSudoku(board):
    
    for i in range(9):
        temp_raw_list = []
        temp_col_list = []
        temp_box_list = []
        if board[i] in temp_raw_list and board[i] != ".":
            return False
        else:
            temp_raw_list.append(board[i])

        for j in range(9):
            if board[i][j] in temp_col_list and board[i] != ".":
                return False
            else:
                temp_col_list.append(board[i][j])
        
        for k in range(3):
            for l in range(3):
                if board[(i/3)*3+k][(i%3)*3+l] in temp_box_list and board[i] != ".":
                    return False
                else:
                    temp_box_list.append(board[(i/3)*3+k][(i%3)*3+l])

    return True

    
print(isValidSudoku([["1","2",".",".","3",".",".",".","."],
                     ["4",".",".","5",".",".",".",".","."],
                     [".","9","8",".",".",".",".",".","3"],
                     ["5",".",".",".","6",".",".",".","4"],
                     [".",".",".","8",".","3",".",".","5"],
                     ["7",".",".",".","2",".",".",".","6"],
                     [".",".",".",".",".",".","2",".","."],
                     [".",".",".","4","1","9",".",".","8"],
                     [".",".",".",".","8",".",".","7","9"]]))

print(isValidSudoku([["1","2",".",".","3",".",".",".","."],
                     ["4",".",".","5",".",".",".",".","."],
                     [".","9","1",".",".",".",".",".","3"],
                     ["5",".",".",".","6",".",".",".","4"],
                     [".",".",".","8",".","3",".",".","5"],
                     ["7",".",".",".","2",".",".",".","6"],
                     [".",".",".",".",".",".","2",".","."],
                     [".",".",".","4","1","9",".",".","8"],
                     [".",".",".",".","8",".",".","7","9"]]))