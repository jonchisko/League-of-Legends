
import ReadData
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


dataObject = ReadData.ReadData("data", "kills", read=False)

dfKill = dataObject.returnDataFrame("kills")

print("Head")
print(dfKill.head())
print("st vrstic:",dfKill.shape[0])
print(dfKill.columns)
#selektaj ce so kaksni nan
print(dfKill.x_pos.value_counts()[:2])
print(dfKill.y_pos.value_counts()[:2])
selekcija1 = np.logical_or(dfKill.x_pos.isnull(), dfKill.y_pos.isnull()) #kjer je either one nan
selekcija2 = np.logical_or(dfKill.y_pos == "TooEarly", dfKill.x_pos == "TooEarly")
print("Toliko vrstic je neuporabnih", dfKill.loc[np.logical_or(selekcija1, selekcija2), :].shape[0])
dfKill = dfKill.loc[np.logical_not(np.logical_or(selekcija1, selekcija2)), :]

print("Modri uboji, rdeci uboji:\n", dfKill.Team.value_counts())
print("Sum", dfKill.Team.value_counts().sum())

#diskredetirajmo x pos in y pos ter narisimo kvadratni heatmap

x_pos = dfKill.x_pos.apply(float)
y_pos = dfKill.y_pos.apply(float)
print("X")
print("std", np.std(x_pos), "mean", np.mean(x_pos), "min", np.min(x_pos), "max", np.max(x_pos))
print("Y")
print("std", np.std(y_pos), "mean", np.mean(y_pos), "min", np.min(y_pos), "max", np.max(y_pos))



#Koliko kvadratkov hočemo?
#recimo da gre mapa od 0 do 15 000
stKvadratkov = 400

velikostKvadratka = 15000/stKvadratkov

velikostSlike = stKvadratkov
slika1 = np.zeros((velikostSlike,velikostSlike))
slika2 = np.zeros((velikostSlike,velikostSlike))

for i,coord in enumerate(zip(x_pos,y_pos)):
    x, y = coord
    xK = int(x // velikostKvadratka)
    yK = int(y // velikostKvadratka)
    slika1[xK, (stKvadratkov-1) - yK] += 1 #da invertam po y
    if dfKill.iloc[i, 1] == "bKills":
        slika2[xK, (stKvadratkov-1) - yK] -=1
    else:
        slika2[xK, (stKvadratkov-1) - yK] +=1

fig = plt.figure(figsize=(40,40))
print("Minimalna vrednost:", slika2.min())
print("Maksimalna vrednost:", slika2.max())
print("Mediana:", np.median(slika2))
print("Mean:", slika2.mean())
ax = fig.add_axes([0, 0, 1, 1])
im = ax.imshow(slika2.T, cmap="magma")  #se po diagonali, da dobim korektno obrnjeno
fig.colorbar(im)
plt.savefig("ubojiEkipa.png", dpi=200)
im = ax.imshow(slika1.T, cmap="magma")
plt.savefig("uboji.png", dpi=200)
#plt.show()


print("Videli smo, da se število ubojev po ekipi razlikuje:\n", dfKill.Team.value_counts())

print("Vzamemo po igrah in poglejmo distribucijo modre ekipe stevila ubojev in rdece!")

grupiranoIgra = dfKill.groupby("Address") #grupiramo po igrah
modri = []
rdeci = []

for x, data in grupiranoIgra:
    modri.append(sum(data["Team"]=="bKills"))
    rdeci.append(sum(data["Team"]=="rKills"))

#Narisi distribucijo :)

fig = plt.figure(figsize=(40,40))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212, sharex=ax1)
ax1.hist(modri, bins=len(modri)//300, color="blue", alpha=0.8)
ax1.axvline(np.mean(modri), color="cyan")
ax1.annotate("povprecje %.2f" % np.mean(modri), xy=(np.mean(modri), 50), xytext=(30,222), arrowprops=dict(facecolor="black", shrink=0.05, alpha=0.6),)
ax2.hist(rdeci, bins=len(modri)//300, color="red", alpha=0.8)
ax2.axvline(np.mean(rdeci), color="cyan")
ax2.annotate("povprecje %.2f" % np.mean(rdeci), xy=(np.mean(rdeci), 50), xytext=(30,222), arrowprops=dict(facecolor="black", shrink=0.05, alpha=0.6),)
ax1.set_title("Distribucija ubojev modrih na igro")
ax2.set_title("Distribucija ubojev rdecih na igro")
ax1.set_xlabel("Stevilo smrti")
ax1.set_ylabel("Koliko primerov")
ax2.set_xlabel("Stevilo smrti")
ax2.set_ylabel("Koliko primerov")
fig.savefig("distribucija.png", dpi=200)
#plt.show()

print("Povprecje modri", np.mean(modri))
print("Povprecje rdeci", np.mean(rdeci))


print("H0 je, da sta povprečji enaki! Torej mean modrih je enak meanu rdečih. d = 0")
print("Ha je, da sta povprečji različni, torej mean modrih je različen od meana rdečih.")

from scipy.stats import stats

res = stats.ttest_ind(modri, rdeci, equal_var=False)
print("signif level 0.05")
print("Rezultat, p value =",res[1])
print("P value je skoraj nič, kar pomeni, da je šansa, da bi videli dve distribuciji iz kao iste populacije tako narazen skoraj ničta.\n"+
      "Ker je p value manjši od našega nastavga 0.05, ne moremo sprejeti H0.")




#Še ena vizualizacija
#Nariši uboje na krožnico, kot je čas, velikost je število ubojev ob tem času

#diskretiziraj čas :p

#0 time v 0pi in max time v 2pi
#čas/maks čas * 2pi

grupirano = dfKill.groupby("Team")
timeBlue=[]
timeRed=[]

for c, x in grupirano:
    if c == "rKills":
        timeRed = x["Time"]
    else:
        timeBlue = x["Time"]



timeWindow = 1 #1min
timeBlue = timeBlue//timeWindow
timeRed = timeRed//timeWindow

timeAll = timeBlue.append(timeRed, ignore_index=True)
timeAll = timeAll.value_counts()

fig = plt.figure(figsize=(40,40))
ax = fig.add_subplot(111, polar=True)

maxTime = max(timeAll.index)
kot = timeAll.index/maxTime * 2*np.pi
ax.set_title("Uboji razporejeni po času")
ax.bar(kot, timeAll, color="greenyellow", alpha=0.6, label="Obe ekipi")
tb = timeBlue.value_counts()
tr = timeRed.value_counts()
ax.bar(tb.index/max(tb.index) * 2*np.pi, tb, color="blue", alpha=0.7, label="Modra")
ax.bar(tr.index/max(tr.index) * 2*np.pi, tr, color="red", alpha=0.7, label="Rdeči")

#da bo uniformno koti
casKot = np.arange(0, maxTime, 5)/maxTime * 2*np.pi
ax.set_xticks(casKot) #treba dat kot
ax.set_xticklabels(np.arange(0, maxTime, 5))
ax.legend(loc=1)
fig.savefig("ubojiCas", dpi=200)
plt.show()




