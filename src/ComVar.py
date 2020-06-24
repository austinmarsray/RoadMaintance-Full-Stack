import pyodbc

conn = pyodbc.connect(DSN='SQL',UID='sa',pwd='5202020l')
Tokens = ["LHX123"]

_RoadType_ = {1:"沥青路", 0:"水泥路"}
_SurfaceLevel_ = {1:"高级", 2:"次高级", 3:"中级", 4:"低级"}
_RoadLevel_ = {1:"快速路", 2:"主干路", 3:"次干路", 4:"支路"}
_TranLevel_ = {1:"特轻", 2:"轻", 3:"中", 4:"重", 5:"特重"}
_InnerType_ = {1:"柔性基层", 2:"半刚性基层", 3:"刚性基层", 4:"复合式基层"}
_ConservationLevel_ = {1:"1等养护道路", 2:"2等养护道路", 3:"3等养护道路"}

R_RoadType_ = {"沥青路":1, "水泥路":0}
R_SurfaceLevel_ = {"高级":1, "次高级":2, "中级":3, "低级":4}
R_RoadLevel_ = {"快速路":1, "主干路":2, "次干路":3, "支路":4}
R_TranLevel_ = {"特轻":1, "轻":2, "中":3, "重":4, "特重":5}
R_InnerType_ = {"柔性基层":1, "半刚性基层":2, "刚性基层":3, "复合式基层":4}
R_ConservationLevel_ = {"1等养护道路":1, "2等养护道路":2, "3等养护道路":3}


Warning_List = []