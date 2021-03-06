
chinese_number_dict = {'一':1, '七':7, '萬':10000, '三':3, '九':9,'兩':2, '二':2, '五':5, '八':8, '六':6, '十':10,'三':3, '千':1000, '四':4, '百':100, '零':0,"億":100000000}
not_in_decimal = "十百千萬億點"
def ch2num(chstr):
    if '點' not in chstr:
        return ch2round(chstr)
    splits = chstr.split("點")
    if len(splits) != 2:
        return splits
    rount = ch2round(splits[0])
    decimal = ch2decimal(splits[-1])
    if rount is not None and decimal is not None:
        return float(str(rount) + "." + str(decimal))
    else:
        return None

def ch2round(chstr):
    no_op = True
    if len(chstr) >= 2:
        for i in chstr:
            if i in not_in_decimal:
                no_op = False
    else:
        no_op = False
    if no_op:
        return ch2decimal(chstr)

    result = 0
    now_base = 1
    big_base = 1
    big_big_base = 1
    base_set = set()
    chstr = chstr[::-1]
    for i in chstr:
        if i not in chinese_number_dict:
            return None
        if chinese_number_dict[i] >= 10:
            if chinese_number_dict[i] > now_base:
                now_base = chinese_number_dict[i]
            elif now_base >= chinese_number_dict["萬"] and now_base < chinese_number_dict["億"] and chinese_number_dict[i] > big_base:
                now_base = chinese_number_dict[i] * chinese_number_dict["萬"]
                big_base = chinese_number_dict[i]
            elif now_base >= chinese_number_dict["億"] and chinese_number_dict[i] > big_big_base:
                now_base = chinese_number_dict[i] * chinese_number_dict["億"]
                big_big_base = chinese_number_dict[i]
            else:
                return None
        else:
            if now_base in base_set and chinese_number_dict[i] != 0:
                return None
            result = result + now_base * chinese_number_dict[i]
            base_set.add(now_base)
    if now_base not in base_set:
        result = result + now_base * 1
    return result

def ch2decimal(chstr):
    result = ""
    for i in chstr:
        if i in not_in_decimal:
            return None
        if i not in chinese_number_dict:
            return None
        result = result + str(chinese_number_dict[i])
    return int(result)
