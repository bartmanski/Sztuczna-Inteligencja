

# blotkarzowe obliczenia

B_Poker = 5 * 4
B_Kareta = 9 * 32
B_Full = 9 * 4 * 8 * 6
B_kolor = 2 * 7 * 9 * 4 - 5 * 4
B_strit = 5 * 4 * 4 * 4 * 4 * 4 - 5 * 4
B_trojka = 9 * 4 * 28 * 16
B_dwie_pary = 36 * 6 * 6 * 7 * 4
B_para = 9 * 6 * 56 * 4 * 4 * 4
B_hc = 376992 - B_Poker - B_Kareta - B_Full - B_kolor - B_strit - B_trojka - B_dwie_pary - B_para
print(B_Poker, B_Kareta, B_Full, B_kolor, B_strit, B_trojka, B_dwie_pary, B_para, B_hc)

F_Kareta = 4 * 12
F_Full = 4 * 4 * 3 * 6
F_trojka = 4 * 4 * 3 * 4 * 4
F_dwie_pary = 6 * 6 * 6 * 2 * 4
F_para = 4 * 6 * 4 * 4 * 4

wygrane_Pokerem = B_Poker * (F_Kareta + F_Full + F_trojka + F_dwie_pary + F_para)
wygrane_Kareta = B_Kareta * (F_Full + F_trojka + F_dwie_pary + F_para)
wygrane_Full = B_Full * (F_trojka + F_dwie_pary + F_para)
wygrane_kolor = B_kolor * (F_trojka + F_dwie_pary + F_para)
wygrane_strit = B_strit * (F_trojka + F_dwie_pary + F_para)
wygrane_trojka = B_trojka * (F_dwie_pary + F_para)
wygrane_dwie_pary = B_dwie_pary * F_para

wygrane = wygrane_Pokerem + wygrane_Kareta + wygrane_Full + wygrane_kolor + wygrane_strit + wygrane_trojka + wygrane_dwie_pary
# 36 po 5 * 16 po 5
wszystkie = 4 * 11 * 17 * 7 * 36  *  13 * 14 * 3 * 16
print(wygrane, wszystkie, wygrane / wszystkie)