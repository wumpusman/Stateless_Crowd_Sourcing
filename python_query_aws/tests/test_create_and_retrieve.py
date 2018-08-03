import unittest
from mturk_samples.python_query_aws.env_info import Environment_Info

class Test_Env_Info(unittest.TestCase):
    '''
        In principal what i'd be using to validate some of the setup for this script
    '''
    def setUp(self):
        self.Env_Info=Environment_Info
        self.number=4

    def test_create_and_destroy_hit(self):
        #result=self.Env_Info.make_hit()


        self.assertEqual(self.number, 4)



