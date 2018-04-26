import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from dat_utils import *

# datオブジェクトを作成
dat = Dat("testfile.dat")

# 各パラメータを参照する
print(dat.n)
print(dat.m)
print(dat.dk)

# パラメータを取得する際の動作をカスタマイズする
# read_paramsに与えるlambda式を変更することで通常とは異なる形式でパラメータを得ることができる
# dat.capacityは通常(int, int, float)の形式だが(str, str, float)に変更して取得する
converter = lambda params: (params[0], params[1], float(params[2]))
for params in dat.read_params("capacity", converter):
    print(params)
