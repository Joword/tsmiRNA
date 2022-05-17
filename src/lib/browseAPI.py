from src.db.TissueSpecificTable import *
from flask import request
from json import dumps
from datetime import datetime


def get_parameter(label, default=None):
    tem = request.args.get(label)
    
    if tem is None:
        return default
    return tem.strip()


class Ajax:
    
    def __init__(self, table, columns, orderable=None):
        self.table = table
        self.columns = columns
        if orderable is None:
            self.orderable = columns
        else:
            self.orderable = orderable
    
    def _set_search_(self, condition=None):
        u"""
        设置搜索框的搜索条件
        """
        term = get_parameter("search[value]", None)
        
        if not term:
            return condition
        
        searchCondition = None
        for i in self.columns:
            if isinstance(i, TextField):
                if searchCondition is None:
                    searchCondition = (i.contains(term))
                else:
                    searchCondition = searchCondition | (i.contains(term))
        
        if condition:
            return condition & searchCondition
        return searchCondition
    
    def _set_order_(self):
        u"""
        设置排序顺序
        """
        order_by = int(get_parameter("order[0][column]", 0))
        order_by = self.orderable[order_by]
        order_dir = get_parameter("order[0][dir]")
        
        if order_dir == "desc":
            return order_by.desc()
        return order_by
    
    def query_(self, condition=None, all=False):
        u"""
        查询
        """
        query = self.table.select(*self.columns)
        # 设置查询条件
        condition = self._set_search_(condition)
        
        if condition:
            query = query.where(condition)
        
        query = query.order_by(self._set_order_()).distinct()
        # print(query.sql)
        total = query.count()
        
        draw = get_parameter("draw", 1)
        per_page = int(get_parameter("length", 10))
        page = int(get_parameter("start", 0)) // per_page
        
        if all == False:
            data = query.paginate(page, per_page)
        else:
            data = query
        
        data = [x for x in data.dicts()]
        
        return {
            "data": data,
            "draw": draw,
            "start": page,
            "length": per_page,
            "recordsTotal": total,
            "recordsFiltered": total
        }
