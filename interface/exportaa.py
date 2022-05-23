import xlrd
import xlsxwriter
import tkinter as tk
from tkinter import filedialog


def export(corrente,cutil, variadt, yplot, custoop, custocapital, custocapitalanual, custotot,uf,uq,maindt,akt, ajustado, cpf, cpq, areak, deltalmnk):

    myw=tk.Tk()
    myw.withdraw()

    file = filedialog.asksaveasfilename(
        filetypes=[("Excel files", ".xlsx")],
        defaultextension=".xlsx")

    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    worksheet2 = workbook.add_worksheet("Graphs")

    worksheet.set_column(9,10, 15)
    worksheet.set_column(11,11, 24)
    worksheet.set_column(12,12, 13)
    worksheet.set_column(15,16, 11)
    format1=workbook.add_format({'bg_color':'#8db4e2','border':2,'align':'center','valign':'vcenter','bold':True})
    format2=workbook.add_format({'border':1,'align':'center','valign':'vcenter','bold':True})
    #data2 input das correntes

    Data1=['Stream','Tin','Tout','CP','Type','h']
    Data2=corrente
    Dataut=cutil
    row=2
    col=0

    for TE,TS,C,T,H in Data2:
        worksheet.write_number(row, col,row-1,format2)
        worksheet.write_number(row, col+1, TE,format2)
        worksheet.write_number(row, col+2,TS,format2)
        worksheet.write_number(row, col+3,C,format2)
        worksheet.write_string(row, col+4,T,format2)
        worksheet.write_number(row, col+5,H,format2)
        row+=1

    k=row
    worksheet.merge_range('A1:F1', 'Streams', format1)
    worksheet.write_row('A2', Data1, format1)
    row += 2
    worksheet.merge_range('A' + str(row) + ':F' + str(row), 'Utility', format1)
    for TE,TS,C,T,H in Dataut:
        worksheet.write_number(row, col,k-1,format2)
        worksheet.write_number(row, col+1, TE,format2)
        worksheet.write_number(row, col+2,TS,format2)
        worksheet.write_number(row, col+3,C,format2)
        worksheet.write_string(row, col+4,T,format2)
        worksheet.write_number(row, col+5,H,format2)
        k+=1
        row+=1


    Datass = ['ΔTmin', 'Area', 'Operating Cost', 'Capital Cost', 'Annualized Capital Cost', 'Total Cost']

    Data3=variadt
    Data33=yplot
    Data4=custoop
    Data5=custocapital
    Data6=custotot
    Data7=custocapitalanual
    print(Data7)
    worksheet.write_column('H2', Data3,format2)
    worksheet.write_column('I2', Data33,format2)
    worksheet.write_column('J2', Data4,format2)
    worksheet.write_column('K2', Data5,format2)
    worksheet.write_column('L2', Data7,format2)
    worksheet.write_column('M2', Data6,format2)
    worksheet.write_row('H1', Datass, format1)

    Datass = ['ΔTmin', 'Hot Utility', 'ColdUtility']

    Datauf=uf
    Datauq=uq

    worksheet.write_column('O2', Data3,format2)
    worksheet.write_column('P2', Datauq,format2)
    worksheet.write_column('Q2', Datauf,format2)
    worksheet.write_row('O1', Datass, format1)

    row=2
    Datass = ["T Hot (In)","T Hot (Out)","T Cold (In)","T Cold (Out)","CP (Hot)", "CP (Cold)","MLDT","Area"]
    worksheet.write_row('S2', Datass, format1)
    worksheet.merge_range('S1:Z1', "ΔTmin : "+ str(round(maindt,2)), format1)
    worksheet.set_column(24,24, 11)
    col=18
    for data in range(0, len(areak)):
        worksheet.write_number(row, col,ajustado[0][data],format2)
        worksheet.write_number(row, col+1,ajustado[0][data+1],format2)
        worksheet.write_number(row, col+2,ajustado[1][data],format2)
        worksheet.write_number(row, col+3,ajustado[1][data+1],format2)
        worksheet.write_number(row, col+4,cpq[data],format2)
        worksheet.write_number(row, col+5,cpf[data],format2)
        worksheet.write_number(row, col+6,deltalmnk[data],format2)
        worksheet.write_number(row, col+7,areak[data],format2)
        row+=1
    worksheet.write_string(row, col+6,"Total Area",format1)
    worksheet.write_number(row, col+7,akt,format2)

    chart1 = workbook.add_chart({'type': 'line'})


    chart1.add_series({'categories': '=Sheet1!$H$1:$H$10',
                       'categories': ['Sheet1', 1, 7, len(variadt), 7],
                       'values':     ['Sheet1', 1, 9, len(variadt), 9],
                       'line': {
                           'color': 'blue'
                       },
    })

    chart1.add_series({'categories': ['Sheet1', 1, 6, len(variadt), 6],
                       'values':     ['Sheet1', 1, 11,len(variadt), 11],
                       'line': {
                           'color': 'black'
                       },
    })

    chart1.add_series({'categories': ['Sheet1', 1, 6, len(variadt), 6],
                       'values':     ['Sheet1', 1, 12,len(variadt), 12],
                       'line': {
                           'color': 'red'
                       },
    })

    chart1.set_title({'name': 'Cost x Dtmin'})

    # Add x-axis label
    chart1.set_x_axis({'name': 'Dtmin'})

    # Add y-axis label
    chart1.set_y_axis({'name': 'Cost'})


    worksheet2.insert_chart('B5', chart1)

    ########################################
    chart2 = workbook.add_chart({'type': 'scatter'})

    chart2.add_series({'categories': '=Sheet1!$H$1:$H$10',
                       'categories': ['Sheet1', 1, 7, len(variadt), 7],
                       'values': ['Sheet1', 1, 8, len(variadt), 8],
                       })



    chart2.set_title({'name': 'Area x Dtmin'})

    # Add x-axis label
    chart2.set_x_axis({'name': 'Dtmin'})

    # Add y-axis label
    chart2.set_y_axis({'name': 'Area'})

    worksheet2.insert_chart('J5', chart2)
###########################################################
    chart3 = workbook.add_chart({'type': 'line'})

    chart3.add_series({
                       'categories': ['Sheet1', 1, 14, len(variadt), 14],
                       'values': ['Sheet1', 1, 16, len(variadt), 16],
                       })

    chart3.add_series({
                       'categories': ['Sheet1', 1, 14, len(variadt), 14],
                       'values': ['Sheet1', 1, 15, len(variadt), 15],
                       })




    chart3.set_title({'name': 'Utility x Dtmin'})

    # Add x-axis label
    chart3.set_x_axis({'name': 'Dtmin'})

    # Add y-axis label
    chart3.set_y_axis({'name': 'Utility'})


    worksheet2.insert_chart('R5', chart3)
###########################################################


    workbook.close()