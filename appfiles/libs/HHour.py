from datetime import datetime

def HeureDate(Separator=" "):
	Heure=str(datetime.now())
	FormatedHeureDate=Heure[0:-7].replace("-",Separator)
	return FormatedHeureDate

def Heure(Separator = ":"):
	Heure=str(datetime.now())
	FormatedTotalHeure=Heure[11:-7].replace(":",Separator)
	return FormatedTotalHeure

def HeureOnly():
	Heure=str(datetime.now())
	FormatedHeure=Heure[11:-13]
	return FormatedHeure

def MinutesOnly():
	Heure=str(datetime.now())
	FormatedMinutes=Heure[14:-10]
	return FormatedMinutes

def SecondesOnly():
	Heure=str(datetime.now())
	FormatedSecondes=Heure[17:-7]
	return FormatedSecondes

def Secconds():
	return str(datetime.now())[1:2] # TODO

