from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import pymysql
from PyQt5.uic import loadUiType
import re
import datetime

ui,_ = loadUiType('library.ui')
login,_ = loadUiType('login.ui')

class Login(QMainWindow, login):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
        self.pushButton_2.clicked.connect(self.Handel_Exit)

    def Handel_Login(self):
        username    = self.lineEdit.text()
        password    = self.lineEdit_2.text()

        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        sql = ''' SELECT * FROM users '''

        self.cur.execute(sql)
        data            = self.cur.fetchall()

        for row in data:
            if username == row[1] and password == row[4]:
                self.window2    = MainApp()
                self.close()
                self.window2.show()
            else:
                self.label_3.setText('             Make sure that you have entered your username and password correctly.')
    
    def Handel_Exit(self):
        self.close()

class MainApp(QMainWindow , ui):

    def email_validity_check(self, email_address):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if(re.fullmatch(regex, email_address)):
            return True
        else:
            return False

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_buttons()

        self.Show_All_Books()
        self.Show_Category()
        self.Show_Category_Combo()

        self.Show_Day_To_Day_Table()

    def Handel_UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def Handel_buttons(self):
        self.pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Members_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_5.clicked.connect(self.ClearDayToDay)
        self.pushButton_6.clicked.connect(self.Rent_and_Return)
        self.pushButton_13.clicked.connect(self.Check_Book_Avaibality)
        self.pushButton_9.clicked.connect(self.Search_Your_Books)

        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_28.clicked.connect(self.ClearEnterBook)
        self.pushButton_27.clicked.connect(self.ClearUpdateAndDeleteBook)
        self.pushButton_11.clicked.connect(self.Search_Books)
        self.pushButton_10.clicked.connect(self.Update_Books)
        self.pushButton_12.clicked.connect(self.Delete_Books)

        self.pushButton_8.clicked.connect(self.Issuse_Membership)
        self.pushButton_14.clicked.connect(self.Search_Membership)
        self.pushButton_15.clicked.connect(self.Update_Membership)
        self.pushButton_16.clicked.connect(self.Delete_Memberships)
        self.pushButton_23.clicked.connect(self.ClearEnterMembership)

        self.pushButton_24.clicked.connect(self.ClearCatageories)
        self.pushButton_17.clicked.connect(self.Add_Category)
        self.pushButton_18.clicked.connect(self.Remove_Category)

        self.pushButton_25.clicked.connect(self.ClearAddStaff)
        self.pushButton_26.clicked.connect(self.ClearDeleteStaff)
        self.pushButton_22.clicked.connect(self.Add_Staff)
        self.pushButton_19.clicked.connect(self.Staff_View)
        self.pushButton_20.clicked.connect(self.Staff_Update)
        self.pushButton_21.clicked.connect(self.Staff_Delete)


    ################################################################
    #############Opening Tabs#######################################

    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Members_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    ################################################################
    #############Dat to Day#########################################
    def Rent_and_Return(self):
        self.label_52.setText('')
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        book_code       = self.lineEdit.text()
        member_regno    = self.lineEdit_2.text()
        process_type    = self.comboBox_3.currentText()

        self.cur.execute('''
            SELECT book_code, available FROM book where book_code=%s
        ''', (book_code))
        data_1          = self.cur.fetchall()
        data_1_length   = len(data_1)
        if data_1_length == 0:
            book_checker = False
        else:
            book_checker = True
            book_avaibality  = data_1[0][1]

        self.cur.execute('''
            SELECT mem_regno,numbers_book FROM members where mem_regno=%s
        ''', (member_regno))
        data_2          = self.cur.fetchall()
        data_2_length   = len(data_2)
        if data_2_length == 0:
            code_checker = False
        else:
            code_checker = True
            no_of_books_taken_by_users = data_2[0][1]
        
        if book_checker:
            if code_checker:
                if process_type=='Rent':
                    if book_avaibality=='True':
                        if no_of_books_taken_by_users < 10 and no_of_books_taken_by_users>=0:

                            self.lineEdit_40.setValidator(QIntValidator())
                            days            = int(self.lineEdit_40.text())
                            if days <= 60 and days >0:
                                
                                rented_date     = str(datetime.date.today())
                                return_date     = str(datetime.date.today()  + datetime.timedelta(days=days))
                                sql = '''
                                  INSERT INTO dayoperations (renter_regno, rented_bookcode, type, days, rented_date, return_date)
                                  VALUES
                                  (%s, %s, %s, %s, %s, %s)
                                    '''
                                values = (member_regno, book_code, process_type, days, rented_date, return_date)
                                self.cur.execute(sql, values)
                                self.db.commit()
                                
                                sql = '''
                                  UPDATE book SET available='False' WHERE book_code=%s
                                  '''
                                value  = book_code
                                self.cur.execute(sql,value)
                                self.db.commit()
                                    
                                sql = '''
                                      UPDATE members SET numbers_book=numbers_book+1 WHERE mem_regno=%s
                                      '''
                                value  = member_regno
                                self.cur.execute(sql,value)
                                self.db.commit()

                                self.lineEdit.setText('')
                                self.lineEdit_2.setText('')
                                self.lineEdit_40.setText('')

                                self.statusBar().showMessage('The operation was completed.')
                                self.Show_Day_To_Day_Table()
                            elif days < 0:
                                self.label_52.setText('The minimum you can rent is for 1 day.')
                            else:
                                self.label_52.setText('The maximum you can rent is for 30 days.')
                        else:
                            self.label_52.setText('The member has already rented 10 books.')
                    else:
                        self.label_52.setText('The book with this code is already rented.')

                else:
                    if no_of_books_taken_by_users==0:
                        self.label_52.setText('The member has no book in his posession.')
                    else:
                        sql = '''
                              DELETE from dayoperations WHERE rented_bookcode=%s
                            '''
                        values = (book_code)
                        self.cur.execute(sql, values)
                        self.db.commit()
                            
                        sql = '''
                              UPDATE book SET available='True' WHERE book_code=%s
                              '''
                        value  = book_code
                        self.cur.execute(sql,value)
                        self.db.commit()

                        sql = '''
                              UPDATE members SET numbers_book=numbers_book-1 WHERE mem_regno=%s
                              '''
                        value  = member_regno
                        self.cur.execute(sql,value)
                        self.db.commit()

                        self.lineEdit.setText('')
                        self.lineEdit_2.setText('')

                        self.statusBar().showMessage('The operation was completed')
                        self.Show_Day_To_Day_Table()
            else:
                self.label_52.setText('The member with code '+ member_regno+ ' wasnot found.')
        else:
            self.label_52.setText('The book with code '+ book_code + ' wasnot found.')

                
    def Check_Book_Avaibality(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        self.label_52.setText('')
        book_name       = self.lineEdit_5.text()

        value           = book_name
        sql             = f'''
                          SELECT book_code, book_name, available FROM book WHERE book_name LIKE '%{value}%'
                          '''
        
        self.cur.execute(sql)
        data          = self.cur.fetchall()      
        length        = len(data)

        if length !=0:
            if data:
                self.tableWidget_3.setRowCount(0)
                self.tableWidget_3.insertRow(0)
                for row, form in enumerate(data):
                    for column, item in enumerate(form):
                        self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1

                    row_position    = self.tableWidget_3.rowCount()
                    self.tableWidget_3.insertRow(row_position)
        else:
            self.label_52.setText('No such book in our record.')
            self.tableWidget_3.clearContents()


    def Show_Day_To_Day_Table(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        sql             = '''
                          SELECT renter_regno, rented_bookcode, type, days, rented_date, return_date from dayoperations
                          '''
        self.cur.execute(sql)
        data          = self.cur.fetchall()

        if data:
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position    = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
        else:
            self.tableWidget.clearContents()

    def Search_Your_Books(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        mem_regno       = self.lineEdit_6.text()

        sql             = '''
                          SELECT rented_bookcode, return_date FROM dayoperations WHERE renter_regno=%s
                          '''
        values          = mem_regno
        self.cur.execute(sql, values)
        data            = self.cur.fetchall()

        length          = len(data)

        if length !=0 :
            if data:
                self.tableWidget_4.setRowCount(0)
                self.tableWidget_4.insertRow(0)
                for row, form in enumerate(data):
                    for column, item in enumerate(form):
                        self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1

                    row_position    = self.tableWidget_4.rowCount()
                    self.tableWidget_4.insertRow(row_position)
        else:
            self.tableWidget_4.clearContents()

    def ClearDayToDay(self):
        self.lineEdit_2.setText('')
        self.lineEdit.setText('')
        self.lineEdit_40.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')

    ################################################################
    #############Books##############################################

    def ClearEnterBook(self):
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_9.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.plainTextEdit.setPlainText('')

    def ClearUpdateAndDeleteBook(self):
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_15.setText('')
        self.label_51.setText('')
        self.label_52.setText('')
        self.plainTextEdit_2.setPlainText('')

    def Add_New_Book(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        book_title      = self.lineEdit_4.text()
        book_code       = self.lineEdit_3.text()
        book_category   = self.comboBox.currentText()
        book_price      = self.lineEdit_9.text()
        book_author     = self.lineEdit_7.text()
        book_publisher  = self.lineEdit_8.text()  
        book_description= self.plainTextEdit.toPlainText()

        self.cur.execute('''
            SELECT book_code FROM book where book_code=%s
        ''', (book_code))
        data            = self.cur.fetchall()

        number_data     = len(data)

        if number_data==0:
            self.cur.execute('''
                INSERT INTO book (book_name, book_code, book_description, book_price, book_author, book_publisher, book_catageory) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (book_title, book_code, book_description, book_price, book_author, book_publisher, book_category))

            self.db.commit()
            self.statusBar().showMessage('New book '+ book_title +' added ') 
            self.lineEdit_4.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_9.setText('')
            self.lineEdit_8.setText('')
            self.lineEdit_7.setText('')
            self.plainTextEdit.setPlainText('')
        else:
            self.label_50.setText('The book with same code already exists.')

        self.Show_All_Books()

    def Search_Books(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()
        self.label_51.setText('')

        book_code       = self.lineEdit_11.text()
        self.cur.execute('''
            SELECT * FROM book where book_code=%s
        ''', (book_code))
        data            = self.cur.fetchall()

        number_data     = len(data)
        
        if number_data==0:
            self.label_51.setText('The book of given code not found.')
            self.lineEdit_15.setText('')
            self.lineEdit_10.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_14.setText('')
            self.lineEdit_12.setText('')
            self.plainTextEdit_2.setPlainText('')
        else:
            for row in data:
                self.lineEdit_15.setText(row[1])
                self.lineEdit_10.setText(row[2])
                self.lineEdit_10.setDisabled(True)
                self.lineEdit_13.setText(row[4])
                self.lineEdit_14.setText(row[5])
                self.lineEdit_12.setText(row[6])
                self.plainTextEdit_2.setPlainText(row[3])
                self.comboBox_2.setCurrentText(row[7])

    def Show_All_Books(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        sql_qurey       = '''
                            SELECT book_name, book_code, book_author, book_catageory, book_price, book_publisher, available FROM book 
                          '''  
        self.cur.execute(sql_qurey)
        data            = self.cur.fetchall()   

        if data :
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position    = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)

    def Update_Books(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        book_name       = self.lineEdit_15.text()
        book_code       = self.lineEdit_11.text()
        book_description= self.plainTextEdit_2.toPlainText()
        book_category   = self.comboBox_2.currentText()
        book_price      = self.lineEdit_13.text()
        book_author     = self.lineEdit_14.text()
        book_publisher  = self.lineEdit_12.text()

        self.cur.execute('''
            SELECT * FROM book where book_code=%s
        ''', (book_code))
        data            = self.cur.fetchall()
        length          = len(data)

        if not length==0:
            warning = QMessageBox.warning(self, 'Update Book', "Are you sure you want to update this book", QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                sql     = '''
                        UPDATE book SET
                        book_name=%s, book_description=%s, book_price=%s, book_author=%s, book_publisher=%s, book_catageory=%s
                        WHERE
                        book_code=%s
                '''
                values  = (book_name, book_description, book_price, book_author, book_publisher, book_category, book_code)
                self.cur.execute(sql, values)
                self.db.commit()
                self.lineEdit_15.setText('')
                self.lineEdit_10.setText('')
                self.lineEdit_10.setDisabled(False)
                self.lineEdit_13.setText('')
                self.lineEdit_14.setText('')
                self.lineEdit_12.setText('')
                self.plainTextEdit_2.setPlainText('')
                self.statusBar().showMessage('Book was updates.') 
            else:
                self.statusBar().showMessage('Book wasnot deleted.')    
        else:
            self.label_51.setText('The book of given code not found.')
        self.Show_All_Books()

    def Delete_Books(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()


        book_code       = self.lineEdit_10.text()
        self.cur.execute('''
            SELECT * FROM book where book_code=%s
        ''', (book_code))
        data            = self.cur.fetchall()
        length          = len(data)

        if not length==0:
            warning = QMessageBox.warning(self, 'Delete Book', "Are you sure you want to delete this book", QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''
                    DELETE FROM book where book_code=%s
                ''', (book_code))
                self.db.commit()
                self.lineEdit_15.setText('')
                self.lineEdit_10.setText('')
                self.lineEdit_10.setDisabled(False)
                self.lineEdit_13.setText('')
                self.lineEdit_14.setText('')
                self.lineEdit_12.setText('')
                self.plainTextEdit_2.setPlainText('')
                self.statusBar().showMessage('Book was deleted.') 
            else:
                self.statusBar().showMessage('Book wasnot deleted.')    
        else:
            self.label_51.setText('The book of given code not found.')
        self.Show_All_Books()


    ################################################################
    #############Members############################################

    def ClearEnterMembership(self):
        self.lineEdit_16.setText('')
        self.lineEdit_17.setText('')
        self.lineEdit_18.setText('')
        self.lineEdit_19.setText('')
        self.lineEdit_20.setText('')
        self.lineEdit_21.setText('')
        self.lineEdit_22.setText('')
        self.lineEdit_23.setText('')
        self.lineEdit_24.setText('')
        self.lineEdit_25.setText('')
        self.label_37.setText('')
        self.label_52.setText('')

    def Issuse_Membership(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        member_regno    = self.lineEdit_16.text()
        member_fullname = self.lineEdit_17.text()
        member_email    = self.lineEdit_18.text()
        member_email    = member_email.lower()
        member_address  = self.lineEdit_19.text()
        member_phone    = self.lineEdit_20.text()

        is_email_valid = self.email_validity_check(member_email)

        sql = '''
                SELECT mem_regno, mem_email, mem_phone from members
            '''
        self.cur.execute(sql)
        data = self.cur.fetchall()

        email_parity = False
        regno_parity = False
        phone_parity = False

        for row in data:
            if row[0] == member_regno:
                regno_parity = True
                break
            elif row[1] == member_email:
                email_parity = True
                break
            elif row[2] == member_phone:
                phone_parity = True
                break  

        if is_email_valid:

            if email_parity==False and regno_parity==False and phone_parity ==False:
                self.cur.execute('''
                    INSERT INTO members (mem_regno, mem_fullname, mem_email, mem_address, mem_phone) VALUES (%s, %s, %s, %s, %s)
                ''', (member_regno, member_fullname, member_email, member_address, member_phone))

                self.db.commit()
                self.statusBar().showMessage('New member with name '+member_fullname+ ' and regno.' + ' added ') 
                self.lineEdit_16.setText('')
                self.lineEdit_17.setText('')
                self.lineEdit_18.setText('')
                self.lineEdit_19.setText('')
                self.lineEdit_20.setText('')
                self.label_36.setText('') 
            else:
                if regno_parity:
                    self.label_36.setText('The reg no. is already used.')
                elif email_parity:
                    self.label_36.setText('The email is already used.')
                elif phone_parity:
                    self.label_36.setText('The phone no. is already used.')
        else:
            self.label_36.setText('The email entered is invalid.')


    def Search_Membership(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        regno           = self.lineEdit_21.text()

        sql = '''
              SELECT * from members where mem_regno=%s
        '''
        self.cur.execute(sql, (regno))
        data            = self.cur.fetchall()
        
        length = len(data)

        if not length==0:
            for row in data:
                self.lineEdit_22.setText(row[2])
                self.lineEdit_23.setText(row[5])
                self.lineEdit_24.setText(row[3])
                self.lineEdit_24.setDisabled(True)
                self.lineEdit_25.setText(row[4])
        else:
            self.label_37.setText('No member with the entered regno.')
            self.lineEdit_22.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_24.setText('')
            self.lineEdit_25.setText('')

    def Update_Membership(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        member_regno    = self.lineEdit_21.text()
        member_fullname = self.lineEdit_22.text()
        member_email    = self.lineEdit_24.text()
        member_address  = self.lineEdit_25.text()
        member_phone    = self.lineEdit_23.text()

        warning = QMessageBox.warning(self, 'Update Member', "Are you sure you want to update this member", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = '''
                    UPDATE members SET mem_fullname=%s, mem_address=%s, mem_phone=%s WHERE mem_regno=%s
                '''
            val = (member_fullname, member_address, member_phone, member_regno)
            self.cur.execute(sql, val)
            self.db.commit()
            self.statusBar().showMessage( 'Member no ' + member_regno +' has been updated.')
            self.lineEdit_22.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_24.setText('')
            self.lineEdit_25.setText('')
            self.lineEdit_24.setDisabled(False)
            self.lineEdit_21.setText('')
        else:
            self.statusBar().showMessage( 'Member no ' + member_regno +' not updated.')


    def Delete_Memberships(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        member_regno    = self.lineEdit_21.text()

        warning = QMessageBox.warning(self, 'Delete Member', "Are you sure you want to delete this member", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = '''
                    DELETE from members where mem_regno=%s
                '''
            val = (member_regno)
            self.cur.execute(sql, val)
            self.db.commit()
            self.statusBar().showMessage( 'Member no ' + member_regno +' has been deleted.')
            self.lineEdit_22.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_24.setText('')
            self.lineEdit_25.setText('')
            self.lineEdit_24.setDisabled(False)
            self.lineEdit_21.setText('')
        else:
            self.statusBar().showMessage( 'Member no ' + member_regno +' wasnot updated.')


    ################################################################
    #############Users##############################################

    def ClearAddStaff(self):
        self.lineEdit_35.setText('')
        self.lineEdit_36.setText('')
        self.lineEdit_37.setText('')
        self.lineEdit_38.setText('')
        self.lineEdit_39.setText('')
        self.label_52.setText('')
        self.label_31.setText('')

    def ClearDeleteStaff(self):
        self.lineEdit_28.setText('')
        self.lineEdit_29.setText('')
        self.lineEdit_30.setText('')
        self.lineEdit_31.setText('')
        self.lineEdit_32.setText('')
        self.lineEdit_33.setText('')
        self.lineEdit_34.setText('')
        self.label_33.setText('')
        self.label_34.setText('')

    def Add_Staff(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        username    = self.lineEdit_39.text()
        fullname    = self.lineEdit_36.text()
        emailadd    = self.lineEdit_37.text()
        emailadd    = emailadd.lower()
        password    = self.lineEdit_38.text()
        password2   = self.lineEdit_35.text()

        is_email_valid = self.email_validity_check(emailadd)
        if is_email_valid:
            sql = ''' SELECT user_name, user_email  from users '''

            self.cur.execute(sql)
            data        = self.cur.fetchall()

            username_parity = False
            email_parity = False
            for row in data:
                if row[0] == username:
                    username_parity = True
                    break
                else:
                    username_parity = False

                if row[1] == emailadd:
                    email_parity = True
                    break
                else:
                    email_parity = False

            if username_parity==True and email_parity==True:
                self.label_31.setText('The username and email are already in use.')
            elif username_parity==True and email_parity==False:
                self.label_31.setText('The username is already in use.')
            elif username_parity==False and email_parity==True:
                self.label_31.setText('The email is already in use.')
            else:
                if password == password2:
                    self.cur.execute('''
                        INSERT INTO users (user_name, user_fullname, user_email, user_password) VALUES (%s, %s, %s, %s) 
                    ''', (username, fullname, emailadd, password))

                    self.db.commit()
                    self.statusBar().showMessage('New user '+ username + ' added.')

                    self.lineEdit_39.setText('')
                    self.lineEdit_36.setText('')
                    self.lineEdit_37.setText('')
                    self.lineEdit_38.setText('')
                    self.lineEdit_35.setText('')
                else:
                    self.label_31.setText('Your password doesn\'t match.')
        else:
            self.label_31.setText('Your email isn\'t valid.')

    def Staff_View(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        username    = self.lineEdit_28.text()
        password    = self.lineEdit_29.text()

        sql = ''' SELECT user_name, user_password, user_fullname, user_email  from users '''

        self.cur.execute(sql)
        data        = self.cur.fetchall()
        
        for row in data:
            if username == row[0] and password == row[1]:
                flag    = True
                self.lineEdit_30.setText(row[0])
                self.lineEdit_30.setDisabled(True)
                self.lineEdit_31.setText(row[2])
                display_name = row[2]
                self.lineEdit_32.setText(row[3])
                self.lineEdit_32.setDisabled(True)
                self.lineEdit_33.setText(row[1])
                self.lineEdit_34.setText(row[1])
                break
            else:
                flag    = False

        self.lineEdit_28.setText('')
        self.lineEdit_29.setText('')

        if flag:
            self.label_34.setText("Hello "+ display_name)
        else:
            self.label_33.setText('No such user found.')

    def Staff_Update(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        username        = self.lineEdit_30.text()
        fullname        = self.lineEdit_31.text()
        email           = self.lineEdit_32.text()
        email           = email.lower()
        password        = self.lineEdit_33.text()
        password2       = self.lineEdit_34.text()

        is_email_valid = self.email_validity_check(email)

        if is_email_valid:
            if password == password2:
                warning = QMessageBox.warning(self, 'Update Staff', "Are you sure you want to update this staff", QMessageBox.Yes | QMessageBox.No)
                if warning == QMessageBox.Yes:
                    print(username, fullname, password)
                    sql = '''
                        UPDATE users SET user_fullname=%s, user_password=%s WHERE user_name=%s
                    '''
                    val = (fullname, password, username)
                    self.cur.execute(sql, val)
                    self.db.commit()
                    self.statusBar().showMessage('Staff '+ username + ' have been updated.')
                    self.label_34.setText('')
                else:
                    self.statusBar().showMessage('Staff '+ username + ' was\'t updated.')
                self.label_34.setText('')
            else:
                self.label_33.setText('The password doesn\'t match.')
        else:
            self.label_33.setText('The email entered is invalid.')

    def Staff_Delete(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        username        = self.lineEdit_30.text()
        emailadd        = self.lineEdit_32.text()
        password        = self.lineEdit_33.text()
        password2       = self.lineEdit_34.text()

        is_email_valid = self.email_validity_check(emailadd)
        if is_email_valid:
            sql = ''' SELECT user_name, user_password from users '''
            self.cur.execute(sql)
            data        = self.cur.fetchall()

            if password == password2:
                for row in data:
                    if username == row[0] and password == row[1]:
                        flag    = True
                        warning = QMessageBox.warning(self, 'Delete Staff', "Are you sure you want to delete this staff", QMessageBox.Yes | QMessageBox.No)
                        if warning == QMessageBox.Yes:
                            sql     = ''' DELETE from users where user_name=%s'''
                            self.cur.execute(sql, [(username)])
                            self.db.commit()
                            self.statusBar().showMessage('Staff '+ username + ' have been deleted.')
                            self.label_34.setText('')
                            break
                        self.statusBar().showMessage('Staff '+ username + ' wasnot deleted.')
                        self.label_34.setText('')
                        break
                else:
                    flag    = False

            if flag==True:
                self.lineEdit_30.setText('')
                self.lineEdit_31.setText('')
                self.lineEdit_32.setText('')
                self.lineEdit_33.setText('')
                self.lineEdit_34.setText('')
                self.label_33.setText('')
            else:
                self.label_33.setText('The username or password might be wrong.')
        else:
            self.label_33.setText('The email entered is invalid.')

    ################################################################
    #############Category###########################################

    def ClearCatageories(self):
        self.lineEdit_26.setText('')
        self.lineEdit_27.setText('')

    def Add_Category(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        category_name   = self.lineEdit_26.text()

        self.cur.execute(''' SELECT cat_name FROM category ''')
        data            = self.cur.fetchall()

        flag = False
        for cat in data:
            if cat[0].lower() == category_name.lower():
                flag = True

        if not flag:
            self.cur.execute('''
                INSERT INTO category (cat_name) VALUES (%s)
            ''', (category_name,))

            self.db.commit()
            self.statusBar().showMessage('New category '+category_name+ ' added.')
            self.Show_Category()
            self.Show_Category_Combo()
            self.lineEdit_26.setText('')
        else:
            self.label_35.setText("The category "+ category_name+ " already exists.")

    def Show_Category(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        self.cur.execute(''' SELECT cat_name FROM category ''')
        data            = self.cur.fetchall()

        if data :
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position    = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    def Show_Category_Combo(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        self.cur.execute(''' SELECT cat_name FROM category ''')
        data            = self.cur.fetchall()
        
        self.comboBox.clear()
        self.comboBox_2.clear()
        for category in data:
            self.comboBox.addItem(category[0])
            self.comboBox_2.addItem(category[0])

    def Remove_Category(self):
        self.db         = pymysql.connect(host='localhost' , user='root' , password='admin' , db='library')
        self.cur        = self.db.cursor()

        category        = self.lineEdit_27.text()

        self.cur.execute(''' SELECT cat_name FROM category ''')
        data            = self.cur.fetchall()

        flag = False
        for cat in data:
            if cat[0].lower() == category.lower():
                flag = True

        if flag==True:
            warning = QMessageBox.warning(self, 'Delete Catageory', "Are you sure you want to delete this catageory", QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                sql     = ''' DELETE from category where cat_name=%s'''
                self.cur.execute(sql, [(category)])
                self.db.commit()
                self.statusBar().showMessage( category + ' have been deleted.')
                self.lineEdit_27.setText('')
            else:
                self.statusBar().showMessage( category + ' wasnot deleted.')
        else:
            self.label_35.setText("No such category"+ category+ " found.")

        self.Show_Category()
        self.Show_Category_Combo()


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()