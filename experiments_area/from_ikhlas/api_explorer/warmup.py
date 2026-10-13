#List comprehension practice 
list_of_odd_nums = [n for n in range(1,20) if n % 2 != 0]
print(list_of_odd_nums)


#List comprehension practice with if else in one line
list_of_ch_contain = [ch if ch[0] == 'a' else "N/A" for ch in ["apple", "orange", "banana", "cherry"]]
print(list_of_ch_contain)


#Dictionary comprehension practice 
dic_of_names = {names: len(names)for names in ["Ikhlas", "Sara", "wed"]}
print(dic_of_names)