import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from brite_utils import *

# briteオブジェクトを作成
brite = BRITEParser("testfile.brite")

# datファイルとcsvファイルに書き込む
to_dat("testfile.brite", "testfile.dat")
to_coordinate_csv("testfile.brite", "testfile.csv")
