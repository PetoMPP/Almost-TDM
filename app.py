import win32com.client as win32

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = "pietrzyk.p@axito.pl"
mail.Subject = "Problem/Sugestia dotycząca programu Almost TDM"
mail.Display(True)