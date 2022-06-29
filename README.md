## Statistical data set

The UK Land Registry publishes open data on real estate transactions on [gov.uk](https://www.gov.uk/).  The datasets are publsihed in txt and csv formats but their size can make them difficult to work with. 

So I've got the huge .csv file -> `pp-complete.csv`

You may download it [here](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#:~:text=(TXT%2C%2017.9MB)-,Single%20file,-These%20include%20standard). 
Done? Now you see that each line contains an information about property in the following form:
```
{F887F88E-7D15-4415-804E-52EAC2F10958},"70000","1995-07-07 00:00","MK15 9HP","D","N","F","31","","ALDRICH DRIVE","WILLEN","MILTON KEYNES","MILTON KEYNES","MILTON KEYNES","A","A"
```
Here is an [explanations of column headers](https://www.gov.uk/guidance/about-the-price-paid-data#explanations-of-column-headers-in-the-ppd:~:text=30%20September%202015.-,Explanations%20of%20column%20headers%20in%20the%20PPD,-The%20data%20is).

## Purpose
The purpose is to find all properties that has been sold two or more times, and write the result to a separate file.
