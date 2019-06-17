#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 13:37:28 2019

@author: Owner
"""
from PIL import Image

class Shogi:
    #### Parameter ####
    board = [["OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_"] for i in range(9)]
    plyr1 = []
    plyr2 = []
    kif = []
    turn_now = 0 
    id_turn = {0:"先手", 1: "後手"}
    id_turnMk = {0:"☗", 1: "☖"}
    id_piece = {"POH":"王将", "PGK":"玉将", \
                "PHS":"飛車", "NHS":"竜王", \
                "PKK":"角行", "NKK":"竜馬", \
                "PKN":"金将", \
                "PGN":"銀将", "NGN":"成銀", \
                "PKM":"桂馬", "NKM":"成桂", \
                "PKY":"香車", "NKY":"成香", \
                "PFU":"歩兵", "NFU":"と金", \
                "OPN":"＿＿"}
    board_offsetX = 25
    board_offsetY = 25
    show_board_flg = False
    
    def __init__(self):
        self.config()
        self.mkInitBoard()
        self.showBoard()
    def config(self):
        pass
    
    def play(self):
        gameset_flg = False 
        plyr_now = int(self.turn_now%2) # 0:先手, 1:後手
        self.turn_now = 0 
        #### 対局終了までループ ####
        while gameset_flg == False:            
            plyr_now = int(self.turn_now%2)
            pos_from = [0, 0]
            pos_to = [0, 0]       
            pos_flg = False
            chosen_piece = "OPN"
            if plyr_now == 0:
                plyr_pieces = self.plyr1 #駒台の選択
            else:
                plyr_pieces = self.plyr2
                
            print(self.id_turn[plyr_now]+"の番です。") 
            #### 指し手の入力 ####
            """
            アルゴリズム再考
            １．可能な指し手を全列挙（list　前座標　後座標　駒）
            ・関数化しておく
            ・盤上の手番に所属する駒毎の可能な指し手をリストに含める。
            ・持ち駒の探索も含める（set　を使って重複探索を避ける）
            ２．指し手の入力
            ３．入力された指し手が盤上にあるか判定する
            ・関数化しておく
            ４．駒取りなどの処理を行い盤面に反映
            """
            while pos_flg == False:
                print("入力形式: 動かす駒の筋 動かす駒の段")
                print("持駒選択: 0 0")        
                print("投了: -1 0 ")        
                pos_from[1],pos_from[0] = map(int, input("動かす駒: ").split())
                if pos_from[0] == 0 and pos_from[1] == 0:
                    plyr_set = set(plyr_pieces)
                    if len(plyr_set) == 0:
                        print("駒台に駒がありません。")
                        continue
                    plyr_set4show = dict()
                    print("駒台から駒を選択してください。打つ駒の種類に対応するリストの数字を入力してください。")                    
                    for idx, ps in enumerate(plyr_set):
                        plyr_set4show[idx] = self.id_piece[ps]
                    print(self.id_turnMk[plyr_now]+plyr_set4show)
                    print("持駒選択の取消: -1")
                    kind_piece = int(input("持ち駒の入力: "))
                    if kind_piece == -1:
                        continue
                    if kind_piece <-1 or len(plyr_set) <= kind_piece:
                        ("リストにある数字を選択してください。指し手の選択に戻ります。")
                        continue
                    chosen_piece = plyr_set4show[kind_piece] #持ち駒の決定
                    
                else:
                    pos_from[0] = pos_from[0] -1 # 筋、段を行列の座標に変換
                    pos_from[1] = 9- pos_from[1]
                    if self.isInside(pos_from[0],pos_from[1]) == False:
                        print("選択した場所が盤の外です。1～9 筋、1～9 段の範囲で指定してください。")
                        continue
                    if self.isMyPiece(pos_from[0],pos_from[1], plyr_now) == False:
                        print(self.id_turn[plyr_now]+"の駒を選んでください。")
                        continue
                    if pos_from[1] == -1: #投了時
                        plyr_now = int((plyr_now+1)%2)
                        gameset_flg = True
                        pos_flg = True
                        break 
                    chosen_piece = self.getKindPiece(pos_from[0],pos_from[1])
                print(vars())
                print("入力形式: 動かす先の筋 動かす先の段")
                print("動かす駒の選択に戻る: -1 0 ")        
                pos_to[1],pos_to[0] = map(int, input("動かす先: ").split())
                if pos_to[1] == -1:
                    continue
                pos_to[0] = pos_to[0] -1 # 筋、段を行列の座標に変換
                pos_to[1] = 9- pos_to[1]
                if self.isInside(pos_to[0],pos_to[1]) == False:
                    print("選択した場所が盤の外です。1～9 筋、1～9 段の範囲で指定してください。")
                    continue
                if self.isMyPiece(pos_to[0],pos_to[1], plyr_now):
                    print(self.id_turn[plyr_now]+"動かす先に自分の駒があります。")
                    continue
                
                
            if gameset_flg == False:
                self.showBoard()
                
        print("まで"+str(self.turn_now)+"手にて"+self.id_turn[plyr_now]+"の勝ち。")
    
    def mkInitBoard(self):        
        self.board[0][0] = "PKY2" 
        self.board[0][8] = "PKY2" 
        self.board[8][0] = "PKY1" 
        self.board[8][8] = "PKY1" 
        self.board[0][1] = "PKM2" 
        self.board[0][7] = "PKM2" 
        self.board[8][1] = "PKM1" 
        self.board[8][7] = "PKM1" 
        self.board[0][2] = "PGN2" 
        self.board[0][6] = "PGN2" 
        self.board[8][2] = "PGN1" 
        self.board[8][6] = "PGN1" 
        self.board[0][3] = "PKN2" 
        self.board[0][5] = "PKN2" 
        self.board[8][3] = "PKN1" 
        self.board[8][5] = "PKN1" 
        self.board[1][1] = "PKK2" 
        self.board[7][7] = "PKK1" 
        self.board[1][7] = "PHS2" 
        self.board[7][1] = "PHS1" 
        self.board[0][4] = "POH2" 
        self.board[8][4] = "PGK1"
        for i in range(9):
            self.board[2][i] = "PFU2"
            self.board[6][i] = "PFU1"
    
    def showBoard(self):
        #### 表示の準備 ####
        board4show = [["OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_", "OPN_"] for i in range(9)]
        plyr14show = []
        plyr24show = []
        board_img = Image.open("./image/board_bg.png")
        board_w, board_h = board_img.size
        
        #### 表示用盤面の作成 ####
        for i in range(9):
            for j in range(9):
                board4show[i][-j-1] = self.id_piece[self.board[i][j][0:3]]+str(self.board[i][j][3])
                if self.show_board_flg: # 表示用の盤面を作成
                    if self.board[i][j] == "OPN_": #OPN のマスには駒を表示しない
                        continue
                    piece_img = Image.open("./image/"+self.board[i][j][0:3]+".png") # 駒の画像をオープン
                    if int(self.board[i][j][3]) == 1: # ４文字目が２なら後手の駒として駒画像を反転
                        pass
                    else:
                        piece_img = piece_img.rotate(180)
                    piece_w, piece_h = piece_img.size
                    piece_mask = piece_img.split()[3]
                    board_img.paste(piece_img, \
                                    (board_w - self.board_offsetX - piece_w*(j+1), self.board_offsetY + piece_h*i), \
                                    piece_mask)    
        #### 表示用持ち駒の作成 ####
        if len(self.plyr1) == 0:
            plyr14show = ["持ち駒なし"]
        else:
            plyr1 = self.plyr1
            for piece in plyr1:
                plyr14show.append(self.id_piece[piece])
        if len(self.plyr2) == 0:
            plyr24show = ["持ち駒なし"]
        else:
            plyr2 = self.plyr2
            for piece in plyr2:
                plyr24show.append(self.id_piece[piece])
            
        #### 表示 ####
        print("☖: "+str(plyr24show))                    
        for i in board4show:
            print(*i)
        print("☗: "+str(plyr14show))
        if self.show_board_flg:
            board_img = board_img.resize((int(board_w*0.8), int(board_h*0.8)))
            board_img.show()
        
    def mvPiece(self, pos_from, pos_to):
        pass
    
    
    def getKindPiece(self, pos_r, pos_c):
        return self.board[pos_r][pos_c][0:3]
    
    def judgeMoving(self, pos_from, pos_to):
        pass
    
    def isInside(self, pos_r, pos_c):
        if 0 <= pos_r and pos_r <=8 and 0 <= pos_c and pos_c <=8:
            return True
        else:
            return False
        
    def isMyPiece(self, pos_r, pos_c, plyr_now):
        if int(self.board[pos_r][pos_c][3])-1 == plyr_now:
            return True
        else:
            return False