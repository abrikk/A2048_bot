from aiogram import types, Dispatcher
from aiogram.utils.markdown import hcode


async def test(message: types.Message):
    print(message.photo[-1].file_id)


def int_to_roman(num: int) -> str:
    m = ["", "M", "MM", "MMM", "Mↁ", "ↁ", "ↁM", "ↁMM", "ↁMMM", "Mↂ",
         "ↂ", "ↂM", "ↂMM", "ↂMMM", "ↂMↁ", "ↂↁ", "ↂↁM", "ↂↁMM", "ↂↁMMM", "ↂMↂ", "ↂↂ",
         "ↂↂM", "ↂↂMM", "ↂↂMMM", "ↂↂMↁ", "ↂↂↁ", "ↂↂↁM", "ↂↂↁMM", "ↂↂↁMMM", "ↂↂMↂ", "ↂↂↂ",
         "ↂↂↂM", "ↂↂↂMM", "ↂↂↂMMM", "ↂↂↂMↁ", "ↂↂↂↁ", "ↂↂↂↁM", "ↂↂↂↁMM", "ↂↂↂↁMMM", "ↂↂↂMↂ", "ↂↇ",
         "ↂↇM", "ↂↇMM", "ↂↇMMM", "ↂↇMↁ", "ↂↇↁ", "ↂↇↁM", "ↂↇↁMM", "ↂↇↁMMM", "ↂↇMↂ", "ↇ",
         "ↇM", "ↇMM", "ↇMMM", "ↇMↁ", "ↇↁ", "ↇↁM", "ↇↁMM", "ↇↁMMM", "ↇMↂ", "ↇↂ",
         "ↇↂM", "ↇↂMM", "ↇↂMMM", "ↇↂMↁ", "ↇↂↁ", "ↇↂↁM", "ↇↂↁMM", "ↇↂↁMMM", "ↇↂMↂ", "ↇↂↂ"]
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = (thousands + hundreds + tens + ones)

    return ans

