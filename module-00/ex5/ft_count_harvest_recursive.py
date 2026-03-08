def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def helper(day):
        if day <= days:
            print("Day", day)
            helper(day + 1)
        else: 
            print("Harvest time!")
            return
    helper(1)