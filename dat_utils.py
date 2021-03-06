"""
the following statements are model data format of BRITE, COST239, JPNM and NSFNET

* number of demand path
param dk:= val;

* number of traffic
param m:= val;

* number of node
param n:= val;

* HOP
param : EN :HOP:=

* cost metric:delay
param : EM :COST:= 

* link capacity:bandwidth
param : E :c:= 

* traffic matrix:start node
param : SK :s:= 

* traffic matrix:target node
param : TK :t:= 

* demand path
param : DK :d:= 
"""

from os import path
import re
import codecs

class Dat:
    """
    Datクラスは以下の属性を持つ
    * all_lines
    * filename
    * dk
    * m
    * n
    * cost
    * capacity
    * hop
    * traffic
    * DK

    @propertyデコレータによってall_linesとfilename以外のゲッターの動作を変更している
    メソッド__get_attr1,2,3,4を経由してモデルファイルのパラメータを取り出す
    """

    # key: model data parameter name
    # value: regular expression
    attr_regexp = {"dk":       r"param dk\s*:=\s*(\d+);",
                   "m":        r"param m\s*:=\s*(\d+);",
                   "n":        r"param n\s*:=\s*(\d+);",
                   "hop":      r"param : EN\s*:\s*HOP\s*:=",
                   "cost":     r"param : EM\s*:\s*COST\s*:=\s*",
                   "capacity": r"param : E\s*:\s*[cC]\s*:=",
                   "start":    r"param : SK\s*:\s*s\s*:=",
                   "target":   r"param : TK\s*:\s*t\s*:=",
                   "DK":       r"param : DK\s*:\s*d\s*:="}

    def __init__(self, datfile):
        f = codecs.open(datfile, "r", "shift_jis")
        try:
            self.all_lines = f.read()
        finally:
            f.close()
        self.filename   = path.basename(datfile)
        self.__dk       = "dk"
        self.__m        = "m"
        self.__n        = "n"
        self.__hop      = "hop"
        self.__cost     = "cost"
        self.__capacity = "capacity"
        self.__start    = "start"
        self.__target   = "target"
        self.__DK       = "DK"

    def __get_attr1(self, param):
        """
        parameter dk, m, n
        returns:
        * dk、m、またはnの値
        """
        matched = re.search(self.attr_regexp[param], self.all_lines)
        return int(matched.group(1))

    def read_params(self, param, func):
        """
        paramに対応するattr_regexpの正規表現でall_linesを分割した文字列linesを得る
        linesをセミコロンが出現するまで読み込み、各行にfuncを適応するジェネレータ

        arguments:
        * param(string)
          key of attr_regexp
        * func(lambda)

        yields:
         * func(params)
           funcを適応したparams
        """
        _, lines = re.split(self.attr_regexp[param], self.all_lines)
        lines = lines.strip()
        for line in lines.splitlines():
            if line.startswith(";"): break
            line = line.strip()
            params = re.split(r"\s+", line)
            yield func(params)

    def __get_attr2(self, param):
        """
        parameter capacity, cost, hop
        returns:
        * タプル(i,j,attr)を要素とするリスト
        """
        matched = [params for params in\
                   self.read_params(param,lambda params: (int(params[0]),
                                                          int(params[1]),
                                                          float(params[2])))]
        return matched

    def __get_attr3(self, start, target):
        """
        parameter traffic
        returns:
        * タプル(i,j)を要素とするリスト
        """
        start_nodes = [node for node in\
                       self.read_params(start, lambda node: int(node[1]))]
        target_nodes = [node for node in\
                        self.read_params(target, lambda node: int(node[1]))]
        traffic = [(start_nodes[i], target_nodes[i]) for i in range(len(start_nodes))]
        return traffic

    def __get_attr4(self, param):
        """
        parameter DK
        returns:
        * リスト
        """
        DK = [d for d in self.read_params(param, lambda d: float(d[1]))]
        return DK

    @property
    def dk(self):
        return self.__get_attr1(self.__dk)

    @property
    def m(self):
        return self.__get_attr1(self.__m)

    @property
    def n(self):
        return self.__get_attr1(self.__n)

    @property
    def cost(self):
        return self.__get_attr2(self.__cost)

    @property
    def capacity(self):
        return self.__get_attr2(self.__capacity)

    @property
    def hop(self):
        return self.__get_attr2(self.__hop)

    @property
    def traffic(self):
        return self.__get_attr3(self.__start, self.__target)

    @property
    def DK(self):
        return self.__get_attr4(self.__DK)
