import unittest
from validations import *

class Test(unittest.TestCase):

    def testEmailValidation(self):
        email = "haghshenas.amir74@gmail.com"
        self.assertEqual(email_validation(email),True)

    def testEmailFail(self):
        falseEmail = "123email"
        self.assertEqual(email_validation(falseEmail),False)


    def testPasswordValidation(self):
        password = "Amir123456"
        
        self.assertEqual(password_validation(password)[0], True)
        

    def testPassFail(self):
        falsePass = "123"
        self.assertEqual(password_validation(falsePass)[0], False)


    def testNameValidation(self):
        name = "amir"
        
        self.assertEqual(name_validation(name), True)
        

    def testNameFail(self):
        falseName = "123"
        self.assertEqual(name_validation(falseName), False)

if __name__ == '__main__':
    unittest.main()